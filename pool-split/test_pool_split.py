import random
import unittest

from pool_split import split_pool


class SplitPoolTests(unittest.TestCase):
    def test_regression_equal_weights(self) -> None:
        result = split_pool(10000, [1, 1, 1])
        self.assertEqual(result, [3334, 3333, 3333])
        self.assertEqual(sum(result), 10000)

    def test_bankers_rounding_regression(self) -> None:
        self.assertEqual(split_pool(1, [1, 1]), [1, 0])

    def test_zero_weight_receives_nothing(self) -> None:
        self.assertEqual(split_pool(13, [0, 2, 3]), [0, 5, 8])

    def test_zero_pool(self) -> None:
        self.assertEqual(split_pool(0, [2, 0, 3]), [0, 0, 0])

    def test_randomized_invariant_and_quota(self) -> None:
        random.seed(20261114)
        for _ in range(5_000):
            pool = random.randint(0, 100_000)
            weights = [random.randint(0, 500) for _ in range(random.randint(1, 30))]
            if sum(weights) == 0:
                weights[0] = 1
            result = split_pool(pool, weights)
            self.assertEqual(sum(result), pool)
            self.assertEqual(len(result), len(weights))
            for amount, weight in zip(result, weights):
                floor_quota = pool * weight // sum(weights)
                self.assertIn(amount, (floor_quota, floor_quota + 1))

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            split_pool(10, [])
        with self.assertRaises(ValueError):
            split_pool(10, [0, 0])
        with self.assertRaises(ValueError):
            split_pool(-1, [1])
        with self.assertRaises(ValueError):
            split_pool(10, [1, -1])


if __name__ == "__main__":
    unittest.main()
