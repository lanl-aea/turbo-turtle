.. _api:

############
Internal API
############

********
Python 3
********

These modules are intended purely for use in Python 3.

main
====

.. automodule:: turbo_turtle.main
    :members:

_wrappers
=========

.. automodule:: turbo_turtle._wrappers
    :members:

**********
Python 2/3
**********

These modules are intended for re-use in both Python 3 and Abaqus Python. Care should be taken to maintain backward
compatibility with the Python 2.7 site-packages provided by Abaqus. For re-use in the Abaqus Python scripts, they must
be co-located in the Abaqus Python module. Each module should be self-contained to minimize the risk of polluting the
Abaqus Python namespace with Python 3 modules, and vice versa.

parsers
=======

.. automodule:: turbo_turtle._abaqus_python.parsers
    :members:

lines_and_splines
=================

.. automodule:: turbo_turtle._abaqus_python.lines_and_splines
    :members:

*************
Abaqus Python
*************

The modules are intended purely for Abaqus Python use, but may freely use the mixed Python 2/3 compatible modules.

geometry
========

.. automodule:: turbo_turtle._abaqus_python.geometry
    :members:

cylinder
========

.. automodule:: turbo_turtle._abaqus_python.cylinder
    :members:

sphere
======

.. automodule:: turbo_turtle._abaqus_python.sphere
    :members:

partition
=========

.. automodule:: turbo_turtle._abaqus_python.partition
    :members:

mesh
====

.. automodule:: turbo_turtle._abaqus_python.mesh
    :members:

image
=====

.. automodule:: turbo_turtle._abaqus_python.image
    :members:

merge
=====

.. automodule:: turbo_turtle._abaqus_python.merge
    :members:

export
======

.. automodule:: turbo_turtle._abaqus_python.export
    :members:
