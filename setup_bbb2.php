<?php
/**
 * Configure BBB with Blindside test server + add room to RUS-1 course
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->libdir . '/filelib.php');

// Server credentials (Blindside public test server)
$bbb_url    = "https://test-install.blindsidenetworks.com/bigbluebutton/";
$bbb_secret = "8cd8ef52e8e101574e400365b55e11a6";

// Set config
set_config('server_url',    $bbb_url,    'bigbluebuttonbn');
set_config('shared_secret', $bbb_secret, 'bigbluebuttonbn');
set_config('sendnotifications_enabled',             0, 'bigbluebuttonbn');
set_config('recordings_enabled',                    0, 'bigbluebuttonbn');
set_config('recordings_html_enabled',               0, 'bigbluebuttonbn');
set_config('recordings_deleted_activities_enabled', 0, 'bigbluebuttonbn');
set_config('general_settings_showreleasenotes',     0, 'bigbluebuttonbn');
echo "BBB server configured: $bbb_url" . PHP_EOL;

// Make module visible
$DB->set_field('modules', 'visible', 1, array('name' => 'bigbluebuttonbn'));
echo "Module enabled." . PHP_EOL;

// Add BBB room to RUS-1 (id=2) — section 0 (main section)
$course = $DB->get_record('course', array('shortname' => 'RUS-1'));
$module = $DB->get_record('modules', array('name' => 'bigbluebuttonbn'));

// Check if already exists
$existing = $DB->get_record('bigbluebuttonbn', array('course' => $course->id));
if ($existing) {
    echo "BBB room already exists in RUS-1 (id=" . $existing->id . ")" . PHP_EOL;
} else {
    // Create the BBB activity record
    $bbb = new stdClass();
    $bbb->course        = $course->id;
    $bbb->name          = "Урок онлайн";
    $bbb->intro         = "<p>Видеоурок с учителем</p>";
    $bbb->introformat   = FORMAT_HTML;
    $bbb->type          = 0;  // 0=room only, 1=recordings only, 2=room+recordings
    $bbb->meetingid     = '';
    $bbb->record        = 0;
    $bbb->welcome       = "Добро пожаловать на урок!";
    $bbb->participants  = json_encode(array(
        array('selectiontype' => 'all', 'selectionid' => 'all', 'role' => 'viewer'),
    ));
    $bbb->timecreated   = time();
    $bbb->timemodified  = time();
    $bbb->presentation  = '';
    $bbb->closingtime   = 0;
    $bbb->openingtime   = 0;
    $bbb->wait          = 1;  // Students wait for teacher
    $bbb->userlimit     = 0;
    $bbb->muteonstart   = 0;
    $bbb->disablecam    = 0;
    $bbb->disablemic    = 0;
    $bbb->disableprivatechat  = 0;
    $bbb->disablepublicchat   = 0;
    $bbb->disablenote   = 0;
    $bbb->hideuserlist  = 0;

    $bbb->id = $DB->insert_record('bigbluebuttonbn', $bbb);
    echo "Created BBB room id=" . $bbb->id . PHP_EOL;

    // Add to course_modules
    $cm = new stdClass();
    $cm->course     = $course->id;
    $cm->module     = $module->id;
    $cm->instance   = $bbb->id;
    $cm->section    = 0;  // general section
    $cm->visible    = 1;
    $cm->added      = time();
    $cm->id = $DB->insert_record('course_modules', $cm);
    echo "Created course_module id=" . $cm->id . PHP_EOL;

    // Create context
    context_module::instance($cm->id);

    // Add to section sequence
    $section = $DB->get_record('course_sections', array('course' => $course->id, 'section' => 0));
    if ($section) {
        $seq = trim($section->sequence);
        $newseq = $seq ? $seq . ',' . $cm->id : (string)$cm->id;
        $DB->set_field('course_sections', 'sequence', $newseq, array('id' => $section->id));
        echo "Added to section 0 sequence." . PHP_EOL;
    }

    // Rebuild course cache
    rebuild_course_cache($course->id, true);
    echo "Course cache rebuilt." . PHP_EOL;
}

purge_all_caches();
echo PHP_EOL . "Done! BBB room 'Урок онлайн' added to RUS-1." . PHP_EOL;
echo "URL: http://130.12.47.10/course/view.php?id=" . $course->id . PHP_EOL;
