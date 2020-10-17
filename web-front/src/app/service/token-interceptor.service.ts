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
    const token = this.authService.getJWTToken();
    let tokenizedReq = req.clone({
      setHeaders : {
        Authorization: `Bearer ${token}`
      }

    })
    return next.handle(tokenizedReq)
  }
}
