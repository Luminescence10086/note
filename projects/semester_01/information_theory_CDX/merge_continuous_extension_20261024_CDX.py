"""Merge the reviewed six-lecture baseline with the authorized continuous extension."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
WORK=ROOT/'professors/MATH/handout_MA404_CDX'
OLD='MA404_信息论_有限离散六讲.md'
NEW='MA404_信息论_离散与连续十二讲.md'
SOURCE=ROOT/'lectures/math/approved'/OLD
TARGET=SOURCE.with_name(NEW)
manifest=json.loads((WORK/'20261024_baseline_CDX.json').read_text(encoding='utf-8'))
assert not TARGET.exists(), 'target exists; do not overwrite a concurrent version'
assert json.loads((WORK/'20261024_连续部分核验_CDX.json').read_text(encoding='utf-8'))['status']=='PASS'


def normalized(text):
    return text.replace('\r\n','\n').replace('\r','\n')


def encode(text):
    return normalized(text).replace('\n','\r\n').encode('utf-8')


def read_checked(relative):
    path=ROOT/relative
    data=path.read_bytes()
    assert hashlib.sha256(data).hexdigest()==manifest[relative]['sha256'], f'concurrent changes: {relative}'
    return data,normalized(data.decode('utf-8-sig'))


def guarded_write(path, before, content):
    assert path.read_bytes()==before, f'concurrent changes before mutation: {path}'
    data=encode(content)
    path.write_bytes(data)
    assert path.read_bytes()==data
    return data


relative='lectures/math/approved/'+OLD
before,original=read_checked(relative)
anchor='## 第一讲\u3000把问题变成概率表'
prefix,oldbody=original.split(anchor,1)
prefix=prefix.replace('# 信息论：从不确定性到信息处理', '# 信息论：从不确定性到信息处理（离散与连续十二讲）',1)
prefix=prefix.replace('> **版本**：v0.1-fix1 ｜ **日期**：2026-10-11 ｜ **作者**：Codex 侧数学教授分身（CDX）',
'> **版本**：v0.2 合订自校稿 ｜ **日期**：2026-10-24（原六讲：2026-10-11）｜ **作者**：Codex 侧数学教授分身（CDX）',1)
prefix=prefix.replace('> **状态**：按首轮审稿意见修订，待 DSH 增量复核；未经批准不归档。',
'> **状态**：原六讲已有 2026-10-11 学科／综合审稿记录；新增第 7–12 讲作者自校完成，待独立增量审稿。历史批准不覆盖新增内容。',1)
prefix=prefix.replace('你需要的起点是有限集合、分数运算和中学对数。第一讲补齐概率对象与条件分布；之后的推导只操作有限和。所有对数以 2 为底，信息量单位为 bit。小数保留六位时使用近似号，精确式优先保留。',
'第一部分（第 1–6 讲）只需有限集合、分数运算和中学对数；第一讲补齐概率对象与条件分布，之后的推导只操作有限和。第二部分（第 7–12 讲）增加密度、积分、协方差与条件期望，前置和外部输入在第二部分导读及附录 H 明示。信息量的对数以 2 为底，单位 bit；Fisher 得分明确使用自然对数，不能把两种底数混用。小数保留六位时使用近似号，精确式优先保留。',1)
prefix=prefix.replace('**待证工具 U1–U4**','**第一部分待证工具 U1–U4**',1)
prefix=prefix.replace('它们集中列于附录 C，也在首次使用处点名。','它们集中列于附录 C，也在首次使用处点名；第二部分新增外部接口列于附录 H。',1)
prefix+='''## 合订目录与阅读次序

| 部分 | 讲次 | 主题 |
| --- | --- | --- |
| 有限离散 | 1–2 | 概率表、自信息与熵 |
| 有限离散 | 3–4 | 条件熵、互信息 |
| 有限离散 | 5–6 | 信息处理、有限信道与模型报告 |
| 原六讲附录 | A–E | 提示、解答、证明账本、术语、历史核验 |
| 连续部分 | 7 | 密度、量化、微分熵与坐标 |
| 连续部分 | 8 | KL、连续／混合互信息、数据处理 |
| 连续部分 | 9 | 高斯最大熵与协方差几何 |
| 连续部分 | 10 | 功率受限高斯信道 |
| 连续部分 | 11 | Fisher 信息、局部 KL 与 CR 界 |
| 连续部分 | 12 | 高斯率失真、重建与综合报告 |
| 新增附录 | F–J | 提示、解答、前置与来源、术语、自校说明 |

按同学要求，新增正文直接接在原文件末尾，旧附录 A–E 保留原位。原六讲中“本册只用有限和”等叙述指第一部分历史范围。此处十二讲是合订版阅读编号，完整 MA404 十六讲规划另含 AEP、操作编码等专题，并未在本次全部完成。讲义写成与同学学完分别记录。

'''
addon=normalized((WORK/'20261024_连续部分正文_CDX.md').read_text(encoding='utf-8'))
combined=prefix+anchor+oldbody.rstrip()+'\n\n'+addon.strip()+'\n'
assert combined[combined.index(anchor):combined.index('## 第二部分导读')].rstrip()==(anchor+oldbody).rstrip()

# Preserve the baseline, then modify and rename the user's actual single document.
updated=guarded_write(SOURCE,before,combined)
assert SOURCE.read_bytes()==updated
assert not TARGET.exists()
SOURCE.rename(TARGET)
assert TARGET.read_bytes()==updated and not SOURCE.exists()

rp='professors/MATH/本科开课总清单.md'
b,t=read_checked(rp)
lines=t.split('\n')
for i,line in enumerate(lines):
    if line.startswith('| **1（提前，原 6）** | **MA404**'):
        line=line.replace(OLD,NEW)
        line=line.replace('16 讲（首批 6 讲）','16 讲课程规划（现有合订本 12 个阅读单元）')
        line=line.replace('形式层（AEP／编码定理）待实分析成熟后回补',
                          '2026-10-24 连续六讲已补写并合订，新增部分作者自校、待独立增量审稿；不改变学习完成状态。AEP／操作编码定理仍待后续回补')
        lines[i]=line
    if line.startswith('### MA404 信息论（'):
        lines[i]='### MA404 信息论（原六讲已归档；连续六讲已补写合订、待增量审稿；原十六讲课程规划保留）'
t='\n'.join(lines)+'''\n
## 2026-10-24 MA404 连续部分合订留痕（CDX）

按同学直接请求，原 `MA404_信息论_有限离散六讲.md` 续写后更名为 `MA404_信息论_离散与连续十二讲.md`。前六讲及旧附录正文保留；新增第 7–12 讲覆盖微分熵、连续／混合互信息、高斯最大熵与信道、Fisher 信息、率失真。十二个阅读单元不替代本表原十六讲专题规划，编号不逐项对应；原有“CDX 侧已学完”只指离散入口六讲，未自动扩展到新六讲。新增正文作者自校完成、待独立增量审稿，旧批准只覆盖原版本范围。历史记录中的旧文件名不回写；上方有效入口已更新。
'''
guarded_write(ROOT/rp,b,t)

rp='lectures/math/unproven_registry.md'
b,t=read_checked(rp)
lines=t.split('\n')
for i,line in enumerate(lines):
    if line.startswith('| **R13**'):
        lines[i]=line.replace('lectures/math/'+OLD,'lectures/math/approved/'+NEW)
t='\n'.join(lines)+'''\n
## 2026-10-24 MA404 合订版接口留痕（CDX）

同学授权补写连续部分并更名；R13 的当前引用入口已指向 `approved/MA404_信息论_离散与连续十二讲.md`，R14–R16 的“同上”沿用该入口。历史记录不改。原 R13–R16 状态不因作者补写证明而自动销号；R18／R19 仍是连续模型显式前置。

新增合订稿附录 H2 列出局部候选别名 C-U1（一般互信息、正则条件核与有限量化表示）、C-U2（高斯信道操作编码定理）、C-U3（高斯率失真操作定理）。请学科审稿时核对并按权威规则分配正式编号；当前不自行占用 R 编号。C-U1 在一般／奇异模型中实际引用；C-U2、C-U3 是明确未在本册证明的后续操作桥梁，未用于冒充本文单字母优化的证明。
'''
guarded_write(ROOT/rp,b,t)

rp='learning_progress.md'
b,t=read_checked(rp)
t+='''\n
### 2026-10-24｜MA404 信息论连续部分补写与合订（CDX）

- **材料变更**：按同学请求，离散六讲后接连续第 7–12 讲，统一文件为 `lectures/math/approved/MA404_信息论_离散与连续十二讲.md`；有效文件名已更正，旧正文和历史审稿记录保留。
- **新增范围**：密度与量化、微分熵、连续／混合互信息、KL 与数据处理、高斯最大熵与功率受限信道、Fisher／局部 KL／CR 界、高斯率失真与条件均值报告。新增 42 个例题／练习单元及解答，作者核验代码位于 `projects/semester_01/information_theory_CDX/verify_continuous_extension_20261024_CDX.py`（教师材料核验产出，不是学生已完成项目）。
- **材料状态**：作者自校完成；新增部分待独立学科增量审稿，旧六讲批准不覆盖新增内容。沿既有文件位置续写，不据目录名宣称新稿已经批准。
- **学习状态**：本次只补写材料，未验收新六讲，不增加“已学完”范围；AEP、操作编码、信息瓶颈等完整课程专题仍后置，不自动增排课时。
'''
guarded_write(ROOT/rp,b,t)

rp='professors/MATH/teaching_log.md'
b,t=read_checked(rp)
t+='''\n
## 2026-10-24｜MA404 连续部分补写、单文件合并与更名（CDX）

- 同学直接请求“补上信息论连续部分，接原文件后合成一个，改文件名称”。CDX 沿用原六讲受众与教学范式，从续写阶段执行；新增六讲章节依赖和前置写入 `handout_MA404_CDX/20261024_连续部分设计与章节规划_CDX.md`。
- 单一阅读文件改为 `lectures/math/approved/MA404_信息论_离散与连续十二讲.md`。只改原顶部导读和版本状态；原第一讲至附录 E 正文保持同一，新增第七至十二讲及附录 F–J 接于文末。原件字节快照与 SHA256 保存在工作过程目录。
- 新增 42 个题目单元，涵盖负微分熵／尺度、KL 方向、混合目标、奇异联合分布、高斯最大熵、信道功率优化、Fisher 正则性失效反例、后向率失真构造及预测报告。作者作确定性积分／闭式交叉核验；核验并不等于独立审稿。
- 更新当前课程入口和未证登记当前引用；不回写旧审稿报告、历史信号、历史学习日志，不销 R13–R16，不把新增一般测度结论伪装为已证。新增部分创建独立增量送审请求；一般工具 C-U1–C-U3 仅为候选别名。
- 本条是材料编写记录，不是本日已授课、已测验或同学学会记录。原 MA404 十六讲专题规划保留，合订十二阅读单元不冒充完整课程。
'''
guarded_write(ROOT/rp,b,t)

progress={'project':'MA404 信息论：离散与连续十二讲合订','format':'md','date':'2026-10-24',
 'phase':5,'request':'用户直接授权续写连续部分、同文件追加合并与更名；复用既有六讲设计',
 'chapters_written':list(range(1,13)),'chapters_pending':[],
 'author_checks':'42 added units PASS','independent_review':'pending_incremental',
 'original_review_scope':'2026-10-11 first six lectures only','student_completion_changed':False,
 'canonical':'lectures/math/approved/'+NEW}
(WORK/'.progress.json').write_bytes(encode(json.dumps(progress,ensure_ascii=False,indent=2)+'\n'))
print(json.dumps({'canonical':str(TARGET),'bytes':len(updated),'sha256':hashlib.sha256(updated).hexdigest(),
 'renamed':True,'original_body_preserved':True},ensure_ascii=False,indent=2))
