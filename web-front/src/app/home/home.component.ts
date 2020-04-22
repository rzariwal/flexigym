import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { Router } from '@angular/router';
import { User } from '../models/user';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  user: User;

  constructor(private router: Router, private authService: AuthService) {
    this.user = new User();
    this.user.active = false;
  }

  ngOnInit(): void {
  }

  onLogin(){
    //this.userService.register(this.user).subscribe(res => console.log('Done'));
    this.authService.login(this.user).
        subscribe(
          response => {
            console.log(response.message);
            this.router.navigate(['/product']);
          },
          e => {
            console.log("error");
          }
        )
  }
}
