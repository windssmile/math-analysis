# 第二、三部定理依赖与单元 ID 冻结表

本文冻结第二部“数列极限与无限过程”和第三部“函数极限、连续性与方程”的最终单元 ID、教学阅读顺序、定理依赖及内容归属。后续改写正文、注册课程与组织导航时，都应以本表为共同边界。

## 最终单元 ID 与阅读顺序

以下顺序是教学阅读顺序；编号只作为稳定标识，不要求按数字大小排列。

### 第二部

- 第 5 章：`u-02-05-01`、`u-02-05-02`、`u-02-05-05`、`u-02-05-03`、`u-02-05-04`
- 第 6 章：`u-02-06-01`、`u-02-06-04`、`u-02-06-02`、`u-02-06-03`
- 第 7 章：`u-02-07-01`、`u-02-07-02`、`u-02-07-03`、`u-02-07-04`
- 第 8 章：`u-02-08-01`、`u-02-08-02`、`u-02-08-03`、`u-02-08-04`、`u-02-08-06`、`u-02-08-07`、`u-02-08-05`、`u-02-08-08`

### 第三部

- 第 9 章：`u-03-09-01`、`u-03-09-02`、`u-03-09-05`、`u-03-09-06`、`u-03-09-07`、`u-03-09-08`、`u-03-09-03`、`u-03-09-04`
- 第 10 章：`u-03-10-01`、`u-03-10-02`、`u-03-10-03`、`u-03-10-04`、`u-03-10-05`
- 第 11 章：`u-03-11-01`、`u-03-11-02`、`u-03-11-03`
- 第 12 章：`u-03-12-01`、`u-03-12-04`、`u-03-12-02`、`u-03-12-03`

## 章节呈现顺序与定理依赖

第二部的完备性证明链固定为：确界原理 → 单调有界收敛定理 → 区间套定理 → Bolzano–Weierstrass 定理 → Cauchy 收敛准则。尾上确界、尾下确界以及 `limsup`、`liminf` 必须安排在这条证明链完成之后。

第三部按章节依次呈现有限函数极限、连续性、闭区间上的整体性质，以及介值定理、不动点存在性和二分法。这只是为自学组织的阅读顺序，并不表示相邻章节中的所有定理之间都有必要的逻辑依赖。

第三部应按以下分支使用定理：

- 有限函数极限是连续性理论的直接前提。
- 第二部的 Bolzano–Weierstrass 定理与闭区间的封闭性共同推出闭区间的序列紧致性：闭区间内任意序列先由有界性取得收敛子列，再由封闭性保证极限仍在该区间内。
- 连续性与序列紧致性共同推出连续函数在闭区间上有界、取得最大值和最小值，并且一致连续。
- 介值定理（含零点定理）由连续性与第二部的区间套定理推出；也可采用等价的确界论证。它不依赖最值定理或一致连续性。
- 对实闭区间上的连续自映射，把问题化为 `g(x) - x` 的零点问题，再由介值定理得到不动点存在性。
- 二分法中，介值定理与符号不变量保证每一步保留含根区间；区间长度公式给出误差证书。二分误差界不依赖序列紧致性、最值定理或一致连续性。

## 内容归属边界

第二部负责压缩映射定理及其完整数列论内容：不动点唯一性、迭代收敛性和误差界。第三部负责连续映射框架下的存在性、介值定理、二分法以及不同证书的比较，但不得重新证明压缩迭代收敛；需要该结论时应明确回引第二部。

## 迁移结论

当前第二、三部已经发布的 29 个 URL 必须全部继续发布。最终教学顺序可调整，也可增加新单元，但不得移除这些既有地址。因此本次实现不需要新增迁移页或重定向页。

## 机器校验标记

以下字符串仅用于结构测试；语义以上述中文约定为准。

```text
supremum -> monotone
monotone -> nested intervals
nested intervals -> Bolzano-Weierstrass
Bolzano-Weierstrass -> Cauchy
Part II owns contraction convergence
Part III owns continuous existence
finite function limits -> continuity
Bolzano-Weierstrass + closed interval -> sequential compactness
continuity + sequential compactness -> boundedness/extreme value/uniform continuity
continuity + nested intervals -> IVT
IVT -> continuous self-map fixed point existence
IVT/sign invariant + interval length -> bisection certificates
IVT independent of extreme value and uniform continuity
bisection error independent of compactness
```
