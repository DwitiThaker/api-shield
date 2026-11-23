from app.rate_limiter.policies import POLICIES, RateLimitPolicy


def get_rate_limit_policy(
    user_plan: str | None,
    endpoint: str,
) -> RateLimitPolicy:

    # Endpoint-specific policies take priority.
    if endpoint == "/api/exports":
        return POLICIES["export"]

    # Otherwise, use the user's plan.
    if user_plan is None:
        return POLICIES["anonymous"]

    return POLICIES.get(user_plan, POLICIES["anonymous"])
