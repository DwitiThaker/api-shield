from app.rate_limiter.fixed_window import FixedWindowRateLimiter


def test_allows_requests_within_limit():
    limiter = FixedWindowRateLimiter(limit=3, window_seconds=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True


def test_rejects_requests_after_limit():
    limiter = FixedWindowRateLimiter(limit=2, window_seconds=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False


def test_clients_have_independent_limits():
    limiter = FixedWindowRateLimiter(limit=1, window_seconds=60)

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False

    assert limiter.is_allowed("user-2") is True


def test_resets_counter_after_window_expires():
    current_time = [1000.0]

    def fake_clock():
        return current_time[0]

    limiter = FixedWindowRateLimiter(
        limit=2,
        window_seconds=60,
        clock=fake_clock,
    )

    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is True
    assert limiter.is_allowed("user-1") is False

    # Advance time by 60 seconds.
    current_time[0] += 60

    # The new window should allow requests again.
    assert limiter.is_allowed("user-1") is True


def test_fixed_window_allows_boundary_burst():
    current_time = [1000.0]

    def fake_clock():
        return current_time[0]

    limiter = FixedWindowRateLimiter(
        limit=5,
        window_seconds=60,
        clock=fake_clock,
    )

    # Five requests at the end of the first window.
    for _ in range(5):
        assert limiter.is_allowed("user-1") is True

    # Move into the next window.
    current_time[0] = 1060.0

    # Five more requests are allowed.
    for _ in range(5):
        assert limiter.is_allowed("user-1") is True
