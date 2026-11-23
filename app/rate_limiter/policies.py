from dataclasses import dataclass


@dataclass
class RateLimitPolicy:
    name: str
    limit: int
    window_seconds: int
    fail_open: bool = True


POLICIES = {
    "anonymous": RateLimitPolicy(name="anonymous", limit=20, window_seconds=60),
    "free": RateLimitPolicy(name="free", limit=60, window_seconds=60),
    "premium": RateLimitPolicy(
        name="premium", limit=300, window_seconds=60, fail_open=False
    ),
    "export": RateLimitPolicy(
        name="export",
        limit=5,
        window_seconds=60,
        fail_open=False,
    ),
}
