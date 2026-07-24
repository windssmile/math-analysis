---
title: “任意接近”怎样定义函数极限？
unit_id: u-03-09-02
hours:
  theory: 1.75
  applied: 0.25
difficulty: 3
prerequisites:
  book:
  - chapter-05
  - chapter-09
  higher_algebra:
  - 绝对值不等式
  analytic_geometry:
  - 实轴距离
  python: []
capabilities:
- concepts
- proof
- analytic_calculation
- mathematical_expression
learning_goals:
- 按量词顺序陈述有限点有限极限
- 证明线性与可去点极限
- 区分函数值和去心极限
- 完整证明函数极限唯一性
content_standard: 2
---

# “任意接近”怎样定义函数极限？ {#u-03-09-02}


## 先备知识

数列极限中的“给定 \(\varepsilon\)，再寻找 \(N\)”提供了量词经验。函数极限把
离散的下标起点换成实轴距离的控制半径，因此要熟练使用绝对值不等式与实轴距离。
还要记住：\(a\) 必须是定义域 \(D\) 的聚点，考察点来自
\(D\cap N_\delta^*(a)\)。

## 学习目标

完成本单元后，你应当能够：

1. 按正确的量词顺序写出有限点处的有限函数极限；
2. 说明 \(\delta\) 可以依赖什么、不能依赖什么；
3. 直接证明线性函数和有孔函数的极限；
4. 完整证明函数极限的唯一性，并区分极限与点值。

## 牵引问题

对 \(f(x)=3x-1\)，我们想表达
\[
x\longrightarrow2\quad\Longrightarrow\quad f(x)\longrightarrow5.
\]
若要求函数值误差小于任意给定的 \(\varepsilon>0\)，应当把 \(x\) 限制在多小的
去心邻域中？这个范围必须对该邻域中的每一个定义域点都有效。

## 探索与猜想

由
\[
|(3x-1)-5|=3|x-2|
\]
可猜到取 \(\delta=\varepsilon/3\)。一个常见失败是先看见某个 \(x\)，再为这个
\(x\) 临时选择 \(\delta\)；这样没有得到统一窗口。正确顺序是：对手先指定
\(\varepsilon\)，我们据此选一个 \(\delta\)，随后任意满足距离条件的 \(x\) 都必须
通过检验。

## 概念与理论

### 定义：有限点处的有限函数极限 {#def-u-03-09-02-function-limit}

设 \(f:D\to\mathbb R\)，\(D\subseteq\mathbb R\)，并设 \(a\in\mathbb R\) 是
\(D\) 的聚点，\(L\in\mathbb R\)。若

\[
\forall\varepsilon>0\;\exists\delta>0\;\forall x\in D,\qquad
0<|x-a|<\delta\Longrightarrow |f(x)-L|<\varepsilon,
\]

则称 \(f\) 在 \(x\to a\) 时以 \(L\) 为极限，记作
\[
\lim_{x\to a}f(x)=L.
\]

这一定义同时固定了五件事：

1. **靠近对象：** 自变量 \(x\) 靠近有限实数 \(a\)；
2. **允许范围：** 只取 \(x\in D\)；
3. **目标类型：** \(L\) 是有限实数；
4. **量词依赖：** \(\delta\) 可依赖 \(\varepsilon\)、函数和讨论点，但选定后不能依赖
   随后的 \(x\)；
5. **去心条件：** \(0<|x-a|\) 排除了中心点，所以定义不要求 \(a\in D\)，也不读取
   \(f(a)\)。

把量词顺序交换成“存在一个 \(\delta\) 对所有 \(\varepsilon\) 有效”通常过强；把
\(\delta\) 放在 \(x\) 之后选择则过弱。聚点条件保证距离条件并非最终为空。

### 定理：函数极限的唯一性 {#thm-u-03-09-02-uniqueness}

设 \(a\) 是 \(D\) 的聚点。若
\[
\lim_{x\to a}f(x)=L_1,\qquad \lim_{x\to a}f(x)=L_2,
\]
其中 \(L_1,L_2\in\mathbb R\)，则 \(L_1=L_2\)。

**证明。** 反设 \(L_1\ne L_2\)，令
\[
\varepsilon=\frac{|L_1-L_2|}{3}>0.
\]
由两个极限定义，分别存在 \(\delta_1,\delta_2>0\)，使相应函数值误差小于
\(\varepsilon\)。取
\[
\delta=\min\{\delta_1,\delta_2\}>0.
\]
因为 \(a\) 是 \(D\) 的聚点，存在 \(x\in D\) 满足 \(0<|x-a|<\delta\)。于是
\[
|f(x)-L_1|<\varepsilon,\qquad |f(x)-L_2|<\varepsilon.
\]
由三角不等式，
\[
|L_1-L_2|
\le |L_1-f(x)|+|f(x)-L_2|
<2\varepsilon
=\frac23|L_1-L_2|,
\]
矛盾。因此 \(L_1=L_2\)。\(\square\)

唯一性证明中使用聚点选出一个同时受两套估计控制的定义域点；若没有聚点条件，空窗口
可能让任意 \(L\) 都形式上满足蕴含式。

## 例题与迁移

### 例题 1：线性函数的极限 {#ex-u-03-09-02-linear}

用定义证明
\[
\lim_{x\to2}(3x-1)=5.
\]

**证明。** 给定任意 \(\varepsilon>0\)，取
\(\delta=\varepsilon/3>0\)。任取 \(x\in\mathbb R\)，若
\(0<|x-2|<\delta\)，则
\[
|(3x-1)-5|=3|x-2|<3\delta=\varepsilon.
\]
这对距离条件内的每个 \(x\) 都成立，故所求极限为 \(5\)。\(\square\)

### 例题 2：公式有孔但极限存在 {#ex-u-03-09-02-removable-hole}

令
\[
D=\mathbb R\setminus\{1\},\qquad
q(x)=\frac{x^2-1}{x-1}.
\]
证明 \(\lim_{x\to1}q(x)=2\)。

**证明。** \(1\) 是 \(D\) 的聚点。给定 \(\varepsilon>0\)，取
\(\delta=\varepsilon>0\)。任取 \(x\in D\) 满足 \(0<|x-1|<\delta\)。因为
\(x\ne1\)，
\[
|q(x)-2|
=\left|\frac{(x-1)(x+1)}{x-1}-2\right|
=|x-1|
<\delta=\varepsilon.
\]
所以极限为 \(2\)。证明从未要求给 \(q(1)\) 赋值。\(\square\)

## 即时检验与回望

### 即时检验 1：谁依赖谁？

在极限定义中，\(\delta\) 能否依赖 \(\varepsilon\)？能否在看到具体 \(x\) 后再改变？

??? note "答案"

    \(\delta\) 可以依赖先给定的 \(\varepsilon\)，也可以依赖固定的函数、讨论点和候选极限。
    一旦 \(\delta\) 选定，它必须同时控制所有满足
    \(x\in D\) 且 \(0<|x-a|<\delta\) 的 \(x\)，所以不能再随具体 \(x\) 改变。

### 即时检验 2：端点定义域怎样进入量词？

设 \(D=[0,\infty)\)，\(f(x)=\sqrt{x}\)。证明在 \(x\to0\) 且 \(x\in D\) 时，
\(f(x)\to0\)。

??? note "答案"

    给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon^2\)。任取 \(x\in D\)，若
    \(0<|x|<\delta\)，则 \(x\ge0\)，并且
    \[
    |\sqrt{x}-0|=\sqrt{x}<\sqrt{\delta}=\varepsilon.
    \]
    定义只量化 \(D\) 中的点，因此不需要处理 \(x<0\)。

## 习题与答案

### 习题 1：常数函数 {#pr-u-03-09-02-constant}

设 \(a\) 是 \(D\) 的聚点，\(f(x)=c\) 对所有 \(x\in D\) 成立。用定义证明
\(\lim_{x\to a}f(x)=c\)。

??? note "答案"

    给定 \(\varepsilon>0\)，可取任意 \(\delta>0\)，例如 \(\delta=1\)。任取
    \(x\in D\) 满足 \(0<|x-a|<\delta\)，都有
    \[
    |f(x)-c|=|c-c|=0<\varepsilon.
    \]
    故极限为 \(c\)。

### 习题 2：一般仿射函数 {#pr-u-03-09-02-affine}

设 \(m,b,a\in\mathbb R\)。证明
\(\lim_{x\to a}(mx+b)=ma+b\)，并分别处理 \(m=0\) 与 \(m\ne0\)。

??? note "答案"

    若 \(m=0\)，函数恒为 \(b\)，由常数函数结论即得。若 \(m\ne0\)，给定
    \(\varepsilon>0\)，取 \(\delta=\varepsilon/|m|\)。当
    \(0<|x-a|<\delta\) 时，
    \[
    |(mx+b)-(ma+b)|=|m|\,|x-a|<|m|\delta=\varepsilon.
    \]
    所以两种情形下结论均成立。

### 习题 3：另一个有孔函数 {#pr-u-03-09-02-second-hole}

在 \(D=\mathbb R\setminus\{-2\}\) 上定义
\[
h(x)=\frac{x^2-4}{x+2}.
\]
用定义证明 \(\lim_{x\to-2}h(x)=-4\)。

??? note "答案"

    给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon\)。若 \(x\in D\) 且
    \(0<|x+2|<\delta\)，则
    \[
    h(x)=\frac{(x-2)(x+2)}{x+2}=x-2,
    \]
    从而
    \[
    |h(x)-(-4)|=|x+2|<\delta=\varepsilon.
    \]
    故极限为 \(-4\)。

### 习题 4：改变中心点值 {#pr-u-03-09-02-change-point}

定义 \(g(x)=2x+1\)（\(x\ne3\)）且 \(g(3)=-10\)。求并证明
\(\lim_{x\to3}g(x)\)。

??? note "答案"

    候选极限是 \(7\)。给定 \(\varepsilon>0\)，取 \(\delta=\varepsilon/2\)。若
    \(0<|x-3|<\delta\)，则 \(x\ne3\)，所以
    \[
    |g(x)-7|=|2x+1-7|=2|x-3|<2\delta=\varepsilon.
    \]
    中心点的值 \(-10\) 不进入去心条件，故极限为 \(7\)。

### 习题 5：否定一个错误候选 {#pr-u-03-09-02-refute-candidate}

证明 \(\lim_{x\to0}x\ne1\)。要求给出一个固定的 \(\varepsilon_0\)，并说明任意
\(\delta>0\) 都会失败。

??? note "答案"

    取 \(\varepsilon_0=1/2\)。任给 \(\delta>0\)，令
    \[
    x=\min\left\{\frac{\delta}{2},\frac14\right\}>0.
    \]
    则 \(0<|x|<\delta\)，且 \(0<x\le1/4\)，所以
    \[
    |x-1|=1-x\ge\frac34>\varepsilon_0.
    \]
    因此不存在能使所有去心点都满足 \(|x-1|<\varepsilon_0\) 的 \(\delta\)，错误候选
    \(1\) 被否定。

## 常见误区与后续

- **误区 1：** 先固定某个 \(x\)，再选 \(\delta\)。定义要求一个 \(\delta\) 控制
  随后的所有允许点。
- **误区 2：** 忘记写 \(x\in D\)。定义域外没有函数值，不能参与蕴含式。
- **误区 3：** 删除 \(0<|x-a|\) 中的 \(0<\)。那会额外约束中心点，改变极限概念。
- **误区 4：** 把某个成功的 \(\delta\) 当作唯一选择。任何更小的正半径也有效。

下一单元将系统练习如何从目标误差反向设计局部半径，再把探索过程整理成从
\(\varepsilon\) 出发的正向证明。
