"""Exact integer-cent allocation for a weighted prize pool."""

from collections.abc import Sequence


def split_pool(pool_cents: int, weights: Sequence[int]) -> list[int]:
    """Allocate ``pool_cents`` proportionally using the largest-remainder method.

    Ties are resolved by the original input order. This makes the function
    deterministic while preserving the invariant ``sum(result) == pool_cents``.
    """
    if isinstance(pool_cents, bool) or not isinstance(pool_cents, int):
        raise TypeError("pool_cents must be an integer")
    if pool_cents < 0:
        raise ValueError("pool_cents must be non-negative")
    if not weights:
        if pool_cents == 0:
            return []
        raise ValueError("weights cannot be empty when the pool is positive")
    if any(isinstance(weight, bool) or not isinstance(weight, int) for weight in weights):
        raise TypeError("every weight must be an integer")
    if any(weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative")

    total = sum(weights)
    if total == 0:
        if pool_cents == 0:
            return [0] * len(weights)
        raise ValueError("at least one weight must be positive")

    numerators = [pool_cents * weight for weight in weights]
    allocation = [numerator // total for numerator in numerators]
    cents_left = pool_cents - sum(allocation)

    order = sorted(range(len(weights)), key=lambda index: (-(numerators[index] % total), index))
    for index in order[:cents_left]:
        allocation[index] += 1

    assert sum(allocation) == pool_cents
    return allocation


if __name__ == "__main__":
    print(split_pool(10000, [1, 1, 1]))
