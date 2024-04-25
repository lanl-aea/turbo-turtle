#! /usr/bin/env python

import os
import pathlib
import warnings

import waves
import setuptools_scm


warnings.filterwarnings(action="ignore", message="tag", category=UserWarning, module="setuptools_scm")

project_variables = {
    "project_dir": Dir(".").abspath,
    "version": setuptools_scm.get_version(),
}
project_variables_substitution = waves.scons_extensions.substitution_syntax(project_variables)

AddOption(
    "--build-dir",
    dest="variant_dir_base",
    default="build",
    nargs=1,
    type="string",
    action="store",
    metavar="DIR",
    help="SCons build (variant) root directory. Relative or absolute path. (default: '%default')"
)

env = Environment(
    ENV=os.environ.copy(),
    variant_dir_base=GetOption("variant_dir_base")
)
for key, value in project_variables.items():
    env[key] = value
env["abaqus"] = waves.scons_extensions.add_program(["/apps/abaqus/Commands/abq2023", "abq2023"], env)

variant_dir_base = pathlib.Path(env["variant_dir_base"])
build_dir = variant_dir_base / "docs"
SConscript(dirs="docs", variant_dir=pathlib.Path(build_dir), exports=["env", "project_variables_substitution"])

# Add pytests, style checks, and static type checking
workflow_configurations = ["pytest", "flake8", "mypy", "cProfile"]
for workflow in workflow_configurations:
    build_dir = variant_dir_base / workflow
    SConscript(build_dir.name, variant_dir=build_dir, exports='env', duplicate=False)

waves.scons_extensions.project_help_message()
