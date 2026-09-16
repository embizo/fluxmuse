<?php
// Safaricom Daraja API (M-Pesa) — STK Push (Lipa Na M-Pesa Online), for cardless
// in-person checkout in Kenya. Mirrors the self-contained gateway-library pattern
// used by Paystack_class_ecommerce.php.
// Docs: https://developer.safaricom.co.ke/APIs/MpesaExpressSimulate
class Mpesa_class_ecommerce{

	public $consumer_key;
	public $consumer_secret;
	public $shortcode;
	public $passkey;
	public $environment = 'sandbox'; // 'sandbox' or 'live'

	function __construct()
	{
		$this->CI =& get_instance();
	}

	private function base_url()
	{
		return $this->environment=='live'
			? "https://api.safaricom.co.ke"
			: "https://sandbox.safaricom.co.ke";
	}

	// OAuth token — short-lived, callers should not cache across requests since
	// each STK push in this codebase is a one-off ajax call.
	public function get_access_token()
	{
		$curl = curl_init();
		curl_setopt_array($curl, array(
			CURLOPT_URL => $this->base_url()."/oauth/v1/generate?grant_type=client_credentials",
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_TIMEOUT => 30,
			CURLOPT_USERPWD => $this->consumer_key.":".$this->consumer_secret,
			CURLOPT_HTTPHEADER => array("Cache-Control: no-cache"),
		));

		$result = curl_exec($curl);
		$err = curl_error($curl);
		curl_close($curl);

		if($err) return array('status'=>'Error','message'=>"cURL Error #:".$err);

		$result = json_decode($result,true);

		if(empty($result['access_token'])) return array('status'=>'Error','message'=>isset($result['errorMessage']) ? $result['errorMessage'] : "Unable to obtain M-Pesa access token");

		return array('status'=>'Success','access_token'=>$result['access_token']);
	}

	// Triggers the STK Push prompt on the customer's phone. $phone must be MSISDN
	// format (2547XXXXXXXX / 2541XXXXXXXX, no leading + or 0).
	public function stk_push($phone, $amount, $account_reference, $description, $callback_url)
	{
		$token_response = $this->get_access_token();
		if($token_response['status']=='Error') return $token_response;

		$timestamp = date('YmdHis');
		$password = base64_encode($this->shortcode.$this->passkey.$timestamp);

		$payload = array(
			"BusinessShortCode" => $this->shortcode,
			"Password" => $password,
			"Timestamp" => $timestamp,
			"TransactionType" => "CustomerPayBillOnline",
			"Amount" => intval(round($amount)),
			"PartyA" => $phone,
			"PartyB" => $this->shortcode,
			"PhoneNumber" => $phone,
			"CallBackURL" => $callback_url,
			"AccountReference" => substr($account_reference,0,12),
			"TransactionDesc" => substr($description,0,13)
		);

		$curl = curl_init();
		curl_setopt_array($curl, array(
			CURLOPT_URL => $this->base_url()."/mpesa/stkpush/v1/processrequest",
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_TIMEOUT => 30,
			CURLOPT_CUSTOMREQUEST => "POST",
			CURLOPT_POSTFIELDS => json_encode($payload),
			CURLOPT_HTTPHEADER => array(
				"Authorization: Bearer ".$token_response['access_token'],
				"Content-Type: application/json",
			),
		));

		$result = curl_exec($curl);
		$err = curl_error($curl);
		curl_close($curl);

		if($err) return array('status'=>'Error','message'=>"cURL Error #:".$err);

		$result = json_decode($result,true);

		if(!isset($result['ResponseCode']) || $result['ResponseCode']!='0')
		{
			return array('status'=>'Error','message'=>isset($result['errorMessage']) ? $result['errorMessage'] : (isset($result['ResponseDescription']) ? $result['ResponseDescription'] : "STK push request failed"));
		}

		return array(
			'status' => 'Success',
			'checkout_request_id' => $result['CheckoutRequestID'],
			'merchant_request_id' => $result['MerchantRequestID']
		);
	}

	// Optional fallback poll if the async callback is delayed/missed.
	public function query_stk_status($checkout_request_id)
	{
		$token_response = $this->get_access_token();
		if($token_response['status']=='Error') return $token_response;

		$timestamp = date('YmdHis');
		$password = base64_encode($this->shortcode.$this->passkey.$timestamp);

		$payload = array(
			"BusinessShortCode" => $this->shortcode,
			"Password" => $password,
			"Timestamp" => $timestamp,
			"CheckoutRequestID" => $checkout_request_id
		);

		$curl = curl_init();
		curl_setopt_array($curl, array(
			CURLOPT_URL => $this->base_url()."/mpesa/stkpushquery/v1/query",
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_TIMEOUT => 30,
			CURLOPT_CUSTOMREQUEST => "POST",
			CURLOPT_POSTFIELDS => json_encode($payload),
			CURLOPT_HTTPHEADER => array(
				"Authorization: Bearer ".$token_response['access_token'],
				"Content-Type: application/json",
			),
		));

		$result = curl_exec($curl);
		$err = curl_error($curl);
		curl_close($curl);

		if($err) return array('status'=>'Error','message'=>"cURL Error #:".$err);

		return array('status'=>'Success','result'=>json_decode($result,true));
	}

}
?>
