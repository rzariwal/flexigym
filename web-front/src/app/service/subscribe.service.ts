import {Injectable} from '@angular/core';
import { HttpClientModule, HttpClient, HttpRequest, HttpHeaders, HttpEventType, HttpResponse} from '@angular/common/http';

import { User, AuthResponse } from '../models/user';
import {Product} from '../models/product';
import {ProductInOrder} from "../models/ProductInOrder";
import {Cart} from "../models/Cart";
import {AuthService} from '../service/auth.service';
import {BehaviorSubject, Observable, of} from 'rxjs';
import {CookieService} from 'ngx-cookie-service';
import {catchError, map, tap} from "rxjs/operators";
import {authApi} from '../../environments/environment';
import {subscribeApi} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SubscribeService {

  //private subscribeUrl = "http://35.198.220.113:9100/"
  //private subscribeUrl = "http://flexigym-subscribe-api:5000";
  //private authApiUrl = 'http://35.198.220.113:5000/auth';

  private subscribeUrl = `${subscribeApi}`;
  private authApiUrl = `${authApi}`;

  localMap = {};
  // private itemsSubject: BehaviorSubject<Item[]>;
  // private totalSubject: BehaviorSubject<number>;
  // public items: Observable<Item[]>;
  // public total: Observable<number>;
  private currentUser: AuthResponse;

  constructor(
    private http: HttpClient,
    private cookieService: CookieService,
    private authService: AuthService
  ) {
    // this.itemsSubject = new BehaviorSubject<Item[]>(null);
    // this.items = this.itemsSubject.asObservable();
    // this.totalSubject = new BehaviorSubject<number>(null);
    // this.total = this.totalSubject.asObservable();
    this.authService.currentUser.subscribe(user => this.currentUser = user);
  }

  //ProductInOrder[]
  getCart(): Observable<any> {
        const localCart = this.getLocalCart();
        let url = `${this.subscribeUrl}/get`;
        let options = {
          headers: new HttpHeaders().append('Content-Type', 'application/json')
          .append('Access-Control-Allow-Origin', '*')
        };
        let cart_id = 0;
        if (this.cookieService.check('cart_id')) {
          cart_id = JSON.parse(this.cookieService.get('cart_id'));
          console.log("cart_id in get method : " + cart_id);
        }
        if (this.currentUser) {
          console.log("current user : " + JSON.stringify(this.currentUser));
            if (localCart.length > 0) {
              console.log("Cart from local : " + JSON.stringify(localCart));;
              let body1 = JSON.stringify({ "cart_id":cart_id });
              return this.http.post<any>(url,body1,options).pipe(
                  tap(_ => {
                      this.clearLocalCart();
                  }),
                  map(cart => cart.cart_Items),
                  catchError(_ => of([]))

              );
            } else {
              console.log("Cart from server : " );
                let body = JSON.stringify({ "user_id": this.currentUser.user_id });
                return this.http.post<any>(url,body,options).pipe(
                    map(cart => cart.cart_Items),
                    catchError(_ => of([]))
                );
            }
        } else {
            console.log("local cart : " );
            return of(localCart);
        }
    }

  private getLocalCart(): ProductInOrder[] {
    if (this.cookieService.check('cart')) {
      this.localMap = JSON.parse(this.cookieService.get('cart'));
      return Object.values(this.localMap);
    } else {
      this.localMap = {};
      return [];
    }
  }

  addItem(productInOrder): Observable<any> {
    // if (!this.currentUser) {
    //   if (this.cookieService.check('cart')) {
    //     this.localMap = JSON.parse(this.cookieService.get('cart'));
    //   }
    //   if (!this.localMap[productInOrder.package_id]) {
    //     this.localMap[productInOrder.package_id] = productInOrder;
    //   } else {
    //     this.localMap[productInOrder.package_id].qty += productInOrder.qty;
    //   }
    //   this.cookieService.set('cart', JSON.stringify(this.localMap));
    //   return of(true);
    // } else {
    console.log("Add Item : this.currentUser  " + JSON.stringify(this.currentUser));

    // if (!this.currentUser) {
    //   return of(false);
    // }

    let url = `${this.subscribeUrl}/add`;
    let body = JSON.stringify({  "qty": productInOrder.qty,"package_id": productInOrder.package_id, "user_id": this.currentUser.user_id});
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    }



    let cart_id = 0;
    if (this.cookieService.check('cart_id')) {
          cart_id = JSON.parse(this.cookieService.get('cart_id'));
          console.log("cart_id in add method : " + cart_id);
          body = JSON.stringify({  "qty": productInOrder.qty,"package_id": productInOrder.package_id, "user_id": this.currentUser.user_id, "cart_id": cart_id});
    }
    console.log("user_id in add method : " + this.currentUser.user_id);
    console.log("body in add method : " + body);

    return this.http.post<any>(url,body,options).pipe(
       tap(resp => {
            this.cookieService.set('cart_id', resp.cart_Info.cart_id);
        }),
        catchError(_ => of([]))
    );





    // }
  }

  update(productInOrder): Observable<ProductInOrder> {

    // if (this.currentUser) {
      const url = `${this.subscribeUrl}/${productInOrder.productId}`;
      return this.http.put<ProductInOrder>(url, productInOrder.count);
    // }
  }


  remove(productInOrder) {

    let cart_id = 0;
    if (this.cookieService.check('cart_id')) {
          cart_id = JSON.parse(this.cookieService.get('cart_id'));
          console.log("cart_id in delete method : " + cart_id);
    }

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
    if (this.cookieService.check('cart_id')) {
        cart_id = JSON.parse(this.cookieService.get('cart_id'));
        console.log("cart_id in add method : " + cart_id);
    }
    let url = `${this.subscribeUrl}/checkout`;
    let body = JSON.stringify({ "cart_id":cart_id });
    let options = {
                  headers: new HttpHeaders().append('Content-Type', 'application/json')
                  .append('Access-Control-Allow-Origin', '*')
                }
    return this.http.post(url,body,options).pipe();
  }

  storeLocalCart() {
    this.cookieService.set('cart', JSON.stringify(this.localMap));
  }

  clearLocalCart() {
    console.log('clear local cart');
    this.cookieService.delete('cart');
    this.localMap = {};
  }

}
