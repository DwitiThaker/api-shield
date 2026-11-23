from app.rate_limiter.redis_client import redis_client
from app.rate_limiter.policies import RateLimitPolicy

INCREMENT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return count
"""


class RedisFixedWindowRateLimiter:
    def __init__(self, policy: RateLimitPolicy):
        self.policy = policy
        self.limit = policy.limit
        self.window_seconds = policy.window_seconds
        self.fail_open = policy.fail_open

        self.increment_script = redis_client.register_script(INCREMENT_SCRIPT)

    async def is_allowed(self, client_id: str) -> tuple[bool, int]:
        key = f"rate_limit:{self.policy.name}:{client_id}"

        count = await self.increment_script(
            keys=[key],
            args=[self.window_seconds],
        )

        allowed = count <= self.limit

        print(
            f"Client: {client_id}, "
            f"Policy: {self.policy.name}, "
            f"Count: {count}, "
            f"Allowed: {allowed}"
        )

        if not allowed:
            ttl = await redis_client.ttl(key)
            return False, max(ttl, 0)

        return True, 0
