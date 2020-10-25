import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AdvertiseService } from '../service/advertise.service';
//import { AuthService } from '../service/auth.service';
import { User } from '../models/user';
import { Product } from '../models/product';
import {Subscription} from "rxjs";
import { SecureStorage } from "nativescript-secure-storage";


@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {
  user: User;
  products: Product;
  currentUserSubscription: Subscription;
  secureStorage: SecureStorage;

  constructor(private router: Router,
              private advertiseService: AdvertiseService) 
  { 
      this.secureStorage = new SecureStorage();
  }

  ngOnInit(): void {
    this.user = new User();

    var value = this.secureStorage.getSync({
      key: "user"
    });
    console.log("User from storage : " + value);
    var userObj = JSON.parse(value);
    this.user.token= userObj.token;

    this.advertiseService.getAllPackages(this.user).subscribe(
      resp => {
        this.products = resp;
        console.log(this.products.packages);
      }
    );

    // this.currentUserSubscription = this.authService.currentUser.subscribe(user => {
    //   console.log("User in user profile :" + JSON.stringify(user) );
    //   //this.currentUser = user;
    //   this.user = user;
    //   //this.user.admin =true;
    // });
  }

  remove(product : Product) {
    this.advertiseService.delete(product).subscribe(prod => {
        if (!prod) throw new Error;
        this.router.navigate(['/']);
      },
      e => {
      });
  }

  logout() {
    this.secureStorage.removeAll().then(success => console.log("Cleared storage"));
    //this.location.back();
    this.router.navigate(['/home']);
  }

  mycart() {
    this.router.navigate(['/cart']);
  }

}
