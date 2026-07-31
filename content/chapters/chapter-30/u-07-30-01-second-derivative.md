---
title: 二阶微分和 Hessian 为什么是双线性对象？
unit_id: u-07-30-01
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites: {book: [Fréchet 微分, 链式法则, 连续偏导], higher_algebra: [双线性映射, 矩阵], analytic_geometry: [], python: []}
capabilities: [second_derivative, hessian_representation, mixed_partial_symmetry]
learning_goals: [把导数再次微分, 用 Hessian 表示二阶微分, 陈述混合偏导相等的充分条件]
content_standard: 2
---

# 二阶微分和 Hessian 为什么是双线性对象？ {#u-07-30-01}

## 先备知识
掌握 Fréchet 导数、线性映射空间、连续偏导与矩阵表示。

## 学习目标
1. 把 \(D^2f(a)\) 识别为双线性映射；2. 正确写出 Hessian；3. 不遗漏混合偏导
相等所需的连续性条件。

## 牵引问题
一阶导数把增量变成线性主部；这个线性主部随基点怎样变化，为什么答案需要两个方向？

## 探索与猜想
若 \(f:\mathbb R^n\to\mathbb R\)，则 \(Df\) 的值本身是线性泛函。
对 \(Df\) 再求导会先接收一个“基点移动方向” \(u\)，再把所得线性泛函作用于
“函数增量方向” \(v\)，所以自然出现两个方向。

## 概念与理论

### 二阶 Fréchet 导数 {#def-u-07-30-01-second}
设 \(U\subset\mathbb R^n\) 开，\(f:U\to\mathbb R^m\)，且 \(Df\) 在 \(a\) 可微。
定义
\[
D^2f(a)=D(Df)(a)\in\mathcal L(\mathbb R^n,\mathcal L(\mathbb R^n,\mathbb R^m)).
\]
通过 \(D^2f(a)[u,v]=(D(Df)(a)u)v\)，它等价于从
\(\mathbb R^n\times\mathbb R^n\) 到 \(\mathbb R^m\) 的连续双线性映射。
双线性不是记号游戏：固定任一变量，关于另一变量都线性。

### Hessian 矩阵 {#def-u-07-30-01-hessian}
实值函数 \(f\) 的二阶导数在标准基下由 Hessian 表示：
\[
H_f(a)=\bigl(\partial_{ij}f(a)\bigr)_{i,j=1}^n,\qquad
D^2f(a)[u,v]=u^\mathsf T H_f(a)v.
\]
向量值函数则每个分量有一个 Hessian；不能把它误压成单个 \(n\times n\) 矩阵。

### 混合偏导的对称性 {#thm-u-07-30-01-schwarz}
若 \(\partial_{ij}f,\partial_{ji}f\) 在 \(a\) 的某邻域存在且连续，则
\[
\partial_{ij}f(a)=\partial_{ji}f(a).
\]
证明取只改变第 \(i,j\) 坐标的矩形增量，二次使用一元中值定理，再令矩形边长趋零。
连续性把两个中间点上的混合偏导送到同一点 \(a\)。因此 \(H_f(a)\) 对称，
\(D^2f(a)[u,v]=D^2f(a)[v,u]\)。

条件必须陈述：混合偏导仅存在，并不足以无条件交换次序。

## 例题与迁移
### 例 1：一个二次函数 {#ex-u-07-30-01-quadratic}
\(f(x,y)=x^2+3xy+2y^2\) 有
\[
H_f=\begin{pmatrix}2&3\\3&4\end{pmatrix},\quad
D^2f[(u_1,u_2),(v_1,v_2)]
=2u_1v_1+3u_1v_2+3u_2v_1+4u_2v_2.
\]

### 例 2：向量值映射 {#ex-u-07-30-01-vector}
\(F(x,y)=(xy,e^{x+y})\) 的二阶导数有两个分量双线性形式；第一分量 Hessian 为
\(\begin{pmatrix}0&1\\1&0\end{pmatrix}\)，第二分量 Hessian 为
\(e^{x+y}\begin{pmatrix}1&1\\1&1\end{pmatrix}\)。

## 即时检验与回望
### 即时检验 1
\(D^2f(a)[u,v]\) 为什么不是通常意义上的向量点积？
??? note "答案"
    它由函数决定，是对两个方向分别线性的映射；只有选定坐标后才由 Hessian 给出矩阵表达。

### 即时检验 2
混合偏导在一点都存在，能否直接断言 Hessian 对称？
??? note "答案"
    不能。本节使用邻域内混合偏导存在且在该点连续这一充分条件。

## 常见误区与后续
- \(Df(a)\) 是线性映射，\(D^2f(a)\) 是双线性映射，不是“把矩阵逐项求导后仍得到矩阵”。
- Hessian 只直接表示实值函数的二阶导数。
- 本节只建立二阶结构，不从矩阵符号推出极值结论。

## 习题与答案
### 习题 1 {#pr-u-07-30-01-01}
求 \(f(x,y)=x^3y+y^2\) 的 Hessian。
??? note "答案"
    \(\begin{pmatrix}6xy&3x^2\\3x^2&2\end{pmatrix}\)。

### 习题 2 {#pr-u-07-30-01-02}
写出上题 \(D^2f(a)[u,v]\)。
??? note "答案"
    令 \(H=H_f(a)\)，则为 \(u^\mathsf THv\)。

### 习题 3 {#pr-u-07-30-01-03}
证明连续双线性映射 \(B\) 满足 \(\|B[u,v]\|\le C\|u\|\|v\|\)。
??? note "答案"
    在两个单位球的紧乘积上取 \(\|B\|\) 的最大值，再用双线性缩放。

### 习题 4 {#pr-u-07-30-01-04}
若 \(f(x)=c^\mathsf Tx\)，求 \(D^2f\)。
??? note "答案"
    恒为零双线性映射。

### 习题 5 {#pr-u-07-30-01-05}
若 \(f(x)=\frac12x^\mathsf TAx\)，其中 \(A\) 不必对称，求 Hessian。
??? note "答案"
    \(H_f=(A+A^\mathsf T)/2\)。

### 习题 6 {#pr-u-07-30-01-06}
解释为什么反对称矩阵不影响 \(x^\mathsf TAx\)。
??? note "答案"
    反对称部分 \(K\) 满足标量 \(x^\mathsf TKx=-(x^\mathsf TKx)\)，故为零。

### 习题 7 {#pr-u-07-30-01-07}
求 \(f(x,y)=e^{xy}\) 在原点的 Hessian。
??? note "答案"
    \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\)。

### 习题 8 {#pr-u-07-30-01-08}
给出混合偏导交换时必须检查的一项条件。
??? note "答案"
    例如两混合偏导在该点邻域存在并在该点连续。

### 习题 9 {#pr-u-07-30-01-09}
实值 \(C^2\) 函数的 \(D^2f(a)\) 有何对称性？
??? note "答案"
    \(D^2f(a)[u,v]=D^2f(a)[v,u]\)。

