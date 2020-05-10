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
import { UserDetailComponent } from './user-detail/user-detail.component';
import { ProductEditComponent } from './product-edit/product-edit.component';
import { PaymentstatusComponent } from './paymentstatus/paymentstatus.component';
import { HashLocationStrategy, LocationStrategy } from '@angular/common';

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    NavigationComponent,
    LoginComponent,
    HomeComponent,
    ProductComponent,
    DetailComponent,
    CartComponent,
    UserDetailComponent,
    ProductEditComponent,
    PaymentstatusComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [
    AuthService,
    CookieService,
    //{provide: LocationStrategy, useClass: HashLocationStrategy},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
