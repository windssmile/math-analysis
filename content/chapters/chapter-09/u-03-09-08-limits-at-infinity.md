---
title: 自变量趋于无穷时怎样定义函数极限？
unit_id: u-03-09-08
hours:
  theory: 1.5
  applied: 0.5
difficulty: 3
prerequisites:
  book:
  - chapter-05
  - chapter-09
  higher_algebra:
  - 多项式与有理式
  - 绝对值不等式
  analytic_geometry:
  - 实轴上的射线
  python: []
capabilities:
- concepts
- proof
- analytic_calculation
- mathematical_expression
learning_goals:
- 定义自变量趋于正负无穷时的有限极限
- 定义自变量和函数值同时趋于无穷
- 证明基本有理函数的无穷远极限
- 用初等不等式比较多项式增长
content_standard: 2
---

# 自变量趋于无穷时怎样定义函数极限？ {#u-03-09-08}


## 先备知识

需要会在实轴上的射线 $x>R$ 与 $x<-R$ 上使用绝对值不等式，并能对多项式与有理式作合法恒等变形。第 5 章的数列无穷极限提供了 $M$ 阈值语言；上一单元则说明无穷记号表达量词行为，而不是实数值。

## 学习目标

1. 定义 $x\to+\infty$ 与 $x\to-\infty$ 时的有限极限；
2. 写出自变量方向与函数值方向组合成的四种无穷极限；
3. 按定义证明基本有理函数的无穷远有限极限；
4. 用初等不等式证明多项式增长，并准确解释水平渐近线。

## 牵引问题

“$x$ 趋于正无穷”不是让 $x$ 靠近实轴上的某个点，而是让 $x$ 最终越过任意足够远的右侧位置。此时，函数值既可能靠近有限数，也可能向正方向或负方向越过任意门槛。怎样用一个尾部阈值 $R$ 统一描述这些情形？

## 探索与猜想

对 $f(x)=2+1/x$，只要 $|x|>1/\varepsilon$，便有 $|f(x)-2|<\varepsilon$；这个估计同时适用于很大的正数和绝对值很大的负数。对 $x^3$，自变量走向右端时函数值向上越过门槛，走向左端时函数值向下越过门槛。可见必须分别记录“自变量去向哪一端”和“函数值去向哪一类目标”。

## 概念与理论

### 定义（无穷远处的有限极限） {#def-u-03-09-08-finite-limit-at-infinity}

设 $f:D\to\mathbb R$，且 $D$ 在右方无界。对 $L\in\mathbb R$，若

$$
\forall\varepsilon>0\;\exists R>0\;\forall x\in D,\qquad
x>R\Longrightarrow |f(x)-L|<\varepsilon,
$$

则称 $f(x)$ 在 $x\to+\infty$ 时趋于 $L$，记作

$$
\lim_{x\to+\infty}f(x)=L.
$$

若 $D$ 在左方无界，并且

$$
\forall\varepsilon>0\;\exists R>0\;\forall x\in D,\qquad
x<-R\Longrightarrow |f(x)-L|<\varepsilon,
$$

则称 $f(x)$ 在 $x\to-\infty$ 时趋于 $L$。右端使用射线 $(R,+\infty)$，左端使用射线 $(-\infty,-R)$；两端的结论必须分别证明。

### 定义（无穷远处的无穷极限） {#def-u-03-09-08-infinite-limit-at-infinity}

目标不再是有限实数时，用高度门槛 $M$ 取代误差 $\varepsilon$。四种组合的完整定义如下：

$$
\begin{aligned}
\forall M>0\;\exists R>0\;\forall x\in D,\quad
x>R&\Longrightarrow f(x)>M
&&\text{表示 }x\to+\infty,\ f(x)\to+\infty,\\
\forall M>0\;\exists R>0\;\forall x\in D,\quad
x>R&\Longrightarrow f(x)<-M
&&\text{表示 }x\to+\infty,\ f(x)\to-\infty,\\
\forall M>0\;\exists R>0\;\forall x\in D,\quad
x<-R&\Longrightarrow f(x)>M
&&\text{表示 }x\to-\infty,\ f(x)\to+\infty,\\
\forall M>0\;\exists R>0\;\forall x\in D,\quad
x<-R&\Longrightarrow f(x)<-M
&&\text{表示 }x\to-\infty,\ f(x)\to-\infty.
\end{aligned}
$$

每一行都要求 $D$ 在相应方向无界，以免尾部没有定义域点而使条件真空成立。$+\infty$ 和 $-\infty$ 不是实数；这些定义只表达尾部的序与距离条件，不允许把无穷记号代入实数的四则运算。

### 水平渐近线的方向性 {#def-u-03-09-08-horizontal-asymptote}

若 $\lim_{x\to+\infty}f(x)=L$ 或 $\lim_{x\to-\infty}f(x)=L$，则直线 $y=L$ 称为图像在相应一端的水平渐近线。一端成立已经足够；同一函数在左右两端可以有不同的水平渐近线，而且图像在有限位置穿过这条直线也不违反定义。

### 命题（幂函数的初等增长） {#thm-u-03-09-08-power-growth}

设 $n$ 为正整数。则

$$
\lim_{x\to+\infty}x^n=+\infty.
$$

当 $x\to-\infty$ 时，偶数次幂趋于 $+\infty$，奇数次幂趋于 $-\infty$。

**证明。** 给定 $M>0$，取 $R=M^{1/n}>0$。若 $x>R$，则 $x^n>R^n=M$，证明了右端结论。若 $x<-R$，则 $|x|>R$，所以 $|x|^n>M$。当 $n$ 为偶数时，$x^n=|x|^n>M$；当 $n$ 为奇数时，$x^n=-|x|^n<-M$。这分别满足左端正无穷与负无穷的定义。$\square$

证明具体多项式的增长时，还要用不等式控制低次项；仅写最高次项而不给控制范围，不构成证明。

## 例题与迁移

### 例题 1：有理函数的双端水平行为 {#ex-u-03-09-08-rational}

设

$$
r(x)=\frac{2x+1}{x}=2+\frac1x,\qquad x\ne0.
$$

给定 $\varepsilon>0$，取 $R=1/\varepsilon$。若 $x>R$ 或 $x<-R$，都有 $|x|>R$，因而

$$
|r(x)-2|=\frac1{|x|}<\frac1R=\varepsilon.
$$

所以

$$
\lim_{x\to+\infty}r(x)=2,\qquad
\lim_{x\to-\infty}r(x)=2.
$$

这是对一个有理函数的定义证明，结论来自恒等变形与绝对值估计；直线 $y=2$ 是左右两端共同的水平渐近线。

### 例题 2：二次多项式压过一次项 {#ex-u-03-09-08-polynomial-growth}

证明 $p(x)=x^2-3x$ 在左右两端都趋于 $+\infty$。

给定 $M>0$。对右端取

$$
R_+=\max\{6,\sqrt{2M}\}.
$$

若 $x>R_+$，则 $x-3>x/2$，故

$$
p(x)=x(x-3)>\frac{x^2}{2}>M.
$$

对左端取 $R_-=\sqrt M$。若 $x<-R_-$，则 $x^2>M$ 且 $-3x>0$，所以

$$
p(x)=x^2-3x>x^2>M.
$$

两个阈值分别完成两个方向的证明。这是“高次增长压过低次项”的一个具体初等估计，并未借助尚未建立的通用多项式法则。

## 即时检验与回望

### 即时检验 1：写出左端的两个方向

按定义证明

$$
\lim_{x\to-\infty}(x^2+1)=+\infty.
$$

??? note "答案"

    给定 $M>0$，取 $R=\sqrt M$。若 $x<-R$，则 $|x|>R$，从而 $x^2>M$，于是

    $$
    x^2+1>M.
    $$

    这里 $x<-R$ 指定自变量走向左端，$x^2+1>M$ 指定函数值走向正方向，两者不可混写。

### 即时检验 2：识别双端水平渐近线

求 $q(x)=3-2/x$ 在 $x\to+\infty$ 与 $x\to-\infty$ 时的有限极限，并指出水平渐近线。

??? note "答案"

    给定 $\varepsilon>0$，取 $R=2/\varepsilon$。若 $x>R$ 或 $x<-R$，则

    $$
    |q(x)-3|=\frac2{|x|}<\frac2R=\varepsilon.
    $$

    故两个方向的极限都为 $3$，直线 $y=3$ 是图像左右两端的水平渐近线。

## 习题与答案

### 习题 1：倒数的双端有限极限 {#pr-u-03-09-08-01}

按定义证明

$$
\lim_{x\to+\infty}\frac1x=0,\qquad
\lim_{x\to-\infty}\frac1x=0.
$$

??? note "答案"

    给定 $\varepsilon>0$，取 $R=1/\varepsilon$。若 $x>R$ 或 $x<-R$，都有 $|x|>R$，所以

    $$
    \left|\frac1x-0\right|=\frac1{|x|}<\frac1R=\varepsilon.
    $$

    同一个 $R$ 分别验证了两条射线上的定义。

### 习题 2：一次有理函数的水平线 {#pr-u-03-09-08-02}

证明 $(5x-1)/x$ 在左右两端都以 $5$ 为极限，并说明相应水平渐近线。

??? note "答案"

    对 $x\ne0$，

    $$
    \frac{5x-1}{x}-5=-\frac1x.
    $$

    给定 $\varepsilon>0$，取 $R=1/\varepsilon$。当 $x>R$ 或 $x<-R$ 时，上式绝对值为 $1/|x|<\varepsilon$。故左右极限均为 $5$，相应水平渐近线是 $y=5$。

### 习题 3：奇次幂的两种目标 {#pr-u-03-09-08-03}

按定义证明

$$
\lim_{x\to+\infty}x^3=+\infty,\qquad
\lim_{x\to-\infty}x^3=-\infty.
$$

??? note "答案"

    给定 $M>0$，取 $R=M^{1/3}$。若 $x>R$，则 $x^3>M$，满足右端正无穷的定义。若 $x<-R$，由于立方保持严格大小次序，有 $x^3<-R^3=-M$，满足左端负无穷的定义。

### 习题 4：控制二次式的左端低次项 {#pr-u-03-09-08-04}

证明 $s(x)=x^2+2x$ 在 $x\to+\infty$ 与 $x\to-\infty$ 时都趋于 $+\infty$。

??? note "答案"

    给定 $M>0$。在右端取 $R_+=\sqrt M$；若 $x>R_+$，则 $2x>0$，所以 $s(x)>x^2>M$。

    在左端取

    $$
    R_-=\max\{4,\sqrt{2M}\}.
    $$

    若 $x<-R_-$，令 $u=|x|>R_-$，则

    $$
    s(x)=u^2-2u=u(u-2)>\frac{u^2}{2}>M,
    $$

    其中 $u>4$ 保证 $u-2>u/2$。因此两个方向都满足正无穷定义。

### 习题 5：两端不同的水平渐近线 {#pr-u-03-09-08-05}

设

$$
h(x)=
\begin{cases}
1+1/x,&x<0,\\
3+1/x,&x>0.
\end{cases}
$$

求左右无穷远处的有限极限，并说明图像的水平渐近线。

??? note "答案"

    给定 $\varepsilon>0$，取 $R=1/\varepsilon$。若 $x<-R$，则

    $$
    |h(x)-1|=\frac1{|x|}<\varepsilon,
    $$

    故 $\lim_{x\to-\infty}h(x)=1$。若 $x>R$，则

    $$
    |h(x)-3|=\frac1x<\varepsilon,
    $$

    故 $\lim_{x\to+\infty}h(x)=3$。图像左端的水平渐近线为 $y=1$，右端的水平渐近线为 $y=3$；两端不必共享同一条水平线。

## 常见误区与后续

- 把“$x\to\infty$”理解成靠近一个实数点。正确图景是最终进入任意足够远的实轴射线。
- 混淆接近方向与目标方向。$x\to-\infty$ 时，函数值仍可能趋于有限数、$+\infty$ 或 $-\infty$。
- 把无穷记号直接代入有理式。例题的有理函数结论来自恒等变形和尾部估计，而不是对无穷作分式运算。
- 认为水平渐近线必须左右相同，或图像不能穿过它；定义只约束相应的无穷远尾部。

后续的极限运算法则将把已证明的局部估计组织成可复用定理；在那之前，每个无穷远结论都应能还原为 $\varepsilon$--$R$ 或 $M$--$R$ 证明。
