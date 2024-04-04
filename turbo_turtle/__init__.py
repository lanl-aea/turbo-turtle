"""
Copyright (c) 2023, Triad National Security, LLC. All rights reserved.

This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL),
which is operated by Triad National Security, LLC for the U.S.  Department of Energy/National Nuclear Security
Administration. All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of
Energy/National Nuclear Security Administration. The Government is granted for itself and others acting on its behalf a
nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare derivative works, distribute
copies to the public, perform publicly and display publicly, and to permit others to do so.
"""

from importlib.metadata import version, PackageNotFoundError

from turbo_turtle import scons_extensions
from turbo_turtle import geometry_xyplot

try:
    __version__ = version("turbo_turtle")
except PackageNotFoundError:
    try:
        from turbo_turtle import _version
        __version__ = _version.version
    except ImportError:
        # Should only hit this when running as an un-installed package in the local repository
        import pathlib
        import warnings
        warnings.filterwarnings(action='ignore', message='tag', category=UserWarning, module='setuptools_scm')
        import setuptools_scm
        __version__ = setuptools_scm.get_version(root=pathlib.Path(__file__).parent.parent)
        # Remove third-party packages from the project namespace
        del warnings, pathlib, setuptools_scm

# Remove third-party packages from the project namespace
del version, PackageNotFoundError
