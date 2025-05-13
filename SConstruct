#! /usr/bin/env python

import os
import pathlib
import platform
import warnings

import waves
import setuptools_scm


warnings.filterwarnings(action="ignore", message="tag", category=UserWarning, module="setuptools_scm")


AddOption(
    "--build-dir",
    dest="variant_dir_base",
    default="build",
    nargs=1,
    type=str,
    action="store",
    metavar="DIR",
    help="SCons build (variant) root directory. Relative or absolute path. (default: '%default')",
)
default_abaqus_command = "/apps/abaqus/Commands/abq2024"
AddOption(
    "--abaqus-command",
    dest="abaqus_command",
    nargs=1,
    type="string",
    action="append",
    metavar="COMMAND",
    help=f"Override for the Abaqus command. Repeat to specify more than one (default: '[{default_abaqus_command}]')",
)
default_cubit_command = "/apps/Cubit-16.16/cubit"
AddOption(
    "--cubit-command",
    dest="cubit_command",
    nargs=1,
    type="string",
    action="append",
    metavar="COMMAND",
    help=f"Override for the Cubit command. Repeat to specify more than one (default: '[{default_cubit_command}]')",
)

# Inherit Conda environment from user's active environment and add options
env = waves.scons_extensions.WAVESEnvironment(
    ENV=os.environ.copy(),
    variant_dir_base=pathlib.Path(GetOption("variant_dir_base")),
    abaqus_command=GetOption("abaqus_command"),
    cubit_command=GetOption("cubit_command"),
)
env["abaqus_command"] = env["abaqus_command"] if env["abaqus_command"] is not None else [default_abaqus_command]
env["cubit_command"] = env["cubit_command"] if env["cubit_command"] is not None else [default_cubit_command]
env["ENV"]["PYTHONDONTWRITEBYTECODE"] = 1

# Handle OS-aware tee output
system = platform.system().lower()
if system == "windows":  # Assume PowerShell
    env["tee_suffix"] = "$(| Tee-Object -FilePath ${TARGETS[-1].abspath}$)"
else:  # *Nix style tee
    env["tee_suffix"] = "$(2>&1 | tee ${TARGETS[-1].abspath}$)"

# Find third-party software
abaqus_commands = env["abaqus_command"]
abaqus_environments = dict()
for command in abaqus_commands:
    # TODO: more robust version/name recovery without CI server assumptions
    version = pathlib.Path(command).name
    abaqus_environment = env.Clone()
    abaqus_environment["abaqus"] = abaqus_environment.AddProgram([command])
    abaqus_environments.update({version: abaqus_environment})

cubit_commands = env["cubit_command"]
cubit_environments = dict()
for command in cubit_commands:
    # TODO: more robust version/name recovery without CI server assumptions
    version = pathlib.Path(command).parent.name
    cubit_environment = env.Clone()
    cubit_environment["cubit"] = cubit_environment.AddCubit([command])
    cubit_environments.update({version: cubit_environment})

# Set project meta data
project_variables = {
    "project_dir": Dir(".").abspath,
    "version": setuptools_scm.get_version(),
}
for key, value in project_variables.items():
    env[key] = value
project_variables_substitution = env.SubstitutionSyntax(project_variables)

# Add documentation build
build_dir = env["variant_dir_base"] / "docs"
SConscript(dirs="docs", variant_dir=build_dir, exports=["env", "project_variables_substitution"])

# Add pytests, style checks, and static type checking
workflow_configurations = ["pytest", "style", "mypy", "cProfile"]
for workflow in workflow_configurations:
    build_dir = env["variant_dir_base"] / workflow
    SConscript(
        build_dir.name,
        variant_dir=build_dir,
        exports=["env", "abaqus_environments", "cubit_environments"],
        duplicate=False,
    )

# TODO: Remove the exception handling when CI environment re-builds with WAVES>=0.12.6
try:
    waves.scons_extensions.project_help()
except AttributeError:
    waves.scons_extensions.project_help_message()
