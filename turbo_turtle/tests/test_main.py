from turbo_turtle import _main
from turbo_turtle import _settings


def test_print_abaqus_path(capsys):
    """Test the print-abaqus-path subcommand behavior"""

    # Test printing behavior
    expected_output = f"{_settings._abaqus_python_parent_abspath}\n"
    _main._print_abaqus_path_location()
    returned_output = capsys.readouterr()
    assert expected_output == returned_output.out
