package com.flexigym.paymentservice.model;

public class UserLoginInfo {
	
	public UserLoginInfo(String userEmailId, String password) {
		this.userEmailId = userEmailId;
		this.password = password;
	}
	private String userEmailId;
	private String password;
	public String getUserEmailId() {
		return userEmailId;
	}
	public void setUserEmailId(String userEmailId) {
		this.userEmailId = userEmailId;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	
	
	
	
}
