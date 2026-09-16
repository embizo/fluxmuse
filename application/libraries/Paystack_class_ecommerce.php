<?php
class Paystack_class_ecommerce{

	// //https://paystack.com/docs/payments/accept-payments

	public $secret_key;
	public $public_key;	
	public $description;
	public $amount;
	public $action_url;	
	public $currency;
	public $img_url;
	public $title;
	public $customer_first_name;
	public $customer_last_name;
	public $customer_email;
	public $button_lang='';
	public $secondary_button=false;


	function __construct()
	{		
		$this->CI =& get_instance();
	}
	
	function set_button(){

		$receipt="".time()."";
		$paystack_lang = !empty($this->button_lang)?$this->button_lang:$this->CI->lang->line("Paystack Payment");
		$amount=$this->amount*100;
		$button="";
		if($this->secondary_button)
		{
			$button.="
			<a href='#' class='list-group-item list-group-item-action flex-column align-items-start' id='paystack_clone' onclick='payWithPaystack();'>
			    <div class='d-flex w-100 align-items-center'>
			      <small class='text-muted'><img class='rounded' width='60' height='60' src='".base_url('assets/img/payment/paystack.png')."'></small>
			      <h6 class='mb-1'>".$paystack_lang."</h6>
			    </div>
			</a>";
		}
		else $button.="<button onclick='payWithPaystack()''>{$paystack_lang}</button>";
		$button.= "<script src='https://js.paystack.co/v1/inline.js'></script>";

		$button.="<script>
			function payWithPaystack() {
			  var handler = PaystackPop.setup({
			    key: '{$this->public_key}', // Replace with your public key
			    email: '{$this->customer_email}',
			    amount: {$amount}, // the amount value is multiplied by 100 to convert to the lowest currency unit
			    currency: '{$this->currency}', // Use GHS for Ghana Cedis or USD for US Dollars
			    firstname: '{$this->customer_first_name}',
			    lastname: '{$this->customer_last_name}',
			    reference: '{$receipt}', // Replace with a reference you generated
			    callback: function(response) {
			      //this happens after the payment is completed successfully
			      var reference = response.reference;
			      window.location = '{$this->action_url}/' + response.reference;

			      //alert('Payment complete! Reference: ' + reference);
			      // Make an AJAX call to your server with the reference to verify the transaction
			    },
			    onClose: function() {
			      //alert('Transaction was not completed, window closed.');
			    },
			  });
			  handler.openIframe();
			}
		</script>";

		return $button;
	}
	
	// Hosted checkout (Paystack "Initialize Transaction") for cardless/QR/pay-link in-person checkout.
	// https://paystack.com/docs/api/transaction/#initialize
	public function initialize_transaction($cart_id, $amount, $currency, $email, $callback_url, $reference='')
	{
		if(empty($reference)) $reference = strtoupper('CNT'.$cart_id.time());

		$payload = array(
			"amount" => intval(round($amount*100)), // lowest currency unit
			"email" => !empty($email) ? $email : "guest+cart{$cart_id}@example.com",
			"currency" => $currency,
			"reference" => $reference,
			"callback_url" => $callback_url,
			"metadata" => array("cart_id"=>$cart_id)
		);

		$curl = curl_init();
			curl_setopt_array($curl, array(
			CURLOPT_URL => "https://api.paystack.co/transaction/initialize",
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_ENCODING => "",
			CURLOPT_MAXREDIRS => 10,
			CURLOPT_TIMEOUT => 30,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_CUSTOMREQUEST => "POST",
			CURLOPT_POSTFIELDS => json_encode($payload),
			CURLOPT_HTTPHEADER => array(
			  "Authorization: Bearer {$this->secret_key}",
			  "Content-Type: application/json",
			  "Cache-Control: no-cache",
			),
		));

		$result = curl_exec($curl);
		$err = curl_error($curl);
		curl_close($curl);

		if($err)
		{
			return array('status'=>'Error', 'message'=>"cURL Error #:".$err);
		}

		$result = json_decode($result,true);

		if(empty($result['status']))
		{
			return array('status'=>'Error', 'message'=>isset($result['message']) ? $result['message'] : "Transaction initialize error");
		}

		return array(
			'status' => 'Success',
			'authorization_url' => $result['data']['authorization_url'],
			'reference' => $result['data']['reference']
		);
	}

	// Verifies the X-Paystack-Signature header per Paystack's documented webhook contract.
	public function verify_webhook_signature($raw_payload, $signature_header, $secret_key)
	{
		if(empty($signature_header)) return false;
		$computed = hash_hmac('sha512', $raw_payload, $secret_key);
		return hash_equals($computed, $signature_header);
	}

	public function paystack_payment_action($reference)
	{

		  $curl = curl_init();
		  	curl_setopt_array($curl, array(
		  	CURLOPT_URL => "https://api.paystack.co/transaction/verify/{$reference}",
		  	CURLOPT_RETURNTRANSFER => true,
		  	CURLOPT_ENCODING => "",
		  	CURLOPT_MAXREDIRS => 10,
		  	CURLOPT_TIMEOUT => 30,
		  	CURLOPT_SSL_VERIFYPEER =>false,
		  	CURLOPT_CUSTOMREQUEST => "GET",
		  	CURLOPT_HTTPHEADER => array(
		  	  "Authorization: Bearer {$this->secret_key}",
		  	  "Cache-Control: no-cache",
		  	),
		  ));

		  $result = curl_exec($curl);
		  $err = curl_error($curl);
		  curl_close($curl);

		  if ($err) {

			$response['status'] ="Error";
			$response['message'] ="cURL Error #:".$err;
			return $response;

		  } else {

		  	$result=json_decode($result,true);

		  	if(!$result['status']){
			  	$response['status'] ="Error";
				$response['message'] ="Transaction Verification Error :".$result['message'];
				return $response;
		  	}

		  	$response['status']="Success";
			$response['charge_info']=$result;

			return $response;
		  }	
	}




}

?>