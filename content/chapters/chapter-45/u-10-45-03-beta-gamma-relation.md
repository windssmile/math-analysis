---
title: Beta–Gamma 关系怎样由重积分与换元推出？
unit_id: u-10-45-03
hours: {theory: 1.25, applied: 0.25}
difficulty: 5
prerequisites: {book: [u-10-45-01, u-10-45-02, 第 34–35 章], higher_algebra: [], analytic_geometry: [第一象限, 极坐标], python: []}
capabilities: [beta_gamma_relation, first_quadrant_transform, polar_jacobian]
learning_goals: [把 Gamma 乘积写成二重积分, 完成第一象限极坐标换元, 推导 Beta–Gamma 关系]
content_standard: 2
---
# Beta–Gamma 关系怎样由重积分与换元推出？ {#u-10-45-03}
## 先备知识
熟悉非负截断积分、经典 Fubini、二重积分换元与极坐标 Jacobian。
## 学习目标
能在有限截断上逐步换元，并由单调扩域得到特殊函数关系。
## 牵引问题
两个一维 Gamma 积分的乘积怎样显现 Beta 积分？
## 探索与猜想
平方根极坐标把指数核合并为径向项，角向比例则产生 Beta 核。
## 概念与理论
### 第一象限二重积分 {#thm-u-10-45-03-product}
对 \(p,q>0\)，先在有限矩形上使用经典 Fubini，再让矩形单调扩张：

\[
\Gamma(p)\Gamma(q)
=\int_0^\infty\int_0^\infty x^{p-1}y^{q-1}e^{-(x+y)}\,dx\,dy.
\]

令 \(x=r^2\cos^2\theta,\ y=r^2\sin^2\theta\)，其中 \(r>0\)、\(0<\theta<\pi/2\)。其 Jacobian 绝对值为 \(4r^3\sin\theta\cos\theta\)。
### 变量分离 {#thm-u-10-45-03-polar}
径向换元 \(u=r^2\) 给出 \(\frac12\Gamma(p+q)\)，角向令 \(z=\cos^2\theta\) 给出 \(\frac12B(p,q)\)。系数合并后

\[
\Gamma(p)\Gamma(q)=\Gamma(p+q)B(p,q),
\qquad
B(p,q)=\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}.
\]

所有换元先在远离坐标轴的有界区域完成，再借非负积分的单调扩张取极限。
## 例题与迁移
### 例 1：整数参数 {#ex-u-10-45-03-integers}
\(B(2,3)=\Gamma(2)\Gamma(3)/\Gamma(5)=1/12\)。
### 例 2：对称性 {#ex-u-10-45-03-symmetry}
右端关于 \(p,q\) 对称，再次得到 \(B(p,q)=B(q,p)\)。
## 即时检验与回望
### 即时检验 1
为何先在有限区域换元？
??? note "答案"
    经典 Fubini 与换元可直接适用，反常极限随后处理。
### 即时检验 2
Jacobian 可否遗漏？
??? note "答案"
    不可，它决定径向幂次和最终系数。
## 常见误区与后续
- 极坐标变换还必须变换面积元。
- 更广参数范围需后续函数论，本章只处理正实参数。
## 习题与答案
### 习题 1 {#pr-u-10-45-03-01}
乘积积分位于哪个象限？
??? note "答案"
    第一象限。
### 习题 2 {#pr-u-10-45-03-02}
\(x+y\) 换元后是什么？
??? note "答案"
    \(r^2\)。
### 习题 3 {#pr-u-10-45-03-03}
角度范围是什么？
??? note "答案"
    \(0<\theta<\pi/2\)。
### 习题 4 {#pr-u-10-45-03-04}
Jacobian 是多少？
??? note "答案"
    \(4r^3\sin\theta\cos\theta\)。
### 习题 5 {#pr-u-10-45-03-05}
径向积分产生什么？
??? note "答案"
    Gamma 型因子。
### 习题 6 {#pr-u-10-45-03-06}
角向积分产生什么？
??? note "答案"
    Beta 型因子。
### 习题 7 {#pr-u-10-45-03-07}
写出关系式。
??? note "答案"
    \(B(p,q)=\Gamma(p)\Gamma(q)/\Gamma(p+q)\)。
### 习题 8 {#pr-u-10-45-03-08}
\(B(2,3)\) 是多少？
??? note "答案"
    \(1/12\)。
### 习题 9 {#pr-u-10-45-03-09}
为何可以单调扩域？
??? note "答案"
    核非负且有限截断积分单调增加。
### 习题 10 {#pr-u-10-45-03-10}
证明的参数条件是什么？
??? note "答案"
    \(p,q>0\)。
??? note "答案"
    该条件同时保证 Gamma 与 Beta 积分收敛。
