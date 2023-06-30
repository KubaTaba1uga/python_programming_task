from unittest.mock import patch
from datetime import datetime

from src.buissness_logic import generate_upstream_jwt
from src.buissness_logic import generate_unique_value
from src.buissness_logic import generate_today_date

import tests.utils.jwt as jwt_utils


def test_generate_today_date():
    now, expected_value = datetime(1970, 1, 1), "1970-01-01"

    with patch("src.buissness_logic.generate_now", lambda: now):
        received_value = generate_today_date()

    assert received_value == expected_value


def test_generate_unique_value():
    NUMBER_OF_TESTS = 100000

    # test optimized for efficiency
    unique_values = set()
    for _ in range(NUMBER_OF_TESTS):
        potentially_unique_value = generate_unique_value()

        before_add_size = len(unique_values)

        unique_values.add(potentially_unique_value)

        after_add_size = len(unique_values)

        assert before_add_size != after_add_size


def test_generate_upstream_jwt():
    UNIQUE_VALUE, SECONDS_SINCE_EPOCH, TODAY, NOW = (
        "foo",
        1,
        "1970-01-01",
        datetime(1970, 1, 1),
    )

    expected_claims = {
        "jti": UNIQUE_VALUE,
        "iat": SECONDS_SINCE_EPOCH,
        "payload": {"user": "username", "date": TODAY},
    }

    with patch("src.buissness_logic.generate_uuid", lambda: UNIQUE_VALUE):
        with patch(
            "src.buissness_logic.generate_seconds_since_epoch",
            lambda: SECONDS_SINCE_EPOCH,
        ):
            with patch("src.buissness_logic.generate_now", lambda: NOW):
                jwt = generate_upstream_jwt()

    received_claims = jwt_utils.decode(jwt)

    assert received_claims == expected_claims
