.. _internal_api:

############
Internal API
############

********
Python 3
********

These modules are intended purely for use in Python 3. They do not need to be Abaqus Python compatible.

scons_extensions
================

.. automodule:: turbo_turtle.scons_extensions
   :noindex:
   :members:
   :private-members:

_main
=====

.. automodule:: turbo_turtle._main
   :members:
   :private-members:

_abaqus_wrappers
================

.. automodule:: turbo_turtle._abaqus_wrappers
   :members:
   :private-members:

_cubit_wrappers
===============

.. automodule:: turbo_turtle._cubit_wrappers
   :members:
   :private-members:

.. _cubit_python_api:

_cubit_python
=============

.. automodule:: turbo_turtle._cubit_python
   :members:
   :private-members:

.. _gmsh_python_api:

_gmsh_python
============

.. automodule:: turbo_turtle._gmsh_python
   :members:
   :private-members:

_utilities
==========

.. automodule:: turbo_turtle._utilities
   :members:
   :private-members:

.. _python3_tests:

**************
Python 3 tests
**************

These modules are intended purely for use in Python 3. They do not need to be Abaqus Python compatible, but they may
have corresponding :ref:`abaqus_python_tests`.

Python 3 unit test files may be executed with the ``pytest`` command directly, where the Abaqus Python test exclusions
is handled by the default pytest options in ``pyproject.toml``. For example from the project root directory

.. code-block::

   $ pytest

The test execution is also available as an SCons alias: ``pytest``, which is collected under the aliases: ``unittest``
and ``regression``. These aliases may provide additional ``pytest`` command line options which are not or can not be set
in ``pyproject.toml``.


test_main
=========

.. automodule:: turbo_turtle.tests.test_main
   :members:
   :private-members:

test_cubit_python
=================

.. automodule:: turbo_turtle.tests.test_cubit_python
   :members:
   :private-members:

test_fetch
==========

.. automodule:: turbo_turtle.tests.test_fetch
   :members:
   :private-members:

test_utilities
==============

.. automodule:: turbo_turtle.tests.test_utilities
   :members:
   :private-members:

test_geometry_xyplot.py
=======================

.. automodule:: turbo_turtle.tests.test_geometry_xyplot
   :members:
   :private-members:

test_parsers.py
===============

.. automodule:: turbo_turtle.tests.test_parsers
   :members:
   :private-members:

test_scons_extensions.py
========================

.. automodule:: turbo_turtle.tests.test_scons_extensions
   :members:
   :private-members:

test_system.py
==============

The system tests are not included in the default pytest options. They are marked with a ``systemtest`` marker and may be
executed with ``pytest -m systemtest``. They are also collected under the SCons alias ``systemtest`` which contains
additional pytest command line options to control test failure output more convenient to the system test execution.

.. automodule:: turbo_turtle.tests.test_system
   :members:
   :private-members:

test_wrappers.py
================

.. automodule:: turbo_turtle.tests.test_wrappers
   :members:
   :private-members:

test_vertices
=============

.. automodule:: turbo_turtle.tests.test_vertices
   :members:
   :private-members:

test_mixed_utilities
====================

.. automodule:: turbo_turtle.tests.test_mixed_utilities
   :members:
   :private-members:

**********
Python 2/3
**********

These modules are intended for re-use in both Python 3 and Abaqus Python. Care should be taken to maintain backward
compatibility with the Python 2.7 site-packages provided by Abaqus. For re-use in the Abaqus Python scripts, they must
be co-located in the Abaqus Python module. Modules may not perform internal package imports to minimize the risk of
polluting the Abaqus Python namespace with Python 3 modules, and vice versa.

These modules may have duplicate :ref:`python3_tests` ``turbo_turtle/tests/test*.py`` and :ref:`abaqus_python_tests`
``turbo_turtle/_abaqus_python/turbo_turtle_abaqus/test*.py``

parsers
=======

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers
   :members:
   :private-members:

vertices
========

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices
   :members:
   :private-members:

_mixed_utilities
================

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus._mixed_utilities
   :members:
   :private-members:

_mixed_settings
===============

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus._mixed_settings
   :members:
   :private-members:

.. _abaqus_python_api:

*************
Abaqus Python
*************

These modules are intended purely for Abaqus Python use, but may freely use the mixed Python 2/3 compatible modules and
other Abaqus Python modules. For the purposes of Sphinx compatible documentation, Abaqus package imports are not
located at the module level. Abaqus Python imports must be made in each function where they are used.

Internal package imports must treat the ``turbo_turtle_abaqus`` directory as the Abaqus Python compatible package root
to avoid accidentally placing Python 3 packages in PYTHONPATH before Abaqus Python packages. This is managed by common
boilerplate to modify ``sys.path``. The boilerplate is irreducible and must be duplicated in each module because the
modified import path is not available until after the ``sys.path`` modification.

_abaqus_utilities
=================

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus._abaqus_utilities
   :members:
   :private-members:

.. _abaqus_python_geometry_api:

geometry
========

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.geometry
   :members:
   :private-members:

cylinder
========

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.cylinder
   :members:
   :private-members:

sphere
======

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.sphere
   :members:
   :private-members:

.. _abaqus_python_partition_api:

partition
=========

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.partition
   :members:
   :private-members:

sets
====

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.sets
   :members:
   :private-members:

mesh_module
===========

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.mesh_module
   :members:
   :private-members:

image
=====

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.image
   :members:
   :private-members:

merge
=====

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.merge
   :members:
   :private-members:

export
======

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.export
   :members:
   :private-members:

.. _abaqus_python_tests:

*******************
Abaqus Python tests
*******************

These modules are intended purely for use in Abaqus Python. They do not need to be Python 3 compatible, but they may
have corresponding :ref:`python3_tests`. These tests would be signifacantly improved by understanding and adding Abaqus
Python mocking. Without mocking behavior, some of the Python 3 test conditions can not be replicated in Abaqus Python.

Abaqus python unit test files may be executed as ``abaqus python -m unittest discover <directory>``, for example from
the project root directory

.. code-block::

   $ /apps/abaqus/Commands/abq2024 python -m unittest discover turbo_turtle/_abaqus_python/turbo_turtle_abaqus

The test execution is also available as an SCons alias: ``test_abaqus_python``, which is collected under the aliases:
``unittest`` and ``regression``.

test_abaqus_utilities
=====================

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.test_abaqus_utilities
   :members:
   :private-members:

test_mixed_utilities
====================

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.test_mixed_utilities
   :members:
   :private-members:

test_parsers
============

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.test_parsers
   :members:
   :private-members:

test_vertices
=============

.. automodule:: turbo_turtle._abaqus_python.turbo_turtle_abaqus.test_vertices
   :members:
   :private-members:
