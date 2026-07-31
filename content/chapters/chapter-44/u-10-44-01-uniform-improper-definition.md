---
title: 含参反常积分的一致收敛应怎样定义？
unit_id: u-10-44-01
hours: {theory: 1.25, applied: 0.00}
difficulty: 4
prerequisites: {book: [第 22 章, 第 25 章, u-10-42-01], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [uniform_improper_integral, infinite_tail, singular_endpoint]
learning_goals: [定义无穷区间上的一致收敛, 定义有限奇端点的一致收敛, 区分逐参数截断与统一截断]
content_standard: 2
---
# 含参反常积分的一致收敛应怎样定义？ {#u-10-44-01}
## 先备知识
熟悉反常积分、函数列一致收敛与含参正常积分。
## 学习目标
能按量词写出两类一致收敛定义，并判断截断是否独立于参数。
## 牵引问题
每个参数都收敛时，为什么还可能无法统一交换运算？
## 探索与猜想
关键不只是每条尾巴最终变小，而是同一个截断要同时控制全部参数。
## 概念与理论
### 无穷区间 {#def-u-10-44-01-infinity}
设 \(F_A(t)=\int_a^A f(x,t)\,dx\)。若存在 \(F:T\to\mathbb R\)，且

\[
\forall\varepsilon>0\ \exists A_0\quad
\forall t\in T\ \forall A\ge A_0,\qquad |F_A(t)-F(t)|<\varepsilon,
\]

就称 \(\int_a^\infty f(x,t)\,dx\) 关于 \(t\in T\) 一致收敛。这里的 \(A_0\) 不能依赖 \(t\)。
### 有限端点奇性 {#def-u-10-44-01-singular}
若 \(f\) 在 \(a\) 附近可能无界，令 \(G_\delta(t)=\int_{a+\delta}^b f(x,t)\,dx\)。要求

\[
\forall\varepsilon>0\ \exists\delta_0>0\quad
\forall t\in T\ \forall\,0<\delta\le\delta_0,\qquad |G_\delta(t)-G(t)|<\varepsilon.
\]

两类定义都是统一截断：无穷端把截断推远，奇端点把删去区间统一缩小。
## 例题与迁移
### 例 1：统一指数尾 {#ex-u-10-44-01-exp}
若 \(t\ge1\)，则 \(\int_A^\infty e^{-tx}dx\le e^{-A}\)，故关于 \(t\in[1,\infty)\) 一致。
### 例 2：边界参数破坏统一性 {#ex-u-10-44-01-boundary}
\(\int_0^\infty e^{-tx}dx\) 对每个 \(t>0\) 收敛，但尾项 \(e^{-tA}/t\) 在 \(t\downarrow0\) 时不能由一个 \(A\) 统一控制。
## 即时检验与回望
### 即时检验 1
统一截断能依赖参数吗？
??? note "答案"
    不能；它只可依赖误差阈值。
### 即时检验 2
逐参数收敛是否推出一致收敛？
??? note "答案"
    不推出，靠近边界的参数可能需要越来越远的截断。
## 常见误区与后续
- “算了许多参数都稳定”不是全体参数的一致量词证明。
- 两端都反常时，应分别建立两端统一控制再合并误差。
## 习题与答案
### 习题 1 {#pr-u-10-44-01-01}
一致定义中哪个量可依赖 \(\varepsilon\)？
??? note "答案"
    截断阈值 \(A_0\) 或 \(\delta_0\)。
### 习题 2 {#pr-u-10-44-01-02}
\(A_0\) 可依赖 \(t\) 吗？
??? note "答案"
    不可。
### 习题 3 {#pr-u-10-44-01-03}
无穷端的方向是什么？
??? note "答案"
    令上限 \(A\to\infty\)。
### 习题 4 {#pr-u-10-44-01-04}
左奇端怎样截断？
??? note "答案"
    从 \(a+\delta\) 开始积分并令 \(\delta\downarrow0\)。
### 习题 5 {#pr-u-10-44-01-05}
若尾界为 \(e^{-A}\)，怎样选 \(A_0\)？
??? note "答案"
    取 \(A_0>\log(1/\varepsilon)\)。
### 习题 6 {#pr-u-10-44-01-06}
一致收敛的极限是什么对象？
??? note "答案"
    参数函数 \(F(t)\)。
### 习题 7 {#pr-u-10-44-01-07}
有限截断稳定能否证明一致收敛？
??? note "答案"
    不能，它只检查有限样本和有限上限。
### 习题 8 {#pr-u-10-44-01-08}
两端反常时怎样分配误差？
??? note "答案"
    可让两端尾项分别小于 \(\varepsilon/2\)。
### 习题 9 {#pr-u-10-44-01-09}
参数集缩小会否更易一致？
??? note "答案"
    会，远离危险边界常能得到统一界。
### 习题 10 {#pr-u-10-44-01-10}
概括“一致”的核心。
??? note "答案"
    一个截断同时服务所有参数。
