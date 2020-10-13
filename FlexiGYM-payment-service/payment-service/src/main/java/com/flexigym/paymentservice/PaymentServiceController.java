package com.flexigym.paymentservice;

import io.swagger.annotations.ApiOperation;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;


@RestController
@EnableAutoConfiguration
public class PaymentServiceController {

	@Value("${service.url}")
	String service_url;


	PayPalClient payPalClient = new PayPalClient();
    	
	@RequestMapping(value = "/payment/create", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
	@ApiOperation(value = "create payment via PayPal will return a sandbox redirect URL where user have to login:password (danyjacob45@icloud.com:flexigym) and make payment")
	@ResponseBody
	Map<String, Object> createPayment(@RequestBody Map<String, String> amount) {
		Map<String, Object> response = new HashMap<String, Object>();

		//return a redirect URL
		try{
			System.out.println(service_url);
			System.out.println(amount.get("amount"));
			String sum = amount.get("amount");
			return payPalClient.createPayment(sum, service_url);
		}
		catch (Exception e){
			response.put("status", "failed");
			return response;
		}

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
	public String home() {
		return "Payment Service Home\nPlease try \n /api/create\n /api/complete\n /api/cancel\n /api/notify";					 
	}
	
	@PostMapping("/payment/cancel")
	@RequestMapping(value = "/payment/cancel", method = RequestMethod.GET)
	@ApiOperation(value = "cancel payment called by PayPal")
	@ResponseBody
	public String cancel() {
		return "cancel Payment";
	}
	
	@PostMapping("/payment/notify")
	@ApiOperation(value = "call notify api")
	@ResponseBody
	public String notification() {
		return "notify";
	}

}
