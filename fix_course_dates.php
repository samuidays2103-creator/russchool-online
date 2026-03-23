<?php
/**
 * Fix course start dates - they were set to 2026-09-01 (future),
 * which makes myoverview block classify them as "future" and hide them
 * in the default "inprogress" view.
 * Set to 2025-09-01 (current academic year).
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// September 1, 2025 00:00:00 UTC
$new_start = mktime(0, 0, 0, 9, 1, 2025);
// June 30, 2026 23:59:59 UTC
$new_end = mktime(23, 59, 59, 6, 30, 2026);

echo "New startdate: " . date('Y-m-d', $new_start) . " ($new_start)" . PHP_EOL;
echo "New enddate:   " . date('Y-m-d', $new_end)   . " ($new_end)"   . PHP_EOL;
echo PHP_EOL;

// Get all real courses (not site course id=1)
$courses = $DB->get_records_select('course', 'id > 1', null, 'id ASC', 'id,fullname,shortname,startdate,enddate');

foreach ($courses as $c) {
    $DB->set_field('course', 'startdate', $new_start, array('id' => $c->id));
    $DB->set_field('course', 'enddate',   $new_end,   array('id' => $c->id));
    echo "Updated: id=" . $c->id . " " . $c->shortname . PHP_EOL;
}

echo PHP_EOL;
echo "Purging caches..." . PHP_EOL;
purge_all_caches();
echo "Done. Courses now start 2025-09-01, end 2026-06-30." . PHP_EOL;
echo "They are now 'inprogress' and will show in Мои курсы." . PHP_EOL;
