---
title: 为什么集合运算必须对可数过程封闭？
unit_id: u-11-47-01
hours: {theory: 1.25, applied: 0.25}
difficulty: 3
prerequisites: {book: [第 1 章, u-11-46-05], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [sigma_algebra_definition, countable_set_operations, generated_sigma_algebra]
learning_goals: [定义 σ-代数, 推导可数交封闭, 解释生成 σ-代数]
content_standard: 2
---
# 为什么集合运算必须对可数过程封闭？ {#u-11-47-01}
## 先备知识
熟悉补集、并、交、De Morgan 律与可数集合。
## 学习目标
掌握 σ-代数的定义和最小生成思想。
## 牵引问题
若每个集合都可测，为什么它们的极限集合也应可测？
## 探索与猜想
函数列会产生可数并交，因此允许的集合类必须对补集和可数并封闭。
## 概念与理论
### 障碍
只对有限运算封闭的集合代数无法稳定承接 \(\limsup E_n\) 与 \(\liminf E_n\)。
### 证明路线
冻结补集和可数并两项公理，再由 De Morgan 律推出其余运算。
### 逐步证明 {#def-u-11-47-01-sigma}
全集 (X) 上的集合族 \(\mathcal A\) 称为 σ-代数，若：

1. (X\in\mathcal A\)；
2. (E\in\mathcal A\Rightarrow E^c\in\mathcal A\)；
3. (E_n\in\mathcal A\Rightarrow\bigcup_{n\ge1}E_n\in\mathcal A\)。

于是 \(\varnothing=X^c\in\mathcal A\)，且由 De Morgan 律，
\(\bigcap_nE_n=(\bigcup_nE_n^c)^c\in\mathcal A\)。有限并交只是补空集后的特例。
给定集合族 \(\mathcal C\)，所有包含 \(\mathcal C\) 的 σ-代数之交仍是 σ-代数，称
\(\sigma(\mathcal C)\)，即由 \(\mathcal C\) 生成的最小 σ-代数。
### 假设用在何处
补集配合可数并产生可数交；任意 σ-代数之交逐项保留三条公理。
### 失败边界
σ-代数只规定“哪些集合允许”，没有给出大小；测度是下一层结构。
## 例题与迁移
### 例 1：最小 σ-代数 {#ex-u-11-47-01-trivial}
\(\{\varnothing,X\}\) 是最小 σ-代数。
### 例 2：单个集合生成 {#ex-u-11-47-01-one-set}
若 \(\varnothing\ne E\ne X\)，则 \(\sigma(\{E\})=\{\varnothing,E,E^c,X\}\)。
## 即时检验与回望
### 即时检验 1
为何可数交不必单列为公理？
??? note "答案"
    它由补集封闭、可数并封闭和 De Morgan 律推出。
### 即时检验 2
生成 σ-代数为什么存在？
??? note "答案"
    至少幂集包含生成族；所有包含它的 σ-代数之交仍是 σ-代数。
## 常见误区与后续
- σ 表示可数运算，不表示任意不可数并。
- 集合属于 σ-代数不自动给出其测度值。
## 习题与答案
### 习题 1 {#pr-u-11-47-01-01}
写出 σ-代数三条公理。
??? note "答案"
    含全集、对补集封闭、对可数并封闭。
### 习题 2 {#pr-u-11-47-01-02}
证明空集属于 σ-代数。
??? note "答案"
    空集是全集的补集。
### 习题 3 {#pr-u-11-47-01-03}
证明有限交封闭。
??? note "答案"
    用 De Morgan 律把有限交写成有限个补集之并的补集。
### 习题 4 {#pr-u-11-47-01-04}
幂集是否是 σ-代数？
??? note "答案"
    是，它包含所有子集，当然对所需运算封闭。
### 习题 5 {#pr-u-11-47-01-05}
两个 σ-代数的并一定是 σ-代数吗？
??? note "答案"
    不一定；跨两个族取并可能不属于任一族。
### 习题 6 {#pr-u-11-47-01-06}
两个 σ-代数的交呢？
??? note "答案"
    一定是。
### 习题 7 {#pr-u-11-47-01-07}
写出 \(\limsup E_n\) 的集合表达式。
??? note "答案"
    \(\bigcap_N\bigcup_{n\ge N}E_n\)。
### 习题 8 {#pr-u-11-47-01-08}
为何有限代数不够处理上题？
??? note "答案"
    表达式包含可数并和可数交。
### 习题 9 {#pr-u-11-47-01-09}
最小 σ-代数是什么？
??? note "答案"
    \(\{\varnothing,X\}\)。
### 习题 10 {#pr-u-11-47-01-10}
σ-代数是否要求对不可数并封闭？
??? note "答案"
    不要求。

