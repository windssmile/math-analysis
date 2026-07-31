---
title: Borel 集、零测集及其子集怎样进入 Lebesgue 可测世界？
unit_id: u-11-47-05
hours: {theory: 1.00, applied: 0.50}
difficulty: 4
prerequisites: {book: [u-11-46-04, u-11-46-05, u-11-47-03, u-11-47-04], higher_algebra: [], analytic_geometry: [], python: []}
capabilities: [borel_sets, lebesgue_measurable_sets, measure_completeness]
learning_goals: [定义 Borel σ-代数, 证明开集可测, 证明 Lebesgue 测度完备]
content_standard: 2
---
# Borel 集、零测集及其子集怎样进入 Lebesgue 可测世界？ {#u-11-47-05}
## 先备知识
熟悉区间外测度、零测集、可测 σ-代数和 Lebesgue 测度。
## 学习目标
区分 Borel 集与 Lebesgue 可测集，并理解完备性。
## 牵引问题
从开区间生成的集合世界，是否自动包含零测集的所有子集？
## 探索与猜想
开集由可数个区间组成而可测；零测集的任意子集也可测，这使 Lebesgue 世界更完备。
## 概念与理论
### 障碍
拓扑生成和测度完备是不同闭合要求。
### 证明路线
先证明区间可测，再生成 Borel σ-代数，最后用零测性证明完备。
### 逐步证明 {#thm-u-11-47-05-borel-lebesgue}
对区间 (I) 和任意 (T)，分别覆盖 (T\cap I) 与 (T\setminus I)，利用区间端点的
有序性和第 46 章长度结论可得 Carathéodory 分裂，故区间可测。每个开集是至多可数个
两两不交开区间之并，所以开集可测。

由所有开集生成的 σ-代数称 Borel σ-代数 \(\mathcal B(\mathbb R)\)。由于 Lebesgue
可测集族是包含开集的 σ-代数，\(\mathcal B(\mathbb R)\subseteq\mathcal L\)。

若 (N\in\mathcal L\) 且 (m(N)=0\)，任意 (A\subseteq N\) 由单调性满足 (m^*(A)=0\)，
因而 (A\in\mathcal L\)。所以 Lebesgue 测度是完备的：零测集的任意子集都可测。
Lebesgue σ-代数可理解为 Borel σ-代数加入所有 Borel 零测集子集后完成的集合世界。
### 假设用在何处
区间可测和 σ-代数封闭包含所有 Borel 集；外测度单调性保证零集子集仍为零。
### 失败边界
Borel 测度本身若只定义在 Borel 集上并不自动完备；Borel 与 Lebesgue 可测不能混称。
## 例题与迁移
### 例 1：闭集 {#ex-u-11-47-05-closed}
闭集是开集补集，因此是 Borel 集，也 Lebesgue 可测。
### 例 2：Cantor 集 {#ex-u-11-47-05-cantor}
标准 Cantor 集闭且测度零；它不可数，说明“零测”远大于“可数”。它的每个子集都
Lebesgue 可测，但不必都是 Borel 集。
## 即时检验与回望
### 即时检验 1
Borel 集为何一定 Lebesgue 可测？
??? note "答案"
    Lebesgue 可测集构成包含所有开集的 σ-代数。
### 即时检验 2
完备性说的是什么？
??? note "答案"
    每个零测可测集的任意子集仍可测且测度为零。
## 常见误区与后续
- Borel 集都 Lebesgue 可测，反向并不成立。
- 完备性不是实数完备性，而是零测集子集的闭合性质。
## 习题与答案
### 习题 1 {#pr-u-11-47-05-01}
定义 Borel σ-代数。
??? note "答案"
    由 \(\mathbb R\) 中开集生成的最小 σ-代数。
### 习题 2 {#pr-u-11-47-05-02}
闭集为何是 Borel 集？
??? note "答案"
    它是开集的补集。
### 习题 3 {#pr-u-11-47-05-03}
可数集是 Borel 集吗？
??? note "答案"
    是，单点闭，可数并仍 Borel。
### 习题 4 {#pr-u-11-47-05-04}
可数集的任意子集可测吗？
??? note "答案"
    可测；子集仍可数，也由完备性得到。
### 习题 5 {#pr-u-11-47-05-05}
Cantor 集为何可测？
??? note "答案"
    它是闭集，故 Borel 可测。
### 习题 6 {#pr-u-11-47-05-06}
不可数集合能是零测集吗？
??? note "答案"
    能，Cantor 集即例子。
### 习题 7 {#pr-u-11-47-05-07}
Lebesgue 测度完备吗？
??? note "答案"
    完备。
### 习题 8 {#pr-u-11-47-05-08}
Borel 集和 Lebesgue 可测集相同吗？
??? note "答案"
    不相同；后者还包含零测 Borel 集的所有子集。
### 习题 9 {#pr-u-11-47-05-09}
零测集的任意子集测度是多少？
??? note "答案"
    0。
### 习题 10 {#pr-u-11-47-05-10}
本章最终得到什么对象？
??? note "答案"
    Lebesgue 可测 σ-代数及其上的完备可数可加 Lebesgue 测度。
