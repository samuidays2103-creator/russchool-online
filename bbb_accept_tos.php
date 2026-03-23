<?php
/**
 * Accept BBB release notes / dismiss warnings so the plugin works cleanly
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// Dismiss the "new release notes" popup
set_config('general_settings_showreleasenotes', 0, 'bigbluebuttonbn');

// Set meetingid for the room (random unique ID)
$bbb = $DB->get_record('bigbluebuttonbn', array('id' => 1));
if ($bbb && empty($bbb->meetingid)) {
    $meetingid = 'moodle-bbb-' . $bbb->course . '-' . $bbb->id . '-' . substr(md5(uniqid()), 0, 8);
    $DB->set_field('bigbluebuttonbn', 'meetingid', $meetingid, array('id' => $bbb->id));
    echo "Set meetingid: $meetingid" . PHP_EOL;
}

// Check config is saved
$url = get_config('bigbluebuttonbn', 'server_url');
$secret = get_config('bigbluebuttonbn', 'shared_secret');
echo "server_url: $url" . PHP_EOL;
echo "shared_secret: " . substr($secret, 0, 8) . "..." . PHP_EOL;

// Verify the connection using BBB API
require_once($CFG->dirroot . '/mod/bigbluebuttonbn/locallib.php');

// Simple manual check
$checksum = sha1('getMeetings' . $secret);
$api_url = rtrim($url, '/') . "/api/getMeetings?checksum=$checksum";
$resp = file_get_contents($api_url, false, stream_context_create(array('http' => array('timeout' => 10))));
if ($resp && strpos($resp, 'SUCCESS') !== false) {
    echo "API connection: OK" . PHP_EOL;
} else {
    echo "API connection: FAILED" . PHP_EOL;
    echo substr($resp, 0, 200) . PHP_EOL;
}

purge_all_caches();
echo PHP_EOL . "Ready! Open http://130.12.47.10/course/view.php?id=2 and click 'Урок онлайн'" . PHP_EOL;
