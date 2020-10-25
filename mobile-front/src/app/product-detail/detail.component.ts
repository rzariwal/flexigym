import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { AdvertiseService } from '../service/advertise.service';
import { SubscribeService } from '../service/subscribe.service';
import {AuthResponse, User} from '../models/user';
import { Product } from '../models/product';
import { ProductInOrder } from '../models/ProductInOrder';
//import {AuthService} from "../service/auth.service";
//import {CookieService} from 'ngx-cookie-service';
import { SecureStorage } from "nativescript-secure-storage";


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
  currentUser: AuthResponse;
  secureStorage: SecureStorage;

  constructor(
    private router: Router,
    private advertiseService: AdvertiseService,
    private subscribeService: SubscribeService,
    //private cookieService: CookieService,
    private route: ActivatedRoute,
    //private authService: AuthService
  ) {
    this.secureStorage = new SecureStorage();
  }



  ngOnInit() {
    this.getProduct();
    this.title = 'Product Detail';
    this.count = 1;
  }

  getProduct(): void {
    this.user = new User();

    var value = this.secureStorage.getSync({
      key: "user"
    });
    console.log("User from storage : " + value);
    var userObj = JSON.parse(value);
    this.user.token= userObj.token;
    const id = this.route.snapshot.paramMap.get('id');
    this.advertiseService.getDetail(id,this.user).subscribe(
        prod => {
          console.log("get by product is " + JSON.stringify(prod));
          this.products = prod;
          console.log(this.products);
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
                }
                console.log('addToCart() Status :  ' + res.status);
                console.log('addToCart() cart_id : ' + res.cart_Info.cart_id);
                this.router.navigateByUrl('/cart');
               
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
