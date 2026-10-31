from pathlib import Path
import hashlib,json,itertools,math,re

ROOT=Path(__file__).resolve().parents[4]
D=ROOT/'professors/MATH/handout_MA105_CDX'
checks=[]
def check(name,value):
    assert value,name
    checks.append(name)
def det(a):
    if len(a)==0:return 1
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))
def divisors(a):
    result=[1]
    for k in range(1,min(len(a),len(a[0]))+1):
        minors=[abs(det([[a[i][j] for j in cs] for i in rs])) for rs in itertools.combinations(range(len(a)),k) for cs in itertools.combinations(range(len(a[0])),k)]
        result.append(math.gcd(*minors))
    return result
A=[[4,6,0],[2,8,0],[0,0,12]]
check('E5 determinantal divisors',divisors(A)==[1,2,4,240])
B=[r[:] for r in A]
B[0],B[1]=B[1],B[0]
B[1]=[y-2*x for x,y in zip(B[0],B[1])]
for r in B:r[1]-=4*r[0]
B[1]=[-v for v in B[1]]
check('first diagonal operations',B==[[2,0,0],[0,10,0],[0,0,12]])
B[1]=[x+y for x,y in zip(B[1],B[2])]
for r in B:r[2]-=r[1]
for r in B:r[1],r[2]=r[2],r[1]
B[2]=[y-6*x for x,y in zip(B[1],B[2])]
for r in B:r[2]-=5*r[1]
B[2]=[-x for x in B[2]]
check('second diagonal operations',B==[[2,0,0],[0,2,0],[0,0,60]])
check('rectangular minors',divisors([[2,4,6],[0,6,12]])==[1,2,12])
check('T2 minors',divisors([[4,0,0],[0,6,0],[0,0,9]])==[1,1,6,216])
for total,rows in [(360,[(360,),(3,120),(2,180),(6,60),(2,2,90),(2,6,30)]),(72,[(72,),(3,24),(2,36),(6,12),(2,2,18),(2,6,6)])]:
    check(f'{total} group orders and chain',len(set(rows))==6 and all(math.prod(r)==total and all(b%a==0 for a,b in zip(r,r[1:])) for r in rows))
check('torsion counts',[sum((j*a)%4==0 and (j*b)%8==0 for a in range(4) for b in range(8)) for j in (2,4)]==[4,16])
check('Jordan kernels',[sum(min(j,e) for e in [2,3]) for j in [1,2,3]]==[2,4,5])
check('nilpotent kernels',[sum(min(j,e) for e in [2,4]) for j in [1,2,3,4]]==[2,4,5,6])

names=['MA105_模论与结构定理_第01至02讲_CDX.md','MA105_模论与结构定理_第03至04讲_CDX.md','MA105_第05讲_Smith标准形_CDX.md','MA105_第06至08讲_三个应用_CDX.md']
sources={n:(D/n).read_text(encoding='utf8') for n in names}
first=sources[names[0]]
first_body=first[first.index('## 第一讲'):first.index('## 附录 A')]
first_answers=first[first.index('## 附录 A'):]
third=sources[names[1]];third=third[third.index('## 第三讲'):]
def promote(text):
    text=re.sub(r'^---\n.*?\n---\n','',text,flags=re.S).strip()
    return re.sub(r'^(#+) ',r'#\1 ',text,flags=re.M)
body='\n\n'.join([first_body,third,promote(sources[names[2]]),promote(sources[names[3]])])
# Historical component files remain untouched; reading order is prospective in the bound edition.
body=body.replace('第5讲待写，未作输入使用','第5讲证明，阅读至此尚未作输入使用').replace('存在性仍留给第5讲','存在性在第5讲完成').replace('存在性仍待第第5讲','存在性在第5讲')
intro='''---
title: MA105 模论与结构定理（八讲合订作者稿）
author: Codex 数学教授 CDX
date: 2026-10-31
version: 0.2-author-draft
status: 八讲正文及题解齐备，待独立审稿，不表示学生已学完
---

# MA105 模论与结构定理

本合订本沿2026-10-12八讲设计及用户2026-10-30/31写作授权完成。阅读顺序：模语言→自由模与关系→结构定理目标→子模与唯一性→Smith存在性→算子分类→阿贝尔群→零化理想与Cayley–Hamilton。各讲习题的提示与答案集中于后部；教学验收需实际作答。

前置：有限维线性代数及PID的环论基础（Bézout、素元、因子分解）；前置要求不代表用户已掌握。一般PID上的算法在理论上有限终止，实际计算还需有效的环运算接口。交换代数、同调代数为后续方向，不冒充本课程已完成。

历史分篇保留作为来源；本件是统一阅读入口。早期章节的“后证”描述阅读依赖，其对应证明已在后文。作者计算核验不是一般数学证明，也不等于DSH独立审稿。
'''
answers=[first_answers]+[promote((D/n).read_text(encoding='utf8')) for n in ['第03至04讲_答案与核验.md','第05讲_答案与核验.md','第06至08讲_答案与全课自测.md']]
bound=intro+'\n'+body+'\n\n# 分离答案与全课自测\n\n'+'\n\n'.join(answers)+'\n'
bound=bound.replace('零因子项','值为零的参数项')
from enrich_bound import enrich
bound=enrich(bound)
target=D/'MA105_模论与结构定理_八讲合订作者稿_CDX.md'
before_bound=target.read_bytes() if target.exists() else None
assert (target.read_bytes() if target.exists() else None)==before_bound
target.write_text(bound,encoding='utf8',newline='\n')
for p in D.glob('*.md'):
    b=p.read_bytes();s=b.decode('utf8')
    check('format '+p.name,not b.startswith(b'\xef\xbb\xbf') and b'\r' not in b and '$$' not in s and all(l.count('$')%2==0 for l in s.splitlines()))
check('eight chapter headings',all('## '+h+'讲' in bound for h in ['第一','第二','第三','第四','第五','第六','第七','第八']))
p=D/'.progress.json';before=p.read_bytes();d=json.loads(before)
d.update(chapters_written=list(range(1,9)),chapters_drafted=list(range(1,9)),chapters_complete=list(range(1,9)),chapters_pending=[],updated='2026-10-31',phase=4,canonical_author_draft=target.name,review_status='author_checked_pending_independent_review',proof_boundary='PID结构定理存在唯一及三应用作者证明齐备，等待独立复核',completion_requirements_pending=['独立审阅与修订','依据真实审批结果归档'],verification='projects/semester_01/handout_completion_20261031/ma105/verification.json')
assert p.read_bytes()==before;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
report={'date':'2026-10-31','checks':checks,'status':'PASS','bound_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'proof_scope':'Computations verify examples only; general arguments are in prose; independent review pending.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'status':'PASS','checks':len(checks),'bound_bytes':target.stat().st_size},ensure_ascii=False))
