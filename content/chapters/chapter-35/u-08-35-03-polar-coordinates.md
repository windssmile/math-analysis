---
title: 极坐标怎样处理圆形与径向对称区域？
unit_id: u-08-35-03
hours: {theory: 1.5, applied: 0.25}
difficulty: 3
prerequisites: {book: [重积分换元公式], higher_algebra: [二阶行列式], analytic_geometry: [极坐标], python: []}
capabilities: [polar_jacobian, radial_integral, angle_range]
learning_goals: [推导极坐标面积元, 选择不重复角度范围, 计算圆形区域积分]
content_standard: 2
---

# 极坐标怎样处理圆形与径向对称区域？ {#u-08-35-03}

## 先备知识
掌握换元定理、三角函数和圆形区域。

## 学习目标
从坐标映射推导 \(dA=r\,dr\,d\theta\)，并检查覆盖范围。

## 牵引问题
把 \(x,y\) 换成 \(r,\theta\) 后，为什么不能只把 \(dx\,dy\) 写成 \(dr\,d\theta\)？

## 探索与猜想
半径增加相同量时，外圈扇形比内圈更宽，面积元必须随 \(r\) 增长。

## 概念与理论

极坐标映射
\[
T(r,\theta)=(r\cos\theta,r\sin\theta)
\]
的 Jacobian 为
\[
DT=\begin{pmatrix}\cos\theta&-r\sin\theta\\
\sin\theta&r\cos\theta\end{pmatrix},\qquad
\det DT=r(\cos^2\theta+\sin^2\theta)=r.
\]
因此在 \(r\ge0\) 且角度不重复覆盖的参数域上，
\[
\iint_Df(x,y)\,dA
=\iint_Gf(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
\]
原点处 Jacobian 为零，但它位于参数域边界的退化集合；不能因此忽略其他内部点的
非退化检查。完整圆通常取任意长度 \(2\pi\) 的半开角度范围。

## 例题与迁移

### 例 1：圆盘面积 {#ex-u-08-35-03-disk}
\[
\int_0^{2\pi}\int_0^R r\,dr\,d\theta=\pi R^2.
\]

### 例 2：环形扇区 {#ex-u-08-35-03-sector}
若 \(a\le r\le b,\ \alpha\le\theta\le\beta\)，面积为
\((\beta-\alpha)(b^2-a^2)/2\)，角度必须用弧度。

## 即时检验与回望

### 即时检验 1
面积元中的 \(r\) 来自哪里？
??? note "答案"
    来自极坐标映射 Jacobian 行列式的绝对值。

### 即时检验 2
\(0\le\theta\le4\pi\) 有何问题？
??? note "答案"
    除退化边界外，圆盘被覆盖两次，积分会重复计数。

## 常见误区与后续
- \(r\) 是 Jacobian 因子，不是被积函数的一部分。
- 同时变换区域、函数和面积元。
- 径向对称函数可先完成角度积分。

## 习题与答案

### 习题 1 {#pr-u-08-35-03-01}
单位圆盘面积是多少？
??? note "答案"
    \(\pi\)。

### 习题 2 {#pr-u-08-35-03-02}
半径 \(1\) 到 \(2\) 的圆环面积？
??? note "答案"
    \(3\pi\)。

### 习题 3 {#pr-u-08-35-03-03}
第一象限圆盘的角度范围？
??? note "答案"
    \(0\le\theta\le\pi/2\)。

### 习题 4 {#pr-u-08-35-03-04}
\(x^2+y^2\) 在极坐标中是什么？
??? note "答案"
    \(r^2\)。

### 习题 5 {#pr-u-08-35-03-05}
为什么角度要用弧度？
??? note "答案"
    三角函数导数与 Jacobian 推导按弧度成立。

### 习题 6 {#pr-u-08-35-03-06}
计算单位圆盘上 \(x^2+y^2\) 的积分。
??? note "答案"
    \(\int_0^{2\pi}\int_0^1r^3drd\theta=\pi/2\)。

### 习题 7 {#pr-u-08-35-03-07}
极坐标在原点是否一一对应？
??? note "答案"
    不是，所有角度都给同一点；它作为边界退化点处理。

### 习题 8 {#pr-u-08-35-03-08}
负半径为何通常不进入标准参数域？
??? note "答案"
    它与角度平移 \(\pi\) 重复表示同一点，破坏一一对应。

### 习题 9 {#pr-u-08-35-03-09}
径向函数 \(g(r)\) 在圆盘上的积分通式？
??? note "答案"
    \(2\pi\int_0^R g(r)r\,dr\)。

### 习题 10 {#pr-u-08-35-03-10}
极坐标换元的四项核验是什么？
??? note "答案"
    半径范围、角度范围、覆盖次数、Jacobian 因子。
