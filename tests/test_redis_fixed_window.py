import asyncio
import uuid

from app.rate_limiter.redis_fixed_window import (
    RedisFixedWindowRateLimiter,
)
from app.rate_limiter.redis_client import redis_client

from app.rate_limiter.policies import RateLimitPolicy


def test_two_instances_share_rate_limit():
    async def run_test():
        client_id = f"shared-user-{uuid.uuid4()}"

        policy = RateLimitPolicy(
            name="test",
            limit=10,
            window_seconds=60,
        )

        server_a = RedisFixedWindowRateLimiter(policy=policy)
        server_b = RedisFixedWindowRateLimiter(policy=policy)

        try:
            requests_a = [server_a.is_allowed(client_id) for _ in range(6)]
            requests_b = [server_b.is_allowed(client_id) for _ in range(6)]

            results_a, results_b = await asyncio.gather(
                asyncio.gather(*requests_a),
                asyncio.gather(*requests_b),
            )

            allowed_a = sum(1 for allowed, _ in results_a if allowed)
            rejected_a = sum(1 for allowed, _ in results_a if not allowed)

            allowed_b = sum(1 for allowed, _ in results_b if allowed)
            rejected_b = sum(1 for allowed, _ in results_b if not allowed)

            print(f"Server A: {allowed_a} allowed, {rejected_a} rejected")
            print(f"Server B: {allowed_b} allowed, {rejected_b} rejected")

            assert allowed_a + allowed_b == 10
            assert rejected_a + rejected_b == 2

        finally:
            await redis_client.delete(f"rate_limit:{client_id}")

    asyncio.run(run_test())
