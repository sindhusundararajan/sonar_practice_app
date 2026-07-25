from app import calculate_discount, divide


def test_calculate_discount():
    assert calculate_discount(100, 10) == 90


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
