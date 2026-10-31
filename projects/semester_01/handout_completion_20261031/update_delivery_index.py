"""Refresh the delivery index from verified archive records, preserving history."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
manifest = json.loads((HERE / 'archive_manifest.json').read_text(encoding='utf-8'))
courses = [('MA105', '模论与结构定理', 8), ('MA106', '有限群表示论', 12),
           ('MA302', '常微分方程与动力系统', 20), ('MA306', '概率论II：测度论概率', 16)]
completed = len(manifest) == 4
heading = '四门56讲已完成审核与归档' if completed else '56讲已写齐，归档收尾中'
lines = [f'# {heading}', '', '2026-10-31。按用户确认的四门既有设计完成编写；不扩展到总清单其他课程。每门有合订正文、例题、引导题、独立题及答案。', '',
         '| 课程 | 讲数 | 正式阅读入口 | 当前状态 |', '|---|---:|---|---|']
for code, title, n in courses:
    if code in manifest:
        path = manifest[code]['archive']
        lines.append(f'| {code} {title} | {n}/{n} | [合订讲义](../../{path}) | 已审核归档 |')
    else:
        lines.append(f'| {code} {title} | {n}/{n} | 作者合订本已齐备 | 综合审稿收尾中 |')
lines += ['', '数学学科审稿均已通过。涉及跨科的 MA106、MA302、MA306 另走真实综合审稿；MA105为数学内部结构内容。已归档文件前置当前状态说明，并完整保留被审核正文。', '',
          '每门沿原设计明确区分“本课完整证明”“只陈述的输入”和“后续课程”。例如 ODE 的一般 Hartman–Grobman、Poincaré–Bendixson、中心流形等，及测度论概率的一般 Polish 空间版本、Birkhoff 与 Brownian 连续版本，保留原定证明边界。', '',
          '核验资料：[归档与正文指纹清单](../../projects/semester_01/handout_completion_20261031/archive_manifest.json)、[56讲作者稿格式检查](../../projects/semester_01/handout_completion_20261031/author_manuscript_audit.json)、[教务长核验说明](../../lectures/math/review_reports/20261031_四门讲义归档核验_CDX.md)。', '',
          '本次完成的是教材编写与审核，不代表学生已学完；原待讲、待测验、R/B 登记不自动关闭。教师核验代码保存在 `projects/semester_01/handout_completion_20261031/`，不记作学生已完成项目。', '', '---', '']
p = ROOT / 'professors/MATH/20261031_四门讲义续写进度_CDX.md'
old = p.read_text(encoding='utf-8')
marker = '# 四门讲义续写进度（2026-10-31）'
assert marker in old
history = old[old.index(marker):]
p.write_text('\n'.join(lines) + history, encoding='utf-8')

readme = ROOT / 'lectures/math/README.md'
text = readme.read_text(encoding='utf-8')
start = '<!-- FOUR_COURSES_20261031_BEGIN -->'
end = '<!-- FOUR_COURSES_20261031_END -->'
section = [start, '', '## 2026-10-31 四门课程讲义', '',
           '[编写与审核总览](../../professors/MATH/20261031_四门讲义续写进度_CDX.md)', '']
for code, title, n in courses:
    if code in manifest:
        name = Path(manifest[code]['archive']).name
        section.append(f'- [{code} {title}（{n}讲）](approved/{name})')
section += ['', '正文中的旧待审标记属于写作历史；当前状态见各文件最前面的归档说明。', '', end]
new = '\n'.join(section)
if start in text:
    a = text.index(start); b = text.index(end, a) + len(end)
    text = text[:a] + new + text[b:]
else:
    text = text.rstrip() + '\n\n' + new + '\n'
readme.write_text(text, encoding='utf-8')
print(heading)
