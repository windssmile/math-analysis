---
title: 一致 Cauchy 判据怎样把尾部转化为可检查条件？
unit_id: u-10-44-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 5
prerequisites: {book: [u-10-44-01, 第 8 章], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [uniform_cauchy_criterion, tail_control, necessity_sufficiency]
learning_goals: [陈述一致 Cauchy 判据, 证明必要性与充分性, 用统一尾项避免预知极限]
content_standard: 2
---
# 一致 Cauchy 判据怎样把尾部转化为可检查条件？ {#u-10-44-02}
## 先备知识
熟悉实数完备性、Cauchy 准则和一致收敛。
## 学习目标
能用任意两个远端截断之间的积分判断一致收敛。
## 牵引问题
不知道极限函数时，怎样只用被积函数检查一致收敛？
## 探索与猜想
比较两个足够远的截断，就能把未知极限从条件中消去。
## 概念与理论
### 一致 Cauchy 判据 {#thm-u-10-44-02-cauchy}
\(\int_a^\infty f(x,t)dx\) 关于 \(T\) 一致收敛，当且仅当
\[
\forall\varepsilon>0\ \exists A_0\quad
\forall B>A\ge A_0\ \forall t\in T,\qquad
\left|\int_A^B f(x,t)\,dx\right|<\varepsilon.
\]
这就是统一尾项条件，也是充要性陈述。
### 必要性
若截断积分一致趋于 \(F\)，取所有截断到 \(F\) 的误差小于 \(\varepsilon/2\)。由三角不等式，任意两个远端截断之差小于 \(\varepsilon\)。
### 充分性
固定每个 \(t\)，条件使截断积分成为 Cauchy 族，由实数完备性得到极限 \(F(t)\)。再固定 \(A\ge A_0\)，令 \(B\to\infty\)，保留同一估计，得到 \(|F(t)-F_A(t)|\le\varepsilon\)，而且对所有参数同时成立。
### 奇端点版本
把 \(B>A\ge A_0\) 换成 \(0<\eta<\delta\le\delta_0\)，控制 \(\left|\int_{a+\eta}^{a+\delta}f(x,t)dx\right|\) 即可。
## 例题与迁移
### 例 1：绝对尾界 {#ex-u-10-44-02-majorant}
若 \(|f(x,t)|\le g(x)\) 且 \(\int_A^\infty g\to0\)，统一 Cauchy 条件立即成立。
### 例 2：失败诊断 {#ex-u-10-44-02-failure}
若能为每个 \(A_0\) 找到 \(t,A,B\) 使尾积分不小，则一致收敛失败。
## 即时检验与回望
### 即时检验 1
判据为何不出现 \(F\)？
??? note "答案"
    它只比较两个截断积分之差。
### 即时检验 2
充分性依赖哪条实数性质？
??? note "答案"
    Cauchy 完备性。
## 常见误区与后续
- 只控制 \(\int_A^{A+1}\) 通常不够，判据要求任意 \(B>A\)。
- 绝对值在积分外；振荡抵消可使尾积分小。
## 习题与答案
### 习题 1 {#pr-u-10-44-02-01}
判据中的截断阈值依赖什么？
??? note "答案"
    只依赖 \(\varepsilon\)。
### 习题 2 {#pr-u-10-44-02-02}
为何要求任意 \(B>A\)？
??? note "答案"
    Cauchy 性要比较所有足够远的截断。
### 习题 3 {#pr-u-10-44-02-03}
必要性怎样分配误差？
??? note "答案"
    两个截断各控制在 \(\varepsilon/2\) 内。
### 习题 4 {#pr-u-10-44-02-04}
充分性先固定什么？
??? note "答案"
    先固定参数，得到实数 Cauchy 族。
### 习题 5 {#pr-u-10-44-02-05}
怎样恢复一致性？
??? note "答案"
    令远端截断趋于极限并保留统一估计。
### 习题 6 {#pr-u-10-44-02-06}
判据是否允许条件收敛？
??? note "答案"
    允许，因为控制的是尾积分绝对值而非绝对值积分。
### 习题 7 {#pr-u-10-44-02-07}
反证失败时要构造什么？
??? note "答案"
    远端截断与参数，使尾积分保持不小。
### 习题 8 {#pr-u-10-44-02-08}
奇端点版本比较哪两个截断？
??? note "答案"
    比较 \(a+\eta\) 与 \(a+\delta\)。
### 习题 9 {#pr-u-10-44-02-09}
统一尾项有什么优势？
??? note "答案"
    不必预先知道极限函数。
### 习题 10 {#pr-u-10-44-02-10}
判据是充分还是必要？
??? note "答案"
    二者都是，即充要条件。
