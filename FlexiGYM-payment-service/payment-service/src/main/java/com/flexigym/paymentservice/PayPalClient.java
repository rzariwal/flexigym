package com.flexigym.paymentservice;

import com.paypal.api.payments.*;
import com.paypal.base.rest.APIContext;
import com.paypal.base.rest.PayPalRESTException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PayPalClient {
	
	//String clientId = "Ad2B9OIlW4CcxQDBChki_fxyL_674wRQ02BKZexs808ZewMbZVSEh8Y1QTgx7E8iiNQULzNTAW-7MKe2";
	String clientId = "AS7GA_K71C4Uht_6wSXvzfAyp0c0TihSy_cHU_XFhROlxvNHDZbDuTpyIVp5-la9_A26bq7hUMM9q8xd";

	//String clientSecret = "EOkqwmJcSx5HHhZnHmiNtm8ZK_CO6y3NVotWbCOB2Sa5RFolYehmEZYSikrEowYv4aV6ZqEBZo9AEtoL";
	String clientSecret = "EHU1IKl6kqQdrFivDxsTeValURdA-cZtelehTbsnifb6UDkUJNApYPlA4zOp_RnNB3qfszOsPW39rhuu";
	public Map<String, Object> createPayment(String sum){
	    Map<String, Object> response = new HashMap<String, Object>();
	    Amount amount = new Amount();
	    amount.setCurrency("SGD");
	    amount.setTotal(sum);
	    Transaction transaction = new Transaction();
	    transaction.setAmount(amount);
	    List<Transaction> transactions = new ArrayList<Transaction>();
	    transactions.add(transaction);

	    Payer payer = new Payer();
	    payer.setPaymentMethod("paypal");

	    Payment payment = new Payment();
	    payment.setIntent("sale");
	    payment.setPayer(payer);
	    payment.setTransactions(transactions);

	    RedirectUrls redirectUrls = new RedirectUrls();
	    redirectUrls.setCancelUrl("http://localhost:4200/cancel");
	    redirectUrls.setReturnUrl("http://localhost:8000/api/complete");
	    payment.setRedirectUrls(redirectUrls);
	    Payment createdPayment;
	    try {
	        String redirectUrl = "";
	        APIContext context = new APIContext(clientId, clientSecret, "sandbox");
	        createdPayment = payment.create(context);
	        if(createdPayment!=null){
	            List<Links> links = createdPayment.getLinks();
	            for (Links link:links) {
	                if(link.getRel().equals("approval_url")){
	                    redirectUrl = link.getHref();
	                    break;
	                }
	            }
	            response.put("status", "success");
	            response.put("redirect_url", redirectUrl);
	        }
	    } catch (PayPalRESTException e) {
	        System.out.println("Error happened during payment creation!");
	    }
	    return response;
	}
	//public Map<String, Object> completePayment(HttpServletRequest req){
	public Map<String, Object> completePayment(String paymentId, String payerId){
	    Map<String, Object> response = new HashMap();
	    Payment payment = new Payment();
	    //payment.setId(req.getParameter("paymentId"));
		payment.setId(paymentId);
	    PaymentExecution paymentExecution = new PaymentExecution();
		//paymentExecution.setPayerId(req.getParameter("PayerID"));
		paymentExecution.setPayerId(payerId);
	    try {
	        APIContext context = new APIContext(clientId, clientSecret, "sandbox");
	        Payment createdPayment = payment.execute(context, paymentExecution);
	        //createdPayment.getState();
	        if(createdPayment!=null){
	            response.put("status", "success");
	            response.put("payment", createdPayment);
	        }
	    } catch (PayPalRESTException e) {
	        System.err.println(e.getDetails());
	    }
	    return response;
	}


}
