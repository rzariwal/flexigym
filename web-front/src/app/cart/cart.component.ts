import {AfterContentChecked, Component, OnDestroy, OnInit} from '@angular/core';
import {User,AuthResponse} from '../models/user';
import {Product} from '../models/product';
import {ProductInOrder} from '../models/ProductInOrder';
import {Subject, Subscription} from 'rxjs';
import {debounceTime, switchMap} from 'rxjs/operators';
import {ActivatedRoute, Router} from '@angular/router';
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
  currentUser: AuthResponse;
  userSubscription: Subscription;

  private updateTerms = new Subject<ProductInOrder>();
  sub: Subscription;

  static validateCount(productInOrder) {
    const max = productInOrder.productStock;
    if (productInOrder.count > max) {
      productInOrder.count = max;
    } else if (productInOrder.count < 1) {
      productInOrder.count = 1;
    }
    console.log(productInOrder.count);
  }

  ngOnInit() {
    this.subscribeService.getCart(this.currentUser.user_id).subscribe(prods => {
      this.productInOrders = prods;
      console.log('Products in cards: ' + JSON.stringify(prods));
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
      switchMap((productInOrder: ProductInOrder) => this.subscribeService.update(productInOrder))
    ).subscribe(prod => {
        if (prod) {
          throw new Error();
        }
      },
      _ => console.log('Update Item Failed'));
  }


  ngOnDestroy() {
      if (!this.currentUser) {
          this.subscribeService.storeLocalCart();
      }
      this.userSubscription.unsubscribe();
  }

  ngAfterContentChecked() {
      this.total = this.productInOrders.reduce(
          (prev, cur) => prev + cur.count * cur.productPrice, 0);
  }

  addOne(productInOrder) {
      productInOrder.count++;
      CartComponent.validateCount(productInOrder);
      if (this.currentUser) { this.updateTerms.next(productInOrder); }
  }

  minusOne(productInOrder) {
      productInOrder.count--;
      CartComponent.validateCount(productInOrder);
      if (this.currentUser) { this.updateTerms.next(productInOrder); }
  }

  onChange(productInOrder) {
      CartComponent.validateCount(productInOrder);
      if (this.currentUser) { this.updateTerms.next(productInOrder); }
  }


  remove(productInOrder: ProductInOrder) {
      this.subscribeService.remove(productInOrder).subscribe(
          success => {
             this.productInOrders = this.productInOrders.filter(e => e.productId !== productInOrder.productId);
              console.log('Cart: ' + this.productInOrders);
          },
          _ => console.log('Remove Cart Failed'));
  }

  checkout() {
      if (!this.currentUser) {
          this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
      // } else if (this.currentUser.role !== Role.Customer) {
      //     this.router.navigate(['/seller']);
      } else {
          this.subscribeService.checkout().subscribe(
              _ => {
                  this.productInOrders = [];
              },
              error1 => {
                  console.log('Checkout Cart Failed');
              });
         // this.router.navigate(['/']);
      }

  }
}

