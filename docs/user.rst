###########
User Manual
###########

.. include:: README.txt
    :start-after: user-start-do-not-remove
    :end-before: user-end-do-not-remove

********
Examples
********

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

      turbo-turtle sphere --inner-radius 1 --outer-radius 2 --output-file axisymmetric.cae --model-name axisymmetric --part-name axisymmetric --angle 0

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
