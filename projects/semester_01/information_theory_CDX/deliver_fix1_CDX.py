"""Codex 侧数学教授分身（CDX）：增量修订交付与原件保真消费。"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,sys
out=Path(sys.argv[1]);root=Path(sys.argv[2]);now=datetime.now(ZoneInfo('Asia/Shanghai'));stamp=now.isoformat()
def md5(p):return hashlib.md5(p.read_bytes()).hexdigest().upper()
c=json.loads((out/'11-增量核验_v0.1-fix1_CDX.json').read_text(encoding='utf-8'))
main=out/'02-信息论六讲_v0.1-fix1_CDX.md';text=main.read_text(encoding='utf-8');assert md5(main)==c['revised_md5']
def lineof(part):return next(i for i,s in enumerate(text.splitlines(),1) if part in s)
report=f'''# 信息论六讲 v0.1-fix1：首轮审稿修订说明

> **作者**：Codex 侧数学教授分身（Prof-Math · CDX）｜**日期**：{now:%Y-%m-%d}｜**版本**：v0.1-fix1
> **状态**：修订及作者增量核验完成，待 Reviewer_MATH 复核。数学部分首轮通过不等于全稿已批准。

## 依据与版本核对

- 已读取权威报告：`lectures/math/review_reports/review_20261011_MA404_信息论_有限离散六讲.md`，结论为“需修改”。
- 已核对 DSH 实际送审位：MD5 `{c['reviewed_dsh_md5']}`，与报告指纹相符；内容含 CDX v0.1 主稿完整原文。
- 已核对返件：`20261011_math_information_theory_review_return_DSH.md`，MD5 `{c['inbound_md5']}`。
- 已回读权威登记表 R13–R16 四行；状态均为未证，映射 U1→R13、U2→R14、U3→R15、U4→R16。CDX 未改登记表或 DSH 送审位。

## 逐项处置

| 意见 | 处置 | 新稿位置 |
| :--- | :--- | :--- |
| P1 YAML 嵌入正文 | 去掉本地主稿 YAML，改为可见版本栏；新交付件无嵌套 YAML。讲义正文界限用明确标记，不把封面当正文 | L{lineof('**版本**')}–L{lineof('**状态**')} |
| P2 编号口径 | C2 标题、首段与表格改为已登记，加入正式编号及未证状态列 | L{lineof('### C2')} 起 |
| P3 标题前空行 | 第三讲、第五讲、附录 A 均补空行；检查全部标题 | L{lineof('## 第三讲')}、L{lineof('## 第五讲')}、L{lineof('## 附录 A')} |
| S1 首用双标签 | 四个工具首次陈述处加入“登记表 R13”等 | L{lineof('**待证工具 U1')}、L{lineof('**待证工具 U2')}、L{lineof('**待证工具 U3')}、L{lineof('**待证工具 U4')} |
| S2 每讲新图 | 本轮不增补；保留现有全册图与各讲覆盖说明。自读稿可选项，避免扩大此次增量复核范围 | 既有全册地图 |
| S3 题号回链 | 本轮保留现有题号与 B1–B6 分讲解答定位；不新增链接 | 附录 B |

## 增量核验原始结果

核验时点：{c['checked_at']}。新主稿 MD5 `{c['revised_md5']}`，{c['lines']} 行，{c['bytes']} 字节（UTF-8，LF，每行含末尾换行）。

- `all_formula_tokens_identical = true`：逐个数学公式内容及顺序与 v0.1 相同。
- `core_text_identical_except_S1_and_blank_lines = true`：第一讲至附录 B，除 S1 编号文字和空行外，正文、概率表、题干与解答完全相同。
- `question_count = 42`；`issues = []`。
- 无 YAML 字段残留、无双美元、单行定界符均配对、中文公式间隔合规、标题前空行合规、无缺下标求和、无未注明底的 log。
- 未重复进行整册数值测试：题目与公式未变，沿用 v0.1 作者逐题数据及首轮 Reviewer_MATH 的独立复算。当前执行的是审稿指定的增量检查。
- 版本记录只追加；原 v0.1、原审稿报告及原返件保留。差异文件 `10-修订差异_v0.1-fix1_CDX.diff`，检查数据 `11-增量核验_v0.1-fix1_CDX.json`。

## 本件分工与请求

**本件产出、内容修订、后续答复：CDX 数学教授。权威落位、重建送审信号、安排真实增量复核：DSH 数学教授。** 此为本件约定，不扩展为长期分工。

请 DSH 将下述完整修订正文落位为 `lectures/math/MA404_信息论_有限离散六讲.md`，按返件约定将旧送审版保留于 `.harness/superseded/`，并为新版本创建新信号；不要沿用旧送审指纹。若添加 DSH 来源栏，可在正文之前放一次来源说明并留空行，原稿已使用可见版本栏，无需嵌入 YAML 或重复分隔线。

请 Reviewer_MATH 按返件约定复核 P1–P3、S1 对应及机械项。未获对应版本批准前不归档；是否需跨学科复核由教务长按内容判定；不触发教学完成，不更新同学学完状态。意见仍经数学跨侧交换区回送 CDX。
'''
reportpath=out/'09-首轮审稿修订说明_v0.1-fix1_CDX.md';assert not reportpath.exists() or md5(reportpath)=='311E38297D3025FF4840163C2191C15B';reportpath.write_text(report,encoding='utf-8',newline='\n')
packet=report+'''\n## 完整讲义正文的提取约定

以下 BEGIN/END 两个独占行标记之间是主稿全部字节对应的文本，不包含标记行；UTF-8、LF，并保留正文末尾一个换行。提取后应与上述主稿 MD5 完全相符。请不要把本修订说明、检查数据或标记行拼入学生阅读稿。

<!-- BEGIN_HANDOUT_CDX_V01_FIX1 -->
'''+text+'<!-- END_HANDOUT_CDX_V01_FIX1 -->\n'
extracted=packet.split('<!-- BEGIN_HANDOUT_CDX_V01_FIX1 -->\n',1)[1].split('<!-- END_HANDOUT_CDX_V01_FIX1 -->',1)[0]
assert extracted.encode('utf-8')==main.read_bytes()
local=out/'12-跨侧重送_v0.1-fix1_CDX.md';assert not local.exists();local.write_text(packet,encoding='utf-8',newline='\n')
name='20261011_math_information_theory_v01fix1_讲义初稿_CDX.md'
dest=root/'signals/xside/to_dsh/math'/name
stage=root/'projects/semester_01/information_theory_CDX/delivery_v01fix1_CDX.tmp'
inbound=root/'signals/xside/to_codex/math/20261011_math_information_theory_review_return_DSH.md'
consumed=root/'signals/xside/consumed'/now.strftime('%Y%m%d')/inbound.name
assert not dest.exists() and not stage.exists() and not consumed.exists()
assert md5(inbound)==c['inbound_md5']
stage.write_bytes(local.read_bytes());assert md5(stage)==md5(local);stage.rename(dest)
dh=md5(dest);assert dh==md5(local)
p=out/'.progress.json';oldhash=md5(p);d=json.loads(p.read_text(encoding='utf-8'))
d.setdefault('review_history',[]).append({'received_file':inbound.name,'source_md5':c['inbound_md5'],'report':'lectures/math/review_reports/review_20261011_MA404_信息论_有限离散六讲.md','verdict':'requires_changes','math_and_42_question_checks':'passed_per_independent_report','required_changes':['P1','P2','P3'],'applied_optional':['S1'],'revised_version':'0.1-fix1'})
d.update(status='v0.1-fix1 已修复首轮须修项并重送；待 DSH 增量复核',handout=main.name,verification=reportpath.name,independent_review='incremental_review_pending',next_action='收到对应修订版的真实复核意见后处理；批准前不归档',delivery='signals/xside/to_dsh/math/'+name,delivered_at=stamp,delivery_md5=dh,updated=now.strftime('%Y-%m-%d'),unproven_registry_mapping={'U1':'R13','U2':'R14','U3':'R15','U4':'R16'})
assert md5(p)==oldhash;p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
# Single-file move inside the explicitly scoped workspace; original bytes unchanged.
assert consumed.is_relative_to(root/'signals/xside/consumed')
consumed.parent.mkdir(parents=True,exist_ok=True)
assert md5(inbound)==c['inbound_md5'];inbound.rename(consumed);assert md5(consumed)==c['inbound_md5']
log=f'''\n\n## 审稿返件处理与 fix1 重送（CDX）

- 时点：{stamp}。
- 首轮返件原件已移入 `{consumed}`；MD5 `{md5(consumed)}`，与收件时一致。已核实。
- 新交付件：`{dest}`；MD5 `{dh}`，{len(packet.splitlines())} 行。写后读取校验成功，已核实。
- 主稿：`{main.name}`；MD5 `{md5(main)}`，{len(text.splitlines())} 行。提取界限内文本与主稿逐字节相同。
- 进度写前 MD5 `{oldhash}`；写后 `{md5(p)}`。
- DSH 权威正文与登记表未写入。原 v0.1 和首次交付件未改写。待增量复核，不视为批准。
'''
with (out/'08-状态与交付记录_CDX.md').open('a',encoding='utf-8') as f:f.write(log)
print(json.dumps({'delivered_at':stamp,'delivery_md5':dh,'main_md5':md5(main),'consumed_md5':md5(consumed),'status':'resubmitted_and_inbound_archived'},ensure_ascii=True))