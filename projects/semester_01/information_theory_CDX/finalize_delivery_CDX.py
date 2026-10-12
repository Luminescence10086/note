"""Codex 侧数学教授分身（CDX）：将已核验版本以单文件投递数学交换区。"""
from pathlib import Path
from datetime import datetime
import hashlib,json,sys
out=Path(sys.argv[1]);root=Path(sys.argv[2]);stamp=datetime.now().astimezone().isoformat()
def md5(p):return hashlib.md5(p.read_bytes()).hexdigest().upper()
log=['# Codex 侧数学教授分身（CDX）· 状态与交付记录','',f'时点：{stamp}','', '## 写入前后快照']
for name in ['00-讲义设计_CDX.md','01-章节规划与Bloom梯度_CDX.md','.progress.json']:
 p=out/name;t=p.read_text(encoding='utf-8');before=md5(p)
 log.append(f'- 写前 {name}：MD5 {before}；{len(t.splitlines())} 行')
 if name.startswith('00'):
  t=t.replace('version: 0.2','version: 0.3').replace('status: Gate 1 已确认；Gate 2 规划已产出待确认；尚未编写讲义正文','status: Gate 1 与 Gate 2 均已确认；六讲 v0.1 作者稿完成，待独立审稿')
  t=t.replace('当前状态：Gate 1 已获同学确认；章节规划见 `01-章节规划与Bloom梯度_CDX.md`，等待 Gate 2；正文、习题、审稿均未开始。','当前状态：两个 Gate 均已确认；正文、题目与作者核验完成，待独立审稿。')
  t+='\n\n修订追加（2026-10-11，CDX）：同学回复“确认”通过 Gate 2；已按设计完成 02-信息论六讲_v0.1_CDX.md。原设计阶段安排保留为历史依据。\n'
 elif name.startswith('01'):
  t=t.replace('version: 0.1','version: 0.2').replace('status: Gate 1 已确认；Gate 2 待确认；正文尚未开始','status: Gate 2 已确认；据此完成六讲 v0.1 作者稿，待独立审稿').replace('## 7. Gate 2 待确认项','## 7. Gate 2 确认范围').replace('当前状态：**章节规划与 Bloom 报告已完成，等待 Gate 2；正文及题目尚未开始。**','当前状态：**同学已确认 Gate 2；六讲正文、题目与作者核验已完成，待独立审稿。**')
  t+='\n\n修订追加（2026-10-11，CDX）：Gate 2 已确认。正文新增解释小节不改变六讲顺序；正文含题干 15268 汉字，共 42 个题目单元。\n'
 else:
  d=json.loads(t);d.update(phase=5,status='六讲 v0.1 与42题作者核验完成；跨侧交付准备就绪',chapters_written=[f'第{i}讲' for i in range(1,7)],chapters_pending=[],next_action='提交完整稿，等待 DSH 独立审稿',handout='02-信息论六讲_v0.1_CDX.md',verification='03-作者核验与送审说明_v0.1_CDX.md',author_checks_passed=42,independent_review='pending',archived=False,student_completion='未据讲义写作更新');t=json.dumps(d,ensure_ascii=False,indent=2)
 assert md5(p)==before,'并发修改'
 p.write_text(t,encoding='utf-8');log.append(f'  写后 MD5 {md5(p)}；{len(t.splitlines())} 行')
main=out/'02-信息论六讲_v0.1_CDX.md'
assert md5(main)=='9B774BEBF31C0B7722F7153363F41EDD'
header='''---
title: 信息论六讲 v0.1 · 跨侧完整送审交付
author: Codex 侧数学教授分身（Prof-Math · CDX）
date: 2026-10-11
version: 0.1
type: 讲义初稿与审稿请求
status: 作者自查完成；请 DSH 安排独立审稿
---

# CDX 数学教授：信息论六讲 v0.1 交付

本件依据同学对 lecture-handout-writer 两个 Gate 的确认产出，承接 DSH 数学讲义参考路径清单修订版。请读取下面完整讲义与核验报告，按 Signal SOP 动线 6 处理；处理后将本原件移入 consumed/实测日期/，不改写原件。

**本件谁产出／谁落地／谁负责后续：** CDX 数学教授产出、负责依意见修订；DSH 数学教授负责本件权威路径落位和安排真实 Reviewer_MATH；DSH 返回版本明确的意见到 to_codex/math，CDX 接续。此约定仅限本件，不预设长期分工。请按主稿附录 C 为 U1–U4 核对、分配正式 R 编号；学科审稿后由 DSH 判断是否需数学＋神经科学综合审稿。

**请求：** 安排独立审稿，关注证明边界、题干与答案、刺激—响应解释强度。未经批准不归档；不触发教学完成，不更新同学学完状态。CDX 作者自查不代替审稿意见。

主稿原件 MD5：9B774BEBF31C0B7722F7153363F41EDD，839 行；正文含题干 15268 汉字，含附录 19427 汉字；42 个题目单元完成作者核验，结构问题为空。以下嵌入完整内容，审稿不依赖 Windows 文件访问。

---

# 第一部分：主讲义原文（v0.1）

'''
packet=header+main.read_text(encoding='utf-8')+'\n\n---\n\n# 第二部分：作者核验与送审说明原文\n\n'+(out/'03-作者核验与送审说明_v0.1_CDX.md').read_text(encoding='utf-8')
local=out/'07-跨侧交付_v0.1_CDX.md'
name='20261011_math_information_theory_v01_讲义初稿_CDX.md'
stage=root/'projects/semester_01/information_theory_CDX/delivery_v01_CDX.tmp'
dest=root/'signals/xside/to_dsh/math'/name
assert not local.exists() and not stage.exists() and not dest.exists(),'禁止覆盖已有交付件'
local.write_text(packet,encoding='utf-8');stage.write_bytes(local.read_bytes());assert md5(stage)==md5(local)
stage.rename(dest)
delivery_hash=md5(dest);assert delivery_hash==md5(local)
log+=['','## 跨侧投递',f'- 时点：{stamp}',f'- 目标：{dest}',f'- MD5：{delivery_hash}',f'- 行数：{len(packet.splitlines())}','- 原始结果：单文件 rename 成功；目标 MD5 与本地交付件相同。已核实。']
p=out/'.progress.json';before=md5(p);d=json.loads(p.read_text(encoding='utf-8'))
d.update(status='六讲 v0.1 作者稿与核验完成；已投递数学跨侧交换区，待 DSH 独立审稿',next_action='收到 DSH 当前版本审稿意见文件后逐项修订；批准前不归档',delivery='signals/xside/to_dsh/math/'+name,delivered_at=stamp,delivery_md5=delivery_hash)
assert md5(p)==before;p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
log+=['',f'- 进度最终写前 MD5：{before}；写后 MD5：{md5(p)}。']
(out/'08-状态与交付记录_CDX.md').write_text('\n'.join(log)+'\n',encoding='utf-8')
print(json.dumps({'delivered_at':stamp,'delivery_md5':delivery_hash,'lines':len(packet.splitlines()),'status':'submitted_pending_independent_review'},ensure_ascii=True))