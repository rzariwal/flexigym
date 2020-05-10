import { Component, OnInit, OnDestroy } from '@angular/core';
import {Router} from "@angular/router";
import { Subscription } from 'rxjs';
import {User, AuthResponse} from "../models/user";
import {AuthService} from "../service/auth.service";

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit, OnDestroy {

  currentUserSubscription: Subscription;
  name$;
  name: string;
  currentUser: AuthResponse;
  root = '/';
  user : User;

  constructor(private authService: AuthService,
              private router: Router)
  { }

  ngOnDestroy(): void {
    throw new Error("Method not implemented.");
  }

  ngOnInit() {
    this.name$ = this.authService.name$.subscribe(aName => this.name = aName);
     this.currentUserSubscription = this.authService.currentUser.subscribe(user => {
            this.currentUser = user;
            this.user = user;
            console.log("user is in Navigation : " + JSON.stringify(user) );
            // if (!user || user.role == Role.Customer) {
            //     this.root = '/';
            // } else {
            //     this.root = '/seller';
            // }
        });
  }

   logout() {
        this.authService.logout();
         this.router.navigate(['/'], {queryParams: {logout: 'true'}} );
    }

}
