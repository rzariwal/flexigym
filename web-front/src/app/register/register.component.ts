import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { AuthService } from '../service/auth.service';
import { User } from '../models/user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  user: User;

  constructor(private router: Router, private authService: AuthService) {
    this.user = new User();
    this.user.active = false;
  }

  ngOnInit(): void {

  }

  onRegister() {
    //this.userService.register(this.user).subscribe(res => console.log('Done'));
    this.authService.register(this.user).
        subscribe(
          response => {
            console.log(response.auth_token);
            console.log(response.auth_token);
            this.user.active = true;
            this.router.navigate(['/']);
          },
          e => {
            console.log("error");
          }
        )
  }
}
