from app.rate_limiter.policy_resolver import get_rate_limit_policy


def test_free_user_gets_free_policy():
    policy = get_rate_limit_policy("free", "/api/products")

    assert policy.name == "free"
    assert policy.limit == 60


def test_premium_user_gets_premium_policy():
    policy = get_rate_limit_policy("premium", "/api/products")

    assert policy.name == "premium"
    assert policy.limit == 300


def test_anonymous_user_gets_anonymous_policy():
    policy = get_rate_limit_policy(None, "/api/products")

    assert policy.name == "anonymous"
    assert policy.limit == 20


def test_export_endpoint_overrides_user_plan():
    policy = get_rate_limit_policy("premium", "/api/exports")

    assert policy.name == "export"
    assert policy.limit == 5
    assert policy.fail_open is False


def test_unknown_plan_falls_back_to_anonymous():
    policy = get_rate_limit_policy("enterprise", "/api/products")

    assert policy.name == "anonymous"
