// import { Component, OnInit } from '@angular/core';
// import { Router } from "@angular/router";
// import { AuthService } from '../service/auth.service';
// import { User } from '../models/user';
// import { FormControl, FormGroup, Validators } from "@angular/forms";

// @Component({
//   selector: 'app-register',
//   templateUrl: './register.component.html',
//   styleUrls: ['./register.component.css']
// })
// export class RegisterComponent implements OnInit {
//   user: User;
//   userForm: FormGroup;

//   get email() { return this.userForm.get('email'); }
//   get password() { return this.userForm.get('password'); }
//   get mobile() { return this.userForm.get('mobile'); }

//   constructor(private router: Router, private authService: AuthService) {
//     this.user = new User();    
//     this.user.active = false;
//   }

//   ngOnInit(): void {
//     this.userForm = new FormGroup({
//       email: new FormControl(this.user.email, [
//         Validators.required,
//         Validators.email,
//         Validators.minLength(4)
//       ]),
//       password: new FormControl(this.user.password, [
//         Validators.required,
//         Validators.minLength(8)
//       ]),
//       mobile: new FormControl(this.user.mobile, Validators.required)
//     });

//   }

//   onRegister() {
//     //this.userService.register(this.user).subscribe(res => console.log('Done'));
//     this.authService.register(this.user).
//         subscribe(
//           response => {
//             console.log(response.auth_token);            
//             this.user.active = true;
//             this.router.navigate(['/']);
//           },
//           e => {
//             console.log("error");
//           }
//         )
//   }
// }


import { Component, OnInit } from '@angular/core';
import { Router} from "@angular/router";
import { AuthService } from '../service/auth.service';
import { User } from '../models/user';
import { FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  user: User;
  userForm: FormGroup;

  constructor(private router: Router, private authService: AuthService,private fb: FormBuilder) {
    this.user = new User();
    this.user.active = false;
    this.createForm();
  }


  ngOnInit(): void {
    // this.userForm = new FormGroup({
    //     email: new FormControl(this.user.email, [
    //       Validators.required,
    //       Validators.email,
    //       Validators.minLength(4)
    //     ]),
    //     password: new FormControl(this.user.password, [
    //       Validators.required,
    //       Validators.minLength(8)
    //     ]),
    //     mobile: new FormControl(this.user.mobile, Validators.required)
    //   });

  }

  get email() { return this.userForm.get('email'); }
  get password() { return this.userForm.get('password'); }
  get mobile() { return this.userForm.get('mobile'); }

  onRegister() {
    //this.userService.register(this.user).subscribe(res => console.log('Done'));
    this.authService.register(this.user).
        subscribe(
          response => {
            console.log(JSON.stringify(response));   
            if (response.status="fail")
            {              
              alert(response.message  );
              this.router.navigate(['/']);
            }
            else{
              console.log(response.auth_token);            
              this.user.active = true;
              this.router.navigate(['/']);
            }            
          },
          e => {
            //var error = JSON.parse(e);
            console.log("error" + JSON.stringify(e));
            alert("Error " + e.error.message  );
          }
        )
  }

  createForm() {
    this.userForm = this.fb.group({
      email: new FormControl(this.user.email, [
        Validators.required,
        Validators.email,
        Validators.minLength(4)
      ]),
      password: new FormControl(this.user.password, [
        Validators.required,
        Validators.minLength(8)
      ]),
      mobile: new FormControl(this.user.mobile, Validators.required)
    });
  //   this.userForm = this.fb.group({
  //     email: ['', Validators.required ],
  //     password: ['', Validators.required ],
  //     mobile: ['', Validators.required ],
  //  });
  }
}
