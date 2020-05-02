import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { AdvertiseService } from '../service/advertise.service';
import { SubscribeService } from '../service/subscribe.service';
import { User } from '../models/user';
import { Product } from '../models/product';
import { ProductInOrder } from '../models/ProductInOrder';
//import {CookieService} from 'ngx-cookie-service';


@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})

export class DetailComponent implements OnInit {
  user: User;
  products: Product;
  title: string;
  count: number;

  constructor(
    private router: Router,
    private advertiseService: AdvertiseService,
    private subscribeService: SubscribeService,
    //private cookieService: CookieService,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.getProduct();
    this.title = 'Product Detail';
    this.count = 1;
  }

  getProduct(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.advertiseService.getDetail(id).subscribe(
        prod => {
          this.products = prod;
          console.log(this.products.packages);
          console.log(prod.packages);
        },
        _ => console.log('Get Cart Failed')
    );
  }

  addToCart() {
    this.subscribeService
        .addItem(new ProductInOrder(this.products, this.count))
        .subscribe(
            res => {
              if (!res) {
                console.log('Add Cart failed' + res);
                throw new Error();
              }
              //this.router.navigateByUrl('/cart');
              console.log('Add Cart Success')
            },
            _ => console.log('Add Cart Failed')
        );
  }

  // validateCount() {
  //   console.log('Validate');
  //   const max = this.products;
  //   if (this.count > max) {
  //     this.count = max;
  //   } else if (this.count < 1) {
  //     this.count = 1;
  //   }
  // }
}
