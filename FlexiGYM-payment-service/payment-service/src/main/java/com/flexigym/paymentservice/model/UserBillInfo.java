package com.flexigym.paymentservice.model;

public class UserBillInfo {
	
	private String userEmailId;
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
