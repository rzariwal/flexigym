import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { SubscribeService } from '../service/subscribe.service';
import { Router } from '@angular/router';
import { AuthResponse, User} from '../models/user';
import { Subscription} from "rxjs";
import { Page } from "tns-core-modules/ui/page";


import { SecureStorage } from 'nativescript-secure-storage';

@Component({   
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  user: User;
  currentUserSubscription: Subscription;
  currentUser: AuthResponse;
  isLoggingIn = true;
  secureStorage: SecureStorage;

  constructor(private router: Router,
              private authService: AuthService,
              private subscribeService: SubscribeService,              
              private page: Page) {
    this.user = new User();
    this.user.active = false;
    this.secureStorage = new SecureStorage();
  }

  submit() {
    if (this.isLoggingIn) {
        this.login();
    } else {
        this.signUp();
    }
  }

  signUp() {     
      
  }

  toggleDisplay() {
    this.isLoggingIn = !this.isLoggingIn;
  }

  ngOnInit()  {

    // this.currentUserSubscription = this.authService.currentUser.subscribe(
    //   user => {
    //     this.currentUser = user;
    // });
    // if (this.currentUser) {
    //   this.router.navigate(['/product']);
    // }
    this.page.actionBarHidden = true;

    var user = this.secureStorage.getSync({
      key: "user"     
    });
    if (user) {
        this.router.navigate(['/product']);
    }


  }

  //onLogin
  login(){
    //this.userService.register(this.user).subscribe(res => console.log('Done'));

    this.authService.login(this.user).subscribe(
        response => {
          console.log("Login response.message : " + response.message);

          this.authService.getStatus(response.auth_token).subscribe(
            response => {
              console.log("getStatus : " + JSON.stringify(response) );

              //  this.subscribeService.getCartByUser(response.data.user_id).subscribe(
              //     responsecart =>{
              //       console.log("getCartByUser : " + JSON.stringify(responsecart) );
              //       this.router.navigate(['/product']);
              //     },
              //     e => {
              //       console.log("error in getcartbyUser");
              //     }
              //   );

           
              this.router.navigate(['/product']);
            },
            e => {
              console.log("error");
            }
          );          
        },
        (exception)  => {
          if (exception.message) {
              alert("Exception : " + exception.message);
          } else {
              alert("Error : " + exception)
          }
        }
    );
  }
}
