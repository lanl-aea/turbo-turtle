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

      PYTHONPATH=$(turbo_turtle print-abaqus-path):$PYTHONPATH abq2023 cae -noGui myScript.py

Importing Turbo-Turtle Modules
------------------------------

Turbo-Turtle's Abaqus Python package has been designed for you to make import statements at the package level. This
removes the risks of clashing with the Abaqus Python namespace when importing Turbo-Turtle modules. In your Python
script, you can use an import statement like shown below (assuming the ``_abaqus_python`` package directory is on your
``PYTHONPATH``).

.. code-block:: Python

   import turbo_turtle_abaqus.partition

   turbo_turtle_abaqus.partition.main()
