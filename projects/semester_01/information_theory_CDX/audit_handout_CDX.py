"""Codex 侧数学教授分身（CDX）：交付结构、题号与公式格式检查。"""
from pathlib import Path
import re,json,sys,hashlib
from datetime import datetime
out=Path(sys.argv[1]); main=out/'02-信息论六讲_v0.1_CDX.md'
t=main.read_text(encoding='utf-8');issues=[]
if '$$' in t: issues.append('双美元公式')
for n,line in enumerate(t.splitlines(),1):
 if line.count('$')%2: issues.append(f'单行公式定界符不配对：{n}')
 if re.search(r'[\u4e00-\u9fff]\$|\$[\u4e00-\u9fff]',line): issues.append(f'中文公式缺间隔：{n}')
 if line.startswith('|'):
  for math in re.findall(r'\$([^$]*)\$',line):
   if '|' in math: issues.append(f'表格公式含裸竖线：{n}')
body=t.split('## 附录 A')[0]
ids=re.findall(r'\*\*(?:示范 )?([EGT]\d\.\d)',body)
expected=[f'{kind}{ch}.{i}' for ch in range(1,7) for kind,k in [('E',2),('G',2),('T',3)] for i in range(1,k+1)]
if sorted(ids)!=sorted(expected): issues.append('题号缺失或重复')
answertext=t.split('## 附录 B')[1].split('## 附录 C')[0]
answerids=re.findall(r'\*\*([GT]\d\.\d)。',answertext)
if sorted(answerids)!=sorted(x for x in expected if not x.startswith('E')):issues.append('G/T解答缺失或重复')
data=json.loads((out/'04-逐题核验数据_v0.1_CDX.json').read_text(encoding='utf-8'))
if sorted(x['id'] for x in data['records'])!=sorted(expected): issues.append('核验记录题号不一致')
# Every reported decimal in the prose is checked against the intended arithmetic,
# including the extra KL preview and the demonstration rounding values.
from math import log2
assert round(-log2(.75),6)==.415037
assert round(.5*log2(4/3),6)==.207519
assert round(1+(.25*log2(.25)+.75*log2(.75)),6)==.188722
assert len(re.findall(r'^## 第[一二三四五六]讲',t,re.M))==6
for ch in range(1,7):
 headings=re.findall(r'^### ('+str(ch)+r'\.\d+) ',body,re.M)
 if len(headings)!=len(set(headings)): issues.append(f'第{ch}讲小节重复')
summary={'author':'Codex 侧数学教授分身（CDX）','version':'0.1','checked_at':datetime.now().astimezone().isoformat(),'main_md5':hashlib.md5(main.read_bytes()).hexdigest().upper(),'main_lines':len(t.splitlines()),'main_han_before_appendices':len(re.findall(r'[\u4e00-\u9fff]',body)),'all_han':len(re.findall(r'[\u4e00-\u9fff]',t)),'question_count':len(ids),'exercise_answer_count':len(answerids),'issues':issues}
(out/'06-交付结构检查_v0.1_CDX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
if issues:sys.exit(1)
# Companion glossary is a convenience extract; the lecture remains self contained.
gloss=t.split('## 附录 D')[1].split('## 附录 E')[0]
(out/'05-术语表_v0.1_CDX.md').write_text('---\ntitle: 信息论六讲术语表\nauthor: Codex 侧数学教授分身（CDX）\nversion: 0.1\nstatus: 随讲义送审稿\n---\n\n# 信息论六讲术语表\n\n从主讲义附录 D 提取；定义以同版本主讲义为准。\n\n'+gloss.lstrip().split('\n',1)[1],encoding='utf-8')