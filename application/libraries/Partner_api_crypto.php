<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * AES-256-CBC at rest for the two things this codebase had no precedent for
 * encrypting: the FB Page token and the WhatsApp access token in
 * `partner_api_config`. Keyed on the install's own config['encryption_key']
 * (the same secret Agency_provisioning.php HMACs license keys with), so no
 * new secret needs provisioning on top of what already exists.
 *
 * Format: base64(iv) . ':' . base64(ciphertext). A fresh random IV per call;
 * never reuse an IV with the same key.
 */
class Partner_api_crypto
{
    private $CI;

    public function __construct()
    {
        $this->CI =& get_instance();
    }

    private function key()
    {
        // AES-256 wants a 32-byte key; the configured secret is a hex string
        // longer than that, so this derives a fixed-length key from it rather
        // than truncating it (truncating a hex string throws away entropy
        // unevenly and would silently change if the secret's length changes).
        return hash('sha256', $this->CI->config->item('encryption_key'), true);
    }

    public function encrypt($plaintext)
    {
        if ($plaintext === null || $plaintext === '') return null;
        $iv = openssl_random_pseudo_bytes(16);
        $cipher = openssl_encrypt($plaintext, 'aes-256-cbc', $this->key(), OPENSSL_RAW_DATA, $iv);
        if ($cipher === false) return null;
        return base64_encode($iv) . ':' . base64_encode($cipher);
    }

    public function decrypt($payload)
    {
        if (empty($payload) || strpos($payload, ':') === false) return null;
        list($iv_b64, $cipher_b64) = explode(':', $payload, 2);
        $iv = base64_decode($iv_b64);
        $cipher = base64_decode($cipher_b64);
        if ($iv === false || $cipher === false || strlen($iv) !== 16) return null;
        $plain = openssl_decrypt($cipher, 'aes-256-cbc', $this->key(), OPENSSL_RAW_DATA, $iv);
        return $plain === false ? null : $plain;
    }
}
