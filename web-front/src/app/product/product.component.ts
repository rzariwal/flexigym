import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { Router } from '@angular/router';
import { AdvertiseService } from '../service/advertise.service';
import { userInfo } from 'os';
import { User } from '../models/user';
import { Product } from '../models/product';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {
  user: User;
  product: Product;

  constructor(private router: Router, private advertiseService: AdvertiseService) { }

  ngOnInit(): void {
    this.user = new User();
    this.advertiseService.getAllPackages(this.user).subscribe(resp => {
      console.log(resp[0].id);
    });
  }

}
