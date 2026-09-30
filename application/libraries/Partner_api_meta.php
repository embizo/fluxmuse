<?php  if ( ! defined('BASEPATH')) exit('No Direct Script Access Allowed');

/**
 * Plain cURL calls to Meta's Graph API and WhatsApp Cloud API, for the
 * partner_api module's own marketing identity (one Page, one WhatsApp
 * number, configured once in `partner_api_config`). Deliberately not built
 * on any of the legacy bot/autoposting code paths in this codebase -- those
 * carry per-user page-connection assumptions this does not need, and a
 * fresh, small, reviewable client is safer for something outward-facing.
 */
class Partner_api_meta
{
    const GRAPH_VERSION = 'v21.0'; // bump per Meta's deprecation calendar; verify at setup time.
    const GRAPH_BASE = 'https://graph.facebook.com/';

    private function call($method, $path, $params = array(), $access_token = null)
    {
        $url = self::GRAPH_BASE . self::GRAPH_VERSION . '/' . ltrim($path, '/');
        if ($access_token) $params['access_token'] = $access_token;

        $ch = curl_init();
        if (strtoupper($method) === 'GET') {
            curl_setopt($ch, CURLOPT_URL, $url . '?' . http_build_query($params));
        } else {
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
        }
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        $body = curl_exec($ch);
        $errno = curl_errno($ch);
        $curl_error = curl_error($ch);
        $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($errno) {
            return array('ok' => false, 'error' => 'Could not reach Meta: ' . $curl_error);
        }
        $json = json_decode($body, true);
        if ($status < 200 || $status >= 300) {
            $message = isset($json['error']['message']) ? $json['error']['message'] : ('Meta returned HTTP ' . $status);
            return array('ok' => false, 'error' => $message, 'status' => $status);
        }
        return array('ok' => true, 'data' => $json);
    }

    /** Text or link post to a Facebook Page's own feed. */
    public function post_to_facebook_page($page_id, $page_access_token, $message, $link = null)
    {
        $params = array('message' => $message);
        if ($link) $params['link'] = $link;
        $res = $this->call('POST', $page_id . '/feed', $params, $page_access_token);
        if (!$res['ok']) return $res;
        $id = $res['data']['id'];
        return array('ok' => true, 'platform_post_id' => $id, 'permalink' => 'https://www.facebook.com/' . $id);
    }

    /** Instagram publishing is two calls: create a media container, then publish it. */
    public function post_to_instagram($ig_business_account_id, $page_access_token, $caption, $image_url)
    {
        if (!$image_url) {
            return array('ok' => false, 'error' => 'Instagram requires an image or video URL; a text-only post is not supported by the Graph API.');
        }
        $create = $this->call('POST', $ig_business_account_id . '/media', array(
            'image_url' => $image_url,
            'caption' => $caption,
        ), $page_access_token);
        if (!$create['ok']) return $create;
        $creation_id = $create['data']['id'];

        $publish = $this->call('POST', $ig_business_account_id . '/media_publish', array(
            'creation_id' => $creation_id,
        ), $page_access_token);
        if (!$publish['ok']) return $publish;
        $id = $publish['data']['id'];
        return array('ok' => true, 'platform_post_id' => $id, 'permalink' => null);
    }

    /** Engagement for a Facebook post: likes, comments, shares, impressions,
     *  reach and post_clicks via Graph's insights edge. Instagram media uses a
     *  different insights metric set (impressions/reach/engagement, no
     *  post_impressions_unique naming), handled separately below. */
    public function get_facebook_metrics($platform_post_id, $page_access_token)
    {
        $res = $this->call('GET', $platform_post_id, array(
            'fields' => 'permalink_url,likes.summary(true),comments.summary(true),shares,' .
                'insights.metric(post_impressions,post_impressions_unique,post_clicks,post_engaged_users)',
        ), $page_access_token);
        if (!$res['ok']) return $res;
        $data = $res['data'];

        $metric = function ($name) use ($data) {
            if (empty($data['insights']['data'])) return null;
            foreach ($data['insights']['data'] as $d) {
                if ($d['name'] === $name) return isset($d['values'][0]['value']) ? $d['values'][0]['value'] : null;
            }
            return null;
        };
        $impressions = $metric('post_impressions');
        $engaged = $metric('post_engaged_users');

        return array('ok' => true, 'metrics' => array(
            'url' => isset($data['permalink_url']) ? $data['permalink_url'] : ('https://www.facebook.com/' . $platform_post_id),
            'impressions' => $impressions,
            'reach' => $metric('post_impressions_unique'),
            'likes' => isset($data['likes']['summary']['total_count']) ? $data['likes']['summary']['total_count'] : null,
            'comments' => isset($data['comments']['summary']['total_count']) ? $data['comments']['summary']['total_count'] : null,
            'shares' => isset($data['shares']['count']) ? $data['shares']['count'] : null,
            'clicks' => $metric('post_clicks'),
            'engagement_rate' => ($impressions && $engaged !== null) ? round($engaged / $impressions, 4) : null,
        ));
    }

    /** Engagement for one Instagram media object. */
    public function get_instagram_metrics($platform_post_id, $page_access_token)
    {
        $res = $this->call('GET', $platform_post_id, array(
            'fields' => 'permalink,like_count,comments_count,' .
                'insights.metric(impressions,reach,engagement)',
        ), $page_access_token);
        if (!$res['ok']) return $res;
        $data = $res['data'];

        $metric = function ($name) use ($data) {
            if (empty($data['insights']['data'])) return null;
            foreach ($data['insights']['data'] as $d) {
                if ($d['name'] === $name) return isset($d['values'][0]['value']) ? $d['values'][0]['value'] : null;
            }
            return null;
        };
        $impressions = $metric('impressions');
        $engagement = $metric('engagement');

        return array('ok' => true, 'metrics' => array(
            'url' => isset($data['permalink']) ? $data['permalink'] : null,
            'impressions' => $impressions,
            'reach' => $metric('reach'),
            'likes' => isset($data['like_count']) ? $data['like_count'] : null,
            'comments' => isset($data['comments_count']) ? $data['comments_count'] : null,
            'shares' => null,
            'clicks' => null,
            'engagement_rate' => ($impressions && $engagement !== null) ? round($engagement / $impressions, 4) : null,
        ));
    }

    /** A free-form WhatsApp text message. Meta only allows this within 24 hours
     *  of the recipient's last message to this number; outside that window it
     *  is rejected (code 131047) and an approved template is required instead,
     *  which this client does not send -- not needed for the marketing use this
     *  module exists for today (replies to inbound leads, not cold outreach). */
    public function send_whatsapp_text($phone_number_id, $access_token, $to, $body)
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, self::GRAPH_BASE . self::GRAPH_VERSION . '/' . $phone_number_id . '/messages');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Authorization: Bearer ' . $access_token,
            'Content-Type: application/json',
        ));
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(array(
            'messaging_product' => 'whatsapp',
            'recipient_type' => 'individual',
            'to' => $to,
            'type' => 'text',
            'text' => array('body' => $body, 'preview_url' => false),
        )));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        $response = curl_exec($ch);
        $errno = curl_errno($ch);
        $curl_error = curl_error($ch);
        $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($errno) {
            return array('ok' => false, 'error' => 'Could not reach WhatsApp: ' . $curl_error);
        }
        $json = json_decode($response, true);
        if ($status < 200 || $status >= 300) {
            $message = isset($json['error']['message']) ? $json['error']['message'] : ('WhatsApp returned HTTP ' . $status);
            return array('ok' => false, 'error' => $message, 'status' => $status);
        }
        $message_id = isset($json['messages'][0]['id']) ? $json['messages'][0]['id'] : null;
        return array('ok' => true, 'provider_message_id' => $message_id);
    }
}
