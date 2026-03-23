<?php
/**
 * Check if myoverview block renders courses for student
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");
require_once($CFG->dirroot . "/my/lib.php");
require_once($CFG->dirroot . "/blocks/moodleblock.class.php");

// Simulate student user
$student = $DB->get_record("user", array("username" => "ivanov_misha"));
$USER = $student;
$USER->sesskey = sesskey();

echo "=== Block positions check ===" . PHP_EOL;
// Check if there are block_positions records
$positions = $DB->get_records_sql(
    "SELECT * FROM mdl_block_positions WHERE blockinstanceid = 10"
);
echo "block_positions for myoverview (id=10): " . count($positions) . PHP_EOL;
foreach ($positions as $p) {
    echo "  contextid=" . $p->contextid . " pagetype=" . $p->pagetype . " subpage=" . $p->subpage . " visible=" . $p->visible . " region=" . $p->region . PHP_EOL;
}

echo PHP_EOL . "=== Check webservice for mycourses ===" . PHP_EOL;
// The myoverview block uses web service: core_course_get_enrolled_courses_by_timeline_classification
// Let's simulate that call
$courses = enrol_get_all_users_courses($student->id, true);
echo "Courses via enrol_get_all_users_courses: " . count($courses) . PHP_EOL;

// Try via the actual webservice function
require_once($CFG->dirroot . "/course/externallib.php");
try {
    $result = core_course_external::get_enrolled_courses_by_timeline_classification(
        'all', 0, 0, null, '', 0
    );
    echo "Webservice result: " . print_r($result, true) . PHP_EOL;
} catch (Exception $e) {
    echo "Webservice error: " . $e->getMessage() . PHP_EOL;
}

echo PHP_EOL . "=== Check mdl_user_lastaccess ===" . PHP_EOL;
$lastaccess = $DB->get_records("user_lastaccess", array("userid" => $student->id));
echo "lastaccess records: " . count($lastaccess) . PHP_EOL;
foreach ($lastaccess as $la) {
    echo "  courseid=" . $la->courseid . " timeaccess=" . $la->timeaccess . PHP_EOL;
}

echo PHP_EOL . "=== Timeline classification check ===" . PHP_EOL;
// The myoverview block classifies courses as 'inprogress', 'future', 'past'
$now = time();
foreach ($courses as $c) {
    $start = $c->startdate ?? 0;
    $end = $c->enddate ?? 0;
    if ($end && $end < $now) {
        $status = 'past';
    } elseif ($start && $start > $now) {
        $status = 'future';
    } else {
        $status = 'inprogress';
    }
    echo "  Course id=" . $c->id . " start=" . date('Y-m-d', $start) . " end=" . ($end ? date('Y-m-d', $end) : 'none') . " -> " . $status . PHP_EOL;
}
