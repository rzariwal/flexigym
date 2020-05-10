import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AdvertiseService} from "../service/advertise.service";
import {SubscribeService} from "../service/subscribe.service";
import {PaymentService} from "../service/payment.service";
import {HttpParams} from "@angular/common/http";

@Component({
  selector: 'app-paymentstatus',
  templateUrl: './paymentstatus.component.html',
  styleUrls: ['./paymentstatus.component.css']
})
export class PaymentstatusComponent implements OnInit {

  status: string;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private subscribeService: SubscribeService,
    private paymentService: PaymentService) {
  }

  ngOnInit(): void {
    const status = this.route.snapshot.paramMap.get('status');

    if (status == "complete") {
      this.status = "Payment is successfully completed.";

      let completeUrl: string = this.router.url;
      console.log("this url " + completeUrl);

      let paramValue;
      if (completeUrl.includes('?')) {
        paramValue = completeUrl.split('?')[1];
        console.log("param " + paramValue);
      }
      // this.paymentService.getCompleteStatus(paramValue).subscribe(
      //   response => {
      //     console.log('Payments datail:  ' + JSON.stringify(response));
      //   }
      // )

      this.subscribeService.getCompleteStatus(paramValue).subscribe(
        response => {
          console.log('Payments datail:  ' + JSON.stringify(response));
        }
      )






      this.subscribeService.clearCart();
    } else {
      this.status = "Payment is cancelled.";
    }

  }

}
