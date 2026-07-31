---
title: Jacobian、梯度与条件数怎样描述敏感性？
unit_id: u-07-29-05
hours: {theory: 1.25, applied: 0.50}
difficulty: 4
prerequisites: {book: [Fréchet 微分, 链式法则], higher_algebra: [矩阵范数, 逆矩阵], analytic_geometry: [梯度法向], python: []}
capabilities: [jacobian_orientation, gradient_geometry, condition_number]
learning_goals: [由导数映射得到 Jacobian, 解释梯度方向, 区分问题敏感性与算法稳定性]
content_standard: 2
---

# Jacobian、梯度与条件数怎样描述敏感性？ {#u-07-29-05}

## 先备知识
掌握 Fréchet 导数、矩阵表示、链式法则与算子范数。

## 学习目标
1. 正确排列 Jacobian；2. 解释梯度的几何意义；3. 用条件数描述局部输入敏感性。

## 牵引问题
同一个模型可能导数不大却因尺度选择显得病态。怎样区分模型本身敏感与算法实现不稳？

## 探索与猜想
对 \(f:\mathbb R^n\to\mathbb R^m\)，导数矩阵的第 \(i,j\) 项是
\(\partial f_i/\partial x_j\)。它把输入列向量增量映为输出列向量增量。

## 概念与理论

### Jacobian 与梯度 {#def-u-07-29-05-jacobian}
\[
J_f(a)=\begin{pmatrix}
\partial_1f_1&\cdots&\partial_nf_1\\
\vdots&&\vdots\\
\partial_1f_m&\cdots&\partial_nf_m
\end{pmatrix},\qquad Df(a)h=J_f(a)h.
\]
实值函数的 Jacobian 是 \(1\times n\) 行矩阵；梯度
\(\nabla f(a)\) 约定为对应的列向量，于是 \(Df(a)h=\nabla f(a)^\mathsf Th\)。
Cauchy–Schwarz 表明单位方向中，梯度方向给出最大的方向增长率。

### 局部条件数 {#def-u-07-29-05-condition}
线性系统或局部可逆方阵 \(A\) 的绝对放大由 \(\|A\|\) 控制；相对敏感性常用
\[
\kappa(A)=\|A\|\,\|A^{-1}\|
\]
衡量。矩阵奇异时条件数视为无穷。条件数描述**问题敏感性**：输入误差可能被放大多少。
**算法稳定性**描述实现是否额外放大舍入和离散误差，二者不能混同。

变量与输出重新缩放会改变数值条件数，所以报告必须同时说明范数和尺度。

## 例题与迁移
### 例 1：梯度与等值线 {#ex-u-07-29-05-level}
若 \(f(x,y)=x^2+4y^2\)，梯度 \((2x,8y)\) 与正则等值椭圆切向量正交。
### 例 2：近奇异缩放 {#ex-u-07-29-05-near-singular}
\(A=\operatorname{diag}(1,\varepsilon)\) 的无穷范数条件数为 \(1/|\varepsilon|\)；
第二坐标的输出误差反求输入时被放大。

## 即时检验与回望
### 即时检验 1
\(f:\mathbb R^3\to\mathbb R^2\) 的 Jacobian 尺寸？
??? note "答案"
    \(2\times3\)，输出分量对应行，输入坐标对应列。
### 即时检验 2
条件数大是否证明某个算法不稳定？
??? note "答案"
    不能；它说明问题敏感，算法还可能稳定地达到该问题允许的精度。

## 常见误区与后续
- 梯度是列向量约定，导数是线性泛函；写公式时要核验转置。
- 条件数依赖范数和尺度。
- Jacobian 数值可逆不等于已满足反函数定理的邻域条件。

## 习题与答案
### 习题 1 {#pr-u-07-29-05-01}
求 \(f(x,y)=(x^2+y,xy)\) 的 Jacobian。
??? note "答案"
    \(\begin{pmatrix}2x&1\\y&x\end{pmatrix}\)。
### 习题 2 {#pr-u-07-29-05-02}
求 \(x^2+y^2\) 的梯度。
??? note "答案"
    \((2x,2y)^\mathsf T\)。
### 习题 3 {#pr-u-07-29-05-03}
证明梯度与正则等值线切向量正交。
??? note "答案"
    沿等值线复合函数为常数，链式法则给 \(\nabla f^\mathsf Tv=0\)。
### 习题 4 {#pr-u-07-29-05-04}
单位方向最大方向导数是多少？
??? note "答案"
    \(\|\nabla f(a)\|_2\)，在梯度非零时由其单位方向取得。
### 习题 5 {#pr-u-07-29-05-05}
奇异矩阵为何无有限条件数？
??? note "答案"
    逆映射不存在，某些非零输入方向被压到零，反问题无法唯一恢复。
### 习题 6 {#pr-u-07-29-05-06}
求 \(\operatorname{diag}(2,1)\) 的无穷范数条件数。
??? note "答案"
    \(\|A\|_\infty=2,\|A^{-1}\|_\infty=1\)，故为 \(2\)。
### 习题 7 {#pr-u-07-29-05-07}
链式法则下 Jacobian 怎样相乘？
??? note "答案"
    \(J_{g\circ f}=J_g(f(a))J_f(a)\)。
### 习题 8 {#pr-u-07-29-05-08}
为何缩放变量会改变条件数？
??? note "答案"
    缩放等于在 Jacobian 右乘尺度矩阵，改变其各方向放大比例。
### 习题 9 {#pr-u-07-29-05-09}
区分绝对与相对扰动。
??? note "答案"
    绝对扰动看 \(\|\Delta x\|\)，相对扰动再除以基准量 \(\|x\|\)。
### 习题 10 {#pr-u-07-29-05-10}
为什么报告条件数时要写范数？
??? note "答案"
    不同算子范数给出不同数值；不写范数就缺少可复核定义。

## 小结
Jacobian 是导数映射的坐标矩阵，梯度编码实值函数的一阶几何，条件数刻画局部问题
敏感性。三者都必须与维度、范数和尺度一起解释。

