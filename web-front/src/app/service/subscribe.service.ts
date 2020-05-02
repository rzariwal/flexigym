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


@Injectable({
  providedIn: 'root'
})
export class SubscribeService {

  //private subscribeUrl = "http://35.198.220.113:9100/"
  private subscribeUrl = "http://flexigym-subscribe-api:5000";
  private authApiUrl = 'http://35.198.220.113:5000/auth';

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
        console.log("localCart " + localCart);
        if (this.currentUser) {
          console.log("current user : " + JSON.stringify(this.currentUser));
            if (localCart.length > 0) {
              console.log("Cart from local : " );
                let url = `${this.subscribeUrl}/get`;
                return this.http.post<Cart>(url, localCart).pipe(
                    tap(_ => {
                        this.clearLocalCart();
                    }),
                    map(cart => cart.products),
                    catchError(_ => of([]))
                );
            } else {
              console.log("Cart from server : " );
                let url = `${this.subscribeUrl}/get`;
                let body = JSON.stringify({ "cart_id":"1" });
                let options = {
                  headers: new HttpHeaders().append('Content-Type', 'application/json')
                  .append('Access-Control-Allow-Origin', '*')
                }

                 return this.http.post<any>(url,body,options).pipe(
                    map(cart => cart.cart_Items),
                    catchError(_ => of([]))
                );

                //  return this.http.post<Cart>(url,body,options).pipe(
                //     map(cart => cart.products),
                //     catchError(_ => of([]))
                // );
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

    let url = `${this.subscribeUrl}/add`;
    let body = JSON.stringify({  "qty": productInOrder.qty,"package_id": productInOrder.package_id, "user_id": "1"});
    let options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
      .append('Access-Control-Allow-Origin', '*')
    }
     return this.http.post<any>(url,body,options).pipe(
        catchError(_ => of([]))
    );





    // }
  }

  addItem2(productInOrder): Observable<any>{
    let url = this.authApiUrl+ '/login'
    let body = JSON.stringify({ "email":"ehkalu@gmail.com","password":"1234" });
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
    }
    console.log("Done");
    let resp = this.http.post<any>(url, body, options);
    console.log(url);
    console.log(resp);
    return resp;
  }

  update(productInOrder): Observable<ProductInOrder> {

    // if (this.currentUser) {
      const url = `${this.subscribeUrl}/${productInOrder.productId}`;
      return this.http.put<ProductInOrder>(url, productInOrder.count);
    // }
  }


  // remove(productInOrder) {
  //   if (!this.currentUser) {
  //     delete this.localMap[productInOrder.productId];
  //     return of(null);
  //   } else {
  //     const url = `${this.subscribeUrl}/${productInOrder.productId}`;
  //     return this.http.delete(url).pipe();
  //   }
  // }


  checkout(): Observable<any> {
    let url = `${this.subscribeUrl}/checkout`;
    let body = JSON.stringify({ "cart_id":"2" });
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
