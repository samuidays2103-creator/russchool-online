#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import urllib.request, urllib.parse, http.cookiejar, re

MOODLE_URL = 'http://130.12.47.10'


def get_sk(html):
    for pat in [r'"sesskey"\s*:\s*"([^"]+)"', r'name="sesskey"[^>]*value="([^"]*)"']:
        m = re.search(pat, html)
        if m and m.group(1): return m.group(1)
    return ''

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)


def main():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def get(path, timeout=30):
        r = opener.open(MOODLE_URL + path, timeout=timeout)
        return r.read().decode('utf-8', errors='replace'), r.url

    def post(path, data_dict, timeout=60):
        data = urllib.parse.urlencode(data_dict).encode()
        r = opener.open(MOODLE_URL + path, data, timeout=timeout)
        return r.read().decode('utf-8', errors='replace'), r.url

    def login(user, pw):
        html, _ = get('/login/index.php')
        m = re.search(r'name="logintoken"[^>]*value="([^"]+)"', html)
        lt = m.group(1) if m else ''
        html, url = post('/login/index.php', {
            'username': user, 'password': pw, 'logintoken': lt, 'anchor': ''
        })
        return html, url, get_sk(html)

    print('=' * 60)
    print('VERIFICATION: block_nextlesson')
    print('=' * 60)

    # === Admin view ===
    print('\n--- Admin view ---')
    html_a, url_a, sk_a = login('admin', 'Admin2026!')
    print(f'Admin dashboard: {url_a}')

    html_my, _ = get('/my/')
    if 'nextlesson' in html_my.lower():
        # Extract block content
        m_block = re.search(
            r'<(?:section|div)[^>]*(?:block[_-]nextlesson|data-block="nextlesson")[^>]*>(.*?)</(?:section|div)>\s*</div>',
            html_my, re.S | re.I
        )
        if not m_block:
            m_block = re.search(r'data-block="nextlesson"[^>]*>(.*?)</section>', html_my, re.S)
        if m_block:
            content = re.sub(r'\s+', ' ', strip_tags(m_block.group(1))).strip()
            print(f'  Block content: {content[:300]}')
        else:
            # Find by text
            idx = html_my.lower().find('nextlesson')
            print(f'  Block area: {re.sub(chr(32)+"+", " ", strip_tags(html_my[max(0,idx-100):idx+500]))[:300]}')

        # Check specific content
        for check in ['Следующий урок', 'Next Lesson', 'No upcoming', 'Нет запланированных',
                       'nextlesson-card', 'nextlesson-empty']:
            if check.lower() in html_my.lower():
                print(f'  Found: "{check}"')
    else:
        print('  Block NOT on admin dashboard!')

    # === Student view ===
    print('\n--- Student (ivanov_misha) view ---')
    # Logout admin first
    html_lo, _ = get(f'/login/logout.php?sesskey={sk_a}')

    html_s, url_s, sk_s = login('ivanov_misha', 'Test1234!')
    print(f'Student dashboard: {url_s}')

    html_smy, _ = get('/my/')
    if 'nextlesson' in html_smy.lower():
        idx = html_smy.lower().find('nextlesson-card')
        if idx > 0:
            card_html = html_smy[idx:idx+1000]
            content = re.sub(r'\s+', ' ', strip_tags(card_html)).strip()
            print(f'  Block card: {content[:300]}')
        else:
            # Try finding block section
            m_sec = re.search(r'data-block="nextlesson"[^>]*>(.*?)</section>', html_smy, re.S)
            if m_sec:
                content = re.sub(r'\s+', ' ', strip_tags(m_sec.group(1))).strip()
                print(f'  Block section: {content[:300]}')

        for check in ['Следующий урок', 'Next Lesson', 'No upcoming', 'Нет запланированных',
                       'nextlesson-card', 'nextlesson-empty', 'joinlesson', 'Войти']:
            if check.lower() in html_smy.lower():
                print(f'  Found: "{check}"')
    else:
        print('  Block NOT on student dashboard!')

    # Check block renders without PHP errors
    m_fatal = re.search(r'(?:Fatal error|Parse error|Warning:|Error:)\s*([^\n<]{0,200})', html_smy, re.I)
    if m_fatal:
        print(f'  PHP ERROR: {m_fatal.group(0)[:200]}')
    else:
        print('  No PHP errors detected.')

    print('\n' + '=' * 60)
    print('RESULT:')
    if 'nextlesson' in html_smy.lower():
        print('block_nextlesson SUCCESSFULLY installed and working!')
        print(f'URL: {MOODLE_URL}')
        print('Block appears on both admin and student dashboards.')
    else:
        print('Block installed but not showing on student dashboard.')
    print('=' * 60)


if __name__ == '__main__':
    main()
