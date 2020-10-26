import { Injectable } from '@angular/core';
import { User, AuthResponse } from '../models/user';
import { HttpClientModule, HttpClient, HttpRequest, HttpHeaders, HttpEventType, HttpResponse} from '@angular/common/http';
//import {CookieService} from 'ngx-cookie-service';
import {BehaviorSubject, Observable, of, Subject, throwError} from 'rxjs';
import {catchError, tap} from 'rxjs/operators';
import {authApi} from '../../environments/environment';

import { SecureStorage } from 'nativescript-secure-storage';




@Injectable({
  providedIn: 'root'
})
export class AuthService {
  //auth IP within cluster now.
  //private authApiUrl = 'http://web:5000/auth';
  private authApiUrl =`${authApi}`;
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;
  secureStorage: SecureStorage;

  public nameTerms = new Subject<string>();
  public name$ = this.nameTerms.asObservable();

  constructor(private http: HttpClient) {
        //const memo = localStorage.getItem('currentUser');
        //this.currentUserSubject = new BehaviorSubject<AuthResponse>(JSON.parse(memo));
        //this.currentUser = this.currentUserSubject.asObservable();
        //cookieService.set('currentUser', memo);

        this.secureStorage = new SecureStorage();

        //console.log('currentUser is '+ memo);
  }

  register(user: User): Observable<AuthResponse>{
    let url = this.authApiUrl+ '/register'
    let body = JSON.stringify({ "email":user.email,"password":user.password, "mobile":user.mobile, "admin": user.admin });
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
    }
    console.log("Done");
    return this.http.post<AuthResponse>(url,body,options);
  }

  login(user: User): Observable<AuthResponse>{
    if (!user.email || !user.password) {
        console.log("email or password is blank ");
        return throwError("Please provide both an email address and password.");
    }

    let url = this.authApiUrl+ '/login'
    let body = JSON.stringify({ "email":user.email,"password":user.password });
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
    }    
    return this.http.post<AuthResponse>(url,body,options).pipe(
            tap(resp => {
                if (resp && resp.auth_token) {
                    //this.cookieService.set('currentUser', JSON.stringify(user));
                    // if (loginForm.remembered) {
                      //  localStorage.setItem('currentUser', JSON.stringify(user));
                    // }
                    user.token= resp.auth_token;
                    const success = this.secureStorage.setSync({
                      key: "user",
                      value: JSON.stringify(user)
                    });
                    console.log("user.email " + user.email + resp.auth_token);
                    //this.nameTerms.next(user.email);
                    //this.currentUserSubject.next(resp);
                    return resp;
                }
            }),
            //catchError(this.handleError('Login Failed', null))
        );
  }

  logout() {
        this.currentUserSubject.next(null);
        //localStorage.removeItem('currentUser');
        //this.cookieService.delete('currentUser');
        //this.cookieService.delete('cart_id');
    }

  getStatus(authtoken: string){

    let url = this.authApiUrl+ '/status'
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
        .append("Authorization","authtoken " + authtoken)
    };

    return this.http.get<any>(url,options).pipe(
            tap(resp => {
                if (resp && resp.status=="success") {
                   // this.cookieService.set('currentUser', JSON.stringify(resp.data));
                    // if (loginForm.remembered) {
                       // localStorage.setItem('currentUser', JSON.stringify(resp.data));
                    // }
                    //this.currentUser = resp.data;

                    const success = this.secureStorage.setSync({
                      key: "userStatus",
                      value: JSON.stringify(resp.data)
                    });
                    console.log("user : " + JSON.stringify(resp.data));
                    //this.nameTerms.next(resp.data.email);
                    //this.currentUserSubject.next(resp.data);
                    return resp;
                }
            }),
            //catchError(this.handleError('Login Failed', null))
        );

  }
}
