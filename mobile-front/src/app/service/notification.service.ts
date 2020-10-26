import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notifUrl = 'http://flexigym-notification-api:5000/auth';

  constructor() { }
}
