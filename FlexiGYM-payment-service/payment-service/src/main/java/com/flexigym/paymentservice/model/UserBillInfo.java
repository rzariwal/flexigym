package com.flexigym.paymentservice.model;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;


@ApiModel(description = "All details about the user bill. ")
public class UserBillInfo {
	@ApiModelProperty(notes="user email ID")
	private String userEmailId;
	@ApiModelProperty(notes="user bill amount")
	private int amount;
	
	
	public UserBillInfo(String userEmailId, int amount) {
		this.userEmailId = userEmailId;
		this.amount = amount;
	}
	
	
	public String getUserEmailId() {
		return userEmailId;
	}
	
	public void setUserEmailId(String userEmailId) {
		this.userEmailId = userEmailId;
	}
	
	public int getAmount() {
		return amount;
	}
	
	public void setAmount(int amount) {
		this.amount = amount;
	}
	
}
