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

    def get(path, timeout=30):
        r = opener.open(MOODLE_URL + path, timeout=timeout)
        return r.read().decode('utf-8', errors='replace'), r.url

    def post(path, data_dict, timeout=60):
        data = urllib.parse.urlencode(data_dict).encode()
        r = opener.open(MOODLE_URL + path, data, timeout=timeout)
        return r.read().decode('utf-8', errors='replace'), r.url

    # Login as admin
    html, _ = get('/login/index.php')
    m = re.search(r'name="logintoken"[^>]*value="([^"]+)"', html)
    lt = m.group(1) if m else ''
    html, _ = post('/login/index.php', {
        'username': 'admin', 'password': 'Admin2026!', 'logintoken': lt, 'anchor': ''
    })
    sk = get_sk(html)
    print(f'Login OK. sk={sk[:15]}')

    # Step 1: Go to system dashboard
    html_sys, url_sys = get('/my/indexsys.php')
    sk = get_sk(html_sys) or sk
    print(f'System dashboard: {url_sys}')

    # Step 2: Enable edit mode via editmode.php
    print('\n=== Enable edit mode via editmode.php ===')
    html_em, url_em = post('/editmode.php', {
        'sesskey': sk,
        'setmode': '1',
        'pageurl': MOODLE_URL + '/my/indexsys.php',
        'context': '1',
    })
    sk = get_sk(html_em) or sk
    print(f'  Edit mode enable: {url_em}')

    # Check if we're now in edit mode
    html_sys2, url_sys2 = get('/my/indexsys.php')
    sk = get_sk(html_sys2) or sk
    print(f'  System dashboard: {url_sys2}')

    # Look for edit mode indicators
    if '"editing":true' in html_sys2 or 'editing' in html_sys2:
        print('  Edit mode IS active!')

    # Check for blocks in edit mode
    blocks = set(re.findall(r'data-block="([\w_]+)"', html_sys2))
    print(f'  Current blocks: {blocks}')

    # Look for "Add a block" section
    m_add = re.search(r'(?:add.?a.?block|block-add-menu|addblock)', html_sys2, re.I)
    if m_add:
        idx = html_sys2.find(m_add.group(0))
        print(f'  Add block area: {strip_tags(html_sys2[max(0,idx-50):idx+300])[:200]}')
    else:
        print('  No "Add a block" section found.')

    # Step 3: Try adding block now that edit mode may be active
    print('\n=== Add block to system dashboard ===')
    html_add, url_add = get(f'/my/indexsys.php?addblock=nextlesson')
    sk = get_sk(html_add) or sk
    print(f'  After addblock: {url_add}')
    blocks_after = set(re.findall(r'data-block="([\w_]+)"', html_add))
    print(f'  Blocks after: {blocks_after}')
    if 'nextlesson' in blocks_after:
        print('  SUCCESS: block_nextlesson added to system dashboard!')

    # If still not working, try via POST
    if 'nextlesson' not in blocks_after:
        html_add2, url_add2 = post('/my/indexsys.php', {
            'sesskey': sk,
            'addblock': 'nextlesson',
            'bui_blockregion': 'content',
            '_add_block': '1',
        })
        sk = get_sk(html_add2) or sk
        print(f'  POST addblock: {url_add2}')
        blocks_after2 = set(re.findall(r'data-block="([\w_]+)"', html_add2))
        print(f'  Blocks after POST: {blocks_after2}')

    # Step 4: Get edit form on system dashboard
    print('\n=== Inspect system dashboard edit controls ===')
    html_sys3, _ = get('/my/indexsys.php')
    sk = get_sk(html_sys3) or sk

    # Find block action links
    action_links = re.findall(r'href="([^"]*(?:block|bui)[^"]*)"', html_sys3)
    print(f'  Block action links: {action_links[:5]}')

    # Find edit/add controls
    edit_links = re.findall(r'<a[^>]+href="([^"]+edit[^"]+)"[^>]*>([^<]+)</a>', html_sys3, re.I)
    print(f'  Edit links: {edit_links[:5]}')

    # What blocks are currently on system dashboard
    sys_blocks = set(re.findall(r'data-block="([\w_]+)"', html_sys3))
    print(f'  Current sys dashboard blocks: {sys_blocks}')

    # Step 5: Add the block using Moodle's block instance creation
    # The system dashboard (indexsys.php) is page type 'my-index', subpagepattern '__default'
    # contextid = 2 for the system context? Or 1?

    # Let's find the correct context by looking at the page JS data
    m_page_data = re.search(r'M\.cfg\s*=\s*(\{[^;]+\})', html_sys3)
    if m_page_data:
        try:
            page_data = json.loads(m_page_data.group(1))
            print(f'  Page data keys: {list(page_data.keys())}')
            print(f'  contextid: {page_data.get("contextid")}')
            print(f'  contextInstanceId: {page_data.get("contextInstanceId")}')
        except:
            pass

    # Find the courseId / contextId from window.M.cfg
    m_cfg = re.search(r'"contextid"\s*:\s*(\d+)', html_sys3)
    m_courseid = re.search(r'"courseId"\s*:\s*(\d+)', html_sys3)
    ctx_id = m_cfg.group(1) if m_cfg else '1'
    course_id = m_courseid.group(1) if m_courseid else '1'
    print(f'  contextid={ctx_id}, courseId={course_id}')

    # The block instance add in Moodle is done via:
    # POST /my/indexsys.php with the correct params when in edit mode
    # The "addblock" param needs to match the block name

    # First enable edit mode properly
    html_em2, url_em2 = post('/editmode.php', {
        'sesskey': sk,
        'setmode': '1',
        'pageurl': MOODLE_URL + '/my/indexsys.php',
        'context': ctx_id,
    })
    sk = get_sk(html_em2) or sk
    print(f'\n  editmode.php returned: {url_em2}')

    # Now try adding the block with editmode active (session)
    html_try, url_try = get(f'/my/indexsys.php?addblock=nextlesson&bui_blockregion=content&sesskey={sk}')
    sk = get_sk(html_try) or sk
    print(f'  Try addblock with sesskey: {url_try}')
    blocks_try = set(re.findall(r'data-block="([\w_]+)"', html_try))
    print(f'  Blocks: {blocks_try}')
    if 'nextlesson' in blocks_try:
        print('  SUCCESS!')

    # Last resort: use the "Reset Dashboard for all users" after admin has block on their page
    # This will reset student dashboards to match admin's configured system default
    # But this requires the block to be on system default first

    # Let's try adding to system default via the URL format that Moodle 4.x uses
    print('\n=== Alternative: use /my/?pagehash= approach ===')
    # Get the system page with pagehash
    html_sys4, _ = get('/my/indexsys.php?edit=1')
    sk = get_sk(html_sys4) or sk

    # Find page hash
    m_ph = re.search(r'data-page-hash="([^"]+)"', html_sys4)
    ph = m_ph.group(1) if m_ph else ''
    print(f'  Page hash: {ph[:30] if ph else "not found"}')

    # Try GET with page hash and addblock
    if ph:
        html_ph, url_ph = get(f'/my/indexsys.php?addblock=nextlesson&pagehash={ph}&sesskey={sk}')
        print(f'  With pagehash: {url_ph}')
        if 'nextlesson' in html_ph.lower():
            print('  Block added!')

    print('\n=== Summary ===')
    print('block_nextlesson plugin is installed and working on admin dashboard.')
    print('To add to student dashboards: admin needs to manually add block to')
    print('/my/indexsys.php (system default) via browser UI, then use')
    print('"Reset Dashboard for all users" button.')
    print('\nAlternatively, the block can be added directly to student dashboard')
    print('by the student or via Moodle admin user management.')

    print('\nDone.')


if __name__ == '__main__':
    main()
