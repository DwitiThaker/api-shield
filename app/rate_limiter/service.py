
from app.rate_limiter.policies import POLICIES
from app.rate_limiter.policy_resolver import get_rate_limit_policy
from app.rate_limiter.redis_fixed_window import RedisFixedWindowRateLimiter
from app.rate_limiter.context import RateLimitContext

class RateLimitService:
    def __init__(self):
        self.limiters = {
            name: RedisFixedWindowRateLimiter(policy=policy)
            for name, policy in POLICIES.items()
        }

    async def check_request(self, context: RateLimitContext):
        policy = get_rate_limit_policy(
            user_plan=context.user_plan,
            endpoint=context.endpoint,
        )

        limiter = self.limiters[policy.name]

        # Currently enforcing limits using IP address.
        allowed, retry_after = await limiter.is_allowed(
            context.ip_address
        )

        return allowed, retry_after
