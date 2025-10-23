"""Test configuration for pytest.

Ensure Hypothesis runs with intended settings in all environments by
programmatically registering/loading a CI profile. This avoids relying on
pyproject.toml being discovered in environments where Hypothesis's pyproject
lookup may be skipped.
"""

from hypothesis import HealthCheck, settings

# Register a profile named 'ci' and load it so Hypothesis uses these values
# during the test run. This mirrors the intended values in pyproject.toml.
settings.register_profile(
    "ci",
    max_examples=500,
    deadline=5000,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile("ci")
