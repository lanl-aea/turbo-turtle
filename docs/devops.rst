=====
Clone
=====

.. include:: README.txt
   :start-after: cloning-the-repo-start-do-not-remove
   :end-before: cloning-the-repo-end-do-not-remove

===================
Compute Environment
===================

.. include:: README.txt
   :start-after: compute-env-start-do-not-remove
   :end-before: compute-env-end-do-not-remove

=======
Testing
=======

.. include:: README.txt
   :start-after: testing-start-do-not-remove
   :end-before: testing-end-do-not-remove

There is significant complexity in the test construction. This complexity makes adding new tests non-trivial, but
enables (1) simple regression suite test commands for local testing and (2) matrixed tests against multiple versions of
third-party software, e.g. Abaqus and Cubit.

The relevant files are

#. ``SConstruct``: Specify one or more Abaqus and Cubit command(s) and call the pytest configuration
#. ``pytest``: SConscript test configuration that builds the pytest command suite for both unit and system tests
#. ``pyproject.toml``: Define project specific pytest markers for test control
#. ``turbo_turtle/conftest.py``: Configure custom pytest command line options to allow pass-through Abaqus and Cubit
   executable paths
#. ``turbo_turtle/tests/*``: Directory containing unit and system test source files

   #. ``turbo_turtle/tests/test_system.py``: System test shell command definitions

The design of the system tests is intended to configure a full test suite for a matrix of construction environments. The
pytest marker assignment by associated backend software is important to allow subsets of the full suite to run in
dedicated construction environments. The matrixed construction environments are controlled under the SCons task
definitions for the ``systemtest`` alias.

This design of construction environments on the outside and a single test suite on the inside allows for execution
against a single version of each third-party software. The passthrough complexity also allows for direct pytest
execution. Testing against a non-default or range of third-party software paths can be achieved with the
``--abaqus-command`` and ``--cubit-command`` options to the launching command.

.. code-block::

   scons regression --abaqus-command /my/local/intallation/abaqus --cubit-command /my/local/installation/cubit
   scons regression --abaqus-command /apps/abaqus/Commands/abq2024 --abaqus-command /apps/abaqus/Commands/abq2023 --cubit-command /apps/Cubit-16.16/cubit --cubit-command /apps/Cubit-16.12/cubit

The pytest command only accepts a single version of third-party software at a time because the design intent is to wrap the
matrix of third-party software around the pytest command and limit the pytest suite to a single construction environment
at a time.

.. code-block::

   pytest -m 'systemtest' --abaqus-command /my/local/intallation/abaqus --cubit-command /my/local/installation/cubit
   pytest -m 'systemtest' --abaqus-command /apps/abaqus/Commands/abq2024 --cubit-command /apps/Cubit-16.16/cubit

================================
Package Interfaces and Structure
================================

The structure of this package is more complex than most Python 3 packages due to incompatible Python 3 and Abaqus Python
interpretters and environments. The structure is further complicated by the number of desirable external interfaces for
a variety of use cases. The package is structured for the following external interfaces, but not all are stable public
interfaces yet

#. Python 3 CLI (public): :ref:`turbo_turtle_cli`
#. Python 3 API (public): :ref:`external_api`
#. Abaqus Python GUI plugin (public): :ref:`abaqus_gui_plugins`
#. Abaqus Python API (private): :ref:`abaqus_python_package`
#. Abaqus Python CLI (private)

The primary interfaces are the Python 3 CLI and API. These are the focus for a stable version 1.0 release and promised
long term support. There are no real restrictions on the Python 3 package structure except that it must make selective,
per file imports of the modules found in the Abaqus Python package and directories to avoid importing Abaqus Python
modules which are incompatible with Python 3.

The Abaqus Python GUI interface is considered an experimental public interface. It is desirable to provide interactive
behavior consistent with the non-interactive command line behavior for heavily interactive workflows and debugging
purposes. The plugin structure benefits from the existing :ref:`abaqus_python_package` structure and adds additional
error handling complexity.

The Abaqus Python CLI and API are not currently exposed as public interfaces, but the interfaces and package structure
restrictions must be maintained for internal use. They are considered private mostly to allow instability in internal
module structure and behavior as the project explores the best way to manage the Abaqus Python package structure and
Abaqus Python error handling. These interfaces are subject to change without warning as long as they don't break the
public Python 3 behavior. If these interfaces stabilize, it may be desirable to release a subset of the Abaqus Python
API in the future, e.g. the Abaqus Python set creation utilities. There is little benefit to exposing the Abaqus Python
CLI because it is largely a pass through duplication of the Python 3 CLI.

To accomodate the Abaqus Python API and GUI, the Python 3 and Abaqus Python root package directories must be separated
by an intermediate layer provided by the ``_abaqus_python`` directory. The GUI plugin file, ``_turbo_turtle_plugin.py``,
and the Abaqus Python package root directory, ``turbo_turtle_abaqus``, can be found in this directory.

* ``turbo-turtle/``: repository root

  * ``turbo_turtle/``: Python 3 package root

    * ``_abaqus_python/``: separation layer to avoid cross polluting the Python 3 and Abaqus Python namespaces. Put on
      PYTHONPATH to import Abaqus Python package. Put in Abaqus plugin directory to use the Abaqus GUI.

      * ``_turbo_turtle_plugin.py``
      * ``turbo_turtle_abaqus/``: Abaqus Python package root

This layer of separation makes it possible to put the parent directory of ``turbo_turtle_abaqus`` on PYTHONPATH, which
makes the Abaqus Python API an importable package without accidentally including Python 3 modules. This is necessary for
the GUI behavior, which uses the Abaqus Python API, and helps disambiguate the Abaqus Python package internal imports.

The Abaqus Python package itself is separated into pure Abaqus Python and mixed Python 2/3 compatible modules. This is
necessary to allow re-use of common settings and functions in the Python 3 package for consistency with the Abaqus
Python implementation and CLI options. The Abaqus Python package internal imports are complicated by this module
separation and Python 3 re-use. Each module must put the ``turbo_turtle_abaqus`` package root directory on PYTHONPATH
before the internal imports are possible. This takes the form of boilerplate code required in every module which locates
the package root with respect to the module file and a ``sys.path`` modification prior to internal imports.

.. code-block::

    import os
    import sys
    import inspect

    filename = inspect.getfile(lambda: None)
    basename = os.path.basename(filename)
    parent = os.path.dirname(filename)
    grandparent = os.path.dirname(parent)
    sys.path.insert(0, grandparent)
    from turbo_turtle_abaqus import parsers

In addition to the import structure, the pure Abaqus Python modules must not import Abaqus packages at the module level.
This is required to enable Sphinx documentation of the internal API, which is performed in a Python 3 environment. Mixed
Python 2/3 compatible packages may not perform *any* internal package imports because the ``sys.path`` modifications
would expose the Abaqus Python package to the Python 3 namespace.

Finally, the Abaqus Python CLI is simply direct execution of the individual subcommand modules in the Abaqus Python
package. Executing against the Abaqus Python CLI can be performed by absolute or by a PATH modification independent from
the Abaqus Python API PYTHONPATH modification. To use the CLI, the ``turbo_turtle_abaqus`` directory itself, not its
parent, must be put on PATH. It would be possible to write a dedicated, wrapping main module for the Abaqus Python CLI;
however, this has not been necessary so far. It might be desirable to make the PATH and PYTHONPATH consistent if the
Abaqus Python CLI were made public or if the consolidated CLI implementation could reduce duplication in the Python 3
CLI. This might be easiest with a new file in ``_abaqus_python``, e.g.
``turbo_turtle/_abaqus_python/turbo_turtle_abaqus_cli.py``, to make the CLI PATH and API PYTHONPATH directories
consistent. This is unnecessary in the current Python 3 pass through use of the Abaqus Python CLI, which calls the
Abaqus Python scripts by absolute path.

.. _abaqus_python_package:

=====================
Abaqus Python Package
=====================

Turbo-Turtle's Abaqus Python package can be imported into your own custom Abaqus Python scripts should you wish to use
the internal API rather than running Turbo-Turtle via command line. The :ref:`print_abaqus_path_cli` documentation
describes how to retrieve the absolute path to Turbo-Turtle's Abaqus Python compatible package.

Directory Structure
-------------------

The Turbo-Turtle Abaqus Python package is organized in the directory structure as shown below, where the top-level
``_abaqus_python`` directory is the package parent and plug-in central directory; the sub-directory
``turbo_turtle_abaqus`` is the Abaqus Python package directory.

.. code-block::

   $ pwd
   /path/to/turbo_turtle
   $ tree _abaqus_python
   _abaqus_python/
   ├── turbo_turtle_abaqus
   │   ├── _abaqus_utilities.py
   │   ├── cylinder.py
   │   ├── export.py
   │   ├── geometry.py
   │   ├── image.py
   │   ├── __init__.py
   │   ├── merge.py
   │   ├── mesh_module.py
   │   ├── _mixed_utilities.py
   │   ├── parsers.py
   │   ├── partition.py
   │   ├── sphere.py
   │   ├── test_abaqus_utilities.py
   │   ├── test_mixed_utilities.py
   │   ├── test_parsers.py
   │   ├── test_vertices.py
   │   └── vertices.py
   └── turbo_turtle_plugin.py

PYTHONPATH Modifications
------------------------

.. warning::

   Modifying your local Python environment can have unexpected consequences. Proceed with caution.

In order for the Turbo-Turtle Abaqus Python API to be importable, the package parent directory must be on your
``PYTHONPATH``. You can use the following command to add to your ``PYTHONPATH`` environment variable prior to executing
Abaqus CAE:

   .. code-block::

      PYTHONPATH=$(turbo_turtle print-abaqus-path):$PYTHONPATH abq2024 cae -noGui myScript.py

Importing Turbo-Turtle Modules
------------------------------

Turbo-Turtle's Abaqus Python package has been designed for you to make import statements at the package level. This
removes the risks of clashing with the Abaqus Python namespace when importing Turbo-Turtle modules. In your Python
script, you can use an import statement like shown below (assuming the ``_abaqus_python`` package directory is on your
``PYTHONPATH``).

.. code-block:: Python

   import turbo_turtle_abaqus.partition

   turbo_turtle_abaqus.partition.main()
