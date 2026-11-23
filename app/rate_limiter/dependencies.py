from fastapi import Request, HTTPException

from app.rate_limiter.policies import POLICIES
from app.rate_limiter.policy_resolver import get_rate_limit_policy
from app.rate_limiter.redis_fixed_window import RedisFixedWindowRateLimiter

limiters = {
    name: RedisFixedWindowRateLimiter(policy=policy)
    for name, policy in POLICIES.items()
}


async def rate_limit(request: Request):
    client_id = request.client.host

    # Temporary user simulation
    user_plan = "free"

    policy = get_rate_limit_policy(
        user_plan=user_plan,
        endpoint=request.url.path,
    )

    print(f"Selected policy: {policy.name}")
    print(f"Rate limit: {policy.limit} requests / {policy.window_seconds}s")

    limiter = limiters[policy.name]

    allowed, retry_after = await limiter.is_allowed(client_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)},
        )
