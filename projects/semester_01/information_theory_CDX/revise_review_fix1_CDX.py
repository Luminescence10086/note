"""Codex 侧数学教授分身（CDX）：按真实审稿意见修订 P1–P3 及 S1。"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import re,json,hashlib,difflib,sys
out=Path(sys.argv[1]);root=Path(sys.argv[2]);stamp=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
def md5(p):return hashlib.md5(p.read_bytes()).hexdigest().upper()
old=out/'02-信息论六讲_v0.1_CDX.md'
canonical=root/'lectures/math/MA404_信息论_有限离散六讲.md'
inbound=root/'signals/xside/to_codex/math/20261011_math_information_theory_review_return_DSH.md'
assert md5(old)=='9B774BEBF31C0B7722F7153363F41EDD'
assert md5(canonical)=='AC0CFCCC4FF93DEB2E74D43F5102574B'
assert md5(inbound)=='DEAA81467C10252DEFA0F01ED923C374'
a=old.read_text(encoding='utf-8');landed=canonical.read_text(encoding='utf-8')
assert a.strip() in landed,'DSH落位正文与CDX版本不一致'
# P1: a visible version bar survives DSH placement prefixes without nested YAML.
assert a.startswith('---\n')
b=a.split('---\n',2)[2].lstrip('\n')
title='# 信息论：从不确定性到信息处理'
bar='> **版本**：v0.1-fix1 ｜ **日期**：2026-10-11 ｜ **作者**：Codex 侧数学教授分身（CDX）\n> **状态**：按首轮审稿意见修订，待 DSH 增量复核；未经批准不归档。'
assert b.count(title)==1
b=b.replace(title,title+'\n\n'+bar,1)
# P2: registered R identifiers replace the stale request for allocation.
old_c2='### C2 明示待证、请 DSH 分配正式 R 编号\n\nU1–U4 是此 CDX 项目的临时标识，不占用权威未证登记表编号。以下“定位”用于核对结论；查到来源不等于读者已完成该证明。'
new_c2='### C2 明示待证：已分配正式编号 R13–R16\n\nDSH 已于 2026-10-11 将 U1–U4 分别登记为正式编号 R13–R16，已核对 `lectures/math/unproven_registry.md`。U1–U4 保留为本册工具别名，与正式编号的对应见下表；四项目前均未证。以下“定位”用于核对结论；查到来源不等于读者已完成该证明。'
assert b.count(old_c2)==1;b=b.replace(old_c2,new_c2)
start=b.index('| 标识 | 使用的结果 |');end=b.index('\n### C3',start)
part=b[start:end]
part=part.replace('| 标识 | 使用的结果 | 本册使用位置 | 证明回补 |','| 本册别名 | 正式编号 | 使用的结果 | 本册使用位置 | 证明回补 | 状态 |').replace('| :--- | :--- | :--- | :--- |','| :--- | :--- | :--- | :--- | :--- | :--- |')
rows=part.splitlines()
for i,line in enumerate(rows):
 m=re.match(r'\| U([1-4]) \|',line)
 if m:
  n=int(m.group(1));rows[i]=line.replace(f'| U{n} |',f'| U{n} | **R{12+n}** |',1)+' ⏳ 未证 |'
b=b[:start]+'\n'.join(rows)+'\n'+b[end:]
# S1: match the first-use tool name to the registry.
for n in range(1,5):
 old_label=f'**待证工具 U{n}：'
 assert b.count(old_label)==1
 b=b.replace(old_label,f'**待证工具 U{n}（登记表 R{12+n}）：',1)
# P3: insert a blank before headings where absent; retain all text.
lines=b.splitlines();new=[];added=[]
for line in lines:
 if re.match(r'^#{1,6} ',line) and new and new[-1].strip():
  new.append('');added.append(line)
 new.append(line)
b='\n'.join(new)+'\n'
assert added==['## 第三讲　观测以后还剩多少不确定性','## 第五讲　信息经过处理会怎样','## 附录 A　引导练习的最小提示'],added
old_note='配套 `03-作者核验与送审说明_v0.1_CDX.md` 与 `04-逐题核验数据_v0.1_CDX.json` 记录题号及依据。'
new_note='v0.1 的 `03-作者核验与送审说明_v0.1_CDX.md` 与 `04-逐题核验数据_v0.1_CDX.json` 保留首版题号及数值核验依据；本次仅作呈现与登记口径修订，增量记录见 `09-首轮审稿修订说明_v0.1-fix1_CDX.md`。'
assert b.count(old_note)==1;b=b.replace(old_note,new_note)
b+='\n修订追加（2026-10-11，CDX，v0.1-fix1）：依首轮审稿报告修复 P1 可见版本栏、P2 正式编号 R13–R16 及映射表、P3 三处标题前空行；采纳 S1 首用编号提示。数学表述、概率表、题目与解答不变；当前等待增量复核。\n'
newpath=out/'02-信息论六讲_v0.1-fix1_CDX.md';assert not newpath.exists()
# Required delta evidence: identical ordered math expressions and all E/G/T text.
math=lambda s:re.findall(r'\$([^$]*)\$',s)
assert math(a)==math(b),'数学表达式发生变化'
core=lambda s:s[s.index('## 第一讲'):s.index('## 附录 C')]
normalize=lambda s:re.sub(r'\n\s*\n','\n',re.sub(r'（登记表 R1[3-6]）','',s)).strip()
assert normalize(core(a))==normalize(core(b)),'题干、解答或正文实质改变'
issues=[]
for n,line in enumerate(b.splitlines(),1):
 if line.count('$')%2:issues.append(f'公式配对 {n}')
 if re.search(r'[\u4e00-\u9fff]\$|\$[\u4e00-\u9fff]',line):issues.append(f'公式间隔 {n}')
 if re.match(r'^#{1,6} ',line) and n>1 and b.splitlines()[n-2].strip():issues.append(f'标题空行 {n}')
assert '$$' not in b
assert not re.search(r'^(title|author|date|version|status|subject):',b,re.M)
assert not re.search(r'请 DSH 分配|不占用权威|临时标识',b)
assert not re.search(r'\\sum(?!_)',b)
assert not re.search(r'\\log(?!_2)',b)
assert not issues,issues
newpath.write_text(b,encoding='utf-8')
changes=list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile=old.name,tofile=newpath.name,lineterm=''))
(out/'10-修订差异_v0.1-fix1_CDX.diff').write_text('\n'.join(changes)+'\n',encoding='utf-8')
checks={'author':'Codex 侧数学教授分身（CDX）','version':'0.1-fix1','checked_at':stamp,'source_md5':md5(old),'reviewed_dsh_md5':md5(canonical),'inbound_md5':md5(inbound),'revised_md5':md5(newpath),'lines':len(b.splitlines()),'bytes':len(newpath.read_bytes()),'all_formula_tokens_identical':True,'core_text_identical_except_S1_and_blank_lines':True,'question_count':len(re.findall(r'\*\*(?:示范 )?([EGT]\d\.\d)',b.split('## 附录 A')[0])),'added_blank_before':added,'issues':issues}
assert checks['question_count']==42
(out/'11-增量核验_v0.1-fix1_CDX.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=True))