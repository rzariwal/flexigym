import {AfterContentChecked, Component, OnInit} from '@angular/core';
import { Product } from '../models/product';
import {ActivatedRoute, Router} from "@angular/router";
import { AdvertiseService } from '../service/advertise.service';



@Component({
  selector: 'app-product-edit',
  templateUrl: './product-edit.component.html',
  styleUrls: ['./product-edit.component.css']
})
export class ProductEditComponent implements OnInit, AfterContentChecked {

  product = new Product();

  constructor(private advertiseService: AdvertiseService,
              private route: ActivatedRoute,
              private router: Router) {
  }

  productId: string;
  isEdit = false;

  ngOnInit() {
    this.productId = this.route.snapshot.paramMap.get('id');
    if (this.productId || this.productId != "0" ) {
      this.isEdit = true;
      this.advertiseService.getDetail(this.productId).subscribe(prod => this.product = prod);
    }

  }

  update() {
    this.advertiseService.update(this.product).subscribe(prod => {
        if (!prod) throw new Error();
        this.router.navigate(['/admin']);
      },
      err => {
      });

  }

  onSubmit() {
    if (this.productId && this.productId != "0" ) {
       console.log("update" + this.productId);
      this.update();
    } else {
      console.log("add");
      this.add();
    }
  }

  add() {
    this.advertiseService.create(this.product).subscribe(prod => {
        if (!prod) throw new Error;
        this.router.navigate(['/']);
      },
      e => {
      });
  }

  ngAfterContentChecked(): void {
    console.log(this.product);
  }

}
