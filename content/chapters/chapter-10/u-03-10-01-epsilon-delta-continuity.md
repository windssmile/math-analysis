---
title: 连续性怎样写成局部控制？
unit_id: u-03-10-01
hours:
  theory: 1.6
  applied: 0.4
difficulty: 3
prerequisites:
  book:
  - chapter-09
  higher_algebra:
  - 绝对值不等式
  analytic_geometry: []
  python: []
capabilities:
- concepts
- proof
- mathematical_expression
learning_goals:
- 定义一点连续
- 写出连续性的 epsilon-delta 形式
- 识别函数值与极限的匹配条件
content_standard: 1
---

# 连续性怎样写成局部控制？ {#u-03-10-01}


## 先备知识

已建立函数极限的邻域和 \(\varepsilon\)-\(\delta\) 定义。

## 学习目标

1. 定义一点连续；2. 写成误差形式；3. 区分定义域端点的单侧情形。

## 牵引问题

什么时候“输入很小的改变只造成输出很小的改变”可由同一点的函数值严格表达？

## 探索与猜想

若 \(f(x)\) 在 \(x\to a\) 时趋于它实际取到的 \(f(a)\)，局部极限和函数值就没有断裂。

## 概念与理论

### 定义（连续） {#def-u-03-10-01-continuity}

函数 \(f:D\to\mathbb R\) 在 \(a\in D\) 连续，是指 \(\lim_{x\to a}f(x)=f(a)\)，其中极限按定义域中的点理解。等价地，对每个 \(\varepsilon>0\)，存在 \(\delta>0\)，当 \(x\in D\) 且 \(|x-a|<\delta\) 时，

$$
|f(x)-f(a)|<\varepsilon.
$$

这里无需去心条件：当 \(x=a\) 时左端为零，自动满足。对 \(f(x)=x^2\)，给定 \(\varepsilon\)，先限制 \(|x-a|<1\)，则 \(|x+a|\le2|a|+1\)；再取 \(\delta=\min\{1,\varepsilon/(2|a|+1)\}\)，便有 \(|x^2-a^2|<\varepsilon\)。

## 例题与迁移

分段函数 \(p(x)=x+1\,(x\ne0),p(0)=0\) 在零点不连续：去心邻域的极限为 \(1\)，而函数值为 \(0\)。改变 \(p(0)\) 为 \(1\) 即消除这处断裂。

## 即时检验与回望

1. 常数函数为何连续？答：任取 \(\delta>0\)，输出差恒为零。
2. 连续性是否只谈函数值？答：否，它要求邻域内全部定义域点的输出受统一的 \(\delta\) 控制。

## 习题与答案

1. 证明 \(f(x)=3x-1\) 在任意点连续。答：取 \(\delta=\varepsilon/3\)。
2. \(1/x\) 在零点能否谈连续？答：不能，零点不在定义域。
3. \(\sqrt{x}\) 在零点如何理解？答：相对 \([0,\infty)\) 的右侧定义域连续。
