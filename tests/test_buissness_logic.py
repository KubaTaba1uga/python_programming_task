from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import tests.utils.jwt as jwt_utils
from src._constants import JWT_HEADER_NAME
from src.buissness_logic import generate_today_date
from src.buissness_logic import generate_unique_value
from src.buissness_logic import generate_upstream_headers
from src.buissness_logic import generate_upstream_jwt
from src.buissness_logic import increment_global_counter
from src.utils.global_counter import GlobalCounter


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


def test_generate_upstream_headers():
    request = MagicMock()

    JWT, request.headers = "whatever", {"foo": "bar", "bar": "foo"}

    expected_value = deepcopy(request.headers)
    expected_value[JWT_HEADER_NAME] = JWT

    with patch("src.buissness_logic.generate_upstream_jwt", lambda: JWT):
        received_value = generate_upstream_headers(request)

    assert received_value == expected_value


async def test_increment_global_counter():
    expected_value = GlobalCounter.get() + 7

    @increment_global_counter
    async def dummy_func():
        pass

    for _ in range(expected_value):
        await dummy_func()

    received_value = GlobalCounter.get()

    assert received_value == expected_value


async def test_create_start_time():
    expected_value, mock = datetime.now(), MagicMock()

    with patch("src.buissness_logic.generate_now", lambda: expected_value):
        from src.buissness_logic import create_start_time

        @create_start_time
        def test(*args, **kwargs):
            mock(*args, **kwargs)

    test()

    mock.assert_called_with(expected_value)


# part responsible for talking with upstream is tested in test_proxy.py
# mocking requests would be too time consuming.
