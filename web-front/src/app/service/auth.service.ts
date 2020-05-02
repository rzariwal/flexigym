import { Injectable } from '@angular/core';
import { User, AuthResponse } from '../models/user';
import { HttpClientModule, HttpClient, HttpRequest, HttpHeaders, HttpEventType, HttpResponse} from '@angular/common/http';
import {CookieService} from 'ngx-cookie-service';
import {BehaviorSubject, Observable, of, Subject} from 'rxjs';
import {catchError, tap} from 'rxjs/operators';





@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private authApiUrl = 'http://web:5000/auth';
  private currentUserSubject: BehaviorSubject<AuthResponse>;
  public currentUser: Observable<AuthResponse>;
  public nameTerms = new Subject<string>();
  public name$ = this.nameTerms.asObservable();

  constructor(private http: HttpClient,
              private cookieService: CookieService) {
        const memo = localStorage.getItem('currentUser');
        this.currentUserSubject = new BehaviorSubject<AuthResponse>(JSON.parse(memo));
        this.currentUser = this.currentUserSubject.asObservable();
        cookieService.set('currentUser', memo);

        console.log('currentUser is '+ memo);
  }

  register(user: User): Observable<AuthResponse>{
    let url = this.authApiUrl+ '/register'
    let body = JSON.stringify({ "email":user.email,"password":user.password, "mobile":user.mobile });
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
    }
    console.log("Done");
    return this.http.post<AuthResponse>(url,body,options);
  }

  login(user: User): Observable<AuthResponse>{
    let url = this.authApiUrl+ '/login'
    let body = JSON.stringify({ "email":user.email,"password":user.password });
    const options = {
      headers: new HttpHeaders().append('Content-Type', 'application/json')
    }
    console.log("Done");
    return this.http.post<AuthResponse>(url,body,options).pipe(
            tap(resp => {
                if (resp && resp.auth_token) {
                    this.cookieService.set('currentUser', JSON.stringify(user));
                    // if (loginForm.remembered) {
                        localStorage.setItem('currentUser', JSON.stringify(user));
                    // }
                    console.log("user.email " + user.email);
                    this.nameTerms.next(user.email);
                    this.currentUserSubject.next(resp);
                    return resp;
                }
            }),
            //catchError(this.handleError('Login Failed', null))
        );
  }

  logout() {
        this.currentUserSubject.next(null);
        localStorage.removeItem('currentUser');
        this.cookieService.delete('currentUser');
    }

  getStatus(authtoken: string){

    console.log("Done");

  }
}
