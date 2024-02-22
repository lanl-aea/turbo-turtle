from contextlib import nullcontext as does_not_raise

import pytest
cubit = pytest.importorskip("cubit", reason="Could not import Cubit")

from turbo_turtle import _cubit_python


cubit_command_or_exception = {
    "good command": ("reset aprepro", does_not_raise()),
    "bad command": ("definitetlynotacubitcommand", pytest.raises(RuntimeError)),
}


@pytest.mark.parametrize("command, outcome",
                         cubit_command_or_exception.values(),
                         ids=cubit_command_or_exception.keys())
def test_cubit_command_or(command, outcome):
    with outcome:
        try:
            success = _cubit_python.cubit_command_or_exception(command)
            assert success is True
        finally:
            pass

    if not isinstance(outcome, does_not_raise):
        exit_outcome = pytest.raises(SystemExit)
    else:
        exit_outcome = outcome
    with exit_outcome:
        try:
            success = _cubit_python.cubit_command_or_exit(command)
            assert success is True
        finally:
            pass
