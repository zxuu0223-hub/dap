def split_pool(pool_cents: int, weights: list[int]) -> list[int]:
    total = sum(weights)
    return [round(pool_cents * weight / total) for weight in weights]
