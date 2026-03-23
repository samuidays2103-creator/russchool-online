<?php
defined('MOODLE_INTERNAL') || die();

class block_nextlesson extends block_base {

    public function init() {
        $this->title = get_string('pluginname', 'block_nextlesson');
    }

    public function applicable_formats() {
        return [
            'my'            => true,
            'site'          => false,
            'course'        => false,
            'mod'           => false,
        ];
    }

    public function has_config() {
        return false;
    }

    public function get_content() {
        global $USER, $DB, $OUTPUT, $CFG;

        if ($this->content !== null) {
            return $this->content;
        }

        $this->content = new stdClass();
        $this->content->footer = '';

        $now       = time();
        $weekahead = $now + (7 * 24 * 3600);

        // Query next upcoming event from user's enrolled courses or direct user events
        $sql = "SELECT e.id, e.name, e.timestart, e.courseid,
                       c.fullname AS coursename,
                       e.description, e.modulename, e.instance
                  FROM {event} e
             LEFT JOIN {course} c ON c.id = e.courseid
                 WHERE (
                         e.userid = :userid1
                         OR e.courseid IN (
                             SELECT en.courseid
                               FROM {user_enrolments} ue
                               JOIN {enrol} en ON en.id = ue.enrolid
                              WHERE ue.userid = :userid2
                                AND ue.status = 0
                         )
                       )
                   AND e.timestart > :now
                   AND e.timestart < :weekahead
                   AND (e.eventtype = 'course' OR e.eventtype = 'user' OR e.eventtype = 'group')
              ORDER BY e.timestart ASC
                 LIMIT 1";

        $params = [
            'userid1'   => $USER->id,
            'userid2'   => $USER->id,
            'now'       => $now,
            'weekahead' => $weekahead,
        ];

        $event = $DB->get_record_sql($sql, $params);

        // Determine if user is a teacher/manager (system or course level)
        $isteacher = false;
        if ($event && $event->courseid) {
            $context = context_course::instance($event->courseid);
            $isteacher = has_capability('moodle/course:manageactivities', $context, $USER->id);
        }
        if (!$isteacher) {
            $isteacher = has_capability('moodle/site:config', context_system::instance(), $USER->id);
        }

        if (!$event) {
            // No upcoming events
            $this->content->text = html_writer::div(
                html_writer::div(
                    get_string('nolessons', 'block_nextlesson'),
                    'nextlesson-empty'
                ),
                'nextlesson-card nextlesson-empty-card'
            );
            return $this->content;
        }

        // Format time
        $timestart  = $event->timestart;
        $todaystart = mktime(0, 0, 0, date('n', $now), date('j', $now), date('Y', $now));
        $todayend   = $todaystart + 86400;
        $tomorrowend = $todayend + 86400;

        if ($timestart >= $todaystart && $timestart < $todayend) {
            $daystr = get_string('today', 'block_nextlesson');
        } elseif ($timestart >= $todayend && $timestart < $tomorrowend) {
            $daystr = get_string('tomorrow', 'block_nextlesson');
        } else {
            $daystr = userdate($timestart, get_string('strftimedayshort', 'langconfig'));
        }

        $timestr   = userdate($timestart, get_string('strftimetime', 'langconfig'));
        $diffmins  = (int)(($timestart - $now) / 60);
        $diffhours = (int)($diffmins / 60);
        $difftext  = '';

        if ($diffmins < 60) {
            $difftext = ' (' . get_string('inminutes', 'block_nextlesson', $diffmins) . ')';
        } elseif ($diffhours < 24) {
            $difftext = ' (' . get_string('inhours', 'block_nextlesson', $diffhours) . ')';
        }

        $coursename = !empty($event->coursename) ? $event->coursename : $event->name;
        $eventname  = $event->name;

        // Try to find BBB activity in the course
        $bbburl = null;
        if ($event->courseid && $DB->get_manager()->table_exists('bigbluebuttonbn')) {
            $bbbrecord = $DB->get_record_sql(
                "SELECT b.id FROM {bigbluebuttonbn} b
                  WHERE b.course = :courseid
               ORDER BY b.id ASC LIMIT 1",
                ['courseid' => $event->courseid]
            );
            if ($bbbrecord) {
                $bbbcm = $DB->get_record_sql(
                    "SELECT cm.id FROM {course_modules} cm
                       JOIN {modules} m ON m.id = cm.module
                      WHERE m.name = 'bigbluebuttonbn'
                        AND cm.instance = :instance
                        AND cm.course = :course",
                    ['instance' => $bbbrecord->id, 'course' => $event->courseid]
                );
                if ($bbbcm) {
                    $bbburl = new moodle_url('/mod/bigbluebuttonbn/view.php', ['id' => $bbbcm->id]);
                }
            }
        }

        // Count enrolled students if teacher
        $enrolled_count = 0;
        $total_count    = 0;
        if ($isteacher && $event->courseid) {
            $context = context_course::instance($event->courseid);
            $enrolled = get_enrolled_users($context, 'mod/bigbluebuttonbn:join');
            $total_enrolled = get_enrolled_users($context);
            $enrolled_count = count($enrolled);
            $total_count    = count($total_enrolled);
        }

        // Build HTML
        $html = '';

        // Course / lesson name
        $html .= html_writer::div(
            html_writer::tag('strong', $coursename),
            'nextlesson-course'
        );

        if ($coursename !== $eventname) {
            $html .= html_writer::div(
                $eventname,
                'nextlesson-eventname'
            );
        }

        // Time line
        $html .= html_writer::div(
            $daystr . ' ' . get_string('at', 'block_nextlesson') . ' ' . $timestr . $difftext,
            'nextlesson-time'
        );

        // Teacher-only: enrolled count
        if ($isteacher && $total_count > 0) {
            $html .= html_writer::div(
                get_string('enrolled_of', 'block_nextlesson', ['enrolled' => $enrolled_count, 'total' => $total_count]),
                'nextlesson-enrolled'
            );
        }

        // Button
        if ($bbburl) {
            $btnlabel = $isteacher
                ? get_string('startlesson', 'block_nextlesson')
                : get_string('joinlesson', 'block_nextlesson');
            $html .= html_writer::div(
                html_writer::link($bbburl, $btnlabel, ['class' => 'nextlesson-btn']),
                'nextlesson-btn-wrap'
            );
        } elseif ($event->courseid) {
            $courseurl = new moodle_url('/course/view.php', ['id' => $event->courseid]);
            $html .= html_writer::div(
                html_writer::link($courseurl, get_string('gotocourse', 'block_nextlesson'), ['class' => 'nextlesson-btn nextlesson-btn-secondary']),
                'nextlesson-btn-wrap'
            );
        }

        $this->content->text = html_writer::div($html, 'nextlesson-card');
        return $this->content;
    }
}
