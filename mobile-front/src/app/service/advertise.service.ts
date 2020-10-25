import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {User} from '../models/user';
import {Product} from '../models/product';
import {Observable, of} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {advertiseApi} from '../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class AdvertiseService {
  
  private advertiseUrl = `${advertiseApi}`;

  constructor(private http: HttpClient) {

  }

  getAllPackages(user: User): Observable<any> {
    console.log("this.advertiseUrl " + JSON.stringify(this.advertiseUrl));
    let url = this.advertiseUrl + "/all"
    let body = JSON.stringify({"email": user.email, "password": user.password, "mobile": user.mobile});
    const options = {
      headers: new HttpHeaders()
        .append('Content-Type', 'application/json')
        .append('Access-Control-Allow-Origin', '*')
        .append('Authorization','Bearer ' + user.token),
      mode: 'no-cors'
    }
    console.log("User.Token" + user.token);
    return this.http.get<any>(url,options);
  }

  getDetail(id: String,user: User): Observable<any> {
    const url = `${this.advertiseUrl}/${id}`;
    const options = {
      headers: new HttpHeaders()
        .append('Content-Type', 'application/json')
        .append('Access-Control-Allow-Origin', '*')
        .append('Authorization','Bearer ' + user.token),
      mode: 'no-cors'
    }

    // @ts-ignore
    return this.http.get<any>(url,options).pipe(
      map(prod => prod.packages),
      catchError(_ => {
        console.log("Get Detail Failed");
        return of(new Product());
      })
    );
  }


  update(productInfo: Product): Observable<Product> {
    const url = `${this.advertiseUrl}/${productInfo.id}`;
    let param = "?package_name=" + productInfo.package_name +
      "&package_description=" + productInfo.package_description +
      "&price=" + productInfo.price +
      "&available_qty=" + productInfo.available_qty +
      "&valid_from=2020-12-31 10:10:10" +
      "&valid_to=2025-12-31 10:10:10" +
      "&created_by=1"
    ;
    return this.http.put<Product>(url + param, null);
  }

  create(productInfo: Product): Observable<Product> {
    const url = `${this.advertiseUrl}/all`;
    let param = "?package_name=" + productInfo.package_name +
      "&package_description=" + productInfo.package_description +
      "&price=" + productInfo.price +
      "&available_qty=" + productInfo.available_qty +
      "&valid_from=2020-12-31 10:10:10" +
      "&valid_to=2025-12-31 10:10:10" +
      "&created_by=1"
    ;
    console.log(url + param);
    return this.http.post<any>(url + param, null);
  }

  delete(productInfo: Product): Observable<any> {
    const url = `${this.advertiseUrl}/${productInfo.id}`;
    return this.http.delete(url);
  }


}
