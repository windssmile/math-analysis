---
title: 复指数形式怎样统一正弦与余弦形式？
unit_id: u-12-51-04
hours: {theory: 1.0, applied: 0.25}
difficulty: 4
prerequisites: {book: [u-12-51-01, u-12-51-02], higher_algebra: [复数与 Euler 公式], analytic_geometry: [], python: []}
capabilities: [complex_fourier_form, real_complex_conversion, conjugate_symmetry]
learning_goals: [定义复 Fourier 系数, 完成实复双向换算, 识别共轭对称]
content_standard: 2
---
# 复指数形式怎样统一正弦与余弦形式？ {#u-12-51-04}
## 先备知识
掌握 Euler 公式和实 Fourier 系数。
## 学习目标
在不改变归一化的前提下完成实形式与复指数形式双向换算。
## 牵引问题
能否用一个整数指标同时记录正弦与余弦频率？
## 探索与猜想
\(e^{in\omega x}\) 同时包含余弦和正弦，负频率负责共轭信息。
## 概念与理论
定义

\[
c_n={1\over T}\int_a^{a+T}f(x)e^{-in\omega x}\,dx,\qquad n\in\mathbb Z.
\]

则形式上 \(f\sim\sum_{n\in\mathbb Z}c_ne^{in\omega x}\)。双向换算为
\(c_0=a_0/2\)，\(c_n=(a_n-ib_n)/2\)，\(c_{-n}=(a_n+ib_n)/2\)，以及
\(a_n=c_n+c_{-n}\)，\(b_n=i(c_n-c_{-n})\)。实值 \(f\) 满足共轭对称
\(c_{-n}=\overline{c_n}\)。
### 障碍
指数中的负号与 (b_n) 的符号容易同时写反。
### 证明路线
代入 Euler 公式，分别比较 (e^{in\omega x}) 与 (e^{-in\omega x}) 系数。
### 逐步证明
(a_ncos n\omega x+b_nsin n\omega x)
(=((a_n-ib_n)/2)e^{in\omega x}+((a_n+ib_n)/2)e^{-in\omega x})。
### 假设用在何处
实值性只用于共轭对称；双向换算本身允许复值系数。
### 失败边界
复形式简化记号，但不会自动证明双边无穷和收敛。
## 例题与迁移
### 例 1：余弦 {#ex-u-12-51-04-cosine}
(cos x) 有 (c_1=c_{-1}=1/2)。
### 例 2：正弦 {#ex-u-12-51-04-sine}
(sin x) 有 (c_1=-i/2,c_{-1}=i/2)。
## 即时检验与回望
### 即时检验 1
实值函数的负频率是否独立？
??? note "答案"
    不独立，由正频率的复共轭确定。
### 即时检验 2
(c_0) 与 (a_0) 的关系是什么？
??? note "答案"
    (c_0=a_0/2)。
## 常见误区与后续
- 先固定指数约定，再记换算公式。
- 双向换算是有限代数，不是收敛证明。
## 习题与答案
### 习题 1 {#pr-u-12-51-04-01}
由 (a_n,b_n) 写出 (c_n)。
??? note "答案"
    (c_n=(a_n-ib_n)/2)，(n>0)。
### 习题 2 {#pr-u-12-51-04-02}
由 (c_n,c_{-n}) 写出 (a_n)。
??? note "答案"
    (a_n=c_n+c_{-n})。
### 习题 3 {#pr-u-12-51-04-03}
由二者写出 (b_n)。
??? note "答案"
    (b_n=i(c_n-c_{-n}))。
### 习题 4 {#pr-u-12-51-04-04}
偶实函数的 (c_n) 有何性质？
??? note "答案"
    它们为实数且 (c_{-n}=c_n)。
### 习题 5 {#pr-u-12-51-04-05}
奇实函数的 (c_n) 有何性质？
??? note "答案"
    它们为纯虚数且 (c_{-n}=-c_n)。
### 习题 6 {#pr-u-12-51-04-06}
常数 3 的 (c_0) 是多少？
??? note "答案"
    3。
### 习题 7 {#pr-u-12-51-04-07}
(e^{2ix}) 的唯一非零复系数是什么？
??? note "答案"
    (c_2=1)。
### 习题 8 {#pr-u-12-51-04-08}
为何系数积分指数带负号？
??? note "答案"
    因为它与基函数 (e^{in\omega x}) 取复内积配对。
### 习题 9 {#pr-u-12-51-04-09}
复形式是否改变周期？
??? note "答案"
    不改变，仍由 (omega=2pi/T) 决定。
### 习题 10 {#pr-u-12-51-04-10}
共轭对称能否用于任意复值函数？
??? note "答案"
    不能，它依赖 (f) 为实值。
