from app.rate_limiter.sliding_window_log import (
    SlidingWindowLogRateLimiter,
)


def test_allows_requests_within_limit():
    limiter = SlidingWindowLogRateLimiter(limit=3, window_seconds=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True


def test_rejects_requests_after_limit():
    limiter = SlidingWindowLogRateLimiter(limit=2, window_seconds=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False


def test_allows_request_when_oldest_request_expires():
    current_time = [1000.0]

    def fake_clock():
        return current_time[0]

    limiter = SlidingWindowLogRateLimiter(
        limit=2,
        window_seconds=60,
        clock=fake_clock,
    )

    assert limiter.is_allowed("user-1") is True
    current_time[0] += 10

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False

    # The first request is now outside the rolling window.
    current_time[0] = 1061.0

    assert limiter.is_allowed("user-1") is True
