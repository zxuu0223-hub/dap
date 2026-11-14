# 奖池分账修复

## 1. 可复现输入

- 输入：`pool_cents=10000`，`weights=[1, 1, 1]`
- 原实现返回：`[3333, 3333, 3333]`
- 实际的和：`9999`
- 应有的和：`10000`

另一个最小反例是 `pool_cents=1, weights=[1, 1]`。Python 的银行家舍入会得到 `[0, 0]`，实际和为 0，应有的和为 1。

## 2. 修复方法

先按比例向下取整，再把剩余分币按小数余数从大到小补发（Hamilton / 最大余数法）；余数相同按输入顺序分配。这样结果是确定性的，且每人金额只会是精确配额的下取整或上取整。

## 3. 测试与两次输出

运行原实现的回归测试：

```text
FAIL: test_sum_must_equal_pool
AssertionError: 9999 != 10000
Ran 1 test
FAILED (failures=1)
```

运行修复后的测试：

```text
Ran 6 tests
OK
```

修复后的测试还执行 5,000 组固定随机种子的性质检查：长度不变、结果之和等于奖池、每个结果满足配额上下界。

## 4. AI 使用情况

（留白，由提交人填写）

## 运行

```bash
python -m unittest test_original_regression.py
python -m unittest test_pool_split.py
```
