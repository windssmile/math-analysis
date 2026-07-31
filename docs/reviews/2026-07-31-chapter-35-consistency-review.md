# 第 35 章一致性审查

日期：2026-07-31

## 结论

第 35 章 4 个核心单元已发布：理论 6、应用 1，合计 7 学时；包含 40 道稳定锚点
习题和 48 个折叠答案。发布边界止于第 35 章。

## 数学与范围

- 从线性映射的行列式绝对值推导局部面积体积伸缩，并保留取向区别。
- 换元定理明确一一对应、连续可微、Jacobian 不退化和有限边界分片的用途。
- 证明路线完全处于经典 Riemann 层次，没有借用测度论。
- 极坐标、柱面坐标、球面坐标的因子均由 Jacobian 行列式计算。
- 参数范围、退化轴线和重复覆盖均有明确检查。

## 验证

- `python3.12 -m unittest tests.test_chapter_35 tests.test_part_08_consistency -v`
- `python3.12 scripts/check_content.py`
- `zensical build --strict`
- `python3.12 scripts/check_site.py`
- `git diff --check`
