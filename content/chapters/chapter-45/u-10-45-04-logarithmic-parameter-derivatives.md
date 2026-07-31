---
title: 参数求导怎样产生含对数因子的积分与敏感性公式？
unit_id: u-10-45-04
hours: {theory: 0.75, applied: 0.75}
difficulty: 5
prerequisites: {book: [u-10-44-05, u-10-45-01, u-10-45-02], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [logarithmic_integrals, parameter_sensitivity, derivative_hypothesis_audit]
learning_goals: [推导 Gamma 的参数导数, 推导 Beta 的参数偏导, 核查对数核的一致尾项]
content_standard: 2
---
# 参数求导怎样产生含对数因子的积分与敏感性公式？ {#u-10-45-04}
## 先备知识
熟悉反常积分号下求导定理和 Gamma、Beta 收敛证明。
## 学习目标
能解释对数因子的来源，并在紧参数矩形上验证一致收敛。
## 牵引问题
对幂指数求导时，为什么被积函数会多出 \(\log x\)？
## 探索与猜想
\(\partial_s x^{s-1}=x^{s-1}\log x\)，形式导数须通过一致尾项审计。
## 概念与理论
### Gamma 敏感性 {#thm-u-10-45-04-gamma}
在任意紧区间 \(0<\alpha\le s\le\beta\) 上，分别控制零端的
\(x^{\alpha-1}|\log x|\) 与无穷端的 \(x^{\beta-1}e^{-x}\log x\)，得到导数积分一致收敛。因此

\[
\Gamma'(s)=\int_0^\infty x^{s-1}e^{-x}\log x\,dx.
\]

### Beta 敏感性 {#thm-u-10-45-04-beta}
在正参数象限内任意紧矩形上，两端比较给出一致收敛，从而

\[
\partial_pB(p,q)=\int_0^1x^{p-1}(1-x)^{q-1}\log x\,dx,
\]

\[
\partial_qB(p,q)=\int_0^1x^{p-1}(1-x)^{q-1}\log(1-x)\,dx.
\]

参数求导产生对数因子；敏感性公式的关键是第 44 章条件。
## 例题与迁移
### 例 1：Gamma 在 1 处 {#ex-u-10-45-04-gamma1}
\(\Gamma'(1)=\int_0^\infty e^{-x}\log x\,dx\)。
### 例 2：Beta 偏导 {#ex-u-10-45-04-beta}
\(\partial_pB(p,1)=\frac d{dp}(1/p)=-1/p^2\)。
## 即时检验与回望
### 即时检验 1
为什么参数需留在紧子区间？
??? note "答案"
    远离零边界才能统一控制端点幂次。
### 即时检验 2
对 \(q\) 求导产生什么？
??? note "答案"
    \(\log(1-x)\)。
## 常见误区与后续
- 对数无界并不自动导致发散，需与正幂共同比较。
- 高阶参数导数需重复核查更高次对数因子。
## 习题与答案
### 习题 1 {#pr-u-10-45-04-01}
\(\partial_sx^{s-1}\) 是什么？
??? note "答案"
    \(x^{s-1}\log x\)。
### 习题 2 {#pr-u-10-45-04-02}
Gamma 导数核是什么？
??? note "答案"
    \(x^{s-1}e^{-x}\log x\)。
### 习题 3 {#pr-u-10-45-04-03}
零端用哪个参数界？
??? note "答案"
    紧区间的下界 \(\alpha>0\)。
### 习题 4 {#pr-u-10-45-04-04}
无穷端用哪个参数界？
??? note "答案"
    紧区间的上界 \(\beta\)。
### 习题 5 {#pr-u-10-45-04-05}
\(\partial_pB\) 多出什么？
??? note "答案"
    \(\log x\)。
### 习题 6 {#pr-u-10-45-04-06}
\(\partial_qB\) 多出什么？
??? note "答案"
    \(\log(1-x)\)。
### 习题 7 {#pr-u-10-45-04-07}
形式求导足够吗？
??? note "答案"
    不足够，必须证明导数积分一致收敛。
### 习题 8 {#pr-u-10-45-04-08}
为什么正参数边界危险？
??? note "答案"
    参数趋零时端点幂控制退化。
### 习题 9 {#pr-u-10-45-04-09}
\(\partial_pB(p,1)\) 是多少？
??? note "答案"
    \(-1/p^2\)。
### 习题 10 {#pr-u-10-45-04-10}
证明接口来自哪里？
??? note "答案"
    第 44 章反常积分号下求导定理。
