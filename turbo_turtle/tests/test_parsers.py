import argparse
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

import pytest
import numpy

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


positive_float = {
    "zero": ("0.", 0.0, does_not_raise()),
    "one": ("1.", 1.0, does_not_raise()),
    "negative": ("-1.", None, pytest.raises(argparse.ArgumentTypeError)),
    "string": ("negative_one", None, pytest.raises(argparse.ArgumentTypeError)),
}


@pytest.mark.parametrize(
    "input_string, expected_float, outcome",
    positive_float.values(),
    ids=positive_float.keys(),
)
def test_positive_float(input_string, expected_float, outcome):
    with outcome:
        try:
            argument = parsers.positive_float(input_string)
            assert numpy.isclose(argument, expected_float)
        finally:
            pass


positive_int = {
    "zero": ("0", 0, does_not_raise()),
    "one": ("1", 1, does_not_raise()),
    "negative": ("-1", None, pytest.raises(argparse.ArgumentTypeError)),
    "string": ("negative_one", None, pytest.raises(argparse.ArgumentTypeError)),
}


@pytest.mark.parametrize(
    "input_string, expected_int, outcome",
    positive_int.values(),
    ids=positive_int.keys(),
)
def test_positive_int(input_string, expected_int, outcome):
    with outcome:
        try:
            argument = parsers.positive_int(input_string)
            assert argument == expected_int
        finally:
            pass


construct_prog = {"script": ("script", "abaqus cae -noGui script --")}


@pytest.mark.parametrize(
    "basename, expected_prog",
    construct_prog.values(),
    ids=construct_prog.keys(),
)
def test_construct_prog(basename, expected_prog):
    prog = parsers.construct_prog(basename)
    assert prog == expected_prog


subcommand_parser = {
    "geometry": ("geometry", ["--input-file", "input_file", "--output-file", "output_file"], []),
    "cylinder": (
        "cylinder",
        ["--inner-radius", "1.", "--outer-radius", "2.", "--height", "1.", "--output-file", "output_file"],
        [],
    ),
    "sphere": ("sphere", ["--inner-radius", "1.", "--outer-radius", "2.", "--output-file", "output_file"], ["center"]),
    "partition": ("partition", ["--input-file", "input_file"], []),
    "sets": ("sets", ["--input-file", "input_file"], []),
    "mesh": ("mesh", ["--input-file", "input_file", "--element-type", "C3D8"], []),
    "merge": ("merge", ["--input-file", "input_file", "--output-file", "output_file"], []),
    "export": ("export", ["--input-file", "input_file"], ["output_type"]),
    "image": ("image", ["--input-file", "input_file", "--output-file", "output_file"], []),
}


@pytest.mark.parametrize(
    "subcommand, required_argv, exclude_keys",
    subcommand_parser.values(),
    ids=subcommand_parser.keys(),
)
def test_subcommand_parser(subcommand, required_argv, exclude_keys):
    """Test the default value assignments in the subcommand parsers

    :param str subcommand: the subcommand parser to test
    :param list required_argv: the argv list of strings for parser positional (required) arguments that have no
        default(s)
    :param list exclude_keys: keys that aren't used or set by the parser, but are included in the defaults dictionary.
        These are excluded from the key: value argparse.Namespace tests.
    """
    subcommand_defaults = getattr(parsers, f"{subcommand}_defaults")
    subcommand_parser = getattr(parsers, f"{subcommand}_parser")

    defaults_argv = []
    for key, value in subcommand_defaults.items():
        if not isinstance(value, list) and value is not None and value is not False:
            defaults_argv.append(f"--{key.replace('_', '-')}")
            defaults_argv.append(str(value))
        if isinstance(value, list) and value[0] is not None:
            defaults_argv.append(f"--{key.replace('_', '-')}")
            defaults_argv.extend([str(item) for item in value])

    argv = ["dummy"] + required_argv + defaults_argv
    with patch("sys.argv", argv):
        args, unknown = subcommand_parser().parse_known_args()
    args_dictionary = vars(args)
    for key, value in subcommand_defaults.items():
        if key not in exclude_keys:
            assert args_dictionary[key] == value
