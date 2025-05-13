import pathlib

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_settings


_project_root_abspath = pathlib.Path(_mixed_settings._project_root_abspath)
_project_name = "Turbo Turtle"
_project_name_short = "turbo-turtle"
_abaqus_python_parent_abspath = _project_root_abspath / "_abaqus_python"
_abaqus_python_abspath = _abaqus_python_parent_abspath / "turbo_turtle_abaqus"
_installed_docs_index = _project_root_abspath / "docs/index.html"
_default_abaqus_options = ["abaqus", "abq2024"]
_default_cubit_options = ["cubit"]
_backend_choices = ["abaqus", "cubit", "gmsh"]
_default_backend = _backend_choices[0]
_tutorials_directory = _project_root_abspath / "tutorials"
_fetch_exclude_patterns = ["__pycache__", ".pyc", ".sconf_temp", ".sconsign.dblite", "config.log"]
_fetch_subdirectories = ["tutorials"]

_cd_action_prefix = "cd ${TARGET.dir.abspath} &&"
_redirect_action_postfix = "> ${TARGETS[-1].abspath} 2>&1"
