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
