<?php
/**
 * Configure Moove theme and front page
 */
define("CLI_SCRIPT", true);
require_once("/var/www/moodle/config.php");

// === SITE NAME ===
$DB->set_field('course', 'fullname',  'Онлайн-школа', array('id' => 1));
$DB->set_field('course', 'shortname', 'school',        array('id' => 1));

// === FRONT PAGE: show course list + login box ===
// frontpage = what guests see, frontpageloggedin = what logged-in users see
// Values: 0=news, 1=list of courses, 2=list of enrolled courses, 3=combo, 4=category combo, 5=categories
set_config('frontpage',          '1');   // guests: list of courses
set_config('frontpageloggedin',  '2');   // logged in: enrolled courses
set_config('frontpagesummary',   '<h2>Добро пожаловать в онлайн-школу</h2><p>Русский язык и математика для детей русскоязычной диаспоры. 1–4 классы, программа «Школа России».</p>');

// === MOOVE THEME SETTINGS ===
// Brand color (orange like Умскул)
set_config('brandcolor',       '#E87722', 'theme_moove');
set_config('navbarcolor',      'dark',    'theme_moove');

// Site name in header
set_config('fullname', 'Онлайн-школа');

// Disable guest login button (cleaner UI)
set_config('guestloginbutton', 0);

// === SITE POLICY ===
// Redirect logged-in users from front page to /my/
set_config('defaulthomepage', '0'); // 0=site, 1=my, 2=mycourses

echo "Front page configured." . PHP_EOL;

purge_all_caches();
rebuild_course_cache(1, true);
echo "Done. Caches cleared." . PHP_EOL;
