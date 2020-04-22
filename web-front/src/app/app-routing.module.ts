import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import { ProductComponent } from './product/product.component';


const routes: Routes = [

  {path: '', component: HomeComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'product', component: ProductComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
