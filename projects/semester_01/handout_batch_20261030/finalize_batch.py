"""Record this batch without overwriting historical course plans or approvals."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'professors/MATH'
COURSES = {'MA105':8, 'MA106':12, 'MA302':20, 'MA306':16}
fingerprints = []
for code,total in COURSES.items():
    folder = BASE / f'handout_{code}_CDX'
    progress = json.loads((folder/'.progress.json').read_text(encoding='utf-8'))
    assert progress['chapters_written']==[1,2], code
    assert progress['chapters_pending']==list(range(3,total+1)), code
    for path in sorted(folder.iterdir()):
        if path.suffix not in ('.md','.json'): continue
        data=path.read_bytes()
        content=data.decode('utf-8')
        assert not data.startswith(b'\xef\xbb\xbf'), path
        assert b'\r' not in data, path
        assert '$$' not in content, path
        if path.suffix=='.json': json.loads(content)
        for line_number,line in enumerate(content.split('\n'),1):
            assert line.count('$')%2==0, (path,line_number,'odd math delimiters')
        fingerprints.append({'path':path.relative_to(ROOT).as_posix(),'bytes':len(data),'lines':content.count('\n'),'sha256':hashlib.sha256(data).hexdigest()})

def new_file(path,text):
    data=text.encode('utf-8')
    if path.exists():
        assert path.read_bytes()==data, f'Existing different file: {path}'
    else:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)

def append_once(path,heading,text):
    before=path.read_bytes()
    if heading.encode('utf-8') in before: return
    assert path.read_bytes()==before, f'Concurrent edit: {path}'
    path.write_bytes(before+('\n\n'+text.rstrip()+'\n').encode('utf-8'))

inventory='''# 数学讲义批量开工清单（2026-10-30，CDX）

用户请求：到 professors/MATH 查找尚未编写讲义，全部开始编写，并授权 Astra 子代理并行。本批按已经存在独立设计和章节规划、实际没有正文的项目开工；关于是否扩展到总清单全部计划课程，已另询范围，尚无回复，不把未决范围当作已处理。

## 当前可读正文

| 课程 | 总计划 | 本批正文与状态 | 续写 |
|---|---:|---|---|
| MA105 模论与结构定理 | 8讲 | [第1–2讲](handout_MA105_CDX/MA105_模论与结构定理_第01至02讲_CDX.md)，作者内容齐备、已协作复核 | 第3–8讲 |
| MA106 有限群表示论 | 12讲 | [第1–2讲](handout_MA106_CDX/MA106_有限群表示论_讲1-2.md)，作者内容齐备、已主代理复核 | 第3–12讲 |
| MA302 常微分方程与动力系统 | 20讲 | [第1讲](handout_MA302_CDX/03-第01讲.md)、[第2讲](handout_MA302_CDX/04-第02讲.md)，作者内容齐备、已协作复核 | 第3–20讲 |
| MA306 概率论II：测度论概率 | 16讲 | [第1讲](handout_MA306_CDX/讲01-概率空间再访.md)作者内容齐备；[第2讲](handout_MA306_CDX/讲02-测度分布与密度.md)部分完成 | 先补第2讲一般RN、Stieltjes存在性证明，再写第3–16讲 |

合计4门全部启动、8讲已写草稿，其中7讲本批内容齐备、1讲尚有证明缺口，另有48讲尚未写作。计数不表示独立审稿通过，更不表示学生学完。作者同批复核不冒充 Reviewer_MATH 或 DSH 审批。

## 排除重复开工的依据

MA301、MA305旧设计目录的进度仍写待写，但 approved 中已有18讲概率论、16讲数理统计；MA104有16讲归档正文；高代01–08及05A/05B已存在正文；MA404已有离散与连续十二阅读单元。因此不据旧progress直接重写这些课程。MA404后续操作编码等专题仍为原有待补，不伪装为本次已补齐。

## 总清单层面的另列候选

MA202、MA203沿于品现有参考材料精读，不因本地没有自编成稿就判作教材缺失；MA201同样已有参考材料与教学档案。

尚未建独立写作项目或只在课程总清单列章节的计划：MA204、MA205、MA303、MA304、MA307、MA308、MA309、MA401、MA402、MA403、MA405、MA406、MA501、MA502。它们没有在本批被标记成已写，也没有被删除。泛称MA6xx与B级方向专题仍需具体选题，不能按空课号生成讲义。

## 写作约定与来源

沿各门现有设计选用Markdown，不编PDF；本轮“全部开始编写”作为直接开工授权，旧Gate字段保留原历史值并另记本次授权。每门有对标检查、术语表、答案核验和可续写进度；前置是读者需要的准备，不是学生已掌握记录。

MA105由主代理编写；MA106、MA302、MA306由gpt-6-astra子代理并行编写。互不重叠目录。原设计、旧讲义、原批准信号未改；只在共享学习进度及对标总表追加本批记录。

核验报告：[verification.json](../../projects/semester_01/handout_batch_20261030/verification.json)。MA105精确计算脚本及结果在同项目ma105子目录。代码为教师核验工具，不计入学生项目完成量。

## 下一步与审稿边界

本批只请求开篇增量审阅，MA306第2讲需保留部分完成标签。未启动正式全书归档，未生成任何批准信号，未自动关闭R5或MA301/MA305的待证登记。若后续数学审稿通过且判定涉及跨学科，再按既有流程做综合审核。
'''
new_file(BASE/'20261030_待写讲义开工清单_CDX.md',inventory)

report={'date':'2026-10-30','status':'PASS','courses':COURSES,'chapters_drafted':8,'chapters_content_complete':7,'chapters_partial':['MA306:2'],'future_chapters_unwritten':48,'checks':['all four progress lists agree with files','UTF-8 without BOM','LF only','no double dollar delimiters','math delimiters paired per line','valid JSON'],'files':fingerprints,'limit':'Format and state checks plus documented prose review; no DSH approval or student completion.'}
new_file(ROOT/'projects/semester_01/handout_batch_20261030/verification.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')

heading='### 2026-10-30｜四门未写讲义并行开工（CDX）'
entry=heading+'''

- 用户直接要求检查 professors/MATH 的未写讲义并全部开始，授权 Astra 并行。经实际正文与归档对照，已开工 MA105、MA106、MA302、MA306，入口为 `professors/MATH/20261030_待写讲义开工清单_CDX.md`。
- 本批为四门各前两讲，共8讲工作稿；7讲作者内容齐备，MA306第2讲仍缺一般RN和Stieltjes存在性证明；其余48讲待写。每门保留独立进度和核验，未冒充全书完成。
- 旧MA301／MA305设计状态滞后，不重复编写已归档正文。其他仅在总清单列计划的课程另列范围候选，未标完成。
- 第1学期新增教师核验代码位于 `projects/semester_01/handout_batch_20261030/`；不登记学生已完成代码项目。全部材料未经DSH独立审稿，不改变学生学习完成范围，原待讲／待测验／待证项保持原状。
'''
append_once(ROOT/'learning_progress.md',heading,entry)
benchmark_heading='## 2026-10-30 四门开篇增量对标登记（CDX）'
benchmark=benchmark_heading+'''

本次按已有设计开始MA105／MA106／MA302／MA306正文。每门对标文件在 `professors/MATH/handout_<课号>_CDX/02-对标检查.md`。国内对标使用既有求真／北大官方资料的本地历史抽取，另核查官方国际课程／讲义；MA105另访问北大官方课程页。资料日期、覆盖层级、未核教材深度均在各文件说明。历史课程与本地快照不当作2026实时课表，不凭篇幅声称质量或深度相当。当前为开篇，不是全课覆盖验收。
'''
append_once(BASE/'对标检查_数学线总表.md',benchmark_heading,benchmark)

signal='''# 四门数学讲义开篇增量审阅请求

日期：2026-10-30。发起：CDX数学教授。状态：请求已登记，不表示审稿员已经运行或通过。

按 lecture-handout-writer 技能的初稿审阅流程，请仅审阅本批开篇增量。入口 `professors/MATH/20261030_待写讲义开工清单_CDX.md`，逐件SHA256见 `projects/semester_01/handout_batch_20261030/verification.json`。工作稿与分离答案均在四个 handout_MA105_CDX、handout_MA106_CDX、handout_MA302_CDX、handout_MA306_CDX 目录。

范围：MA105/MA106/MA302的第1–2讲、MA306第1讲及部分完成的第2讲。MA306一般RN与Stieltjes存在性证明明确缺失，不能据已写标题批准整讲理论目标完成。作者自校及同批协作复核已记录，非独立批准。

重点：模秩的环条件、Maschke的特征条件、ODE存在唯一与紧集延拓、单调类与外测度的无限值处理。MA306未证候选U306-2/3在局部文件明示，若接受为正式课程依赖，请按登记表规则处理；本请求不自动分配或关闭R编号。

按件分工：CDX产出及后续修订，Reviewer_MATH负责独立学科审阅；是否正式归档及是否需跨学科审核依真实结果另定。本批不写approved、不触发学生教学完成，不改旧批准信号。
'''
new_file(ROOT/'signals/review_request/math/20261030_四门讲义开篇增量_CDX.signal',signal)
print(json.dumps({'status':'PASS','files_checked':len(fingerprints),'inventory':'professors/MATH/20261030_待写讲义开工清单_CDX.md','draft_chapters':8,'complete_content_chapters':7,'partial_chapters':1},ensure_ascii=False))

if __name__=='__main__':
    pass
