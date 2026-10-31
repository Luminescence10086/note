from pathlib import Path
import re,hashlib,json
base=Path('professors/MATH/handout_MA106_CDX')
report=Path('lectures/math/review_reports/review_20261031_MA105_MA106_full_DSH.md')
assert hashlib.sha256(report.read_bytes()).hexdigest()=='d13b8f3361082866befdda297f8c462ec6d7cfb95ece24048e90ccb8de9ce71c'
before={}
def edit(name,pairs):
 p=base/name;s=p.read_text(encoding='utf8');before[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 for a,b in pairs:
  if b in s: continue
  assert a in s,(name,a)
  s=s.replace(a,b)
 p.write_text(s,encoding='utf8',newline='\n')
edit('MA106_有限群表示论_讲1-2.md',[
('## 结构图景与学习目标','## 0 结构图景与学习目标'),('## 结构图景\n','## 0 结构图景\n'),
('则可以选 $v=ae_1+be_2$ 且 $b\\ne0$。','取非零生成向量 $v=ae_1+be_2$。补空间要求 $L\\cap U=0$；若 $b=0$，则 $v\\in U$，与非零向量同时属于二者矛盾。因此 $b\\ne0$。'),
('故没有稳定补空间，表示不完全可约。','故没有稳定补空间。更直接地，上述坐标比较说明任何稳定直线都只能是 $U$；本表示本身可约，若完全可约则在二维中必须分为两条不同的稳定直线，这不可能。因此表示不完全可约。这里是二维 Jordan 型表示，不能在一般 $p$ 下称为维数为 $p$ 的正则表示。'),
('有限维内积空间的正交分解给出','有限维内积空间的正交分解（已证前置：第四课《内积空间》§4 定理2；复数情形也可直接按正交规范基构造 $v-\\sum_{i=1}^{m}\\langle v,u_i\\rangle u_i$ 验证其与 $U$ 正交）给出'),
('延伸 $U$ 的一组基为 $V$ 的基','由第二课《线性映射与秩-零化度定理》§4.1 引理2（基扩张），延伸 $U$ 的一组基为 $V$ 的基')])
edit('MA106_有限群表示论_讲3-4.md',[
('代数闭性保证有根 $\\lambda\\in k$。','代数闭性保证有根 $\\lambda\\in k$。当本课取 $k=\\mathbb C$ 时，所用代数闭性来自未证输入 R6：代数基本定理，见 `lectures/math/unproven_registry.md`；本课不证明或销号 R6。'),
('若它非零，上一节 Schur 引理迫使它可逆，与非零核矛盾。','若它非零，上一节 Schur 引理迫使它为同构，故核应为零；但特征值的定义给出非零核，即它非单射，矛盾。'),
('\\sum_i v_ie_i','\\sum_{i=1}^{n} v_ie_i'),('\\sum_jw_jf_j','\\sum_{j=1}^{m}w_jf_j')])
edit('第05讲.md',[(r'\sum_i m_i^2',r'\sum_{i=1}^{r} m_i^2'),('若 $V=\\bigoplus_iU_i^{\\oplus m_i}$','若 $V=\\bigoplus_{i=1}^{r}U_i^{\\oplus m_i}$')])
edit('第07讲.md',[(r'\sum_j n_j',r'\sum_{j=1}^{c} n_j'),('已知表示 $V$ 的特征标后','设共轭类共 $c$ 个。已知表示 $V$ 的特征标后')])
edit('第08讲.md',[('多项式 $x^m-1$ 在复数上无重根','由未证输入 R6（代数基本定理；登记状态未证）知 $x^m-1$ 在复数上分裂。多项式 $x^m-1$ 在复数上无重根')])
edit('第09讲.md',[('从换位子群诱导其非平凡一维表示','从子群 $\\langle(12)\\rangle\\cong C_2$ 诱导其非平凡一维表示（符号表示）')])
edit('第10讲.md',[('为复查共轭方向，可代诱导公式：左边为','为复查共轭方向，先把诱导公式代入内积，左边为\n\n$\\frac1{|G||H|}\\sum_{g\\in G}\\sum_{\\substack{x\\in G\\x^{-1}gx\\in H}}\\overline{\\psi(x^{-1}gx)}\\chi_V(g)$。\n\n这是有限求和，可以交换先后顺序。固定 $x$ 后，映射 $h\\mapsto g=xhx^{-1}$ 是 $H$ 到满足 $x^{-1}gx\\in H$ 的那些 $g$ 的双射；逆映射就是 $g\\mapsto x^{-1}gx$。因此内层可逐项换元为同一个 $h$，得到')])
# correct substack row separator in new formula
p=base/'第10讲.md';s=p.read_text(encoding='utf8');s=s.replace(r'x\in G\x^{-1}',r'x\in G\\x^{-1}');p.write_text(s,encoding='utf8',newline='\n')
edit('第11讲.md',[('只须把列改为 $1,-1,\\pm i,\\pm j,\\pm k$。','列对应依次为 $1\\leftrightarrow1$、$r^2\\leftrightarrow-1$、$\\{r,r^3\\}\\leftrightarrow\\{\\pm i\\}$、$\\{s,r^2s\\}\\leftrightarrow\\{\\pm j\\}$、$\\{rs,r^3s\\}\\leftrightarrow\\{\\pm k\\}$。一维行标签对应 $(a,b)=(1,1),(1,-1),(-1,1),(-1,-1)$ 与 $++,+-,-+,--$；二维行对应 $E,U$。这仅是表格数据对应，不是群同构。')])
edit('第12讲.md',[(r'\sum_i n_im_i',r'\sum_{i=1}^{r} n_im_i'),('其中 $U_i$ 不同构复不可约','其中 $i=1,\\ldots,r$，$U_i$ 不同构复不可约'),('以符号表示 $g:x\\mapsto-x$ 为例','以符号表示 $g:x\\mapsto-x$（即 $gv=-v$）为例')])
edit('讲3-4_答案与自校.md',[('代数基本定理用于复数代数闭这一已知背景，不在本课重证。','复数代数闭依赖代数基本定理（未证，登记 R6），本课未证明或销号。')])
(base/'附录A_记号与未证输入.md').write_text('''# 附录A 记号与输入边界

| 记号 | 含义与条件 |
|---|---|
| $\\rho_V:G\\to GL(V)$ | 有限群在有限维复空间上的表示，另标任意域时以局部条件为准 |
| $\\mathbb C[G]$ | 群代数，群元素是形式基 |
| $\\chi_V(g)$ | $\\operatorname{tr}\\rho_V(g)$ |
| $\\operatorname{Ind}_H^G W$ | 从子群诱导，维数为指数乘原维数 |
| $\\operatorname{Res}_H^G V$ | 限制到子群，维数不变 |
| $\\langle v,w\\rangle$，讲2向量内积 | 第一变量线性，第二变量共轭线性 |
| $\\langle f,h\\rangle_G$，讲5起类函数内积 | 第一变量共轭线性，第二变量线性；群平均归一化 |
| $\\widehat f(\\chi)$ | 有限阿贝尔群 Fourier 系数，等于类函数内积 $\\langle\\chi,f\\rangle$ |
| $C_G(g)$ | 元素的中心化子，不是共轭类 |

## 未证输入与已证前置小表

| 输入 | 使用处 | 真实状态与来源 |
|---|---|---|
| R6 代数基本定理 | 讲3复数Schur标量结论、讲8有限阶算子的复特征基 | `lectures/math/unproven_registry.md` R6仍未证；只引用不销号 |
| 基扩张 | 讲2任意线性投影 | `lectures/math/approved/02_线性映射与秩-零化度定理.md` §4.1 引理2 |
| 正交基扩充、正交分解 | 讲2平均内积后的稳定补空间 | `lectures/math/approved/04_内积空间.md` §3.3、§4 定理2；复数投影计算在讲2补写 |
| 一般有限维张量积 | 讲4、8 | 本课用基直接构造并验证，不把范畴论普遍性质作为输入 |
| Frobenius–Schur指标、Mackey公式 | 后续方向 | 本课不调用，未宣称证明 |

已证前置不等于学生已通过验收。上述输入表不修改任何共享登记状态。升级对照总表见第12讲§6。
''',encoding='utf8',newline='\n')
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
