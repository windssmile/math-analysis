# 第一部第四章学习单元 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成递推、区间套、二分逼近与极限预理解四个单元，为第二部的数列极限理论建立问题与误差语言。

**Architecture:** 所有存在性依据来自已建立的确界/平方根定理；本章二分法只逼近已知存在的 \(\sqrt2\)，绝不提前用连续性或介值定理证明任意方程有根。两次轻量 Python 活动只展示算法与误差证书，不含可执行 QMD 单元。

**Tech Stack:** Quarto Markdown、Python 3.12 `unittest`、静态 Python 示例、TOML、现有验证器。

---

## Shared contract

- 单元与学时：`u-01-04-01` 1.25+.50，`u-01-04-02` 1.25+.75，`u-01-04-03` 1.50+.25，`u-01-04-04` 1.00+0；合计理论 5、应用 2.5。
- 每页保持八个固定栏目、稳定单元/定义/定理/例题/习题 ID、折叠答案、完整元数据；登记后立即加入第一部导航并取得渲染页证据。
- 本章用 \(\mathbb N=\{1,2,\ldots\}\) 约定；不系统定义 epsilon-N 极限，不调用函数连续性、介值定理、Cauchy 列。

### Task 1: 递推会不会真的“靠近”目标？

- [ ] TDD 并登记 `u-01-04-01`，标题“递推会不会真的‘靠近’目标？”，1.25+.50，book prerequisites `["chapter-03"]`，Python 先备 `["变量赋值", "for 循环", "函数定义"]`，能力含 concepts/proof/numerical_algorithm/mathematical_expression。
- [ ] 正文用 Babylonian 递推 `x_{n+1}=(x_n+a/x_n)/2`（a>0、x_1>\sqrt a）说明不变下界、单调性、有界性；不得在未建立极限理论时声称已收敛到 \(\sqrt a\)，只证明它夹逼并形成越来越可靠的候选。展示静态 Python 表格，解释程序不是证明。稳定例题与练习 ID、3–6 道折叠答案习题。
- [ ] 增量发布、受控构建/站点/MathJax 检查，提交 `docs: add recurrence learning unit`。

### Task 2: 区间怎样把目标逐步夹住？

- [ ] TDD 并登记 `u-01-04-02`，标题“区间怎样把目标逐步夹住？”，1.25+.75，book prerequisites `["chapter-03"]`，Python 先备 `["while 循环", "条件分支", "函数定义"]`，能力含 numerical_algorithm。
- [ ] 从已证明存在的 \(\sqrt2\) 出发，保持 `a_n^2<2<b_n^2`；完整证明每轮保留正确半区间、长度 `2^{-n}(b_0-a_0)`，中点误差不超过半长。用区间套/确界论证唯一目标；明确这不是一般连续方程求根法。给静态 Python 二分示例与可核验停止准则，稳定定义/算法/例题 ID。
- [ ] 发布验证并提交 `docs: add interval bisection learning unit`。

### Task 3: “越来越近”怎样说得严格？

- [ ] TDD 并登记 `u-01-04-03`，标题同上，1.50+.25，book prerequisites `["chapter-03"]`，能力 concepts/proof/mathematical_expression。
- [ ] 引入“任给误差容许量，能给出明确步数”的预极限语言；对二分区间给出 `n\ge\lceil\log_2((b-a)/\varepsilon)\rceil` 的停止步数推导（明确 ceiling/整数部分引理已在 03-03 建立）。用几何级数式误差界说明量词顺序，不系统定义数列收敛或极限运算。稳定锚点、3–6 道折叠答案习题。
- [ ] 发布验证并提交 `docs: add approximation error learning unit`。

### Task 4: 无限逼近何时会失败？

- [ ] TDD 并登记 `u-01-04-04`，标题“无限逼近何时会失败？”，1.00+0，book prerequisites `["chapter-03"]`，能力 concepts/proof/mathematical_expression。
- [ ] 用 `(-1)^n`、周期序列、错误“残差小即位置误差小”停止准则与不保持不变量的伪二分法，区分振荡、发散、无证书近似。保持“正式收敛定义留给第二部”的边界；有稳定例题与练习 ID、折叠答案。
- [ ] 章节测试精确闭合 5+2.5，四页导航；全量受控构建、检查所有 14 个第一部单元均被渲染/无 MathJax 错误，提交 `docs: publish approximation chapter`。
