from datetime import date, datetime, time


class IntMixin:
    method = "int"
    default_value = 3
    expected_value = 8
    other_value = 10
    unonvertible_value = "bar"


class StrMixin:
    method = "str"
    default_value = "foo"
    expected_value = "bar"
    other_value = "baz"
    unonvertible_value = None


class BoolMixin:
    method = "bool"
    default_value = True
    expected_value = False
    other_value = True
    unonvertible_value = "bar"


class DateMixin:
    method = "date"
    default_value = date(2020, 1, 1)
    expected_value = date(2020, 1, 2)
    other_value = date(2020, 1, 3)
    unonvertible_value = "bar"
    choices = [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3)]
    valid_choice = choices[0]
    invalid_choice = date(2020, 1, 4)
    min_val = date(2020, 1, 3)
    too_low = date(2020, 1, 2)
    max_val = date(2020, 1, 8)
    too_high = date(2020, 1, 9)
    goldilock = time(12, 0, 7)
    valid_strings = ["2020-01-01", "2020-01-02"]


class DateTimeMixin:
    method = "datetime"
    default_value = datetime(2020, 1, 1)
    expected_value = datetime(2020, 1, 2)
    other_value = datetime(2020, 1, 3)
    unonvertible_value = "bar"
    choices = [datetime(2020, 1, 1), datetime(2020, 1, 2), datetime(2020, 1, 3)]
    valid_choice = choices[0]
    invalid_choice = datetime(2020, 1, 4)
    min_val = datetime(2020, 1, 3)
    too_low = datetime(2020, 1, 2)
    max_val = datetime(2020, 1, 8)
    too_high = datetime(2020, 1, 9)
    goldilock = time(12, 0, 7)
    valid_strings = ["2020-01-01 12:00:00", "2020-01-02"]


class TimeMixin:
    method = "time"
    default_value = time(12, 0, 0)
    expected_value = time(12, 1, 0)
    other_value = time(12, 2, 0)
    unonvertible_value = "bar"
    choices = [time(12, 0, 0), time(12, 1, 0), time(12, 2, 0)]
    valid_choice = choices[0]
    invalid_choice = time(12, 3, 0)
    min_val = time(12, 1, 0)
    too_low = time(12, 0, 0)
    max_val = time(12, 2, 0)
    too_high = time(12, 3, 0)
    goldilock = time(12, 0, 1)
    valid_strings = ["12:00:00", "12:01", "13"]


class FloatMixin:
    method = "float"
    default_value = 3.0
    expected_value = 8.0
    other_value = 10.0
    unonvertible_value = "bar"
