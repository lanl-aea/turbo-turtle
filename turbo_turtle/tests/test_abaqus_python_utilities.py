from contextlib import nullcontext as does_not_raise

import pytest

from turbo_turtle._abaqus_python import _utilities


validate_part_name = {
    "None one": (
        ["dummy.ext"], [None], ["dummy"], does_not_raise()
    ),
    "None two": (
        ["thing1.ext", "thing2.ext"], [None], ["thing1", "thing2"], does_not_raise()
    ),
    "one part": (
        ["one_part.ext"], ["part_one"], ["part_one"], does_not_raise()
    ),
    "two part": (
        ["one_part.ext", "two_part.ext"], ["part_one", "part_two"], ["part_one", "part_two"], does_not_raise()
    ),
    "seuss": (
        ["one_part.ext", "two_part.ext", "red_part.ext", "blue_part.ext"],
        ["part_one", "part_two", "part_red", "part_blue"],
        ["part_one", "part_two", "part_red", "part_blue"],
        does_not_raise()
    ),
    "wrong length: 2-1": (
        ["one_part.ext", "two_part.ext"],
        ["part_one"],
        [],
        pytest.raises(RuntimeError)
    ),
    "wrong length: 1-2": (
        ["one_part.ext"],
        ["part_one", "part_two"],
        [],
        pytest.raises(RuntimeError)
    ),
}


@pytest.mark.parametrize("input_file, original_part_name, expected, outcome",
                         validate_part_name.values(),
                         ids=validate_part_name.keys())
def test_validate_part_name(input_file, original_part_name, expected, outcome):
    with outcome:
        try:
            part_name = _utilities._validate_part_name(input_file, original_part_name)
            assert part_name == expected
        finally:
            pass
