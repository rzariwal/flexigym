import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { NativeScriptModule } from "@nativescript/angular";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";

import { HomeComponent } from "./home/home.component";
import { ProductComponent } from "./product/product.component";
import { DetailComponent } from "./product-detail/detail.component";
import { CartComponent } from "./cart/cart.component";

import { AuthService } from './service/auth.service';

import { NativeScriptFormsModule } from "@nativescript/angular";
import { HttpClientModule } from '@angular/common/http';

@NgModule({
    bootstrap: [
        AppComponent
    ],
    imports: [
        NativeScriptModule,
        NativeScriptFormsModule,
        AppRoutingModule,
        HttpClientModule
    ],
    declarations: [
        AppComponent,        
        ProductComponent,
        DetailComponent,
        HomeComponent,
        CartComponent
    ],
    providers: [
        AuthService       
    ],
    schemas: [
        NO_ERRORS_SCHEMA
    ]
})
export class AppModule { }
