---
title: 局部连续何时升级为全局一致控制？
unit_id: u-03-11-03
hours:
  theory: 1.5
  applied: 0.5
difficulty: 3
prerequisites:
  book:
  - chapter-10
  - chapter-11
  higher_algebra:
  - 最小值
  analytic_geometry:
  - 闭区间
  python: []
capabilities:
- concepts
- proof
- analytic_calculation
- mathematical_expression
learning_goals:
- 定义一致连续
- 证明闭区间上一致连续
- 解释有限子覆盖如何给出统一 delta
content_standard: 1
---

# 局部连续何时升级为全局一致控制？ {#u-03-11-03}


## 先备知识

一点连续性和闭区间紧致性。普通连续中的 \(\delta\) 可以依赖于观察点；一致连续要求它不依赖点。

## 学习目标

1. 定义一致连续；2. 证明闭区间上一致连续；3. 分析非紧致区间的失败。

## 牵引问题

若要用同一采样间距控制整段曲线的输出误差，能否对每个位置选择不同的 \(\delta_x\)？不能：算法需要一个对全区间有效的 \(\delta\)。

## 探索与猜想

对每个 \(x\) 的连续性先给出局部半径 \(r_x\)。这些邻域覆盖闭区间；紧致性留下有限多个，再取它们的半径最小值，就得到统一尺度。

## 概念与理论

称 \(f:D\to\mathbb R\) 一致连续，若对任意 \(\varepsilon>0\)，存在 \(\delta>0\)，使任意 \(x,y\in D\) 满足 \(|x-y|<\delta\) 时都有 \(|f(x)-f(y)|<\varepsilon\)。

### 定理（Heine--Cantor） {#thm-u-03-11-03-uniform-continuity}

连续函数 \(f:[a,b]\to\mathbb R\) 一致连续。

证明：给定 \(\varepsilon>0\)。每个 \(z\in[a,b]\) 的连续性给出 \(r_z>0\)：若 \(|x-z|<r_z\)，则 \(|f(x)-f(z)|<\varepsilon/2\)。开区间 \(N_{r_z/2}(z)\) 覆盖 \([a,b]\)，取有限子覆盖，对相应有限多个半径令

$$
\delta=\min\{r_{z_1}/2,\ldots,r_{z_m}/2\}>0.
$$

任取 \(x,y\) 且 \(|x-y|<\delta\)。某个 \(z_i\) 满足 \(|x-z_i|<r_{z_i}/2\)，于是 \(|y-z_i|\le|y-x|+|x-z_i|<r_{z_i}\)。两次局部估计与三角不等式给出 \(|f(x)-f(y)|<\varepsilon\)。

## 例题与迁移

\(x^2\) 在 \([0,2]\) 一致连续；直接也可由 \(|x^2-y^2|\le4|x-y|\) 取 \(\delta=\varepsilon/4\)。但 \(1/x\) 在 \((0,1)\) 不一致连续：\(x_n=1/n,y_n=1/(n+1)\) 的距离趋于零，函数值差恒为 \(1\)。

## 即时检验与回望

1. 为什么取最小半径不会是零？答：只取有限多个严格正数的最小值。
2. 一致连续是否比连续强？答：是；定义中 \(\delta\) 不依赖点。

## 习题与答案

1. 常数函数一致连续吗？答：是，任意正 \(\delta\) 都可用。
2. \(x\) 在全体实数一致连续吗？答：是，取 \(\delta=\varepsilon\)。
3. \(x^2\) 在全体实数一致连续吗？答：否；取 \(x_n=n,y_n=n+1/n\)，输入差趋零而函数值差趋于 \(2\)。
