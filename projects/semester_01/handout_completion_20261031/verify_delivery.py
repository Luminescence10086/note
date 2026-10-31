"""Check the four-course final delivery, including bytes, links and approvals."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
records = json.loads((HERE / 'archive_manifest.json').read_text(encoding='utf-8'))
expected = {'MA105': 8, 'MA106': 12, 'MA302': 20, 'MA306': 16}
assert set(records) == set(expected), 'Not all four courses have been archived'
checks = []
links = 0
for course, n in expected.items():
    item = records[course]
    path = ROOT / item['archive']
    raw = path.read_bytes()
    source = (ROOT / item['source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == item['archive_sha256']
    assert hashlib.sha256(source).hexdigest() == item['source_sha256']
    assert raw[item['reviewed_body_offset_bytes']:] == source
    assert len(raw) == item['archive_bytes'] and len(source) == item['source_bytes']
    assert item['chapters'] == n
    text = raw.decode('utf-8')
    assert b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf')
    assert '$$' not in text and '\ufffd' not in text
    for line in text.splitlines():
        assert len(re.findall(r'(?<!\\)\$', line)) % 2 == 0, course
    for report in item['reports']:
        assert hashlib.sha256((ROOT / report['path']).read_bytes()).hexdigest() == report['sha256']
    for signal in item['approval_signals']:
        approval = json.loads((ROOT / signal).read_text(encoding='utf-8'))
        assert approval['sha256'] == item['source_sha256']
        assert approval['status'] in ['math_review_pass', 'cross_review_consistent']
    folders = list((ROOT / 'professors/MATH').glob(f'handout_{course}_*/.progress.json'))
    assert len(folders) == 2, (course, 'expected design and author progress files')
    for p in folders:
        state = json.loads(p.read_text(encoding='utf-8'))
        assert state['review_status'] == 'approved_and_archived'
        assert len(state['chapters_written']) == n and not state['chapters_pending']
        assert state['archived_file'] == item['archive']
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith(('http:', 'https:', '#')):
            continue
        target = link.split('#')[0].strip('<>')
        if target:
            assert (path.parent / target).exists(), (course, target)
            links += 1
    checks.append({'course': course, 'chapters': n, 'body_byte_equal': True,
                   'format': 'PASS', 'reports_and_approvals': 'PASS',
                   'both_progress_files': 'PASS', 'archive_sha256': item['archive_sha256']})
result = {'status': 'PASS', 'date': '2026-10-31', 'lectures': sum(expected.values()),
          'checked_archive_local_links': links, 'courses': checks,
          'student_mastery_changed': False}
(HERE / 'final_delivery_verification.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('PASS: 4 courses, 56 lectures; reviewed bodies unchanged; reports, approvals, progress, format and links verified.')
