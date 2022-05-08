import pytest
def square(x):
    return x * x

def test_square():
    assert square(5) == 25


def throw_exception():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        throw_exception()