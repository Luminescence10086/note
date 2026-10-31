from pathlib import Path
import re,hashlib,json
base=Path('professors/MATH/handout_MA106_CDX')
before={}
# Assemble from revised sources, strip previous-stage meta statements only in current reading edition.
names=['MA106_有限群表示论_讲1-2.md','MA106_有限群表示论_讲3-4.md']+[f'第{i:02}讲.md' for i in range(5,13)]
merged='# MA106 有限群表示论：12讲合订修订作者稿\n\n2026-10-31，修订v0.2。真实DSH初审结论为需修改；本稿按意见修订，等待增量复核，尚未批准归档。学生学习状态未评估。\n\n'
for name in names:
 s=(base/name).read_text(encoding='utf8');s=re.sub(r'\A---\s*\n.*?\n---\s*\n','',s,flags=re.S)
 s=s.replace('> 本版为 CDX 侧新编，未经 DSH 独立审稿；仅第1–2讲，第3–12讲待写。','')
 s=s.replace('本续篇接第1—2讲；全课共12讲，目前写至第4讲，第5—12讲待写。正文完成不代表学生学完。','本节承接第1—2讲。正文完成不代表学生学完。')
 merged+=s+'\n\n'
merged+=(base/'附录A_记号与未证输入.md').read_text(encoding='utf8')+'\n\n'
notes=[]
for name,marker in [('答案与自校.md','# 作者逐项核查'),('讲3-4_答案与自校.md','## 本次自校范围与假设'),('第05至12讲_答案与核验.md','## 作者总自校边界')]:
 s=(base/name).read_text(encoding='utf8'); body,sep,note=s.partition(marker)
 body=body.replace('日期：2026-10-30；本件是作者自校，不是独立审稿。','').replace('2026-10-31，CDX作者自校，未经DSH独立审稿。','').replace('2026-10-31。作者核验，不是独立审稿。','')
 merged+=body+'\n\n'
 if sep:notes.append('### '+name+'\n\n'+note.replace('第5—12讲待写。','第5—12讲现已补齐；原记录为当时阶段状态。'))
merged+='# 作者自校记录（非审稿，不构成通过依据）\n\n'+'\n\n'.join(notes)
(base/'MA106_有限群表示论_12讲合订作者稿.md').write_text(merged,encoding='utf8',newline='\n')
p=base/'.progress.json';j=json.loads(p.read_text(encoding='utf8'));j['review_status']='DSH_initial_changes_requested_revision_v0.2_pending_recheck';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
Path(__file__).with_name('revision_source_hashes.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(hashlib.sha256((base/'MA106_有限群表示论_12讲合订作者稿.md').read_bytes()).hexdigest())
