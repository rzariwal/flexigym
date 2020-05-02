import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PaymentService {

  private notifUrl = 'http://payment-api:5000/auth';

  constructor() { }
}
