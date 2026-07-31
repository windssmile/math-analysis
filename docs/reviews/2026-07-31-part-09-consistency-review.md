# 第九部一致性审查

日期：2026-07-31

## 结论

第九部第 37–41 章已完整发布：21 个核心单元、5 个章导学页、32 核心学时
（理论 24、应用 8），另有 1 篇不计入核心统计且不作为后续前置的微分形式选读附录。
全书发布面保持 186 个学习单元、337 学时，没有第 42 章正文或导航。

## 登记表与实际页面对照

- 依赖登记表的 21 个单元 ID、标题、理论/应用学时，逐页与 front matter、章导学页、
  课程地图及导航唯一顺序核对一致。
- 核心页逐页解析为 201 道稳定锚点习题、247 个折叠答案；附录另计 2 道稳定锚点练习、
  5 个折叠答案，出版面合计 203 道稳定锚点练习、252 个折叠答案。
- 第 37–41 章五份章级 consistency review 均存在；本文件承担会随后续出版变化的全局总数、
  当前边界和跨章闭合事实，历史章测试只保留本章合同及可扩展的后继接口。

## 算法、范围与证书边界

- 两个算法接口唯一源文件均为 `src/mathbook_examples/vector_analysis.py`；教材唯一调用页为
  41.5，线积分与通量接口各调用一次，实际代码由 `tests/test_vector_analysis.py` 和 41 章测试覆盖。
- 固定复合中点结果只核验方向、法向、Jacobian 因子和算术，不是误差证书、定理证明、
  正则性证明或参数化不变性证明。
- 附录不进入核心依赖，不发展一般流形、切丛、链、同调、上同调、完整外代数、弱导数
  或测度论线/曲面积分；第十至十二部范围仍留待后续。

## 生成站点与移动视口抽查

post-build 合同覆盖 37.4、38.2、38.4、39.3、40.4、41.2、41.3 与微分形式附录的稳定
锚点、侧栏、章标题、arithmatex 与 MathJax 错误标记。严格构建后以 390 × 844 浏览器
视口逐页读取 DOM，结果如下：

| page | viewport | clientWidth | scrollWidth | H1 | arithmatex | merror | checked_at | tool |
|---|---|---:|---:|---:|---:|---:|---|---|
| 37.4 | 390×844 | 390 | 390 | 1 | 56 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 38.2 | 390×844 | 390 | 390 | 1 | 69 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 38.4 | 390×844 | 390 | 390 | 1 | 43 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 39.3 | 390×844 | 390 | 390 | 1 | 19 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 40.4 | 390×844 | 390 | 390 | 1 | 50 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 41.2 | 390×844 | 390 | 390 | 1 | 16 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 41.3 | 390×844 | 390 | 390 | 1 | 59 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |
| 微分形式附录 | 390×844 | 390 | 390 | 1 | 88 | 0 | 2026-07-31T23:59:50+08:00 | Chrome DevTools MCP |

38.2 首轮因长叉积展开产生 `scrollWidth=636`；将同一等式引入短记号并拆成两个显示式后，
复核为 `scrollWidth=clientWidth=390`。其余七页首轮即无页面级横向滚动。

## 最终验证记录

focused tests 使用实施计划中的完整可复现命令：

```bash
python3.12 -m unittest \
  tests.test_chapter_37 tests.test_chapter_38 tests.test_chapter_39 \
  tests.test_chapter_40 tests.test_chapter_41 tests.test_vector_analysis \
  tests.test_part_09_consistency tests.test_mkdocs_site -v
```

最终审查还运行 `make verify`、
`python3.12 scripts/check_content.py`、`zensical build --strict`、
`python3.12 scripts/check_site.py` 与 `git diff --check`。focused 与第九部套件为 119 tests；
最终 `make verify` 为 446 tests，随后内容检查、严格构建与生成站点检查均通过。
