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
    	
	@PostMapping("/api/create")
	@ApiOperation(value = "create payment via PayPal will return a sandbox redirect URL where user have to login:password (danyjacob45@icloud.com:flexigym) and make payment")
	@ResponseBody
	Map<String, Object> createPayment(@RequestParam("amount") String amount, @RequestParam("user_token") String token) {
		//for test purpose - sign in first -> to generate a token
		//actual case -> the caller of this service has to pass the user_token
		RestTemplate restTemplate = new RestTemplate();
		HttpHeaders headers = new HttpHeaders();
	        headers.setContentType(MediaType.APPLICATION_JSON);	    
	        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

	        // request body parameters
		Map<String, Object> map = new HashMap<>();
		map.put("email", "danyjacob45@gmail.com");
		map.put("password", "password");
	
		// build the request
		HttpEntity<Map<String, Object>> entity = new HttpEntity<>(map, headers);
		
		
		System.out.println("\nDebug..");
		System.out.println(entity.toString());
		// send POST request
		final String auth_login = "http://34.87.6.16:5000/auth/login";
		ResponseEntity<String> status = restTemplate.postForEntity(auth_login, entity, String.class);
		System.out.println(restTemplate.toString());
		//check token is valid and alive
		System.out.println(status);
		
		//final String auth_status = "http://34.87.6.16:5000/auth/status";
		//UserBillInfo userInfo = restTemplate.getForObject(auth_status, UserBillInfo.class);
	     
	        //System.out.println(userInfo.toString());

		
		//if valid, proceed to payment using PayPal
		
		//return a redirect URL
		return payPalClient.createPayment(amount);
	}
	
	@RequestMapping(value = "/api/complete", method = RequestMethod.GET)
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
	
	@PostMapping("/api/cancel")
	@RequestMapping(value = "/api/cancel", method = RequestMethod.GET)
	@ApiOperation(value = "cancel payment called by PayPal")
	@ResponseBody
	String cancel() {
		return "cancel Payment";
	}
	
	@PostMapping("/api/notify")
	@ApiOperation(value = "call notify api")
	@ResponseBody
	String notification() {
		return "notify";
	}

}
