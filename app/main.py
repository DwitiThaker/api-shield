from itertools import count
from fastapi import FastAPI, HTTPException, Request, Depends
from app.rate_limiter.dependencies import rate_limit
from app.rate_limiter.fixed_window import FixedWindowRateLimiter
from app.rate_limiter.sliding_window_log import SlidingWindowLogRateLimiter
from app.rate_limiter.redis_fixed_window import (
    RedisFixedWindowRateLimiter,
)
from app.rate_limiter.policy_resolver import get_rate_limit_policy
from app.rate_limiter.policies import POLICIES

app = FastAPI(title="API Shield")

# limiter = FixedWindowRateLimiter(
#     limit=5,
#     window_seconds=60,
# )

# limiter = SlidingWindowLogRateLimiter(
#     limit=5,
#     window_seconds=60,
# )

# limiter = RedisFixedWindowRateLimiter(limit=5, window_seconds=60)

limiters = {
    name: RedisFixedWindowRateLimiter(policy=policy)
    for name, policy in POLICIES.items()
}


@app.get("/api/products", dependencies=[Depends(rate_limit)])
async def get_products():
    return {
        "success": True,
        "data": [
            {"id": 1, "name": "Product A"},
            {"id": 2, "name": "Product B"},
        ],
    }


@app.get("/api/exports", dependencies=[Depends(rate_limit)])
async def export_data():
    return {
        "success": True,
        "message": "Export completed",
    }
