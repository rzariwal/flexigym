package com.flexigym.paymentservice;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;


@RestController
@EnableAutoConfiguration
public class PaymentServiceController {
	
	PayPalClient payPalClient = new PayPalClient();
    	
	@PostMapping("/api/create")
	@ResponseBody
	Map<String, Object> createPayment(@RequestParam("amount") String amount, @RequestParam("user_token") String token) {
		//for test purpose - sign in first -> to generate a token
		//actual case -> the caller of this service has to pass the user_token
		RestTemplate restTemplate = new RestTemplate();
		//RestTemplate restTemplateJson = new RestTemplate();
	    
		HttpHeaders headers = new HttpHeaders();
	    headers.setContentType(MediaType.APPLICATION_JSON);	    
	    headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
		// request body parameters
		Map<String, Object> map = new HashMap<>();
		map.put("email", "danyjacob45@gmail.com");
		map.put("password", "password");
	
		// build the request
		HttpEntity<Map<String, Object>> entity = new HttpEntity<>(map, headers);
		
		
		System.out.println("\nDebug................");
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
	
	@PostMapping(value = "/api/complete")
	public Map<String, Object> completePayment(HttpServletRequest request){
		//paypal emailid = sb-5u3jf1249026@personal.example.com
		
		return payPalClient.completePayment(request);
	}
	
	@PostMapping("/")
	@ResponseBody
	String home() {
		return "Payment Service Home";
	}
	
	@PostMapping("/api/cancel")
	@ResponseBody
	String cancel() {
		return "cancel Payment";
	}
	
	@PostMapping("/api/notify")
	@ResponseBody
	String notification() {
		return "notify";
	}

}
