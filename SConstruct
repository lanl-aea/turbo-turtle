#! /usr/bin/env python

import os
import pathlib

import waves


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
project_dir = Dir(".").abspath

variant_dir_base = pathlib.Path(env["variant_dir_base"])
build_dir = variant_dir_base / "docs"
SConscript(dirs="docs", variant_dir=pathlib.Path(build_dir), exports=["env", "project_dir"])

build_dir = variant_dir_base / "systemtests"
SConscript(build_dir.name, variant_dir=build_dir, exports="env", duplicate=False)

waves.builders.project_help_message()
