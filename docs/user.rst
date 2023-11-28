###########
User Manual
###########

.. include:: README.txt
    :start-after: user-start-do-not-remove
    :end-before: user-end-do-not-remove

****************
Examples: Abaqus
****************

See the :ref:`turbo_turtle_cli` documentation for additional subcommands and options.

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

      turbo-turtle export --input-file sphere.cae --output-file sphere.inp --model-name sphere --part-name sphere

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

      turbo-turtle export --input-file axisymmetric.cae --output-file axisymmetric.inp --model-name axisymmetric --part-name axisymmetric

***************
Examples: Cubit
***************

These examples are (nearly) identical to the Abaqus examples above, but appended with the ``--cubit`` flag. Because the
commands are (nearly) identical, they will be included as a single command block. See the :ref:`turbo_turtle_cli`
documentation for caveats in behavior for the Cubit implementation and translation of Abaqus jargon to Cubit jargon. The
list of commands will be expanded as they are implemented.

.. note::

   * The ``--model-name`` option has no corresponding Cubit concept and is ignored in all Cubit implementations.
   * The :ref:`mesh_cli` subcommand ``--element-type`` option maps to the Cubit meshing scheme concept. It is only used
     if a non-default scheme is passed: trimesh or tetmesh. Because the Abaqus and Cubit implementations share a command
     line parser, and the Abaqus implementation requires this option, it is always required in the Cubit implementation
     as well.

Three-dimensional sphere
========================

.. code-block::

   turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file sphere.cub --part-name sphere --cubit
   turbo-turtle partition --input-file sphere.cub --output-file sphere.cub --part-name sphere --cubit
   turbo-turtle mesh --input-file sphere.cub --output-file sphere.cub --part-name sphere --element-type dummy --global-seed 0.15 --cubit

Two-dimensional, axisymmetric sphere
====================================

.. code-block::

   turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file axisymmetric.cub --part-name axisymmetric --revolution-angle 0 --cubit
   turbo-turtle partition --input-file axisymmetric.cub --output-file axisymmetric.cub --part-name axisymmetric
   turbo-turtle mesh --input-file axisymmetric.cub --output-file axisymmetric.cub --part-name axisymmetric --element-type dummy --global-seed 0.15
