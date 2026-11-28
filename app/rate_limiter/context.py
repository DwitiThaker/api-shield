from dataclasses import dataclass


@dataclass
class RateLimitContext:
    ip_address: str
    user_id: str | None
    api_key: str | None
    endpoint: str
    user_plan: str | None