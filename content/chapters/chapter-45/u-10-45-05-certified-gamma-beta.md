---
title: 怎样对 Gamma、Beta 积分作带状态的可靠近似？
unit_id: u-10-45-05
hours: {theory: 0.50, applied: 1.00}
difficulty: 4
prerequisites: {book: [第 22 章, u-10-45-01, u-10-45-02, u-10-45-03, u-10-45-04], higher_algebra: [], analytic_geometry: [], python: [函数调用]}
capabilities: [gamma_beta_quadrature, certificate_status, endpoint_error_budget]
learning_goals: [分解端点与求积误差, 区分三种计算状态, 正确解释外部导数界]
content_standard: 2
---
# 怎样对 Gamma、Beta 积分作带状态的可靠近似？ {#u-10-45-05}
## 先备知识
熟悉端点比较界、复合 Simpson 误差界与状态式算法接口。
## 学习目标
能读取误差字段与三种状态，不把数值稳定误写成数学证书。
## 牵引问题
截断误差和有限区间求积误差怎样合成一个可靠上界？
## 探索与猜想
先解析控制被删去的端点，再由已证明的四阶导数界认证有限主部。
## 概念与理论
### 误差合同 {#workflow-u-10-45-05-certificate}
程序把反常端点界记录为 `endpoint_error_bound`，把 Simpson 界记录为
`quadrature_error_bound`，两者相加为 `total_error_bound`。外部提供的四阶导数界是数学输入，程序不从采样中证明它。

```python
from mathbook_examples.parametric_integrals import beta_integral, gamma_integral

met = gamma_integral(2.0, 1e-5, 4096, fourth_derivative_bound=10.0)
exhausted = gamma_integral(2.0, 1e-12, 2, fourth_derivative_bound=10.0)
diagnostic = beta_integral(2.0, 3.0, 1e-5, 512)
```

### 三种状态
- `target_met`：端点界与条件式求积界之和不超过目标。
- `budget_exhausted`：仍有有限有效总界，但面板预算不足。
- `uncertified`：缺少四阶导数界，只报告诊断值，不返回总误差证书。

`uncertified` 不等于数值错误，`budget_exhausted` 也不等于积分发散。
## 例题与迁移
### 例 1：证书达标 {#ex-u-10-45-05-met}
只有状态达标且总界不超过容差时才可声称满足目标。
### 例 2：缺失数学输入 {#ex-u-10-45-05-uncertified}
诊断值可用于探索，但网格最大值不能冒充全区间导数界。
## 即时检验与回望
### 即时检验 1
谁证明四阶导数界？
??? note "答案"
    调用者；函数只把它作为条件式证书输入。
### 即时检验 2
预算耗尽时还有界吗？
??? note "答案"
    有，返回有限总界，但该界大于目标容差。
## 常见误区与后续
- 采样最大值不是全区间导数上界证书。
- 浮点舍入和外部函数求值误差不包含在解析求积界内。
## 习题与答案
### 习题 1 {#pr-u-10-45-05-01}
端点误差字段是什么？
??? note "答案"
    `endpoint_error_bound`。
### 习题 2 {#pr-u-10-45-05-02}
总误差字段是什么？
??? note "答案"
    `total_error_bound`。
### 习题 3 {#pr-u-10-45-05-03}
达标状态是什么？
??? note "答案"
    `target_met`。
### 习题 4 {#pr-u-10-45-05-04}
预算不足状态是什么？
??? note "答案"
    `budget_exhausted`。
### 习题 5 {#pr-u-10-45-05-05}
缺少导数界状态是什么？
??? note "答案"
    `uncertified`。
### 习题 6 {#pr-u-10-45-05-06}
未认证是否表示积分发散？
??? note "答案"
    不表示，只是缺少求积误差证书。
### 习题 7 {#pr-u-10-45-05-07}
预算耗尽是否没有任何界？
??? note "答案"
    不是，仍返回当前有限总界。
### 习题 8 {#pr-u-10-45-05-08}
四阶导数界可由网格猜测吗？
??? note "答案"
    不可作为证书。
### 习题 9 {#pr-u-10-45-05-09}
总界怎样组成？
??? note "答案"
    端点界加有限主部求积界。
### 习题 10 {#pr-u-10-45-05-10}
可靠报告至少包含什么？
??? note "答案"
    数值、截断区间、误差字段、评估次数和状态。
??? note "答案"
    还应说明导数界来自外部数学证明。
