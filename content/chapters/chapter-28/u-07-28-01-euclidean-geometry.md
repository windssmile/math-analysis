---
title: 向量、内积、范数和距离怎样描述多维几何？
unit_id: u-07-28-01
hours: {theory: 1.25, applied: 0.50}
difficulty: 3
prerequisites: {book: [实数绝对值, 有限和, 向量坐标], higher_algebra: [线性组合], analytic_geometry: [点积], python: []}
capabilities: [euclidean_norm, norm_comparison, geometric_bounds]
learning_goals: [证明 Cauchy–Schwarz 不等式, 从内积推出范数和距离, 比较有限维常用范数]
content_standard: 2
---

# 向量、内积、范数和距离怎样描述多维几何？ {#u-07-28-01}

## 先备知识

会使用实数绝对值、平方和与有限求和。所有向量都属于固定的有限维空间
\(\mathbb R^n\)。

## 学习目标

1. 从内积定义长度与距离；
2. 证明 Cauchy–Schwarz 和三角不等式；
3. 比较 \(\ell^1,\ell^2,\ell^\infty\) 范数；
4. 说明有限维等价范数为何给出相同的收敛概念。

## 牵引问题

一元中的 \(|x-y|\) 同时承担距离和误差。多维中每个坐标都可能变化，应怎样把这些
变化压缩为一个可靠的非负数？

## 探索与猜想

对 \(x=(x_1,\ldots,x_n)\)，令
\[
\langle x,y\rangle=\sum_{i=1}^n x_i y_i,\qquad
\|x\|_2=\sqrt{\langle x,x\rangle}.
\]
若长度符合几何直觉，就应有 \(|\langle x,y\rangle|\le \|x\|_2\|y\|_2\)。

## 概念与理论

### Cauchy–Schwarz 不等式 {#thm-u-07-28-01-cauchy-schwarz}

对任意 \(x,y\in\mathbb R^n\)，
\[
|\langle x,y\rangle|\le \|x\|_2\|y\|_2.
\]

**证明。** 若 \(y=0\) 结论显然。否则对任意实数 \(t\)，
\[
0\le \|x-ty\|_2^2
=\|x\|_2^2-2t\langle x,y\rangle+t^2\|y\|_2^2.
\]
这个二次多项式对所有 \(t\) 非负，因此判别式不大于零，整理即得结论。等号当且
仅当 \(x,y\) 线性相关。

由此
\[
\|x+y\|_2^2
=\|x\|_2^2+2\langle x,y\rangle+\|y\|_2^2
\le(\|x\|_2+\|y\|_2)^2,
\]
得到三角不等式。于是 \(d(x,y)=\|x-y\|_2\) 满足距离的非负性、分离性、对称性和
三角不等式。

### 有限维常用范数

\[
\|x\|_1=\sum_{i=1}^n|x_i|,\qquad
\|x\|_\infty=\max_i|x_i|.
\]
逐坐标估计与 Cauchy–Schwarz 给出
\[
\|x\|_\infty\le \|x\|_2\le \|x\|_1,\qquad
\|x\|_1\le \sqrt n\,\|x\|_2,\qquad
\|x\|_2\le\sqrt n\,\|x\|_\infty.
\]

### 有限维范数等价 {#thm-u-07-28-01-norm-equivalence}

上述不等式说明任取 \(\ell^1,\ell^2,\ell^\infty\) 中两种范数，都存在只依赖于维数的
正常数 \(c,C\)，使
\[
c\|x\|_a\le \|x\|_b\le C\|x\|_a.
\]
所以一个误差在某种范数下趋于零，当且仅当它在另外两种范数下趋于零。这一结论
依赖“有限个坐标”；无限维时不能照搬这些常数。

## 例题与迁移

### 例 1：线性观测的误差 {#ex-u-07-28-01-linear-observation}

若观测量为 \(\langle a,x\rangle\)，输入扰动为 \(h\)，则
\[
|\langle a,x+h\rangle-\langle a,x\rangle|
\le \|a\|_2\|h\|_2.
\]
向量 \(a\) 的长度就是该线性观测对 Euclid 扰动的敏感度。

### 例 2：不同范数下的球 {#ex-u-07-28-01-unit-balls}

在 \(\mathbb R^2\) 中，单位 \(\ell^1\) 球是菱形，单位 \(\ell^2\) 球是圆盘，单位
\(\ell^\infty\) 球是正方形。形状不同，但三者定义同一套“趋近于一点”的序列。

## 即时检验与回望

### 即时检验 1

证明 \(|x_i|\le\|x\|_2\)。

??? note "答案"
    因为 \(x_i^2\le\sum_jx_j^2=\|x\|_2^2\)，两边开平方即可。

### 即时检验 2

若 \(\|x\|_\infty<\varepsilon/\sqrt n\)，\(\|x\|_2\) 有何上界？

??? note "答案"
    由 \(\|x\|_2\le\sqrt n\|x\|_\infty\)，得到 \(\|x\|_2<\varepsilon\)。

## 常见误区与后续

- “等价范数”不是说数值相等，而是相互被固定常数控制。
- Cauchy–Schwarz 的等号条件是线性相关，不是必须相等。
- 有限维范数等价不能不加条件地推广到函数空间。

## 习题与答案

### 习题 1 {#pr-u-07-28-01-01}
验证 \(d(x,y)=\|x-y\|_2\) 的三角不等式。
??? note "答案"
    写成 \(\|x-z\|_2=\|(x-y)+(y-z)\|_2\)，应用范数三角不等式。

### 习题 2 {#pr-u-07-28-01-02}
求 \(x=(1,-2,2)\) 的三种常用范数。
??? note "答案"
    \(\|x\|_1=5,\ \|x\|_2=3,\ \|x\|_\infty=2\)。

### 习题 3 {#pr-u-07-28-01-03}
证明 \(\|x\|_2\le\|x\|_1\)。
??? note "答案"
    平方后，\((\sum|x_i|)^2=\sum x_i^2+2\sum_{i<j}|x_ix_j|\ge\sum x_i^2\)。

### 习题 4 {#pr-u-07-28-01-04}
说明 \(\|x\|_1\le n\|x\|_\infty\)。
??? note "答案"
    每个 \(|x_i|\le\|x\|_\infty\)，对 \(n\) 项求和。

### 习题 5 {#pr-u-07-28-01-05}
何时 \(|\langle x,y\rangle|=\|x\|_2\|y\|_2\)？
??? note "答案"
    当且仅当 \(x,y\) 线性相关；包含其中一个为零的情形。

### 习题 6 {#pr-u-07-28-01-06}
证明反向三角不等式 \(|\|x\|_2-\|y\|_2|\le\|x-y\|_2\)。
??? note "答案"
    由 \(\|x\|\le\|x-y\|+\|y\|\) 得一边，交换 \(x,y\) 得另一边。

### 习题 7 {#pr-u-07-28-01-07}
若 \(\|x_k\|_1\to0\)，证明每个坐标趋于零。
??? note "答案"
    \(|(x_k)_i|\le\|x_k\|_1\to0\)。

### 习题 8 {#pr-u-07-28-01-08}
给出 \(\mathbb R^2\) 中 \(\|x\|_1/\|x\|_\infty=2\) 的向量。
??? note "答案"
    任取 \(x=(a,a)\) 且 \(a\ne0\)，比值为 \(2\)。

## 小结

内积产生 Euclid 范数和距离，Cauchy–Schwarz 控制线性观测，三角不等式控制误差传播。
有限维常用范数虽数值不同，却定义相同的收敛与局部概念。
