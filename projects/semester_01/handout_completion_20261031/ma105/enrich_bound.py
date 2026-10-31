import re

def enrich(bound):
    names=['第一','第二','第三','第四','第五','第六','第七','第八']
    chains=[['改变标量环','模与子模','商模与同态','直和与算子例子'],['生成组给满射','关系给核','自由性要求核为零','有限秩与无挠边界'],['不变因子整除链','CRT拆素元幂','规范列表唯一性目标','存在性待Smith闭合'],['第一坐标像理想','子模自由的归纳','清分母与挠自由分离','层商恢复唯一性'],['关系矩阵','Bezout改善主元','理想升链保证终止','Smith整除链与分类'],['算子定义多项式作用','循环模与伴随矩阵','互素分拆','Jordan块与有理标准形'],['阿贝尔群是整数模','自由部分与有限挠部分','素数幂分拆','规范列表完整分类'],['向量零化理想','最小多项式','循环块行列式','Cayley-Hamilton与结构判据']]
    for name,nodes in zip(names,chains):
        pat=r'(^## '+name+r'讲[^\n]*\n)'
        diagram='\n```mermaid\ngraph LR\n'+'\n'.join(f' N{i}["{a}"] --> N{i+1}["{b}"]' for i,(a,b) in enumerate(zip(nodes,nodes[1:])))+'\n```\n'
        bound,n=re.subn(pat,lambda m:m.group(0)+diagram,bound,count=1,flags=re.M);assert n==1
    # Stable unified exercise identifiers in the reading edition; original components retain provenance.
    ids={'G1':'G1.1','G2':'G2.1','G5':'G5.1','G6':'G6.1','G7':'G7.1','G8':'G8.1','I1':'I1.1','I2':'I1.2','I3':'I2.1','I4':'I2.2','I5':'I2.3'}
    for k in range(5,9):
        for j,a in enumerate('abc',1):ids[f'I{k}{a}']=f'I{k}.{j}'
    bound=re.sub(r'\b(?:G\d+|I\d+[abc]?)(?![\d.a-z])',lambda m:ids.get(m.group(),m.group()),bound)
    bound=bound.replace('## 附录 A 提示、解答与作者核验','## 第1—2讲题解').replace('## 第3–4讲：分离提示、答案与自校','## 第3—4讲题解').replace('## 第5讲分离答案与作者核验','## 第5讲题解').replace('## 第6–8讲分离答案、全课自测与核验','## 第6—8讲题解').replace('# 分离答案与全课自测','# 附录 B 按讲次排列的提示与答案')
    bound=bound.replace('T3.3（结构桥梁）','T3.3（结构类比题）')
    # Extract the questions from the solution appendix into the end-of-course reading section.
    start=bound.index('### 全课T1–T3自测（九题）')
    end=bound.index('### 自测参考解与逐项核验',start)
    questions=bound[start:end]
    bound=bound[:start]+bound[end:]
    appendix=r"""
# 附录 A 记号、前置与升级对照

| 记号 | 含义及适用条件 |
|---|---|
| $R$、$K$ | $R$ 是含幺环；结构定理中限定PID；$K$ 为底域或明示的分式域 |
| $R^r$ | 有限秩自由模；$r=0$ 时是零模 |
| $R/(a)$ | 商去主理想 $(a)$；$a$ 为单位时是零模，$a=0$ 时是自由模 $R$ |
| $M_{\rm tor}$ | 整环上被某个非零标量消去的元素组成的挠子模 |
| $\operatorname{Ann}_R(M)$ | 消去整个 $M$ 的标量理想；零模的零化理想为 $R$ |
| $d_1\mid\cdots\mid d_s$ | 按整除链排列的不变因子；模分类删去单位块，矩阵Smith形保留 |
| $p^{j-1}T/p^jT$ | 剩余域 $R/(p)$ 上的层商；维数差分恢复块长 |
| $V_T$ | 定义 $xv=Tv$ 后的 $K[x]$-模 |
| $m_T,\chi_T$ | 首一最小多项式、特征多项式；零维时均取1 |
| $C(a),J_e(\lambda)$ | 首一多项式伴随矩阵、超对角线为1的Jordan块 |

| 高代现象 | 本课统一机制 | 条件与依据 |
|---|---|---|
| 对两个基分别改变矩阵 | 左右等价与关系矩阵 | 第5讲Smith不变量 |
| 同一算子更换基 | $K[x]$-模同构与相似 | 第1讲同态条件、第6讲 |
| Jordan链长 | 素元 $(x-\lambda)$ 的幂次 | 第6讲，须多项式在底域分裂 |
| 有理标准形 | 循环商 $K[x]/(a)$ | 任意底域，第6讲 |
| 有限阿贝尔群 | 整数PID上的挠模 | 第7讲 |
| 最小多项式整除特征多项式 | 最大不变因子整除全部因子之积 | 第8讲，不借C-H先证挠性 |

**前置与未证输入边界。** 这里只记录作者稿的证明依赖，不变更学生状态或公共登记表。

| 输入 | 本册处理 | 定位 |
|---|---|---|
| PID的Bézout、素因子分解、分式域与有限维线性代数 | 明示环论/高代前置；不暗示用户已掌握 | 第3—5讲 |
| PID中 $R/(p)$ 为域 | 已就地用Bézout证明，不新增未证号 | 第4.4节 |
| PID理想升链条件、交换环上的Cauchy–Binet | 已给证明，不作为未证黑箱 | 第5.2、5.5节 |
| 复数代数闭性 | 若把第6讲结论推广到所有复矩阵，要用代数基本定理（未证，登记 R6） | 第6讲；本册具体数值例已显式分解，不需用R6找根 |
| 交换代数、一般局部化、Ext/Tor、代数几何 | 只列后续方向，未陈述或调用其一般定理 | 本册不覆盖 |

**资料压缩与结构信息。** 用少量不变因子描述同构类型，是保留特定等价关系下的全部分类信息；它不一定减少某个数值算法的存储或运行时间。例如两个矩阵特征多项式相同仍可能不同构，因此这种较短摘要可能丢失块长；完整不变因子列表才是本课程的充分分类数据。
"""
    marker='# 附录 B 按讲次排列的提示与答案'
    bound=bound.replace(marker,'# 全课分层自测\n\n'+questions.replace('### 全课T1–T3自测（九题）','九题请先独立作答，再看附录B。')+appendix+'\n'+marker)
    # Reader can locate each tier at the relevant lecture without revealing answers.
    links={1:'T1.2',2:'T1.1',3:'T1.3',4:'T2.1、T3.2',5:'T2.2、T3.1',6:'T2.3',7:'G7.1、I7.1、I7.2',8:'T3.3'}
    for k in range(1,9):
        nextmarker=('## '+names[k]+'讲') if k<8 else '# 全课分层自测'
        pos=bound.index(nextmarker)
        bound=bound[:pos]+f'本讲自测入口：{links[k]}，题面见本讲练习或全课分层自测，答案统一在附录B。\n\n'+bound[pos:]
    # The problem set and answer set must agree exactly.
    main,answers=bound.split(marker,1)
    pattern=r'\b[GI]\d+\.\d+'
    q=set(re.findall(pattern,main));a=set(re.findall(pattern,answers))
    assert q==a,(q-a,a-q)
    assert bound.count('```mermaid')==8
    return bound
