import {Injectable} from '@angular/core';
import {paymentApi} from "../../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {catchError} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private paymentApiUrl = `${paymentApi}`;

  constructor(private http: HttpClient) {
  }

  getCompleteStatus(param: string): Observable<any> {
    let url = `${this.paymentApiUrl}/complete?` + param ;
    return this.http.get<any>(url).pipe(
      catchError(_ => of([]))
    );
  }
}
