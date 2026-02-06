import pytest


def test_trend_fetcher_contract():
    """
    Defines the REQUIRED contract for trend fetching.

    This test MUST FAIL until a concrete implementation exists
    at services/trend_fetcher.py that satisfies this interface.
    """

    # Import SHOULD fail initially (no implementation yet)
    from services.trend_fetcher import fetch_trends  # noqa: F401

    # Invoke expected API
    trends = fetch_trends(query="ai governance")

    # Top-level structure
    assert isinstance(trends, dict), "Trend fetcher must return a dict"

    required_top_level_keys = {
        "query",
        "source",
        "retrieved_at",
        "trends",
    }

    assert required_top_level_keys.issubset(trends.keys()), (
        f"Missing required keys. Expected at least: {required_top_level_keys}"
    )

    # Trends list
    assert isinstance(trends["trends"], list), "`trends` must be a list"
    assert len(trends["trends"]) > 0, "`trends` list must not be empty"

    # Validate individual trend entries
    for trend in trends["trends"]:
        assert isinstance(trend, dict), "Each trend must be a dict"

        required_trend_keys = {
            "topic",
            "confidence",
            "velocity",
            "time_window",
        }

        assert required_trend_keys.issubset(trend.keys()), (
            f"Trend item missing required keys: {required_trend_keys}"
        )

        assert isinstance(trend["topic"], str)
        assert isinstance(trend["confidence"], (int, float))
        assert 0.0 <= trend["confidence"] <= 1.0
        assert isinstance(trend["velocity"], (int, float))
        assert trend["time_window"] in {"real_time", "recent", "historical"}
