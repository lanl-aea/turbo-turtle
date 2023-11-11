import pathlib
import datetime


_project_name = "Turbo Turtle"
_project_name_short = "turbo-turtle"
_project_root_abspath = pathlib.Path(__file__).parent.resolve()
_abaqus_python_abspath = _project_root_abspath / "_abaqus_python"
_installed_docs_index = _project_root_abspath / "docs/index.html"

_current_year = datetime.datetime.now().year
_final_year = 2016 -1  # First year of the 6.XX to YYYY version number change, less one for the range command
_default_abaqus_command = "abaqus"
_abaqus_search_years = range(_current_year, _final_year, -1)
_abaqus_command_options = [_default_abaqus_command] + [f"abq{abs(number) % 100}" for number in _abaqus_search_years]
