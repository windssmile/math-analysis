# 第 34 章一致性审查

日期：2026-07-31

## 结论

第 34 章 5 个核心单元已发布：理论 6、应用 3，合计 9 学时；包含 50 道稳定锚点
习题和 61 个折叠答案。发布边界止于第 34 章。

## 数学、算法与范围

- 连续闭矩形上的累次积分给出完整 Riemann 和证明，不冒充一般 Fubini–Tonelli。
- x-型、y-型、换序与三重积分都先描述投影和截面，必要时分片。
- 34.5 唯一复用 `mathbook_examples.multiple_integration`，没有复制算法。
- 二维中点法只处理矩形；缺少二阶偏导界时只报告近似，不声称误差证书。

## 验证

- `python3.12 -m unittest tests.test_chapter_34 tests.test_multiple_integration tests.test_part_08_consistency -v`
- `python3.12 scripts/check_content.py`
- `zensical build --strict`
- `python3.12 scripts/check_site.py`
- `git diff --check`
