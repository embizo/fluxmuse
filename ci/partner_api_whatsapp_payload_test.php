<?php
// Run: php ci/partner_api_whatsapp_payload_test.php
// Tests the pure payload builder -- no database, no Meta, no CodeIgniter.
define('BASEPATH', __DIR__);
require __DIR__ . '/../application/libraries/Partner_api_whatsapp_payload.php';

$p = new Partner_api_whatsapp_payload();
$fail = 0; $n = 0;
function check($label, $cond) { global $fail, $n; $n++; if (!$cond) { $fail++; echo "FAIL: $label\n"; } }

// --- the case this whole change exists for: a login code -----------------
$r = $p->build_template_message('27711493926', array('name' => 'sedilaka_login_code', 'language' => 'en', 'otp' => '482913'));
check('otp: ok', $r['ok'] === true);
$t = $r['payload']['template'];
check('otp: type template', $r['payload']['type'] === 'template');
check('otp: body carries the code', $t['components'][0]['type'] === 'body' && $t['components'][0]['parameters'][0]['text'] === '482913');
check('otp: copy-code button ALSO carries it (Meta rejects otherwise)', $t['components'][1]['type'] === 'button' && $t['components'][1]['sub_type'] === 'url' && $t['components'][1]['index'] === '0' && $t['components'][1]['parameters'][0]['text'] === '482913');
check('otp: language shaped for Meta', $t['language'] === array('code' => 'en'));
check('otp: recipient', $r['payload']['to'] === '27711493926');

// --- the log summary must never contain the code -------------------------
$sum = $p->log_summary($r['name'], $r['language']);
check('log summary has no code', strpos($sum, '482913') === false && strpos($sum, 'sedilaka_login_code') !== false);

// --- language defaults, and bad values are refused -----------------------
$r = $p->build_template_message('27711493926', array('name' => 'x', 'otp' => '123456'));
check('language defaults to en', $r['ok'] && $r['payload']['template']['language']['code'] === 'en');
check('en_ZA accepted', $p->build_template_message('1', array('name' => 'x', 'language' => 'en_ZA', 'otp' => '123456'))['ok']);
check('bad language refused', !$p->build_template_message('1', array('name' => 'x', 'language' => 'English', 'otp' => '123456'))['ok']);

// --- names: Meta's rule is lowercase/digits/underscore -------------------
foreach (array('Bad Name', 'UPPER', 'has-dash', '', 'a b', '../etc') as $bad) {
    check("name refused: '$bad'", !$p->build_template_message('1', array('name' => $bad, 'otp' => '123456'))['ok']);
}
check('name missing refused', !$p->build_template_message('1', array('otp' => '123456'))['ok']);
check('template not an object refused', !$p->build_template_message('1', 'sedilaka')['ok']);

// --- otp validation ------------------------------------------------------
foreach (array('123', '1234567890123456', '12 34', '12-34', '', '<script>') as $bad) {
    check("otp refused: '$bad'", !$p->build_template_message('1', array('name' => 'x', 'otp' => $bad))['ok']);
}
check('alphanumeric otp ok', $p->build_template_message('1', array('name' => 'x', 'otp' => 'A1B2C3'))['ok']);
check('otp and components together refused', !$p->build_template_message('1', array('name' => 'x', 'otp' => '123456', 'components' => array()))['ok']);

// --- free-form components (alerts to a circle) ---------------------------
$r = $p->build_template_message('27711493926', array('name' => 'sedilaka_alert', 'components' => array(
    array('type' => 'body', 'parameters' => array(array('type' => 'text', 'text' => 'Naledi'), array('type' => 'text', 'text' => '12 Juta Street'))),
)));
check('components: ok', $r['ok'] && count($r['payload']['template']['components'][0]['parameters']) === 2);
check('empty components list is a list', $p->build_template_message('1', array('name' => 'x', 'components' => array()))['ok']);
check('components must be a list', !$p->build_template_message('1', array('name' => 'x', 'components' => array('type' => 'body')))['ok']);
check('unknown component type refused', !$p->build_template_message('1', array('name' => 'x', 'components' => array(array('type' => 'carousel'))))['ok']);
check('button needs sub_type', !$p->build_template_message('1', array('name' => 'x', 'components' => array(array('type' => 'button'))))['ok']);
check('unknown parameter type refused', !$p->build_template_message('1', array('name' => 'x', 'components' => array(array('type' => 'body', 'parameters' => array(array('type' => 'image', 'image' => 'x'))))))['ok']);
check('oversized parameter refused', !$p->build_template_message('1', array('name' => 'x', 'components' => array(array('type' => 'body', 'parameters' => array(array('type' => 'text', 'text' => str_repeat('a', 2000)))))))['ok']);
$many = array_fill(0, 9, array('type' => 'body'));
check('too many components refused', !$p->build_template_message('1', array('name' => 'x', 'components' => $many))['ok']);
// unknown keys in a component are dropped, not forwarded
$r = $p->build_template_message('1', array('name' => 'x', 'components' => array(array('type' => 'body', 'evil' => 'x', 'parameters' => array(array('type' => 'text', 'text' => 'a', 'evil' => 'y'))))));
check('unknown keys are not forwarded', $r['ok'] && !isset($r['payload']['template']['components'][0]['evil']) && !isset($r['payload']['template']['components'][0]['parameters'][0]['evil']));

echo $fail === 0 ? "OK: all $n checks passed\n" : "$fail of $n FAILED\n";
exit($fail === 0 ? 0 : 1);
