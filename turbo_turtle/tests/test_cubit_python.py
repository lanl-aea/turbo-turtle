import pytest

cubit = pytest.importorskip("badpackage", reason="Could not import Cubit")


def test_cubit_command_or_exception():
    pass

def test_cubit_command_or_exit():
    pass
