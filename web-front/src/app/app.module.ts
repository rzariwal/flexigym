import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import {FormsModule} from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RegisterComponent } from './register/register.component';
import { NavigationComponent } from './navigation/navigation.component';
import { LoginComponent } from './login/login.component';
import { AuthService } from './service/auth.service';
import {CookieService} from "ngx-cookie-service";
import { HomeComponent } from './home/home.component';
import { ProductComponent } from './product/product.component';
import { DetailComponent } from "./product-detail/detail.component";
import { CartComponent } from "./cart/cart.component";
// import {JwtInterceptor} from "../../../frontend/src/app/_interceptors/jwt-interceptor.service";
// import {ErrorInterceptor} from "../../../frontend/src/app/_interceptors/error-interceptor.service";

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    NavigationComponent,
    LoginComponent,
    HomeComponent,
    ProductComponent,
    DetailComponent,
    CartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    AuthService,
    CookieService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
