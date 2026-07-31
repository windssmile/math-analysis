---
title: 柱面、球面坐标怎样处理三维区域？
unit_id: u-08-35-04
hours: {theory: 1.5, applied: 0.25}
difficulty: 3
prerequisites: {book: [三重积分, 极坐标换元], higher_algebra: [三阶行列式], analytic_geometry: [球面, 圆柱面, 圆锥面], python: []}
capabilities: [cylindrical_coordinates, spherical_coordinates, coordinate_selection]
learning_goals: [推导两类体积元, 设置球面坐标范围, 按对称性选择坐标]
content_standard: 2
---

# 柱面、球面坐标怎样处理三维区域？ {#u-08-35-04}

## 先备知识
掌握三重积分、极坐标 Jacobian 与空间曲面。

## 学习目标
从坐标映射推导柱面、球面体积元，而不是背诵。

## 牵引问题
圆柱对称和球对称分别保留哪些变量，体积元为什么不同？

## 探索与猜想
柱面坐标是在 \(xy\) 平面使用极坐标并保留 \(z\)；球面坐标还要把半径方向与
极角分离。

## 概念与理论

柱面坐标
\[
(x,y,z)=(r\cos\theta,r\sin\theta,z)
\]
的导数矩阵为
\[
\left(\begin{smallmatrix}
\cos\theta&-r\sin\theta&0\\
\sin\theta&r\cos\theta&0\\
0&0&1
\end{smallmatrix}\right),
\quad \det=r,
\]
故 \(dV=r\,dr\,d\theta\,dz\)（次序可按区域调整）。

球面坐标取
\[
(x,y,z)=(\rho\sin\phi\cos\theta,\rho\sin\phi\sin\theta,\rho\cos\phi).
\]
直接对三列偏导计算三重积：
\[
\det\frac{\partial(x,y,z)}{\partial(\rho,\phi,\theta)}
=\rho^2\sin\phi.
\]
因此 \(dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta\)。标准范围为
\(\rho\ge0,\ 0\le\phi\le\pi\)，\(\theta\) 取长度 \(2\pi\) 的区间。

| 区域特征 | 优先坐标 | 核验 |
|---|---|---|
| 绕 \(z\) 轴圆柱对称 | 柱面坐标 | \(r,\theta,z\) 范围 |
| 以原点球对称 | 球面坐标 | \(\rho,\phi,\theta\) 覆盖 |
| 直角边界简单 | 直角坐标 | 不为换元而换元 |

## 例题与迁移

### 例 1：球体体积 {#ex-u-08-35-04-ball}
\[
\int_0^{2\pi}\int_0^\pi\int_0^R\rho^2\sin\phi\,d\rho\,d\phi\,d\theta
=\frac{4\pi R^3}{3}.
\]

### 例 2：圆锥内球扇形 {#ex-u-08-35-04-cone}
\(0\le\phi\le\phi_0,\ 0\le\rho\le R\) 描述绕正 \(z\) 轴的球扇形；角度范围
直接表达圆锥边界。

## 即时检验与回望

### 即时检验 1
球面坐标的 \(\sin\phi\) 为什么不可漏？
??? note "答案"
    纬圈在两极收缩，它是 Jacobian 行列式的一部分。

### 即时检验 2
整球的 \(\phi\) 范围是什么？
??? note "答案"
    从 \(0\) 到 \(\pi\)。

## 常见误区与后续
- 不同教材可能交换 \(\phi,\theta\) 名称，必须看坐标定义。
- 轴线和原点的退化不等于可任意重复覆盖。
- 选坐标看区域与被积函数共同的对称性。

## 习题与答案

### 习题 1 {#pr-u-08-35-04-01}
柱体 \(r\le R,0\le z\le h\) 的体积？
??? note "答案"
    \(\pi R^2h\)。

### 习题 2 {#pr-u-08-35-04-02}
上半球的 \(\phi\) 范围？
??? note "答案"
    \(0\le\phi\le\pi/2\)。

### 习题 3 {#pr-u-08-35-04-03}
\(x^2+y^2+z^2\) 在球面坐标中是什么？
??? note "答案"
    \(\rho^2\)。

### 习题 4 {#pr-u-08-35-04-04}
\(x^2+y^2\) 在柱面坐标中是什么？
??? note "答案"
    \(r^2\)。

### 习题 5 {#pr-u-08-35-04-05}
球面 Jacobian 在两极为何为零？
??? note "答案"
    所有方位角在极轴处汇合，参数化退化。

### 习题 6 {#pr-u-08-35-04-06}
计算半径 \(R\) 球内 \(\rho^2\) 的积分。
??? note "答案"
    \(4\pi\int_0^R\rho^4d\rho=4\pi R^5/5\)。

### 习题 7 {#pr-u-08-35-04-07}
圆柱面 \(x^2+y^2=4\) 对应什么？
??? note "答案"
    \(r=2\)。

### 习题 8 {#pr-u-08-35-04-08}
圆锥 \(\phi=\phi_0\) 表示什么？
??? note "答案"
    与正 \(z\) 轴夹角固定的圆锥面。

### 习题 9 {#pr-u-08-35-04-09}
球坐标能否取 \(0\le\theta\le4\pi\)？
??? note "答案"
    不宜，通常导致二重覆盖。

### 习题 10 {#pr-u-08-35-04-10}
何时保留直角坐标更好？
??? note "答案"
    当边界是简单矩形/长方体且函数无圆形或球形对称时。

### 习题 11 {#pr-u-08-35-04-11}
坐标选择表的三项检查是什么？
??? note "答案"
    区域对称、被积函数形式、参数范围与覆盖。
