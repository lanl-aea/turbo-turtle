#! /usr/bin/env python

import os
import pathlib

env = Environment(ENV=os.environ.copy())
project_dir = Dir(".").abspath

SConscript(dirs="docs", variant_dir=pathlib.Path("build/docs"), exports=["env", "project_dir"])
