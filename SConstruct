#! /usr/bin/env python

import os
import pathlib
import warnings

import waves
import setuptools_scm


warnings.filterwarnings(action="ignore", message="tag", category=UserWarning, module="setuptools_scm")


AddOption(
    "--build-dir",
    dest="variant_dir_base",
    default="build",
    nargs=1,
    type=pathlib.Path,
    action="store",
    metavar="DIR",
    help="SCons build (variant) root directory. Relative or absolute path. (default: '%default')"
)

# Inherit Conda environment from user's active environment and add options
env = waves.scons_extensions.WAVESEnvironment(
    ENV=os.environ.copy(),
    variant_dir_base=GetOption("variant_dir_base")
)

# Find third-party software
abaqus_versions = (2024, 2023, 2022, 2021, 2020)
env["abaqus_matrix"] = {
    f"abq{version}": env.AddProgram([f"/apps/abaqus/Commands/abq{version}"]) for version in abaqus_versions
}
cubit_versions = ("16.16", "16.12")
env["cubit_environments"] = dict()
for version in cubit_versions:
    cubit_environment = env.Clone()
    cubit_environment.AddCubit([f"/apps/Cubit-{version}/cubit"])
    env["cubit_environments"].update({f"cubit{version}": cubit_environment})
# TODO: separate the systemtests by third-party software and test against the appropriate environment matrix
env.AddCubit(["/apps/Cubit-16.16/cubit"])

# Set project meta data
project_variables = {
    "project_dir": Dir(".").abspath,
    "version": setuptools_scm.get_version(),
}
for key, value in project_variables.items():
    env[key] = value
project_variables_substitution = env.SubstitutionSyntax(project_variables)

# Add documentation build
build_dir = variant_dir_base / "docs"
SConscript(dirs="docs", variant_dir=build_dir, exports=["env", "project_variables_substitution"])

# Add pytests, style checks, and static type checking
workflow_configurations = ["pytest", "flake8", "mypy", "cProfile"]
for workflow in workflow_configurations:
    build_dir = variant_dir_base / workflow
    SConscript(build_dir.name, variant_dir=build_dir, exports='env', duplicate=False)

waves.scons_extensions.project_help_message()
