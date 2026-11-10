from hypothesis import given, strategies as st
from bike_share_rental_parser import parse_ride_duration, format_station_code, parse_ride_log

# Fuzz testing strategies covering Unicode strings, NoneType, and unexpected primitive types
fuzz_input = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans()
)

# ---------------------------------------------------------
# Fuzz / Robustness Tests: Ensuring functions never crash
# ---------------------------------------------------------

@given(fuzz_input)
def test_parse_ride_duration_no_crash(s):
    """
    Property: parse_ride_duration should handle any arbitrary or invalid input
    gracefully without raising an unhandled exception or crashing.
    """
    try:
        res = parse_ride_duration(s)
        assert res is None or isinstance(res, int)
    except Exception as e:
        assert False, f"parse_ride_duration crashed with: {e}"


@given(fuzz_input)
def test_format_station_code_no_crash(s):
    """
    Property: format_station_code should handle any arbitrary or invalid input
    gracefully without raising an unhandled exception or crashing.
    """
    try:
        res = format_station_code(s)
        assert res is None or isinstance(res, str)
    except Exception as e:
        assert False, f"format_station_code crashed with: {e}"


@given(fuzz_input)
def test_parse_ride_log_no_crash(s):
    """
    Property: parse_ride_log should handle any arbitrary or invalid input
    gracefully without raising an unhandled exception or crashing.
    """
    try:
        res = parse_ride_log(s)
        assert res is None or isinstance(res, tuple)
    except Exception as e:
        assert False, f"parse_ride_log crashed with: {e}"


# ---------------------------------------------------------
# Property-Based Correctness Tests on Valid Domain Inputs
# ---------------------------------------------------------

@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=59))
def test_parse_ride_duration_valid(hours, minutes):
    """
    Property: For valid HH:MM inputs, parsed minutes must equal hours * 60 + minutes.
    """
    input_str = f"{hours:02d}:{minutes:02d}"
    expected = hours * 60 + minutes
    assert parse_ride_duration(input_str) == expected


@given(
    st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    st.integers(min_value=1, max_value=999)
)
def test_format_station_code_valid(zone, number):
    """
    Property: Valid alphanumeric codes like 'a12' should format to 'A-12'.
    """
    input_str = f"{zone}{number}"
    expected = f"{zone.upper()}-{number}"
    assert format_station_code(input_str) == expected


@given(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=15),
    st.integers(min_value=0, max_value=1000),
    st.sampled_from(["yes", "no"])
)
def test_parse_ride_log_valid(bike_type, minutes, sub_flag):
    """
    Property: Valid CSV ride log rows must parse accurately into (type, minutes, is_subscriber).
    """
    input_str = f"{bike_type},{minutes},{sub_flag}"
    expected = (bike_type, minutes, sub_flag == "yes")
    assert parse_ride_log(input_str) == expected
