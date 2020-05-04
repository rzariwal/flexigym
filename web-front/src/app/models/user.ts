export class User {
  email: string;
  password: string;
  mobile: string;
  token: string;
  active: boolean;

  constructor(){
    this.token = " ";
    this.active = false;
  }

}

export interface AuthResponse {
  status: string;
  auth_token: string;
  message: string;
  user_id: number;
}
