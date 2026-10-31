"""Archive reviewed manuscripts without changing their reviewed bytes.

The archive manifest is external: a file cannot contain its own final SHA256.
Run with course IDs after populating archive_config.json from actual approvals.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = HERE / 'archive_manifest.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    config = json.loads((HERE / 'archive_config.json').read_text(encoding='utf-8'))
    records = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {}
    for course in sys.argv[1:]:
        c = config[course]
        source = ROOT / c['source']
        body = source.read_bytes()
        assert sha(body) == c['source_sha256'], (course, 'reviewed source changed')
        body.decode('utf-8')
        assert not body.startswith(b'\xef\xbb\xbf') and b'\r' not in body
        assert b'$$' not in body
        target = ROOT / c['target']
        reports = []
        for rel in c['reports']:
            p = ROOT / rel
            reports.append({'path': rel, 'sha256': sha(p.read_bytes())})
        for rel in c['approval_signals']:
            s = json.loads((ROOT / rel).read_text(encoding='utf-8'))
            assert s['sha256'] == c['source_sha256'], (course, 'approval mismatch')
        def link(rel):
            # All archive files live at lectures/math/approved.
            return '../../../' + rel
        report_links = '\n'.join(f'- [审核记录 {i+1}]({link(x["path"])})' for i,x in enumerate(reports))
        cover = f'''# {course} {c['title']}｜正式归档说明

2026-10-31；本课共 **{c['chapters']} 讲**，属于四门共 56 讲编写批次。数学学科审稿通过；{c['cross_status']}。正文、例题与习题答案齐备，原设计中明确只陈述或预告的高级理论仍保留其证明边界。

下方完整保留被审核的作者稿。其中“待独立审稿”“未经独立审稿”“待复审”“尚未批准”等标签及作者自校区的阶段状态是写作历史，当前审核状态以本说明和对应报告为准。学习验收与 PDF 编译未因此完成；不自动改变学生掌握记录或共享未证结论登记。

审核记录：

{report_links}

被审作者稿 SHA256：`{c['source_sha256']}`；字节数：{len(body)}。归档文件在其前面增加本说明，正文逐字节不变。完整文件的独立 SHA256、字节数和正文起始偏移记录在[归档核验清单]({link('projects/semester_01/handout_completion_20261031/archive_manifest.json')})；完整文件哈希置于外部清单，避免自引用。

---

<!-- REVIEWED_AUTHOR_BYTES_BEGIN -->
'''.encode('utf-8')
        data = cover + body
        if target.exists():
            existing = target.read_bytes()
            old = records.get(course)
            assert existing == body or existing == data or (old and sha(existing) == old['archive_sha256']), (course, 'unrelated existing archive')
        target.write_bytes(data)
        readback = target.read_bytes()
        assert readback[len(cover):] == body
        records[course] = {
            'course': course, 'chapters': c['chapters'], 'date': '2026-10-31',
            'source': c['source'], 'source_sha256': sha(body), 'source_bytes': len(body),
            'archive': c['target'], 'archive_sha256': sha(readback), 'archive_bytes': len(readback),
            'reviewed_body_offset_bytes': len(cover), 'body_byte_equal': True,
            'reports': reports, 'approval_signals': c['approval_signals'],
            'cross_status': c['cross_status'], 'student_mastery_changed': False,
        }
        progress_path = source.parent / '.progress.json'
        progress = json.loads(progress_path.read_text(encoding='utf-8'))
        progress.update(phase=5, review_status='approved_and_archived', archived_file=c['target'],
                        archive_sha256=sha(readback), review_reports=c['reports'],
                        completion_requirements_pending=[], updated='2026-10-31')
        dump(progress_path, progress)
        print(course, c['chapters'], sha(readback), 'body unchanged')
    dump(MANIFEST, records)
    for course, record in records.items():
        data = (ROOT / record['archive']).read_bytes()
        assert sha(data) == record['archive_sha256']
        assert sha(data[record['reviewed_body_offset_bytes']:]) == record['source_sha256']
    print('Verified archived courses:', ', '.join(records))


if __name__ == '__main__':
    main()
