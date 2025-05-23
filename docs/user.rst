###########
User Manual
###########

|PROJECT| is a wrapper around common modeling operations in Abaqus :cite:`abaqus` and Cubit :cite:`cubit`. As much as
possible, the work for each subcommand is perfomed in Python 3 :cite:`python` to minimize solution approach duplication.
|PROJECT| makes a best effort to maintain common behaviors and features across each third-party software's modeling
concepts.

***********
Quick Start
***********

.. include:: README.txt
   :start-after: user-start-do-not-remove
   :end-before: user-end-do-not-remove

************
Installation
************

This project builds and deploys as a `Conda`_ package :cite:`conda,conda-gettingstarted`.

.. include:: README.txt
   :start-after: installation-start-do-not-remove
   :end-before: installation-end-do-not-remove

.. _quickstart:

****************
Examples: Abaqus
****************

|PROJECT| was originally written using Abaqus as the backend modeling and meshing software. Most of the interface
options and descriptions use Abaqus modeling concepts and language. See the :ref:`turbo_turtle_cli` documentation for
additional subcommands and options.

Three-dimensional sphere
========================

.. figure:: sphere.png

1. Create the geometry

   .. code-block::

      turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file sphere.cae --model-name sphere --part-name sphere

2. Partition the geometry

   .. code-block::

      turbo-turtle partition --input-file sphere.cae --output-file sphere.cae --model-name sphere --part-name sphere

3. Mesh the geometry

   .. code-block::

      turbo-turtle mesh --input-file sphere.cae --output-file sphere.cae --model-name sphere --part-name sphere --element-type C3D8 --global-seed 0.15

4. Create an assembly image

   .. code-block::

      turbo-turtle image --input-file sphere.cae --output-file sphere.png --model-name sphere --part-name sphere

5. Export an orphan mesh

   .. code-block::

      turbo-turtle export --input-file sphere.cae --model-name sphere --part-name sphere

Two-dimensional, axisymmetric sphere
====================================

.. figure:: axisymmetric.png

1. Create the geometry

   .. code-block::

      turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file axisymmetric.cae --model-name axisymmetric --part-name axisymmetric --revolution-angle 0

2. Partition the geometry

   .. code-block::

      turbo-turtle partition --input-file axisymmetric.cae --output-file axisymmetric.cae --model-name axisymmetric --part-name axisymmetric

3. Mesh the geometry

   .. code-block::

      turbo-turtle mesh --input-file axisymmetric.cae --output-file axisymmetric.cae --model-name axisymmetric --part-name axisymmetric --element-type CAX4 --global-seed 0.15

4. Create an assembly image

   .. code-block::

      turbo-turtle image --input-file axisymmetric.cae --output-file axisymmetric.png --model-name axisymmetric --part-name axisymmetric

5. Export an orphan mesh

   .. code-block::

      turbo-turtle export --input-file axisymmetric.cae --model-name axisymmetric --part-name axisymmetric

***************
Examples: Cubit
***************

These examples are (nearly) identical to the Abaqus examples above, but appended with the ``--backend cubit`` option.
Because the commands are (nearly) identical, they will be included as a single command block. See the
:ref:`turbo_turtle_cli` documentation for caveats in behavior for the Cubit implementation and translation of Abaqus
language to Cubit language. The list of commands will be expanded as they are implemented.

.. note::

   * The ``--model-name`` option has no corresponding Cubit concept and is ignored in all Cubit implementations.
   * The :ref:`mesh_cli` subcommand ``--element-type`` option maps to the Cubit meshing scheme concept. It is only used
     if a non-default scheme is passed: trimesh or tetmesh. Because the Abaqus and Cubit implementations share a command
     line parser, and the Abaqus implementation requires this option, it is always required in the Cubit implementation
     as well.
   * The :ref:`image_cli` subcommand must launch a Cubit window and the Cubit commands only work in APREPRO journal
     files, so an ``output_file``.jou file is created.

Three-dimensional sphere
========================

.. figure:: sphere-cubit.png

.. code-block::

   turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file sphere.cub --part-name sphere --backend cubit
   turbo-turtle partition --input-file sphere.cub --output-file sphere.cub --part-name sphere --backend cubit
   turbo-turtle mesh --input-file sphere.cub --output-file sphere.cub --part-name sphere --element-type dummy --global-seed 0.15 --backend cubit
   turbo-turtle image --input-file sphere.cub --output-file sphere.png --backend cubit
   turbo-turtle export --input-file sphere.cub --part-name sphere --backend cubit

Two-dimensional, axisymmetric sphere
====================================

.. figure:: axisymmetric-cubit.png

.. code-block::

   turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file axisymmetric.cub --part-name axisymmetric --revolution-angle 0 --backend cubit
   turbo-turtle partition --input-file axisymmetric.cub --output-file axisymmetric.cub --part-name axisymmetric
   turbo-turtle mesh --input-file axisymmetric.cub --output-file axisymmetric.cub --part-name axisymmetric --element-type dummy --global-seed 0.15
   turbo-turtle image --input-file axisymmetric.cub --output-file axisymmetric.png --backend cubit
   turbo-turtle export --input-file axisymmetric.cub --part-name axisymmetric

****************
SCons extensions
****************

|PROJECT| includes extensions to the `SCons`_ :cite:`scons,scons-user` build system in the :ref:`external_api`
:ref:`scons_extensions` module. These may be used when importing |PROJECT| as a Python package in an `SCons`_
configuration file. For example:

.. admonition:: SConstruct

    .. literalinclude:: tutorials_SConstruct
       :language: Python
       :lineno-match:

.. admonition:: SConscript

   .. literalinclude:: tutorials_SConscript
      :language: Python
      :lineno-match:
