import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation


def test_test_slice():
    test_slice = """

@public
def foo(inp1: bytes <= 10) -> bytes <= 3:
    x = 5
    s = slice(inp1, start=3, len=3)
    y = 7
    return s

@public
def bar(inp1: bytes <= 10) -> num:
    x = 5
    s = slice(inp1, start=3, len=3)
    y = 7
    return x * y
    """

    c = get_contract_with_gas_estimation(test_slice)
    x = c.foo(b"badminton")
    assert x == b"min", x

    assert c.bar(b"badminton") == 35

    print('Passed slice test')


def test_test_slice2():
    test_slice2 = """
@public
def slice_tower_test(inp1: bytes <= 50) -> bytes <= 50:
    inp = inp1
    for i in range(1, 11):
        inp = slice(inp, start=1, len=30 - i * 2)
    return inp
    """

    c = get_contract_with_gas_estimation(test_slice2)
    x = c.slice_tower_test(b"abcdefghijklmnopqrstuvwxyz1234")
    assert x == b"klmnopqrst", x

    print('Passed advanced slice test')


def test_test_slice3():
    test_slice3 = """
x: num
s: bytes <= 50
y: num
@public
def foo(inp1: bytes <= 50) -> bytes <= 50:
    self.x = 5
    self.s = slice(inp1, start=3, len=3)
    self.y = 7
    return self.s

@public
def bar(inp1: bytes <= 50) -> num:
    self.x = 5
    self.s = slice(inp1, start=3, len=3)
    self.y = 7
    return self.x * self.y
    """

    c = get_contract_with_gas_estimation(test_slice3)
    x = c.foo(b"badminton")
    assert x == b"min", x

    assert c.bar(b"badminton") == 35

    print('Passed storage slice test')


def test_test_slice4():
    test_slice4 = """
@public
def foo(inp: bytes <= 10, start: num, len: num) -> bytes <= 10:
    return slice(inp, start=start, len=len)
    """

    c = get_contract_with_gas_estimation(test_slice4)
    assert c.foo(b"badminton", 3, 3) == b"min"
    assert c.foo(b"badminton", 0, 9) == b"badminton"
    assert c.foo(b"badminton", 1, 8) == b"adminton"
    assert c.foo(b"badminton", 1, 7) == b"adminto"
    assert c.foo(b"badminton", 1, 0) == b""
    assert c.foo(b"badminton", 9, 0) == b""
    try:
        c.foo(b"badminton", 0, 10)
        assert False
    except:
        pass
    try:
        c.foo(b"badminton", 1, 9)
        assert False
    except:
        pass
    try:
        c.foo(b"badminton", 9, 1)
        assert False
    except:
        pass
    try:
        c.foo(b"badminton", 10, 0)
        assert False
    except:
        pass

    print('Passed slice edge case test')
