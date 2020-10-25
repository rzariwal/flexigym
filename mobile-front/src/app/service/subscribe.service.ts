import {Injectable} from '@angular/core';
import { HttpClientModule, HttpClient, HttpRequest, HttpHeaders, HttpEventType, HttpResponse} from '@angular/common/http';

import { User, AuthResponse } from '../models/user';
import {Product} from '../models/product';
import {ProductInOrder} from "../models/ProductInOrder";
import {Cart} from "../models/Cart";
import {AuthService} from '../service/auth.service';
import {BehaviorSubject, Observable, of} from 'rxjs';
//import {CookieService} from 'ngx-cookie-service';
import {catchError, map, tap} from "rxjs/operators";
import {authApi} from '../../environments/environment';
import {subscribeApi} from '../../environments/environment';
import { SecureStorage } from "nativescript-secure-storage";

@Injectable({
  providedIn: 'root'
})
export class SubscribeService {
  
  private subscribeUrl = `${subscribeApi}`;
  private authApiUrl = `${authApi}`;

  localMap = {};
  // private itemsSubject: BehaviorSubject<Item[]>;
  // private totalSubject: BehaviorSubject<number>;
  // public items: Observable<Item[]>;
  // public total: Observable<number>;
  private currentUser: AuthResponse;
  secureStorage: SecureStorage;

  constructor(
    private http: HttpClient,    
    private authService: AuthService
  ) {
    // this.itemsSubject = new BehaviorSubject<Item[]>(null);
    // this.items = this.itemsSubject.asObservable();
    // this.totalSubject = new BehaviorSubject<number>(null);
    // this.total = this.totalSubject.asObservable();
    //this.authService.currentUser.subscribe(user => this.currentUser = user);
    this.secureStorage = new SecureStorage();  

  }

  //ProductInOrder[]
  getCart(): Observable<any> {
        let url = `${this.subscribeUrl}/get`;
        let options = {
          headers: new HttpHeaders().append('Content-Type', 'application/json')
          .append('Access-Control-Allow-Origin', '*')
        };
        let cart_id = 0;
        // if (this.cookieService.check('cart_id')) {
        //   cart_id = JSON.parse(this.cookieService.get('cart_id'));
        // }
        // console.log("cart_id in getCart() : " + cart_id);
        var cartID= this.secureStorage.getSync({
          key: "cart_id"
        });
        var cartIDObj = JSON.parse(cartID);
        console.log("cart_id in getCart() : " + cartIDObj);
        if (cartIDObj>0){
          cart_id = cartIDObj;
        }

        let body1 = JSON.stringify({ "cart_id":cart_id });
        return this.http.post<any>(url,body1,options).pipe(
            catchError(_ => of([]))
        );

    }

  getCartByUser(user_id : string){
    let url = `${this.subscribeUrl}/get`;
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    };
    console.log("getCartByUser (" + user_id + ")");
    let body = JSON.stringify({ "user_id": user_id});
    return this.http.post<any>(url,body,options).pipe(
       tap(resp => {
          console.log("cart_id : " + resp.cartInfo.cart_id);
          //this.cookieService.set('cart_id', resp.cartInfo.cart_id);
          return resp;
        }),
        catchError(_ => of([]))
    );
  }

  private getLocalCart(): ProductInOrder[] {
    // if (this.cookieService.check('cart')) {
    //   this.localMap = JSON.parse(this.cookieService.get('cart'));
    //   return Object.values(this.localMap);
    // } else {
    //   this.localMap = {};
    //   return [];
    // }
    this.localMap = {};
    return [];
  }

  addItem(productInOrder): Observable<any> {
    //let thisUser= 0 ;
    // if (this.cookieService.check('currentUser')) {
    //    let userObj = JSON.parse(this.cookieService.get('currentUser'));
    //    thisUser = userObj.user_id;
    // }
   

    var user = this.secureStorage.getSync({
      key: "user"
    });
    var userStatus = this.secureStorage.getSync({
      key: "userStatus"
    });
    var userObj = JSON.parse(user);
    var userStatusObj = JSON.parse(userStatus);
    console.log("User from storage : " + user);
    console.log("userStatusObj in add method : " + userStatus);

    let url = `${this.subscribeUrl}/add`;
    let body = JSON.stringify({  "qty": productInOrder.qty,"package_id": productInOrder.package_id, "user_id": userStatusObj.user_id});
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    }

    let cart_id = 0;
    var cartID= this.secureStorage.getSync({
      key: "cart_id"
    });
    var cartIDObj = JSON.parse(cartID);
    // if (this.cookieService.check('cart_id')) {
    //       cart_id = JSON.parse(this.cookieService.get('cart_id'));
    //       body = JSON.stringify({  "qty": productInOrder.qty,"package_id": productInOrder.package_id, "user_id": thisUser, "cart_id": cart_id});
    // }
    console.log("cart_id in add method : " + cart_id);
    console.log("body in add method : " + body);
    return this.http.post<any>(url,body,options).pipe(
       tap(resp => {
            //this.cookieService.set('cart_id', resp.cart_Info.cart_id);
            const success = this.secureStorage.setSync({
              key: "cart_id",
              value: JSON.stringify(resp.cart_Info.cart_id)
            });
        }),
        catchError(_ => of([]))
    );
    // }
  }

  update(productInOrder): Observable<any> {   
    let url = `${this.subscribeUrl}/update`;
    let cart_id = 0;
    // if (this.cookieService.check('cart_id')) {
    //     cart_id = JSON.parse(this.cookieService.get('cart_id'));
    // }

    let body = JSON.stringify({  "cart_id": cart_id,"package_id": productInOrder.package_id, "quantity": productInOrder.qty});
      console.log("body in update method : " + body);
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    }

    return this.http.post<any>(url,body,options).pipe(
         tap(resp => {
            console.log('cart_id'+ JSON.stringify(resp) );
        }),
        catchError(_ => of([]))
    );
  }


  remove(productInOrder) {

    let cart_id = 0;
    // if (this.cookieService.check('cart_id')) {
    //       cart_id = JSON.parse(this.cookieService.get('cart_id'));
    // }
    console.log("cart_id in delete method : " + cart_id);

    let url = `${this.subscribeUrl}/delete`;
    let body = JSON.stringify({  "package_id": productInOrder.package_id, "cart_id": cart_id});
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    }

    return this.http.post<any>(url,body,options).pipe(
        catchError(_ => of([]))
    );

    // if (!this.currentUser) {
    //   delete this.localMap[productInOrder.productId];
    //   return of(null);
    // } else {
    //   const url = `${this.subscribeUrl}/${productInOrder.productId}`;
    //   return this.http.delete(url).pipe();
    // }
  }


  checkout(): Observable<any> {
    let cart_id = 0;
    // if (this.cookieService.check('cart_id')) {
    //     cart_id = JSON.parse(this.cookieService.get('cart_id'));
    //     console.log("cart_id in add method : " + cart_id);
    // }
    let url = `${this.subscribeUrl}/checkout`;
    let body = JSON.stringify({ "cart_id":cart_id });
    let options = {
                  headers: new HttpHeaders().append('Content-Type', 'application/json')
                  .append('Access-Control-Allow-Origin', '*')
                }
    return this.http.post(url,body,options).pipe();
  }

  // storeLocalCart() {
  //   this.cookieService.set('cart', JSON.stringify(this.localMap));
  // }

  // clearLocalCart() {
  //   console.log('clear local cart');
  //   this.cookieService.delete('cart');
  //   this.localMap = {};
  // }

  // clearCart() {
  //   console.log('clear cart');
  //   this.cookieService.delete('cart_id');

  // }


  getCompleteStatus(param: string): Observable<any> {
    let cart_id = 0;
    // if (this.cookieService.check('cart_id')) {
    //     cart_id = JSON.parse(this.cookieService.get('cart_id'));
    //     console.log("cart_id in add method : " + cart_id);
    // }
    let url = `${this.subscribeUrl}/completeCheckout` ;
    console.log("param " + param);
    let body = JSON.stringify({ "cart_id":cart_id, "payload" : "?" + param});
    console.log("param " + JSON.stringify(body));
    let options = {
                  headers: new HttpHeaders().append('Content-Type', 'application/json')
                  .append('Access-Control-Allow-Origin', '*')
                }
    return this.http.post<any>(url,body,options).pipe(
      catchError(_ => of([]))
    );
  }

}
