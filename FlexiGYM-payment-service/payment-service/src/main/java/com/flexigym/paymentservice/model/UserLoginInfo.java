package com.flexigym.paymentservice.model;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;


@ApiModel(description = "All details about the user login. ")
public class UserLoginInfo {
	
	public UserLoginInfo(String userEmailId, String password) {
		this.userEmailId = userEmailId;
		this.password = password;
	}
	@ApiModelProperty(notes="user email ID")
	private String userEmailId;
	@ApiModelProperty(notes="user password")
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
