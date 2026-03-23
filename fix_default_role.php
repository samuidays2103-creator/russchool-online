<?php
/**
 * Fix: set defaultuserroleid = 7 (authenticated user / 'user' role)
 * This is why blocks aren't visible — students don't have basic system context capabilities
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// Check current state
$current = get_config('core', 'defaultuserroleid');
echo "Current defaultuserroleid: '" . $current . "'" . PHP_EOL;

$user_role = $DB->get_record('role', array('shortname' => 'user'));
echo "User role id: " . $user_role->id . PHP_EOL;

// Set the default user role
set_config('defaultuserroleid', $user_role->id);
echo "Set defaultuserroleid = " . $user_role->id . PHP_EOL;

// Also set defaultfrontpageroleid if not set
$frontpage = get_config('core', 'defaultfrontpageroleid');
echo "Current defaultfrontpageroleid: '" . $frontpage . "'" . PHP_EOL;
if (empty($frontpage)) {
    $fp_role = $DB->get_record('role', array('shortname' => 'frontpage'));
    if ($fp_role) {
        set_config('defaultfrontpageroleid', $fp_role->id);
        echo "Set defaultfrontpageroleid = " . $fp_role->id . PHP_EOL;
    }
}

// Purge caches
purge_all_caches();
echo PHP_EOL . "Caches purged." . PHP_EOL;

// Verify: check if student now has block:view capability
$student = $DB->get_record("user", array("username" => "ivanov_misha"));
$sysctx = context_system::instance();
$can_view = has_capability('moodle/block:view', $sysctx, $student);
echo "Student moodle/block:view in system context: " . ($can_view ? 'YES ✓' : 'NO ✗') . PHP_EOL;

// Also check my/courses.php capability
$can_courses = has_capability('moodle/course:view', $sysctx, $student);
echo "Student moodle/course:view in system context: " . ($can_courses ? 'YES' : 'NO') . PHP_EOL;
