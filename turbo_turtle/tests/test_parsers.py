import argparse
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

import pytest
import numpy

from turbo_turtle._abaqus_python import parsers


positive_float = {
    "zero": ("0.", 0., does_not_raise()),
    "one": ("1.", 1., does_not_raise()),
    "negative": ("-1.", None, pytest.raises(argparse.ArgumentTypeError)),
    "string": ("negative_one", None, pytest.raises(argparse.ArgumentTypeError)),
}


@pytest.mark.parametrize("input_string, expected_float, outcome",
                         positive_float.values(),
                         ids=positive_float.keys())
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


@pytest.mark.parametrize("input_string, expected_int, outcome",
                         positive_int.values(),
                         ids=positive_int.keys())
def test_positive_int(input_string, expected_int, outcome):
    with outcome:
        try:
            argument = parsers.positive_int(input_string)
            assert argument == expected_int
        finally:
            pass


construct_prog = {
    "script": ("script", "abaqus cae -noGui script --")
}


@pytest.mark.parametrize("basename, expected_prog",
                         construct_prog.values(),
                         ids=construct_prog.keys())
def test_construct_prog(basename, expected_prog):
    prog = parsers.construct_prog(basename)
    assert prog == expected_prog


subcommand_parser = {
    "geometry": ("geometry", ["--input-file", "input_file", "--output-file", "output_file"]),
}


@pytest.mark.parametrize("subcommand, positional_argv",
                         subcommand_parser.values(),
                         ids=subcommand_parser.keys())
def test_subcommand_parser(subcommand, positional_argv):
    subcommand_defaults = getattr(parsers, f"{subcommand}_defaults")
    subcommand_parser = getattr(parsers, f"{subcommand}_parser")

    defaults_argv = []
    for key, value in subcommand_defaults.items():
        if not isinstance(value, list) and value is not None and value is not False:
            defaults_argv.append(f"--{key.replace('_', '-')}")
            defaults_argv.append(str(value))
        if isinstance(value, list) and value[0] is not None:
            defaults_argv.append(f"--{key.replace('_', '-')}")
            defaults_argv.append(" ".join(map(str, value)))

    argv = ["dummy"] + positional_argv + defaults_argv
    with patch("sys.argv", argv):
        args, unknown = subcommand_parser().parse_known_args()
    args_dictionary = vars(args)
    for key, value in subcommand_defaults.items():
        assert args_dictionary[key] == value
