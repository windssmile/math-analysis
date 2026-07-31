---
title: 梯度法、Newton 法和约束候选怎样可靠核验？
unit_id: u-07-32-06
hours: {theory: 1.00, applied: 1.25}
difficulty: 5
prerequisites: {book: [二阶判别, Lagrange 乘子, Newton 方程组], higher_algebra: [正定矩阵, 线性求解], analytic_geometry: [], python: [函数, 元组, 异常]}
capabilities: [gradient_descent, newton_optimization, equality_candidate_check]
learning_goals: [解释两类优化迭代, 诊断失败状态, 核验等式约束候选残差]
content_standard: 2
---

# 梯度法、Newton 法和约束候选怎样可靠核验？ {#u-07-32-06}

## 先备知识
掌握梯度、Hessian、下降方向、乘子必要条件与数值停止语义。

## 学习目标
1. 运行并解释梯度下降和 Newton 优化；2. 读取失败原因；3. 只核验候选条件而不宣称最优。

## 牵引问题
计算程序怎样既给出可复查结果，又不把“小梯度”或乘子残差小误报为全局最优？

## 探索与猜想
负梯度给局部最速下降方向，回溯线搜索控制实际下降。Newton 步解
\(H_ks_k=-\nabla f_k\)，但 Hessian 奇异或不定时未必给下降方向。

## 概念与理论

### 七步计算单元 {#def-u-07-32-06-workflow}
1. **问题来源：** 明确目标、定义域、尺度、约束和初值。
2. **数学转化：** 推导梯度、Hessian、约束 Jacobian 与乘子残差。
3. **算法思想：** 梯度法配回溯；Newton 法解线性系统并检查正定和下降性。
4. **误差与适用条件：** 停止阈值不是最优值误差证书；约束候选还需正则性和分类。
5. **伪代码：** 计算方向，拒绝病态状态，接受有限下降点，记录轨迹与原因。
6. **Python：** 复用 `mathbook_examples.optimization` 中的三个公开函数。
7. **结果解释：** 报告点、目标、梯度或残差、步长、Hessian 状态、原因和轨迹。

### 状态边界 {#def-u-07-32-06-status}
实现显式报告 `gradient`、`step`、`non_descent_direction`、`singular_hessian`、
`indefinite_hessian`、`nonfinite_value` 与 `max_iterations`。其中前两者只是停止信号。
等式候选核验返回驻点残差与约束残差，**不声明候选点最优**。

```python
from mathbook_examples.optimization import gradient_descent, newton_optimize

f = lambda p: 0.5 * (p[0] ** 2 + 4 * p[1] ** 2)
g = lambda p: (p[0], 4 * p[1])
H = lambda p: ((1.0, 0.0), (0.0, 4.0))
print(gradient_descent(f, g, (2.0, -1.0)).reason)
print(newton_optimize(f, g, H, (2.0, -1.0)).reason)
```

本实现不返回 `optimal` 状态；`converged` 只表示文档化停止信号触发。

## 例题与迁移
### 例 1：正定二次函数 {#ex-u-07-32-06-quadratic}
Newton 法一步到驻点，梯度法通过回溯逐步下降；全局最优性来自正定二次理论，不来自状态字符串。

### 例 2：约束候选 {#ex-u-07-32-06-equality}
对 \(x^2+y^2\) 且 \(x+y=1\)，核验 \((1/2,1/2)\)、\(\lambda=-1\) 时驻点和约束残差均为零；
这只验证必要方程，还需理论分类。

## 即时检验与回望
### 即时检验 1
Hessian 不定时为何拒绝纯 Newton 优化步？
??? note "答案"
    解出的方向可能不是下降方向，且二次模型不是局部凸模型。
### 即时检验 2
约束与驻点残差为零是否自动证明全局最优？
??? note "答案"
    不证明，只说明候选满足所核验的一阶方程。

## 常见误区与后续
- 梯度小可能来自尺度或平坦区。
- `max_iterations` 只是预算耗尽。
- 代码不覆盖不等式约束，也不建立一般 KKT 理论。

## 习题与答案
### 习题 1 {#pr-u-07-32-06-01}
负梯度为何是下降方向？
??? note "答案"
    非零梯度时方向导数为 \(-\|\nabla f\|^2<0\)。
### 习题 2 {#pr-u-07-32-06-02}
回溯线搜索检查什么？
??? note "答案"
    实际目标下降是否达到 Armijo 型充分下降。
### 习题 3 {#pr-u-07-32-06-03}
Newton 步为何解线性系统？
??? note "答案"
    它令二次模型梯度 \(\nabla f+Hs\) 为零。
### 习题 4 {#pr-u-07-32-06-04}
`singular_hessian` 表示什么？
??? note "答案"
    Hessian 线性系统没有可用唯一解。
### 习题 5 {#pr-u-07-32-06-05}
`indefinite_hessian` 表示什么？
??? note "答案"
    Hessian 不满足正定模型要求。
### 习题 6 {#pr-u-07-32-06-06}
`non_descent_direction` 表示什么？
??? note "答案"
    所得方向与梯度内积非负，不能保证局部下降。
### 习题 7 {#pr-u-07-32-06-07}
`gradient` 停止是否是距离最优点证书？
??? note "答案"
    不是，除非另有强凸性等误差界。
### 习题 8 {#pr-u-07-32-06-08}
为什么保留轨迹？
??? note "答案"
    用于复查下降、停滞、尺度和失败前状态。
### 习题 9 {#pr-u-07-32-06-09}
约束候选核验的两个残差是什么？
??? note "答案"
    \(\nabla f+DG^\mathsf T\lambda\) 与 \(G(x)\)。
### 习题 10 {#pr-u-07-32-06-10}
残差小为何仍需正则性检查？
??? note "答案"
    数值满足方程不能补上乘子定理缺失的约束资格。
### 习题 11 {#pr-u-07-32-06-11}
Newton 一步到驻点能否证明全局最优？
??? note "答案"
    不能；需目标结构与定义域理论。
### 习题 12 {#pr-u-07-32-06-12}
非有限候选为何不加入轨迹？
??? note "答案"
    轨迹只保存已接受的有限点，保留最后可信状态。
### 习题 13 {#pr-u-07-32-06-13}
本计算单元对“收敛”的定义是什么？
??? note "答案"
    仅指梯度或步长等文档化停止信号触发，不等同于已证明最优。

### 延伸：尺度
变量重新缩放会怎样影响停止阈值？
??? note "答案"
    会改变梯度、步长和 Hessian 的数值尺度，应按量纲重新设定阈值。

