import pathlib


_project_name = "Turbo Turtle"
_project_name_short = "turbo-turtle"
_project_root_abspath = pathlib.Path(__file__).parent.resolve()
_abaqus_python_abspath = _project_root_abspath / "_abaqus_python"
_installed_docs_index = _project_root_abspath / "docs/index.html"
_default_abaqus_options = ["abaqus", "abq2023"]
_default_cubit_options = ["cubit"]

# Copy from WAVES because some settings aren't available on conda-forge yet.
_cd_action_prefix = 'cd ${TARGET.dir.abspath} &&'
_redirect_action_postfix = "> ${TARGETS[-1].abspath} 2>&1"
