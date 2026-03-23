<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');

function ensure_category($name, $parent_id = 0) {
    global $DB;
    $existing = $DB->get_record('course_categories', ['name' => $name, 'parent' => $parent_id]);
    if ($existing) return $existing->id;
    $cat = new stdClass();
    $cat->name = $name;
    $cat->parent = $parent_id;
    $cat->description = '';
    $cat->sortorder = 999;
    $cat->visible = 1;
    $cat->timemodified = time();
    $id = $DB->insert_record('course_categories', $cat);
    $DB->set_field('course_categories', 'path', "/$id", ['id' => $id]);
    $DB->set_field('course_categories', 'depth', 1, ['id' => $id]);
    return $id;
}

function create_course($fullname, $shortname, $category_id, $summary) {
    global $DB;
    if ($DB->record_exists('course', ['shortname' => $shortname])) {
        $c = $DB->get_record('course', ['shortname' => $shortname]);
        echo "  Exists: $shortname (id={$c->id})\n";
        return $c->id;
    }
    $c = new stdClass();
    $c->fullname = $fullname;
    $c->shortname = $shortname;
    $c->category = $category_id;
    $c->summary = $summary;
    $c->summaryformat = 1;
    $c->format = 'topics';
    $c->visible = 1;
    $c->timecreated = time();
    $c->timemodified = time();
    $c->lang = 'ru';
    $c->startdate = mktime(0,0,0,9,1,2026);
    $c->enddate = mktime(0,0,0,5,31,2027);
    $c->enablecompletion = 1;
    $id = $DB->insert_record('course', $c);
    $ctx = new stdClass();
    $ctx->contextlevel = 50;
    $ctx->instanceid = $id;
    $ctx->depth = 3;
    $ctx->path = '';
    $ctx->locked = 0;
    $ctx_id = $DB->insert_record('context', $ctx);
    $DB->set_field('context', 'path', "/1/3/$ctx_id", ['id' => $ctx_id]);
    echo "  Created: $fullname (id=$id)\n";
    return $id;
}

function set_numsections($course_id, $num) {
    global $DB;
    $existing = $DB->get_record('course_format_options', [
        'courseid' => $course_id, 'format' => 'topics', 'name' => 'numsections'
    ]);
    if ($existing) {
        $DB->set_field('course_format_options', 'value', $num, ['id' => $existing->id]);
    } else {
        $opt = new stdClass();
        $opt->courseid = $course_id;
        $opt->format = 'topics';
        $opt->sectionid = 0;
        $opt->name = 'numsections';
        $opt->value = $num;
        $DB->insert_record('course_format_options', $opt);
    }
}

function add_section($course_id, $num, $name, $summary = '') {
    global $DB;
    $existing = $DB->get_record('course_sections', ['course' => $course_id, 'section' => $num]);
    if ($existing) {
        $DB->set_field('course_sections', 'name', $name, ['id' => $existing->id]);
        return $existing->id;
    }
    $s = new stdClass();
    $s->course = $course_id;
    $s->section = $num;
    $s->name = $name;
    $s->summary = $summary;
    $s->summaryformat = 1;
    $s->sequence = '';
    $s->visible = 1;
    $s->timemodified = time();
    return $DB->insert_record('course_sections', $s);
}

function add_assign($course_id, $section_id, $name, $intro) {
    global $DB;
    if ($DB->record_exists('assign', ['course' => $course_id, 'name' => $name])) return;
    $a = new stdClass();
    $a->course = $course_id;
    $a->name = $name;
    $a->intro = $intro;
    $a->introformat = 1;
    $a->alwaysshowdescription = 1;
    $a->submissiondrafts = 0;
    $a->requiresubmissionstatement = 0;
    $a->sendnotifications = 0;
    $a->sendlatenotifications = 0;
    $a->duedate = time() + 7*86400;
    $a->allowsubmissionsfromdate = time();
    $a->grade = 100;
    $a->timemodified = time();
    $a->completionsubmit = 0;
    $a->teamsubmission = 0;
    $a->requireallteammemberssubmit = 0;
    $a->blindmarking = 0;
    $a->maxattempts = -1;
    $assign_id = $DB->insert_record('assign', $a);

    $sub = new stdClass();
    $sub->assignment = $assign_id;
    $sub->plugin = 'onlinetext';
    $sub->subtype = 'assignsubmission';
    $sub->value = '1';
    $DB->insert_record('assign_plugin_config', $sub);

    $mod_id = $DB->get_field('modules', 'id', ['name' => 'assign']);
    $cm = new stdClass();
    $cm->course = $course_id;
    $cm->module = $mod_id;
    $cm->instance = $assign_id;
    $cm->section = $section_id;
    $cm->visible = 1;
    $cm->visibleold = 1;
    $cm->groupmode = 0;
    $cm->added = time();
    $cm->completion = 2;
    $cm_id = $DB->insert_record('course_modules', $cm);

    $seq = $DB->get_field('course_sections', 'sequence', ['id' => $section_id]);
    $seq = $seq ? $seq . ',' . $cm_id : (string)$cm_id;
    $DB->set_field('course_sections', 'sequence', $seq, ['id' => $section_id]);

    $ctx = new stdClass();
    $ctx->contextlevel = 70;
    $ctx->instanceid = $cm_id;
    $ctx->depth = 4;
    $ctx->path = '';
    $ctx->locked = 0;
    $ctx_id = $DB->insert_record('context', $ctx);
    $DB->set_field('context', 'path', "/1/3/5/$ctx_id", ['id' => $ctx_id]);
}

// ── Категории ─────────────────────────────────────────────────
$root_id = ensure_category('Начальная школа');
$g1_id   = ensure_category('1 класс', $root_id);
echo "Categories: OK\n";

// ══════════════════════════════════════════════════════════════
// РУССКИЙ ЯЗЫК (Канакина, Горецкий)
// ══════════════════════════════════════════════════════════════
echo "\n=== Русский язык ===\n";
$rid = create_course('Русский язык. 1 класс', 'RUS-1', $g1_id, 'Учебник Канакиной В.П., Горецкого В.Г. Школа России.');
$sections = [
    1  => ['Азбука. Подготовительный период', 'Знакомство со звуками и буквами. Гласные и согласные.'],
    2  => ['Азбука. Букварный период. Часть 1', 'Буквы А О И Ы У Э. Слоги и слова.'],
    3  => ['Азбука. Букварный период. Часть 2', 'Буквы Н С К Т Л Р и другие. Чтение слов.'],
    4  => ['Азбука. Послебукварный период', 'Закрепление. Чтение текстов.'],
    5  => ['Наша речь', 'Язык и речь. Устная и письменная речь.'],
    6  => ['Текст, предложение, диалог', 'Текст и предложение. Знаки препинания.'],
    7  => ['Слова, слова, слова', 'Слово и его значение. Однозначные и многозначные слова.'],
    8  => ['Слово и слог. Ударение', 'Деление слов на слоги. Ударный слог.'],
    9  => ['Звуки и буквы', 'Гласные и согласные звуки. Алфавит.'],
    10 => ['Правописание ЖИ-ШИ, ЧА-ЩА, ЧУ-ЩУ', 'Буквосочетания. Заглавная буква в именах.'],
    11 => ['Повторение за год', 'Итоговое повторение. Контрольный диктант.'],
];
$assigns = [
    2  => ['Гласные буквы А О И Ы У', 'Напишите по 3 строчки каждой буквы. Придумайте по одному слову на каждую.'],
    5  => ['Устная и письменная речь', 'Напишите 2-3 предложения о своей семье.'],
    6  => ['Составляем предложения', 'Составьте 3 предложения по картинке. Поставьте знаки препинания.'],
    9  => ['Гласные и согласные в словах', 'Выпишите 10 слов из текста. Подчеркните гласные красным, согласные синим.'],
    10 => ['Диктант по правилам ЖИ-ШИ', 'Вставьте буквы: ж_вот, ш_шка, ч_йник, щ_вель, ч_до. Объясните правило письменно.'],
    11 => ['Итоговое сочинение', 'Напишите рассказ (5-7 предложений) на тему: Моя школа.'],
];
foreach ($sections as $num => $d) {
    $sec_id = add_section($rid, $num, $d[0], $d[1]);
    if (isset($assigns[$num])) add_assign($rid, $sec_id, $assigns[$num][0], $assigns[$num][1]);
}
set_numsections($rid, 11);
echo "  OK: 11 разделов\n";

// ══════════════════════════════════════════════════════════════
// МАТЕМАТИКА (Моро)
// ══════════════════════════════════════════════════════════════
echo "\n=== Математика ===\n";
$mid = create_course('Математика. 1 класс', 'MAT-1', $g1_id, 'Учебник Моро М.И. Школа России.');
$sections = [
    1 => ['Подготовка к изучению чисел', 'Сравнение предметов. Пространственные отношения.'],
    2 => ['Числа 1-5. Сложение и вычитание', 'Цифры 1-5. Состав числа. Задачи.'],
    3 => ['Числа 6-10. Состав чисел', 'Цифры 6-10. Таблица сложения.'],
    4 => ['Задачи на сложение и вычитание', 'Компоненты действий. Простые задачи.'],
    5 => ['Число 0', 'Понятие нуля. Действия с нулём.'],
    6 => ['Числа 11-20', 'Двузначные числа. Запись и чтение.'],
    7 => ['Сложение и вычитание в пределах 20', 'Таблица сложения. Задачи в 2 действия.'],
    8 => ['Геометрические фигуры', 'Точка, отрезок, треугольник, квадрат, прямоугольник.'],
    9 => ['Повторение за год', 'Итоговое повторение. Контрольная работа.'],
];
$assigns = [
    2 => ['Числа 1-5. Примеры', 'Реши: 2+3= 4+1= 5-2= 3-1= 1+4= Нарисуй столько кружков, сколько показывает число.'],
    3 => ['Состав числа 8', 'Запиши все варианты: 8=1+? 8=2+? 8=3+? 8=4+?'],
    4 => ['Задача на вычитание', 'На ветке сидело 7 птиц. Улетели 3. Сколько осталось? Запиши решение и ответ.'],
    6 => ['Числа от 11 до 20', 'Запиши числа от 11 до 20 по порядку. Какое число стоит между 14 и 16?'],
    7 => ['Задача в 2 действия', 'В коробке 12 карандашей. Утром взяли 4, вечером ещё 3. Сколько осталось?'],
    8 => ['Рисуем фигуры', 'Нарисуй прямоугольник 4x2 клетки и квадрат 3x3. Посчитай периметр каждого.'],
    9 => ['Итоговая контрольная', 'Реши задачу: В магазине 15 яблок. Продали 7. Привезли ещё 6. Сколько яблок?'],
];
foreach ($sections as $num => $d) {
    $sec_id = add_section($mid, $num, $d[0], $d[1]);
    if (isset($assigns[$num])) add_assign($mid, $sec_id, $assigns[$num][0], $assigns[$num][1]);
}
set_numsections($mid, 9);
echo "  OK: 9 разделов\n";

// ══════════════════════════════════════════════════════════════
// ЛИТЕРАТУРНОЕ ЧТЕНИЕ (Климанова)
// ══════════════════════════════════════════════════════════════
echo "\n=== Литературное чтение ===\n";
$lid = create_course('Литературное чтение. 1 класс', 'LIT-1', $g1_id, 'Учебник Климановой Л.Ф. Школа России.');
$sections = [
    1 => ['Знакомство с учебником', 'Структура книги. Условные обозначения.'],
    2 => ['Жили-были буквы', 'В.Данько, И.Токмакова, С.Чёрный, Ф.Кривин, Г.Сапгир.'],
    3 => ['Сказки, загадки, небылицы', 'Русские народные сказки. Загадки. Небылицы.'],
    4 => ['Апрель, апрель! Звенит капель', 'А.Майков, А.Плещеев, С.Маршак, И.Токмакова. Природа.'],
    5 => ['И в шутку и всерьёз', 'И.Токмакова, Г.Кружков, К.Чуковский, О.Дриз.'],
    6 => ['Я и мои друзья', 'Ю.Ермолаев, Е.Благинина, В.Орлов, С.Михалков. Дружба.'],
    7 => ['О братьях наших меньших', 'С.Михалков, Г.Снегирёв, В.Берестов. Животные.'],
];
$assigns = [
    2 => ['Стихотворение наизусть', 'Выучи любое стихотворение из раздела. Запиши его по памяти.'],
    3 => ['Пересказ сказки', 'Прочитай сказку Курочка Ряба. Перескажи письменно своими словами (4-6 предложений).'],
    4 => ['Стихи о весне', 'Выучи стихотворение Плещеева Весна. Нарисуй иллюстрацию и опиши её 2-3 предложениями.'],
    6 => ['Рассказ о друге', 'Напиши рассказ (4-5 предложений) о своём лучшем друге.'],
    7 => ['Мой питомец', 'Напиши рассказ о своём домашнем животном или любимом животном (5-6 предложений).'],
];
foreach ($sections as $num => $d) {
    $sec_id = add_section($lid, $num, $d[0], $d[1]);
    if (isset($assigns[$num])) add_assign($lid, $sec_id, $assigns[$num][0], $assigns[$num][1]);
}
set_numsections($lid, 7);
echo "  OK: 7 разделов\n";

// ══════════════════════════════════════════════════════════════
// ОКРУЖАЮЩИЙ МИР (Плешаков)
// ══════════════════════════════════════════════════════════════
echo "\n=== Окружающий мир ===\n";
$oid = create_course('Окружающий мир. 1 класс', 'OKR-1', $g1_id, 'Учебник Плешакова А.А. Школа России.');
$sections = [
    1 => ['Введение. Задавайте вопросы!', 'Знакомство с учебником. Как мы будем учиться.'],
    2 => ['Что и кто?', 'Родина. Природа. Вещи. Новые друзья.'],
    3 => ['Как, откуда и куда?', 'Река. Электричество. Бумага. Стекло. Вода. Мусор.'],
    4 => ['Где и когда?', 'Когда учиться интересно. Времена года. Когда придёт суббота.'],
    5 => ['Почему и зачем?', 'Почему Солнце светит днём. Почему звёзды разные. Зачем мы спим.'],
    6 => ['Итоговое повторение', 'Обобщение знаний за год. Проверочная работа.'],
];
$assigns = [
    2 => ['Моя Родина', 'Напиши: в какой стране живёшь, в каком городе. Чем гордишься? 3-4 предложения.'],
    3 => ['Путь воды в кране', 'Нарисуй схему: река — очистная станция — трубы — кран. Подпиши каждый этап.'],
    4 => ['Времена года', 'Запиши по 2 признака каждого сезона. Какое время года нравится больше и почему?'],
    5 => ['День и ночь', 'Объясни своими словами, почему бывает день и ночь. Можно нарисовать схему.'],
    6 => ['Итоговое сочинение', 'Напиши мини-сочинение (5-6 предложений): что тебя удивило в этом курсе больше всего.'],
];
foreach ($sections as $num => $d) {
    $sec_id = add_section($oid, $num, $d[0], $d[1]);
    if (isset($assigns[$num])) add_assign($oid, $sec_id, $assigns[$num][0], $assigns[$num][1]);
}
set_numsections($oid, 6);
echo "  OK: 6 разделов\n";

echo "\nВсе курсы 1 класса созданы!\n";
echo "Русский язык: id=$rid\n";
echo "Математика: id=$mid\n";
echo "Литературное чтение: id=$lid\n";
echo "Окружающий мир: id=$oid\n";
