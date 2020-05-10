import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import { ProductComponent } from './product/product.component';
import { DetailComponent } from "./product-detail/detail.component";
import { ProfileComponent } from './profile/profile.component';

import {CartComponent} from "./cart/cart.component";
import {UserDetailComponent} from "./user-detail/user-detail.component";
import {ProductEditComponent} from "./product-edit/product-edit.component";
import {PaymentstatusComponent} from "./paymentstatus/paymentstatus.component";

const routes: Routes = [

  {path: '', component: HomeComponent},
  {path: 'home', component: HomeComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'product', component: ProductComponent},
  {path: 'product/:id', component: DetailComponent},
  {path: 'cart', component: CartComponent},
  {path: 'userdetail', component: UserDetailComponent},
  {path: 'admin', redirectTo: 'admin/product', pathMatch: 'full'},
  {
      path: 'admin/product',
      component: ProductComponent,
      //anActivate: [AuthGuard],
      //data: {roles: [Role.Manager, Role.Employee]}
  },
  {
      path: 'admin/product/:id/edit',
      component: ProductEditComponent,
      //canActivate: [AuthGuard],
      //data: {roles: [Role.Manager, Role.Employee]}
  },
  {
      path: 'admin/product/:id/new',
      component: ProductEditComponent,
      //canActivate: [AuthGuard],
      //data: {roles: [Role.Employee]}
  },
  {path: 'profile', component: ProfileComponent},
  {path: 'cart/:status', component: PaymentstatusComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
