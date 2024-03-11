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

======================================
Abaqus Python Module Naming Convention
======================================

The :meth:`turbo_turtle.main._print_abaqus_module_location` function assumes that subcommands have a matching
Abaqus python module with an identical name existing in the ``_settings.abaqus_python_abspath`` directory.
:issue:`134` is scoped to remove this dependency and allow more flexibility in naming of subcommands and the
corresponding Abaqus python modules.

=====================
Abaqus Python Package
=====================

Turbo-Turtle's Abaqus python package can be imported into your own custom Abaqus python scripts should you wish to use
the internal API rather than running turbo-turtle via command line. The :ref:`print_abaqus_path_cli` documentation
describes how to retrieve the absolute path to Turbo-Turtle's Abaqus Python compatible package.

Directory Structure
-------------------

The turbo-turtle Abaqus python package is organized in the directory structure as shown below, where the top-level
``_abaqus_python`` directory is the package parent and plug-in central directory; the sub-directory
``turbo_turtle_abaqus`` is the Abaqus python package directory.

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
   │   ├── mesh.py
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

   Modifying your local python environment can have unexpected consequences. Proceed with caution.

In order for the turbo-turtle Abaqus python API to be importable, the package parent directory must be on your
``PYTHONPATH``. You can use the following command to add to your ``PYTHONPATH`` enviornment variable prior to executing
Abaqus CAE:

   .. code-block::

      PYTHONPATH=$(turbo_turtle print-abaqus-path):$PYTHONPATH abq2023 cae -noGui myScript.py

Importing Turbo-Turtle Modules
------------------------------

Turbo-Turtle's Abaqus python package has been design for you to make import statements at the package level. This
removes the risks of clashing with the Abaqus python namespace when importing turbo-turtle modules. In your python
script, you can use an import statement like shown below (assuming the ``_abaqus_python`` package directory is on your
``PYTHONPATH``).

.. code-block:: Python

   import turbo_turtle_abaqus.partition

   turbo_turtle_abaqus.partition.main()

