<?php
/**
 * Setup BigBlueButton with demo.bigbluebutton.org
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// Check if BBB module exists in DB
$module = $DB->get_record('modules', array('name' => 'bigbluebuttonbn'));
if ($module) {
    echo "BBB module in DB: id=" . $module->id . " visible=" . $module->visible . PHP_EOL;
} else {
    echo "BBB module NOT in DB — need to install" . PHP_EOL;
}

// Check existing BBB config
$bbb_configs = $DB->get_records('config_plugins', array('plugin' => 'bigbluebuttonbn'));
echo "BBB config entries: " . count($bbb_configs) . PHP_EOL;
foreach ($bbb_configs as $c) {
    if (in_array($c->name, array('server_url', 'shared_secret', 'server_url_new', 'shared_secret_new'))) {
        echo "  " . $c->name . " = " . $c->value . PHP_EOL;
    }
}

// Demo server credentials (public BBB demo)
$demo_url = "https://demo.bigbluebutton.org/bigbluebutton/";
$demo_secret = "8cd8ef52e8e101574e400365b55e11a6";

// Set BBB configuration
echo PHP_EOL . "Setting BBB config..." . PHP_EOL;
set_config('server_url', $demo_url, 'bigbluebuttonbn');
set_config('shared_secret', $demo_secret, 'bigbluebuttonbn');
set_config('sendnotifications_enabled', 0, 'bigbluebuttonbn');
set_config('recordings_enabled', 0, 'bigbluebuttonbn');
set_config('recordings_html_enabled', 0, 'bigbluebuttonbn');
set_config('recordings_deleted_activities_enabled', 0, 'bigbluebuttonbn');
echo "Done." . PHP_EOL;

// If module not in DB — trigger install
if (!$module) {
    echo PHP_EOL . "Installing BBB plugin..." . PHP_EOL;
    // Use plugin_manager to install
    $pluginman = core_plugin_manager::instance();

    // Try running upgrade
    $result = update_internal_database();
    echo "Upgrade result: " . ($result ? 'OK' : 'failed') . PHP_EOL;
} else {
    // Make sure it's visible
    if (!$module->visible) {
        $DB->set_field('modules', 'visible', 1, array('name' => 'bigbluebuttonbn'));
        echo "Made BBB module visible." . PHP_EOL;
    }
}

// Test connection to demo server
echo PHP_EOL . "Testing connection to demo server..." . PHP_EOL;
$test_url = $demo_url . "api/getMeetings?checksum=" . sha1("getMeetings" . $demo_secret);
$context = stream_context_create(array('http' => array('timeout' => 10)));
$response = @file_get_contents($test_url, false, $context);
if ($response) {
    echo "Response: " . substr($response, 0, 200) . PHP_EOL;
    if (strpos($response, 'SUCCESS') !== false || strpos($response, 'meetings') !== false) {
        echo "Connection OK!" . PHP_EOL;
    } else {
        echo "Unexpected response." . PHP_EOL;
    }
} else {
    echo "Could not connect to demo server." . PHP_EOL;
}

purge_all_caches();
echo PHP_EOL . "Caches purged." . PHP_EOL;
