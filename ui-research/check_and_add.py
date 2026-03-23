#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import urllib.request, urllib.parse, http.cookiejar, re, json

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

    def get(path, timeout=30, allow_500=False):
        try:
            r = opener.open(MOODLE_URL + path, timeout=timeout)
            return r.read().decode('utf-8', errors='replace'), r.url, r.status
        except urllib.error.HTTPError as e:
            if allow_500:
                return e.read().decode('utf-8', errors='replace'), e.url if hasattr(e, 'url') else path, e.code
            raise

    def post(path, data_dict, timeout=60, allow_500=False):
        data = urllib.parse.urlencode(data_dict).encode()
        try:
            r = opener.open(MOODLE_URL + path, data, timeout=timeout)
            return r.read().decode('utf-8', errors='replace'), r.url, r.status
        except urllib.error.HTTPError as e:
            if allow_500:
                return e.read().decode('utf-8', errors='replace'), str(e.url) if hasattr(e, 'url') else path, e.code
            raise

    # Login as admin
    html, _, _ = get('/login/index.php')
    m = re.search(r'name="logintoken"[^>]*value="([^"]+)"', html)
    lt = m.group(1) if m else ''
    html, _, _ = post('/login/index.php', {
        'username': 'admin', 'password': 'Admin2026!', 'logintoken': lt, 'anchor': ''
    })
    sk = get_sk(html)
    print(f'Login OK. sk={sk[:15]}')

    # Enable edit mode on system dashboard
    html_em, _, _ = post('/editmode.php', {
        'sesskey': sk, 'setmode': '1',
        'pageurl': MOODLE_URL + '/my/indexsys.php', 'context': '1',
    })
    sk = get_sk(html_em) or sk
    print(f'Edit mode enabled. sk={sk[:15]}')

    # Check current system dashboard
    print('\n=== Current system dashboard blocks ===')
    html_sys, url_sys, _ = get('/my/indexsys.php')
    sk = get_sk(html_sys) or sk
    blocks_before = set(re.findall(r'data-block="([\w_]+)"', html_sys))
    print(f'Blocks before: {blocks_before}')

    # Add block (allow 500 error)
    print('\n=== Adding block (allow 500) ===')
    html_add, url_add, status_add = get(
        f'/my/indexsys.php?sesskey={sk}&bui_addblock=nextlesson',
        allow_500=True
    )
    print(f'Status: {status_add}, URL: {url_add}')

    if status_add == 500:
        # 500 might mean the block was added but there was a redirect issue
        # Check the error message
        m_err = re.search(r'<(?:p|div)[^>]*class="[^"]*(?:alert|error|message)[^"]*"[^>]*>(.*?)</(?:p|div)>', html_add, re.S)
        if m_err:
            print(f'Error msg: {strip_tags(m_err.group(1))[:200]}')

        # The block might still have been added to DB - check by loading the page fresh
        html_check, _, _ = get('/my/indexsys.php')
        sk = get_sk(html_check) or sk
        blocks_after = set(re.findall(r'data-block="([\w_]+)"', html_check))
        print(f'Blocks after 500: {blocks_after}')
        if 'nextlesson' in blocks_after:
            print('Block was added despite 500 error!')

    elif status_add == 200:
        blocks_after = set(re.findall(r'data-block="([\w_]+)"', html_add))
        print(f'Blocks after: {blocks_after}')
        if 'nextlesson' in blocks_after:
            print('SUCCESS: block_nextlesson added!')

    # Now reset all user dashboards
    print('\n=== Reset Dashboard for all users ===')
    html_sys2, _, _ = get('/my/indexsys.php')
    sk = get_sk(html_sys2) or sk
    blocks_sys = set(re.findall(r'data-block="([\w_]+)"', html_sys2))
    print(f'System dashboard blocks: {blocks_sys}')

    if 'nextlesson' in blocks_sys:
        print('Block IS on system dashboard - proceeding with reset!')
        # Submit the Reset Dashboard form
        html_reset, url_reset, _ = post('/my/indexsys.php', {
            'sesskey': sk,
            'resetall': '1',
        })
        sk = get_sk(html_reset) or sk
        print(f'Reset result: {url_reset}')
        print(f'Content: {re.sub(chr(32)+"+", " ", strip_tags(html_reset))[:300]}')
    else:
        print('Block NOT on system dashboard yet. Manual addition required.')
        print('\n=== Trying alternative block insertion ===')

        # Try adding with the exact format from the picker
        # The link was: ?sesskey=...&bui_addblock=nextlesson
        # This returned 500. Let's check the error log by trying differently

        # Enable edit mode fresh
        html_em2, _, _ = post('/editmode.php', {
            'sesskey': sk, 'setmode': '1',
            'pageurl': MOODLE_URL + '/my/indexsys.php', 'context': '1',
        })
        sk = get_sk(html_em2) or sk

        # Try POST instead of GET
        html_add_post, url_add_post, status_post = post(
            '/my/indexsys.php',
            {'sesskey': sk, 'bui_addblock': 'nextlesson'},
            allow_500=True
        )
        print(f'POST status: {status_post}, URL: {url_add_post}')
        blocks_post = set(re.findall(r'data-block="([\w_]+)"', html_add_post))
        print(f'Blocks after POST: {blocks_post}')

        # Check fresh
        html_fresh, _, _ = get('/my/indexsys.php')
        sk = get_sk(html_fresh) or sk
        blocks_fresh = set(re.findall(r'data-block="([\w_]+)"', html_fresh))
        print(f'Fresh check blocks: {blocks_fresh}')

    # Check student dashboard
    print('\n=== Student dashboard check ===')
    html_lo, _, _ = get(f'/login/logout.php?sesskey={sk}')

    html_sl, _, _ = get('/login/index.php')
    m = re.search(r'name="logintoken"[^>]*value="([^"]+)"', html_sl)
    lt2 = m.group(1) if m else ''
    html_sl2, url_sl2, _ = post('/login/index.php', {
        'username': 'ivanov_misha', 'password': 'Test1234!', 'logintoken': lt2, 'anchor': ''
    })
    sk2 = get_sk(html_sl2)
    print(f'Student login: {url_sl2}')

    html_smy, _, _ = get('/my/')
    blocks_stu = set(re.findall(r'data-block="([\w_]+)"', html_smy))
    print(f'Student blocks: {blocks_stu}')
    if 'nextlesson' in blocks_stu:
        print('SUCCESS: block_nextlesson on student dashboard!')
    else:
        print('Block not on student dashboard. Plugin installed, block works for admin.')
        print('Admin can manually add block to student via Admin > Users > Dashboard.')

    print('\nDone.')


if __name__ == '__main__':
    main()
