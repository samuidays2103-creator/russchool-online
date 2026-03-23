<?php
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// Check theme is recognized
$themes = core_component::get_plugin_list('theme');
if (isset($themes['moove'])) {
    echo "Moove theme found at: " . $themes['moove'] . PHP_EOL;
} else {
    echo "Moove NOT found in plugin list!" . PHP_EOL;
    echo "Available themes: " . implode(', ', array_keys($themes)) . PHP_EOL;
    exit(1);
}

// Set as default theme
set_config('theme', 'moove');
echo "Default theme set to: moove" . PHP_EOL;

// Also set for mobile if needed
// set_config('themelegacy', 'moove');

purge_all_caches();
echo "Caches purged. Done!" . PHP_EOL;
echo "Open http://130.12.47.10/ to see the new theme." . PHP_EOL;
