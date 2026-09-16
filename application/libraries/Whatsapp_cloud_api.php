<?php
// Minimal WhatsApp Business Cloud API sender, scoped to pushing a checkout
// payment-link/order-confirmation message for a store that has connected a
// WhatsApp Business phone number. Not a general inbox/conversation engine —
// see docs/counter_checkout_and_cardless_payments.md for what's deliberately
// out of scope (that's Livechat.php's separate, pre-existing whatsapp_bots gap).
// https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages
class Whatsapp_cloud_api{

	function __construct()
	{
		$this->CI =& get_instance();
	}

	public function send_text_message($phone_number_id, $to, $text, $access_token)
	{
		$payload = array(
			"messaging_product" => "whatsapp",
			"to" => $to,
			"type" => "text",
			"text" => array("body" => $text)
		);

		$curl = curl_init();
		curl_setopt_array($curl, array(
			CURLOPT_URL => "https://graph.facebook.com/v19.0/{$phone_number_id}/messages",
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_TIMEOUT => 30,
			CURLOPT_CUSTOMREQUEST => "POST",
			CURLOPT_POSTFIELDS => json_encode($payload),
			CURLOPT_HTTPHEADER => array(
				"Authorization: Bearer {$access_token}",
				"Content-Type: application/json",
			),
		));

		$result = curl_exec($curl);
		$err = curl_error($curl);
		curl_close($curl);

		if($err) return array('status'=>'Error','message'=>"cURL Error #:".$err);

		$result = json_decode($result,true);

		if(isset($result['error']))
		{
			return array('status'=>'Error','message'=>isset($result['error']['message']) ? $result['error']['message'] : "WhatsApp send failed");
		}

		return array('status'=>'Success','message_id'=>isset($result['messages'][0]['id']) ? $result['messages'][0]['id'] : '');
	}

}
?>
