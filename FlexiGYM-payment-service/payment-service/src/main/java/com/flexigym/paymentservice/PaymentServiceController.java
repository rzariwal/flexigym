package com.flexigym.paymentservice;

import io.swagger.annotations.ApiOperation;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;


@RestController
@EnableAutoConfiguration
public class PaymentServiceController {
	
	PayPalClient payPalClient = new PayPalClient();
    	
	@RequestMapping(value = "/payment/create", method = RequestMethod.POST)
	@ApiOperation(value = "create payment via PayPal will return a sandbox redirect URL where user have to login:password (danyjacob45@icloud.com:flexigym) and make payment")
	@ResponseBody
	Map<String, Object> createPayment(@RequestParam("amount") String amount) {
		
		//return a redirect URL
		return payPalClient.createPayment(amount);
	}
	
	@RequestMapping(value = "/payment/complete", method = RequestMethod.GET)
	@ApiOperation(value = "complete payment via PayPal; Paypal will call this api if payment is successfull")
	@ResponseBody
	public String completePayment(@RequestParam("paymentId") String paymentId,
				      @RequestParam("token")     String token,
				      @RequestParam("PayerID")   String payerId)
	{
		/*
		public Map<String, Object> completePayment(HttpServletRequest request)
		@RequestParam("paymentId") String paymentId, @RequestParam("token") String token
		return payPalClient.completePayment(request)
		 */
		//paypal emailid = sb-cdspm1225968@business.example.com
		
		return payPalClient.completePayment(paymentId,payerId).toString();
	}
	
	@RequestMapping(value = "/",method = RequestMethod.GET)
	@ApiOperation(value = "home")
	@ResponseBody
	String home() {
		return "Payment Service Home\nPlease try \n /api/create\n /api/complete\n /api/cancel\n /api/notify";					 
	}
	
	@PostMapping("/payment/cancel")
	@RequestMapping(value = "/payment/cancel", method = RequestMethod.GET)
	@ApiOperation(value = "cancel payment called by PayPal")
	@ResponseBody
	String cancel() {
		return "cancel Payment";
	}
	
	@PostMapping("/payment/notify")
	@ApiOperation(value = "call notify api")
	@ResponseBody
	String notification() {
		return "notify";
	}

}
