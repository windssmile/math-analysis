---
title: Weierstrass、Dirichlet 与 Abel 型判据怎样控制参数族？
unit_id: u-10-44-03
hours: {theory: 1.25, applied: 0.50}
difficulty: 5
prerequisites: {book: [u-10-44-02, 第 24–25 章], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [weierstrass_test, dirichlet_test, abel_test]
learning_goals: [使用统一优函数判据, 核对 Dirichlet 型一致条件, 区分 Abel 型的单调因子]
content_standard: 2
---
# Weierstrass、Dirichlet 与 Abel 型判据怎样控制参数族？ {#u-10-44-03}
## 先备知识
熟悉函数项级数的三类判据、分部积分与一致 Cauchy 判据。
## 学习目标
能逐项核查三类判据的不同假设，并由统一尾界推出一致收敛。
## 牵引问题
绝对衰减、振荡抵消与单调因子分别怎样压小尾积分？
## 探索与猜想
三类判据的共同终点是统一尾项，小尾项的来源却不同。
## 概念与理论
### Weierstrass 型判据 {#thm-u-10-44-03-weierstrass}
若对所有参数有 \(|f(x,t)|\le g(x)\)，且 \(\int_a^\infty g(x)dx\) 收敛，则
\[
\left|\int_A^Bf(x,t)dx\right|\le\int_A^Bg(x)dx
\]
给出一致收敛。
### Dirichlet 型判据
若 \(G(X,t)=\int_a^Xg(x,t)dx\) 对 \(X,t\) 一致有界，而 \(h(x,t)\) 关于 \(x\) 单调趋于 \(0\)，且趋零对参数一致，则分部积分给出统一尾界，故 \(\int gh\) 一致收敛。
### Abel 型判据
若 \(\int_a^Xg(x,t)dx\) 关于 \(X\to\infty\) 一致收敛，且 \(h(x,t)\) 关于 \(x\) 单调并对所有 \(x,t\) 一致有界，则分部积分把乘积尾项控制为 \(g\) 的统一 Cauchy 尾项。
### 条件对照
Weierstrass 使用可积优函数；Dirichlet 使用有界原函数与一致趋零单调因子；Abel 使用已一致收敛的积分与一致有界单调因子。不可混写假设。
## 例题与迁移
### 例 1：指数优函数 {#ex-u-10-44-03-exp}
若 \(|f(x,t)|\le e^{-x}\)，则尾项不超过 \(e^{-A}\)。
### 例 2：振荡核 {#ex-u-10-44-03-osc}
\(\int_1^\infty\sin(tx)/x\,dx\) 的一致性取决于参数集是否远离 \(t=0\)；必须核查原函数界能否统一。
## 即时检验与回望
### 即时检验 1
哪一判据要求可积优函数？
??? note "答案"
    Weierstrass 型判据。
### 即时检验 2
“单调”是关于哪个变量？
??? note "答案"
    关于积分变量 \(x\)。
## 常见误区与后续
- 逐参数有界不等于对参数一致有界。
- 分部积分前要确认截断区间上的正则性。
## 习题与答案
### 习题 1 {#pr-u-10-44-03-01}
优函数可依赖参数吗？
??? note "答案"
    统一判据中的优函数应独立于参数。
### 习题 2 {#pr-u-10-44-03-02}
Weierstrass 尾界是什么？
??? note "答案"
    \(\int_A^\infty g(x)dx\)。
### 习题 3 {#pr-u-10-44-03-03}
Dirichlet 的原函数需怎样有界？
??? note "答案"
    对截断位置与参数共同一致有界。
### 习题 4 {#pr-u-10-44-03-04}
Dirichlet 因子需怎样趋零？
??? note "答案"
    关于参数一致地趋于零。
### 习题 5 {#pr-u-10-44-03-05}
Abel 的哪个积分已知一致收敛？
??? note "答案"
    \(\int_a^Xg(x,t)dx\)。
### 习题 6 {#pr-u-10-44-03-06}
Abel 因子需要趋零吗？
??? note "答案"
    不必，但需单调且一致有界。
### 习题 7 {#pr-u-10-44-03-07}
三类判据的共同终点是什么？
??? note "答案"
    一致 Cauchy 尾项估计。
### 习题 8 {#pr-u-10-44-03-08}
振荡可替代绝对收敛吗？
??? note "答案"
    在 Dirichlet 条件完整时可给条件一致收敛。
### 习题 9 {#pr-u-10-44-03-09}
参数靠近零为何危险？
??? note "答案"
    振荡减慢，原函数统一界可能失效。
### 习题 10 {#pr-u-10-44-03-10}
核查判据时应避免什么？
??? note "答案"
    避免把一种判据的结论与另一种的假设拼接。
