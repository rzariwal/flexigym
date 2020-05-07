import {Component, OnInit} from '@angular/core';
import {AuthService} from "../service/auth.service";
import {User, AuthResponse} from "../models/user";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.css']
})
export class UserDetailComponent implements OnInit {

  currentUserSubscription: Subscription;
  currentUser: AuthResponse;
  user : User;

  constructor(private authService: AuthService) {
  }

  ngOnInit(): void {
    // let user= this.cookieService.get('currentUser');
    // console.log(user);
    this.currentUserSubscription = this.authService.currentUser.subscribe(user => {
      console.log("User in user profile :" + JSON.stringify(user) );
      this.currentUser = user;
      this.user = user;
    });
  }

}
