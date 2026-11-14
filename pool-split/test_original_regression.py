import unittest

from original_pool_split import split_pool


class OriginalImplementationRegressionTest(unittest.TestCase):
    def test_sum_must_equal_pool(self) -> None:
        allocation = split_pool(10000, [1, 1, 1])
        self.assertEqual(sum(allocation), 10000)


if __name__ == "__main__":
    unittest.main()
