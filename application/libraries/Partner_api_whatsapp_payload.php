<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Builds and validates WhatsApp Cloud API *template* message payloads for the
 * partner_api module. Pure functions on purpose -- no database, no cURL, no
 * CodeIgniter state -- so the logic that decides what is sent to Meta can be
 * unit-tested without Meta credentials (see ci/partner_api_whatsapp_payload_test.php).
 *
 * WHY TEMPLATES EXIST. Meta only allows a free-form message to a person who
 * messaged this number in the last 24 hours. Anything business-initiated --
 * a login code, an alert to someone who has never written to you -- must be
 * a pre-registered, Meta-approved template. The template's wording lives in
 * Meta (WhatsApp Manager); what is sent per message is only its name, its
 * language and the values for its blanks.
 */
class Partner_api_whatsapp_payload
{
    /** Meta's limit on an authentication code: alphanumeric, at most 15. */
    const OTP_PATTERN = '/^[A-Za-z0-9]{4,15}$/';
    const NAME_PATTERN = '/^[a-z0-9_]{1,512}$/';
    const LANG_PATTERN = '/^[a-z]{2,3}(_[A-Z]{2})?$/';
    const MAX_COMPONENTS = 8;
    const MAX_PARAMETERS = 20;
    const MAX_TEXT_LENGTH = 1024;

    /**
     * The components of an Authentication-category template, from just the code.
     *
     * An authentication template is a body with the code plus a "copy code"
     * button that repeats it, and Meta rejects the send unless BOTH carry the
     * code. That is easy to get wrong from the caller's side, so the common
     * case is one field.
     */
    public function otp_components($otp)
    {
        return array(
            array(
                'type' => 'body',
                'parameters' => array(array('type' => 'text', 'text' => $otp)),
            ),
            array(
                'type' => 'button',
                'sub_type' => 'url',
                'index' => '0',
                'parameters' => array(array('type' => 'text', 'text' => $otp)),
            ),
        );
    }

    /**
     * Validate the `template` object from a request body and return the Cloud
     * API payload, or an error string. Returns array('ok'=>true,'payload'=>...,
     * 'name'=>..., 'language'=>...) or array('ok'=>false,'error'=>...).
     */
    public function build_template_message($to, $template)
    {
        if (!is_array($template)) {
            return $this->fail('"template" must be an object with a "name".');
        }
        $name = isset($template['name']) && is_string($template['name']) ? trim($template['name']) : '';
        if (!preg_match(self::NAME_PATTERN, $name)) {
            return $this->fail('"template.name" must be the approved template\'s name: lowercase letters, digits and underscores only.');
        }

        $language = isset($template['language']) && is_string($template['language']) ? trim($template['language']) : 'en';
        if (!preg_match(self::LANG_PATTERN, $language)) {
            return $this->fail('"template.language" must be a Meta language code such as "en", "en_ZA" or "st".');
        }

        $has_otp = isset($template['otp']);
        $has_components = isset($template['components']);
        if ($has_otp && $has_components) {
            return $this->fail('Send either "template.otp" or "template.components", not both.');
        }

        $components = array();
        if ($has_otp) {
            $otp = is_scalar($template['otp']) ? (string) $template['otp'] : '';
            if (!preg_match(self::OTP_PATTERN, $otp)) {
                return $this->fail('"template.otp" must be 4-15 letters or digits.');
            }
            $components = $this->otp_components($otp);
        } elseif ($has_components) {
            $checked = $this->validate_components($template['components']);
            if (!$checked['ok']) return $checked;
            $components = $checked['components'];
        }

        $body = array(
            'name' => $name,
            'language' => array('code' => $language),
        );
        if (!empty($components)) $body['components'] = $components;

        return array(
            'ok' => true,
            'name' => $name,
            'language' => $language,
            'payload' => array(
                'messaging_product' => 'whatsapp',
                'recipient_type' => 'individual',
                'to' => $to,
                'type' => 'template',
                'template' => $body,
            ),
        );
    }

    /**
     * What is safe to store about a template send. NEVER the parameters: for an
     * authentication template they are a live login code, and this install's
     * message log would otherwise hold valid codes in plaintext.
     */
    public function log_summary($name, $language)
    {
        return '[template ' . $name . ' / ' . $language . ']';
    }

    /**
     * Free-form components are allowed for non-authentication templates (order
     * confirmations, alerts). Only the shapes Meta accepts at SEND time, with
     * bounded sizes -- this is an outward-facing endpoint.
     */
    private function validate_components($components)
    {
        if (!is_array($components) || $this->is_assoc($components)) {
            return $this->fail('"template.components" must be a list.');
        }
        if (count($components) > self::MAX_COMPONENTS) {
            return $this->fail('Too many components.');
        }
        $allowed = array('header', 'body', 'button');
        $clean = array();
        foreach ($components as $c) {
            if (!is_array($c) || !isset($c['type']) || !in_array($c['type'], $allowed, true)) {
                return $this->fail('Each component needs a "type" of header, body or button.');
            }
            $out = array('type' => $c['type']);
            if ($c['type'] === 'button') {
                $sub = isset($c['sub_type']) ? $c['sub_type'] : '';
                if (!in_array($sub, array('url', 'quick_reply', 'copy_code'), true)) {
                    return $this->fail('A button component needs a "sub_type" of url, quick_reply or copy_code.');
                }
                $out['sub_type'] = $sub;
                $out['index'] = isset($c['index']) ? (string) (int) $c['index'] : '0';
            }
            if (isset($c['parameters'])) {
                if (!is_array($c['parameters']) || $this->is_assoc($c['parameters']) || count($c['parameters']) > self::MAX_PARAMETERS) {
                    return $this->fail('"parameters" must be a short list.');
                }
                $params = array();
                foreach ($c['parameters'] as $p) {
                    $type = is_array($p) && isset($p['type']) ? $p['type'] : '';
                    if ($type === 'text' || $type === 'payload' || $type === 'coupon_code') {
                        $value = isset($p[$type]) ? $p[$type] : (isset($p['text']) ? $p['text'] : null);
                        if (!is_scalar($value) || strlen((string) $value) > self::MAX_TEXT_LENGTH) {
                            return $this->fail('A parameter value is missing or too long.');
                        }
                        $params[] = array('type' => $type, $type => (string) $value);
                    } else {
                        return $this->fail('Parameter types supported here: text, payload, coupon_code.');
                    }
                }
                $out['parameters'] = $params;
            }
            $clean[] = $out;
        }
        return array('ok' => true, 'components' => $clean);
    }

    private function is_assoc($arr)
    {
        if ($arr === array()) return false; // range(0, -1) is [0, -1], not [] -- an empty list is a list
        return array_keys($arr) !== range(0, count($arr) - 1);
    }

    private function fail($message)
    {
        return array('ok' => false, 'error' => $message);
    }
}
