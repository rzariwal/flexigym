import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http'
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor {

  constructor(private authService: AuthService) { }

  intercept(req, next){
    const token = localStorage.getItem("id_token");
    if(token) {
      let tokenizedReq = req.clone({
        setHeaders : {
          Authorization: `Bearer ${token}`
        }

      })
      return next.handle(tokenizedReq)
    }
    else {
      return next.handle(req);
    }
  }
}
