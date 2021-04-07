import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { SubscribeService } from '../service/subscribe.service';
import { Router } from '@angular/router';
import {AuthResponse, User} from '../models/user';
import {Subscription} from "rxjs";
import { FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  user: User;
  currentUserSubscription: Subscription;
  currentUser: AuthResponse;
  userForm: FormGroup;

  constructor(private router: Router,
              private authService: AuthService,
              private subscribeService: SubscribeService,
              private fb: FormBuilder) {
    this.user = new User();
    this.user.active = false;
    this.createForm();
  }

  ngOnInit()  {

    this.currentUserSubscription = this.authService.currentUser.subscribe(user => {
            this.currentUser = user;
        });
    if (this.currentUser) {
      this.router.navigate(['/product']);
    }

  }

  get email() { return this.userForm.get('email'); }
  get password() { return this.userForm.get('password'); }

  createForm() {
    this.userForm = this.fb.group({
      email: new FormControl(this.user.email, [
        Validators.required,
        Validators.email,
        Validators.minLength(4)
      ]),
      password: new FormControl(this.user.password, [
        Validators.required
      ])
    });
  
  }

  onLogin(){
    //this.userService.register(this.user).subscribe(res => console.log('Done'));

    this.authService.login(this.user).
      subscribe(
        response => {
          console.log("Login response.message : " + response.message);

          this.authService.getStatus(response.auth_token).subscribe(
            response => {
              console.log("getStatus : " + JSON.stringify(response) );

               this.subscribeService.getCartByUser(response.data.user_id).subscribe(
                  responsecart =>{
                    console.log("getCartByUser : " + JSON.stringify(responsecart) );
                    this.router.navigate(['/product']);
                  },
                  e => {
                    console.log("error in getcartbyUser"  + JSON.stringify(e));
                    alert("Error");
                  }
                ); 
            },
            e => {
              console.log("error"  + JSON.stringify(e));
              alert("Error");
            }
          );
          //this.router.navigate(['/product']);

        },
        e => {
          console.log("error" + JSON.stringify(e));
          alert("Error : " + e.error.message);
        }
      );

  }
}
