---
title: Fatou 引理怎样给出下极限不等式？
unit_id: u-11-50-02
hours: {theory: 1.25, applied: 0.00}
difficulty: 5
prerequisites: {book: [u-11-48-02, u-11-50-01], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [fatou_lemma, tail_infimum, liminf_integral_bound]
learning_goals: [构造尾部下确界, 从 MCT 证明 Fatou, 判断不等式方向]
content_standard: 2
---
# Fatou 引理怎样给出下极限不等式？ {#u-11-50-02}
## 先备知识
会处理可测函数的可数下确界、下极限与 MCT。
## 学习目标
把任意非负序列变成递增尾部下确界序列，得到积分下半连续性。
## 牵引问题
原序列不单调，怎样仍从 MCT 提取可靠的不等式？
## 探索与猜想
丢掉前 n−1 项后取尾部最小高度；随着 n 增大，这个保守高度只能上升。
## 概念与理论
### 尾部下确界
对非负可测 f_n 定义 \(h_n=\inf_{k\ge n}f_k\)。则 h_n 可测且
0≤h_n↑liminf f_n。MCT 给出

\[
\int\liminf_{n\to\infty}f_n\,dm=\lim_n\int h_n\,dm.
\]

又因 h_n≤f_k 对每个 k≥n，故 ∫h_n≤inf_{k≥n}∫f_k。令 n→∞，得到 Fatou 引理

\[
\int\liminf f_n\,dm\le\liminf\int f_n\,dm.
\]

### 假设与方向
非负性为尾部下界提供统一的 0。结论通常只是“≤”；尖峰移动会造成严格不等式。
## 例题与迁移
### 例 1：移动尖峰 {#ex-u-11-50-02-spikes}
每项积分相同而逐点下极限为零时，Fatou 左边为零、右边为正。
### 例 2：单调列 {#ex-u-11-50-02-monotone}
若原列递增，h_n=f_n，Fatou 与 MCT 相容但只保留下界方向。
## 即时检验与回望
### 即时检验 1
h_n 为什么递增？
??? note "答案"
    尾部集合缩小，取下确界只能增大。
### 即时检验 2
Fatou 为什么不是等式？
??? note "答案"
    质量可能随 n 移动，逐点极限看不到每一期全部质量。
## 常见误区与后续
- 不把 liminf 与普通极限混同。
- 反向估计需要额外控制，下一节处理。
## 习题与答案
### 习题 1 {#pr-u-11-50-02-01}
写出 h_n。
??? note "答案"
    \(h_n=\inf_{k\ge n}f_k\)。
### 习题 2 {#pr-u-11-50-02-02}
h_n 可测吗？
??? note "答案"
    可测，可数下确界保持可测。
### 习题 3 {#pr-u-11-50-02-03}
h_n 的极限是什么？
??? note "答案"
    \(\liminf f_n\)。
### 习题 4 {#pr-u-11-50-02-04}
哪里使用 MCT？
??? note "答案"
    交换 h_n 递增极限与积分。
### 习题 5 {#pr-u-11-50-02-05}
比较 h_n 与 f_k。
??? note "答案"
    对 k≥n 有 h_n≤f_k。
### 习题 6 {#pr-u-11-50-02-06}
积分不等式方向是什么？
??? note "答案"
    极限函数积分不大于积分的下极限。
### 习题 7 {#pr-u-11-50-02-07}
允许无穷值吗？
??? note "答案"
    允许。
### 习题 8 {#pr-u-11-50-02-08}
是否要求 f_n 收敛？
??? note "答案"
    不要求。
### 习题 9 {#pr-u-11-50-02-09}
非负性做什么？
??? note "答案"
    给出共同可积意义下界 0。
### 习题 10 {#pr-u-11-50-02-10}
下一节怎样得到反向控制？
??? note "答案"
    对控制函数减去 f_n 后应用 Fatou。
