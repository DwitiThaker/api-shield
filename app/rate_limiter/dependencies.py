
from dataclasses import dataclass

from fastapi import HTTPException, Request

from app.rate_limiter.policies import POLICIES
from app.rate_limiter.policy_resolver import get_rate_limit_policy
from app.rate_limiter.redis_fixed_window import RedisFixedWindowRateLimiter


# Create one limiter instance per policy when the application starts.
limiters = {
    name: RedisFixedWindowRateLimiter(policy=policy)
    for name, policy in POLICIES.items()
}


@dataclass
class RateLimitContext:
    ip_address: str
    user_id: str | None
    api_key: str | None
    endpoint: str
    user_plan: str | None


async def rate_limit(request: Request):
    # Build context for the current request.
    context = RateLimitContext(
        ip_address=(
            request.client.host if request.client else "unknown"
        ),
        user_id="user_123",  # Temporary simulation
        api_key=None,        # Not implemented yet
        endpoint=request.url.path,
        user_plan="free",    # Temporary simulation
    )

    # Resolve the applicable policy.
    policy = get_rate_limit_policy(
        user_plan=context.user_plan,
        endpoint=context.endpoint,
    )

    print(f"Selected policy: {policy.name}")
    print(
        f"Rate limit: {policy.limit} requests / "
        f"{policy.window_seconds}s"
    )

    # Select the Redis limiter for this policy.
    limiter = limiters[policy.name]

    # Currently using IP as the rate-limit identifier.
    allowed, retry_after = await limiter.is_allowed(
        context.ip_address
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={
                "Retry-After": str(retry_after),
            },
        )
