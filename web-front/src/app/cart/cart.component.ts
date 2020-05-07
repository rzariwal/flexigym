import {AfterContentChecked, Component, OnDestroy, OnInit} from '@angular/core';
import {User, AuthResponse} from '../models/user';
import {Product} from '../models/product';
import {ProductInOrder} from '../models/ProductInOrder';
import {Subject, Subscription} from 'rxjs';
import {debounceTime, switchMap} from 'rxjs/operators';
import {ActivatedRoute, NavigationEnd, Router} from '@angular/router';
import {AdvertiseService} from "../service/advertise.service";
import {SubscribeService} from '../service/subscribe.service';
import {AuthService} from '../service/auth.service';


@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {

  constructor(
    private router: Router,
    private subscribeService: SubscribeService,
    private authService: AuthService
  ) {
    this.userSubscription = this.authService.currentUser.subscribe(user => this.currentUser = user);
  }

  productInOrders = [];
  total = 0;
  totalAmount = 0;
  currentUser: AuthResponse;
  userSubscription: Subscription;

  private updateTerms = new Subject<any>();
  sub: Subscription;

  static validateCount(productInOrder) {
    const max = productInOrder.available_qty;
    console.log("available_qty " + JSON.stringify(productInOrder));
    if (productInOrder.qty > max) {
      productInOrder.qty = max;
    } else if (productInOrder.qty < 1) {
      productInOrder.qty = 1;
    }
    console.log("validateCount " + productInOrder.qty);
  }

  ngOnInit() {
    this.subscribeService.getCart().subscribe(response => {
      console.log('Products in cards: ' + JSON.stringify(response));
      this.productInOrders = response.cart_Items;
      this.totalAmount = response.cartInfo.total;
    });

    this.sub = this.updateTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),
      //
      // ignore new term if same as previous term
      // Same Object Reference, not working here
      //  distinctUntilChanged((p: ProductInOrder, q: ProductInOrder) => p.count === q.count),
      //
      // switch to new search observable each time the term changes
      switchMap((productInOrder: any) => this.subscribeService.update(productInOrder))
    ).subscribe
    (response => {
        if (response) {
          console.log('Total :' + response.cartInfo.total);
          this.totalAmount = response.cartInfo.total;
        }
      },
      _ => console.log('Update Item Failed')
    );
  }


  ngOnDestroy() {
    if (!this.currentUser) {
      this.subscribeService.storeLocalCart();
    }
    this.userSubscription.unsubscribe();
  }

  ngAfterContentChecked() {
    this.total = this.productInOrders.reduce(
      (prev, cur) => prev + cur.qty * cur.productPrice, 0);
  }

  addOne(productInOrder) {
    productInOrder.qty++;
    CartComponent.validateCount(productInOrder);
    if (this.currentUser) {
      this.updateTerms.next(productInOrder);
    }
  }

  minusOne(productInOrder) {
    productInOrder.qty--;
    CartComponent.validateCount(productInOrder);
    if (this.currentUser) {
      this.updateTerms.next(productInOrder);
    }
  }

  onChange(productInOrder) {
    CartComponent.validateCount(productInOrder);
    if (this.currentUser) {
      this.updateTerms.next(productInOrder);
    }
  }


  remove(productInOrder: ProductInOrder) {
    this.subscribeService.remove(productInOrder).subscribe(
      success => {
        //this.productInOrders = this.productInOrders.filter(e => e.productId !== productInOrder.productId);
        console.log('Cart: ' + this.productInOrders);
      },
      _ => console.log('Remove Cart Failed')
    );

    this.subscribeService.getCart().subscribe(prods => {
      this.productInOrders = prods.cart_Items;
      console.log('Products in cards: ' + JSON.stringify(prods.cart_Items));
    });
  }

  checkout() {
    if (!this.currentUser) {
      this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
      // } else if (this.currentUser.role !== Role.Customer) {
      //     this.router.navigate(['/seller']);
    } else {
      this.subscribeService.checkout().subscribe(
        resp => {
          this.productInOrders = [];
          console.log(JSON.stringify(resp));
          if (resp.status = "success") {
            console.log(resp.redirect_url);
            //his.router.navigate(resp.redirect_url, {queryParams: {returnUrl: this.router.url}});
            window.open(resp.redirect_url, '_blank');
            this.router.events.subscribe(event => {
              if (event instanceof NavigationEnd) {
                console.log(event.url);
                //if (event.url.includes('faq')) {
                // open in the same tab:
                window.location.href = resp.redirect_url;

                // open a new tab:
                // window.open('https://faq.website.com', '_blank');

                // and redirect the current page:
                // this.router.navigate(['/']);
                //}
              }
            });
          }
        },
        error1 => {
          console.log('Checkout Cart Failed');
        });
      // this.router.navigate(['/']);
    }

  }
}

