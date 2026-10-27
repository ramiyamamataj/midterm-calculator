import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

@pytest.mark.parametrize("operation, a, b, expected", [
    ("add", 10.0, 5.0, 15.0),
    ("subtract", 10.0, 4.0, 6.0),
    ("multiply", 3.0, 5.0, 15.0),
    ("divide", 20.0, 4.0, 5.0),
    ("power", 2.0, 3.0, 8.0),
    ("root", 27.0, 3.0, 3.0),
    ("root", -8.0, 3.0, -2.0),
    ("modulus", 10.0, 3.0, 1.0),
    ("int_divide", 11.0, 2.0, 5.0),
    ("percent", 50.0, 200.0, 25.0),
    ("percent", 10.0, 100.0, 10.0),
    ("abs_diff", 5.0, 12.0, 7.0),
    ("abs_diff", 12.0, 5.0, 7.0),
])
def test_valid_operations(operation, a, b, expected):
    op = OperationFactory.get_operation(operation)
    assert op.execute(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("operation, a, b", [
    ("divide", 5.0, 0.0),
    ("modulus", 5.0, 0.0),
    ("int_divide", 5.0, 0.0),
    ("percent", 50.0, 0.0),
    ("root", 25.0, 0.0),
    ("root", -16.0, 2.0),
    ("power", 1e300, 1e300),
    ("power", -4.0, 0.5),
])
def test_operation_exceptions(operation, a, b):
    op = OperationFactory.get_operation(operation)
    with pytest.raises(OperationError):
        op.execute(a, b)

def test_invalid_operation_lookup():
    with pytest.raises(OperationError):
        OperationFactory.get_operation("non_existent_op")
