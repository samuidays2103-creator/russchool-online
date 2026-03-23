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

    # Enable edit mode on system dashboard
    html_em, _ = post('/editmode.php', {
        'sesskey': sk,
        'setmode': '1',
        'pageurl': MOODLE_URL + '/my/indexsys.php',
        'context': '1',
    })
    sk = get_sk(html_em) or sk

    # Step 1: GET the bui_addblock picker
    print('\n=== GET bui_addblock picker ===')
    html_picker, url_picker = get(f'/my/indexsys.php?bui_addblock&sesskey={sk}')
    sk = get_sk(html_picker) or sk
    print(f'  URL: {url_picker}')

    # Look for nextlesson option in the picker
    if 'nextlesson' in html_picker.lower():
        print('  nextlesson found in picker!')
        idx = html_picker.lower().find('nextlesson')
        print(f'  Context: {strip_tags(html_picker[max(0,idx-200):idx+300])[:300]}')

        # Find the link/form to add it
        m_nl_link = re.search(r'href="([^"]*nextlesson[^"]*)"', html_picker)
        if m_nl_link:
            print(f'  Add link: {m_nl_link.group(1)}')
            add_link = m_nl_link.group(1).replace('&amp;', '&')
            # Follow the link
            html_added, url_added = get(add_link.replace(MOODLE_URL, ''))
            sk = get_sk(html_added) or sk
            print(f'  After clicking add: {url_added}')
            blocks = set(re.findall(r'data-block="([\w_]+)"', html_added))
            print(f'  Blocks: {blocks}')
            if 'nextlesson' in blocks:
                print('  SUCCESS: block_nextlesson added to system dashboard!')
    else:
        print('  nextlesson NOT in picker.')
        # Show what blocks are available
        available = re.findall(r'bui_addblock=([a-z_]+)', html_picker)
        print(f'  Available blocks: {available[:15]}')

        # Try to find the form and submit with nextlesson
        m_form = re.search(r'<form[^>]+>(.*?)</form>', html_picker, re.S | re.I)
        if m_form:
            form_txt = strip_tags(m_form.group(0))[:400]
            print(f'  Picker form: {form_txt}')

    # Step 2: Try bui_addblock with value
    print('\n=== Try bui_addblock=nextlesson ===')
    html_add, url_add = get(f'/my/indexsys.php?bui_addblock=nextlesson&sesskey={sk}')
    sk = get_sk(html_add) or sk
    print(f'  URL: {url_add}')
    blocks = set(re.findall(r'data-block="([\w_]+)"', html_add))
    print(f'  Blocks: {blocks}')
    if 'nextlesson' in blocks:
        print('  SUCCESS!')
    else:
        # Try POST
        html_add2, url_add2 = post(f'/my/indexsys.php', {
            'bui_addblock': 'nextlesson',
            'sesskey': sk,
        })
        sk = get_sk(html_add2) or sk
        print(f'  POST bui_addblock: {url_add2}')
        blocks2 = set(re.findall(r'data-block="([\w_]+)"', html_add2))
        print(f'  Blocks: {blocks2}')
        if 'nextlesson' in blocks2:
            print('  SUCCESS via POST!')

    # Step 3: Use Moodle block manager API
    print('\n=== block_manager_move_block_to_dock ===')

    # In Moodle 4.x, adding a block is triggered by:
    # GET /my/indexsys.php?addblock=nextlesson when in edit mode
    # Let's check if the session is actually in edit mode

    # Refresh system dashboard to check
    html_check, _ = get('/my/indexsys.php')
    sk = get_sk(html_check) or sk
    m_edit = re.search(r'"editing"\s*:\s*(true|false)', html_check)
    print(f'  editing={m_edit.group(1) if m_edit else "unknown"}')

    # Check for "Add a block" button
    m_add_btn = re.search(r'bui_addblock[^"]*"', html_check)
    if m_add_btn:
        print(f'  Add block URL pattern: {m_add_btn.group(0)[:100]}')

    # The edit mode seems to be working (we see "Add a block" link)
    # But addblock param doesn't work - maybe it needs a POST with specific data

    # Let's look at what Moodle 4.x uses for the block add form
    # In Moodle 4.x, when you click "Add a block" it opens a modal
    # and POSTs to /my/indexsys.php with specific form data

    # Try the exact format Moodle uses
    print('\n=== Try exact Moodle 4.x block add format ===')
    # Get the bui_addblock page to see the form structure
    html_bui, url_bui = get(f'/my/indexsys.php?bui_addblock&sesskey={sk}')
    sk = get_sk(html_bui) or sk

    # Get all forms on this page
    forms_on_page = re.findall(r'<form[^>]+action="([^"]+)"[^>]*>(.*?)</form>', html_bui, re.S | re.I)
    print(f'  Forms: {len(forms_on_page)}')
    for i, (action, content) in enumerate(forms_on_page[:5]):
        inputs = re.findall(r'<input[^>]+>', content, re.I)
        selects = re.findall(r'<select[^>]+name="([^"]+)"[^>]*>(.*?)</select>', content, re.S | re.I)
        print(f'  Form {i} action={action[:60]}:')
        for inp in inputs[:5]:
            n = re.search(r'name="([^"]+)"', inp)
            v = re.search(r'value="([^"]*)"', inp)
            t = re.search(r'type="([^"]+)"', inp, re.I)
            if n: print(f'    {t.group(1) if t else "?"}: {n.group(1)}={v.group(1)[:30] if v else "?"}')
        for sname, sopts in selects[:2]:
            opts = re.findall(r'<option[^>]*value="([^"]+)"[^>]*>([^<]+)</option>', sopts)
            print(f'    select: {sname}, options: {opts[:5]}')

    # Try submitting the add block form
    if forms_on_page:
        for action, content in forms_on_page:
            inputs_data = {}
            for inp in re.finditer(r'<input[^>]+>', content, re.I):
                tag = inp.group(0)
                n = re.search(r'name="([^"]+)"', tag)
                v = re.search(r'value="([^"]*)"', tag)
                t = re.search(r'type="([^"]+)"', tag, re.I)
                if n and v and t and t.group(1).lower() in ('hidden', 'text'):
                    inputs_data[n.group(1)] = v.group(1)
            # Find select for block name
            m_sel = re.search(r'<select[^>]+name="([^"]+)"[^>]*>(.*?)</select>', content, re.S | re.I)
            if m_sel:
                sel_name = m_sel.group(1)
                opts = re.findall(r'<option[^>]*value="([^"]+)"[^>]*>([^<]+)</option>', m_sel.group(2))
                nextlesson_opt = next((v for v, n in opts if 'nextlesson' in v.lower()), None)
                if nextlesson_opt:
                    inputs_data[sel_name] = nextlesson_opt
                    print(f'  Found nextlesson option: {nextlesson_opt}')
                    # Submit form
                    inputs_data['sesskey'] = sk
                    post_path = action.replace(MOODLE_URL, '') if action.startswith('http') else action
                    html_submit, url_submit = post(post_path, inputs_data)
                    sk = get_sk(html_submit) or sk
                    print(f'  After form submit: {url_submit}')
                    blocks_s = set(re.findall(r'data-block="([\w_]+)"', html_submit))
                    print(f'  Blocks: {blocks_s}')
                    if 'nextlesson' in blocks_s:
                        print('  SUCCESS via form submit!')

    print('\nDone.')


if __name__ == '__main__':
    main()
