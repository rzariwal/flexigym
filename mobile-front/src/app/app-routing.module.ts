import { NgModule } from "@angular/core";
import { Routes } from "@angular/router";
import { NativeScriptRouterModule } from "@nativescript/angular";

import { HomeComponent } from "./home/home.component";
import { ProductComponent } from "./product/product.component";
import { DetailComponent } from "./product-detail/detail.component";
import { CartComponent } from "./cart/cart.component";


const routes: Routes = [
    { path: "", redirectTo: "/home", pathMatch: "full" },   
    { path: "home", component: HomeComponent }, 
    { path: "product", component: ProductComponent },
    { path: "product/:id", component: DetailComponent},
    { path: 'cart', component: CartComponent},
];

@NgModule({
    imports: [NativeScriptRouterModule.forRoot(routes)],
    exports: [NativeScriptRouterModule]
})
export class AppRoutingModule { }
