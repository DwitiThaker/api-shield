from app.rate_limiter.sliding_window_counter import (
    SlidingWindowCounterRateLimiter,
)


def test_allows_requests_within_limit():
    limiter = SlidingWindowCounterRateLimiter(
        limit=3,
        window_seconds=60,
        clock=lambda: 1000.0,
    )

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False


def test_allows_requests_from_different_clients():
    limiter = SlidingWindowCounterRateLimiter(
        limit=1,
        window_seconds=60,
        clock=lambda: 1000.0,
    )

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-2") is True
