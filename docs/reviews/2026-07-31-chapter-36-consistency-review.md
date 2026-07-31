# 第 36 章一致性审查

日期：2026-07-31

## 结论

第 36 章 5 个核心单元已发布：理论 5.75、应用 3.25，合计 9 学时；包含 51 道
稳定锚点习题和 62 个折叠答案。第八部核心发布边界止于第 36 章。

## 数学与范围

- 无界区域采用区域穷竭定义非负反常重积分，并明确极限方式。
- 奇点通过挖去邻域处理，区分绝对收敛与依赖路径的风险。
- 质量、质心和转动惯量模型持续检查密度、坐标与结果单位。
- 概率内容止于联合密度、边缘密度、期望与协方差，不引入条件分布。
- 综合建模要求分别核验区域、坐标、量纲与数值结果；Monte Carlo 仅作选读提醒。

## 验证

- `python3.12 -m unittest tests.test_chapter_36 tests.test_part_08_consistency -v`
- `python3.12 scripts/check_content.py`
- `zensical build --strict`
- `python3.12 scripts/check_site.py`
- `git diff --check`
