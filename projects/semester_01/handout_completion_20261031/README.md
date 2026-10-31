# 四门讲义完成与核验

2026-10-31。教师材料编写与核验项目，不记为学生代码作业。

- MA105：8讲，模论与结构定理。
- MA106：12讲，有限群表示论。
- MA302：20讲，常微分方程与动力系统。
- MA306：16讲，概率论II：测度论概率。

正式入口见 [数学讲义目录](../../../lectures/math/README.md)。`archive_manifest.json` 记录被审稿与归档件的双指纹、字节偏移、审核报告和批准信号；前置归档说明以外，正文逐字节保留。

`verify_delivery.py` 只核验交付文件并写入 `final_delivery_verification.json`，可用 Python 3 复跑。`archive_handouts.py` 是归档写入工具，`update_delivery_index.py` 是索引更新工具；二者不是数学测试，不宜为了复核而反复重新生成正文。

`ma105/`、`ma106/`、`ma302/` 保留各课例题及数值验证程序和回执。有限样例核验不替代一般证明；完整证明与声明范围由独立数学审稿核对。`cross_review_recovery.json` 保留 MA302 原DSH综合审稿通道限流的失败及后续真实恢复记录。
