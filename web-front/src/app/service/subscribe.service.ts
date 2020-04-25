import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {User} from "../models/user";
import {Product} from '../models/product';
import {ProductInOrder} from "../models/ProductInOrder";
import {Cart} from "../models/Cart";
import {BehaviorSubject, Observable, of} from 'rxjs';
import {CookieService} from 'ngx-cookie-service';


@Injectable({
  providedIn: 'root'
})
export class SubscribeService {

  //private subscribeUrl = "http://35.198.220.113:9100/"
  private subscribeUrl = "http://localhost:5000"

  localMap = {};
  // private itemsSubject: BehaviorSubject<Item[]>;
  // private totalSubject: BehaviorSubject<number>;
  // public items: Observable<Item[]>;
  // public total: Observable<number>;
  // private currentUser: JwtResponse;

  constructor(
    private http: HttpClient
    // private cookieService: CookieService
    // private userService: UserService
  ) {
    // this.itemsSubject = new BehaviorSubject<Item[]>(null);
    // this.items = this.itemsSubject.asObservable();
    // this.totalSubject = new BehaviorSubject<number>(null);
    // this.total = this.totalSubject.asObservable();
    // this.userService.currentUser.subscribe(user => this.currentUser = user);


  }

  // private getLocalCart(): ProductInOrder[] {
  //   if (this.cookieService.check('cart')) {
  //     this.localMap = JSON.parse(this.cookieService.get('cart'));
  //     return Object.values(this.localMap);
  //   } else {
  //     this.localMap = {};
  //     return [];
  //   }
  // }

  addItem(productInOrder): Observable<boolean> {
    // if (!this.currentUser) {
    //   if (this.cookieService.check('cart')) {
    //     this.localMap = JSON.parse(this.cookieService.get('cart'));
    //   }
    //   if (!this.localMap[productInOrder.productId]) {
    //     this.localMap[productInOrder.productId] = productInOrder;
    //   } else {
    //     this.localMap[productInOrder.productId].count += productInOrder.count;
    //   }
    //   this.cookieService.set('cart', JSON.stringify(this.localMap));
    //   return of(true);
    // } else {
    const url = `${this.subscribeUrl}/add`;
    let bodyOriginals = {
      'qty': productInOrder.count,
      'package_id': productInOrder.productId,
      'user_id': 1
    };

     let body = JSON.stringify({
      'qty': 1,
      'package_id': 1,
      'user_id': 1
    });

    const options = {
      headers: new HttpHeaders()
        .append('Content-Type', 'application/json')
        .append('Access-Control-Allow-Origin', '*')
        .append('Access-Control-Allow-Headers', 'Content-Type')
    }
    return this.http.post<any>(url, body, options);
    // }
  }

  // update(productInOrder): Observable<ProductInOrder> {
  //
  //   if (this.currentUser) {
  //     const url = `${this.subscribeUrl}/${productInOrder.productId}`;
  //     return this.http.put<ProductInOrder>(url, productInOrder.count);
  //   }
  // }


  // remove(productInOrder) {
  //   if (!this.currentUser) {
  //     delete this.localMap[productInOrder.productId];
  //     return of(null);
  //   } else {
  //     const url = `${this.subscribeUrl}/${productInOrder.productId}`;
  //     return this.http.delete(url).pipe();
  //   }
  // }


  // checkout(): Observable<any> {
  //   const url = `${this.subscribeUrl}/checkout`;
  //   return this.http.post(url, null).pipe();
  // }
  //
  // storeLocalCart() {
  //   this.cookieService.set('cart', JSON.stringify(this.localMap));
  // }
  //
  // clearLocalCart() {
  //   console.log('clear local cart');
  //   this.cookieService.delete('cart');
  //   this.localMap = {};
  // }
}
