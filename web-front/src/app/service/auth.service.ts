import { Injectable } from '@angular/core';
import { User, AuthResponse } from '../models/user';
import { Observable } from 'rxjs';
import { HttpClientModule, HttpClient, HttpRequest, HttpHeaders, HttpEventType, HttpResponse} from '@angular/common/http';




@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private authApiUrl = 'http://35.198.220.113:5000/auth';

  constructor(private http: HttpClient) {

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
    return this.http.post<AuthResponse>(url,body,options);
  }

  getStatus(authtoken: string){

    console.log("Done");

  }
}
