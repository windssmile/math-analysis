# 第 33 章一致性审查

日期：2026-07-31

## 结论

第 33 章 4 个核心单元已发布：理论 6.25、应用 0.75，合计 7 学时；包含 34 道
稳定锚点习题和 42 个折叠答案。发布边界止于第 33 章。

## 数学与范围

- 从闭矩形分割、最大直径和任意取样定义二重 Riemann 积分。
- 连续可积性明确由紧致性、一致连续性和振幅总和证明。
- 线性、单调性、绝对值估计与有限区域可加性均从 Riemann 和推出。
- 常用区域采用区域外补零；正文只承诺有限分片光滑边界。
- Jordan 内容没有成为核心前置，累次积分与换元没有提前使用。

## 验证

- `python3.12 -m unittest tests.test_chapter_33 tests.test_part_08_consistency -v`
- `python3.12 scripts/check_content.py`
- `zensical build --strict`
- `python3.12 scripts/check_site.py`
- `git diff --check`

以上命令应在本章提交前全部通过。
