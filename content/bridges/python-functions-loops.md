---
title: Python 知识桥：函数、循环与异常
---

# Python 知识桥：函数、循环与异常 {#bridge-python-functions-loops}

在用二分法寻找方程的近似根之前，我们只需要三项 Python 基础：把计算封装成函数、用 `while` 循环重复步骤，以及用异常拒绝无效输入。

```python
def sign_change(function, left, right):
    """判断函数在区间两个端点的值是否异号或有一个为零。"""
    if left >= right:
        raise ValueError("left 必须小于 right")

    left_value = function(left)
    right_value = function(right)
    return left_value == 0 or right_value == 0 or left_value * right_value < 0


def polynomial(x):
    return x**2 - 2


print(sign_change(polynomial, 1, 2))

count = 0
while count < 3:
    print("第", count + 1, "次重复")
    count += 1
```

函数接收输入并返回数据，调用者可以继续使用返回值；`while` 会在条件为真时重复执行代码块。遇到左右端点次序错误等无效输入时，应抛出 `ValueError`，而不是返回一个看似合理但实际错误的结果。

## 在本书中的使用

- [5.4 迭代数据何时值得相信？](../chapters/chapter-05/u-02-05-04-iteration-evidence.md)：区分有限实验与极限证书。
- [6.3 误差如何穿过一次迭代？](../chapters/chapter-06/u-02-06-03-error-propagation.md)：用函数与循环复核已证明的误差分解。
- [7.2 递推的界与单调性怎样建立？](../chapters/chapter-07/u-02-07-02-recursive-invariants.md)：让程序追踪一个已写出的递推不变量。
