import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AdvertiseService } from '../service/advertise.service';
import { SubscribeService } from '../service/subscribe.service';
import { User } from '../models/user';
import { Product } from '../models/product';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {
  user: User;
  products: Product;

  constructor(private router: Router,
              private advertiseService: AdvertiseService,
              private subscribeService: SubscribeService) { }

  ngOnInit(): void {
    this.user = new User();
    this.advertiseService.getAllPackages(this.user).subscribe(
      resp => {
        this.products = resp;
        console.log(this.products.packages);
      }
    );
  }

}
