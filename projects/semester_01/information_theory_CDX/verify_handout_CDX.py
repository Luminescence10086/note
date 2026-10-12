"""Codex 侧数学教授分身（CDX）：v0.1 作者核验，不代替独立审稿。"""
from fractions import Fraction as F
from math import log2, isclose
from pathlib import Path
import json, re, sys
OUT=Path(sys.argv[1]); records=[]
def H(p):
 assert all(x>=0 for x in p) and sum(p)==1
 return -sum(float(x)*log2(float(x)) for x in p if x)
def h(q): return H([F(q),1-F(q)])
def close(a,b): assert isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)
def L(rows):
 a=[[F(v) for v in row] for row in rows]; nr=len(a); nc=len(a[0])
 assert all(len(row)==nc for row in a) and all(v>=0 for row in a for v in row) and sum(map(sum,a))==1
 px=[sum(row) for row in a]; py=[sum(a[i][j] for i in range(nr)) for j in range(nc)]
 hx,hy,hxy=H(px),H(py),H([v for row in a for v in row])
 hx_y=sum(float(py[j])*H([a[i][j]/py[j] for i in range(nr)]) for j in range(nc) if py[j])
 hy_x=sum(float(px[i])*H([a[i][j]/px[i] for j in range(nc)]) for i in range(nr) if px[i])
 ir=sum(float(a[i][j])*log2(float(a[i][j]/(px[i]*py[j]))) for i in range(nr) for j in range(nc) if a[i][j])
 close(hx+hy_x,hxy);close(hy+hx_y,hxy);close(ir,hx-hx_y);close(ir,hy-hy_x)
 return dict(px=list(map(str,px)),py=list(map(str,py)),HX=hx,HY=hy,HXY=hxy,HX_Y=hx_y,HY_X=hy_x,I=ir)
def R(qid,evidence,values=None,kind='数值复算'):
 records.append(dict(id=qid,kind=kind,status='通过',evidence=evidence,values=values or {}))
def J(q,w): return [[p*F(v) for v in row] for p,row in zip([1-F(q),F(q)],w)]
A=[[F(3,8),F(1,8)],[F(1,8),F(3,8)]]
B=[[F(4,5),F(1,10)],[0,F(1,10)]]
C=[[F(1,2),F(1,4)],[F(1,8),F(1,8)]]
D=[[F(3,8),0,F(1,8)],[0,F(3,8),F(1,8)]]
a,b,c,d=map(L,[A,B,C,D])
assert A[0][0]/F(1,2)==F(3,4) and A[0][0]!=F(1,4)
R('E1.1','边缘各半；指定两向条件3/4、1/4；不满足独立分解',a)
close(float(A[0][1]+A[1][0]),.25);R('E1.2','误判格相加，期望1/4',{'loss':.25})
assert C[0][1]/F(3,8)==F(2,3);R('G1.1','第二列条件2/3、1/3',c)
g12=L([[F(1,8),F(1,8)],[F(3,8),F(3,8)]]);close(g12['I'],0)
R('G1.2','边缘乘积表；期望3/4',g12)
assert F(1,2)+3*F(1,4)==F(5,4)
R('T1.1','原表总和5/4；乘4/5修复',L([[F(2,5),F(1,5)],[F(1,5),F(1,5)]]))
t12=L([[F(1,2),0],[F(1,2),0]]);close(t12['I'],0)
R('T1.2','仅第一列条件有定义；常量独立',t12)
ind=L([[F(1,4)]*2]*2);ident=L([[F(1,2),0],[0,F(1,2)]])
close(ind['I'],0);close(ident['I'],1)
R('T1.3','均匀四格与均匀对角表',{'independent':ind,'recoverable':ident})
close(H([F(1,2),F(1,4),F(1,4)]),1.5);R('E2.1','自信息1、2、2；熵1.5',{'H':1.5})
R('E2.2','自信息按真实概率加权',{'common':-log2(.9),'rare':-log2(.1),'H':h(F(1,10))})
close(-log2(1/32),-log2(1/4)-log2(1/8));R('G2.1','自信息5=2+3',{'joint_information':5})
close(H([F(1,2),F(1,4),F(1,4),0]),1.5)
R('G2.2','零项不贡献；两种计数上界',{'H':1.5,'bound_alphabet':2,'bound_support':log2(3)})
close(H([F(1,8)]*8),3);R('T2.1','八个自信息均3',{'H':3})
assert h(F(1,4))<1 and -log2(.25)>-log2(.5)
R('T2.2','平均熵较小，罕见单次自信息较大',{'skew_H':h(F(1,4)),'uniform_H':1,'rare_information':2})
assert F(1,2)*0+F(1,2)*2==F(3,4)*0+F(1,4)*4==1
R('T2.3','{0,2}各半与{0,4}概率3/4、1/4，均值同为1',{'first_H':1,'second_H':h(F(1,4))})
close(a['HXY'],1+h(F(1,4)));R('E3.1','逐格联合熵与两向条件熵链核对',a)
assert b['HX']<1 and b['HX_Y']<b['HX'];close(b['HX_Y'],.2)
R('E3.2','b列条件熵1；外权重1/5；平均0.2',b)
R('G3.1','独立2×4均匀模型',L([[F(1,8)]*4]*2));R('G3.2','联合熵减Y熵为0.2',b)
t31=L([[F(1,2),0],[0,F(1,4)],[0,F(1,4)]]);close(t31['HX_Y'],.5);close(t31['HY_X'],0)
R('T3.1','函数分组两方向条件熵不同',t31)
R('T3.2','作者逐步检查两向证明：正权重非负和为零⇒每个条件熵为零⇒唯一取值；反向代入。例子核对不可逆',t31,'证明自查＋例子复算')
t33=L([[F(3,5),F(1,5)],[0,F(1,5)]]);assert t33['HX']<1 and t33['HX_Y']<t33['HX'];close(t33['HX_Y'],.4)
R('T3.3','新表条件熵1、平均0.4、原熵h(1/5)',t33)
close(a['I'],.75*log2(1.5)-.25);R('E4.1','概率比和与熵差双路线',a)
e42=L([[0,F(1,4)],[F(1,2),0],[0,F(1,4)]]);close(e42['I'],1);close(e42['HX_Y'],.5)
R('E4.2','平方模型保留1 bit，剩余0.5 bit',e42)
R('G4.1','四格比均1，互信息0',ind);R('G4.2','互信息1，小于HX=1.5',t31);R('T4.1','两种熵差复算',b)
R('T4.2','作者逐步检查：熵差定义与恢复判据给出等价；取目标Y、观测X于T3.1反驳双向全部恢复',t31,'证明自查＋反例复算')
assert all(v>0 for row in A for v in row)
R('T4.3','均匀独立表与A均全正、均匀边缘',{'first':ind,'second':a})
e51=L([[F(1,4),F(1,4),0,0],[0,0,F(1,4),F(1,4)]]);close(e51['HY'],2);close(e51['I'],1)
R('E5.1','两种投影同减1 bit响应熵，目标信息不同',{'original':e51,'keep_target':ident,'keep_nuisance':ind})
e52=L([[F(5,16),F(3,16)],[F(3,16),F(5,16)]])
assert F(1,4)*F(3,4)+F(3,4)*F(1,4)==F(3,8) and e52['I']<a['I']
R('E5.2','有效翻转率3/8',e52)
g51=L([list(reversed(row)) for row in A]);close(g51['I'],a['I']);R('G5.1','列交换保持互信息',g51)
g52=L([[F(1,2)],[F(1,2)]]);close(g52['I'],0);R('G5.2','常量输出',g52)
composed=[[sum(A[i][j]*F(1,2) for j in range(2)) for k in range(2)] for i in range(2)]
assert composed==[[F(1,4)]*2]*2;R('T5.1','半概率翻转后独立',L(composed))
R('T5.2','原I=0，新I=1；同一个Y下输出条件随X改变，无法由单行W表达',{'before':g52,'after':ident},'条件自查＋数值复算')
t53rows=[[F(3,16),F(3,16),F(1,8)],[F(1,16),F(1,16),F(3,8)]]
t53=L(t53rows); t53merge=L([[row[0]+row[1],row[2]] for row in t53rows])
close(t53['I'],t53merge['I']);assert t53['HY']>t53merge['HY']
R('T5.3','六格全正；a、b后验相同；合并后A',{'before':t53,'after':t53merge})
R('E6.1','一般代数I=h(q)；U1上界由均匀输入达到',ident,'代数自查＋达到上界复算')
dmerge=L([[F(1,2),0],[F(1,8),F(3,8)]]);close(d['I'],.75);close(dmerge['HX_Y'],F(5,8)*h(F(1,5)))
R('E6.2','擦除模型、合并模型完整账本',{'before':d,'after':dmerge,'loss':d['I']-dmerge['I']})
g61=L([[F(3,4),0],[0,F(1,4)]]);close(g61['I'],h(F(1,4)));R('G6.1','偏斜输入低于容量1',g61)
emp=L([[F(3,8),F(1,8)],[F(1,8),F(3,8)]]);emp10=L([[F(30,80),F(10,80)],[F(10,80),F(30,80)]]);close(emp['I'],emp10['I'])
R('G6.2','计数比例相同；不推出真值',emp)
t61=L(J(F(1,4),[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]));assert t61['I']<a['I']
R('T6.1','固定信道输出1概率3/8；均匀候选更好',{'biased':t61,'uniform':a})
t62=L([[F(1,4),0,F(1,4)],[0,F(1,4),F(1,4)]]);t62merge=L([[F(1,2),0],[F(1,4),F(1,4)]])
close(t62['I'],.5);close(t62merge['I'],h(F(1,4))-.5)
R('T6.2','六项熵账本及合并双路线',{'before':t62,'after':t62merge,'loss':t62['I']-t62merge['I']})
for q in [F(0),F(1,4),F(1,2),F(1)]:
 for e in [F(0),F(1,4),F(1,2),F(1)]:
  close(L(J(q,[[1-e,0,e],[0,1-e,e]]))['I'],float(1-e)*h(q))
R('T6.3','作者一般代数检查：擦除后验等于先验，I=(1-e)h(q)；U1均匀达到容量；16组含端点复算',{'q':.25,'epsilon':.5,'I':.5*h(F(1,4)),'capacity':.5},'代数自查＋16组复算')
assert len(records)==42 and len({r['id'] for r in records})==42
text=(OUT/'02-信息论六讲_v0.1_CDX.md').read_text(encoding='utf-8');body=text.split('## 附录 A')[0]
summary={'author':'Codex 侧数学教授分身（CDX）','version':'0.1','date':'2026-10-11','passed_question_records':len(records),'precision':'Fraction exact probabilities; entropy crosschecks abs_tol=1e-10','scope':'作者核验，不是独立审稿；数值核对不证明一般定理','main_han_count_including_questions':len(re.findall(r'[\u4e00-\u9fff]',body)),'records':records}
(OUT/'04-逐题核验数据_v0.1_CDX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'questions':42,'han_count':summary['main_han_count_including_questions'],'B':b,'C':c,'D':d,'Dmerge':dmerge,'T53':t53,'T61':t61,'T62':t62,'T62merge':t62merge},ensure_ascii=False,indent=2))