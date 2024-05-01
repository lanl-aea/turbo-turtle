.. _turbo_turtle_cli:

######################
Command Line Utilities
######################

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :nosubcommands:

.. _cli_subcommands:

Sub-commands
============

docs
----

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: docs

fetch
-----

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: fetch

.. _print_abaqus_path_cli:

print-abaqus-path
-----------------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: print-abaqus-path

.. _geometry_cli:

geometry
--------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: geometry

.. _geometry_xyplot_cli:

geometry-xyplot
---------------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: geometry-xyplot

.. _cylinder_cli:

cylinder
--------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: cylinder

.. _sphere_cli:

sphere
------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: sphere

.. _partition_cli:

partition
---------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: partition

.. _sets_cli:

sets
----

.. warning::

   Abaqus masks are fragile with respect to geometry creation order. If previously working masks no longer produce the
   expected result, open the model file and verify that the masks still correspond to the expected geometry.

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: sets

.. _mesh_cli:

mesh
----

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: mesh

.. _image_cli:

image
-----

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: image

.. _merge_cli:

merge
-----

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: merge

.. _export_cli:

export
------

.. argparse::
   :ref: turbo_turtle._main.get_parser
   :nodefault:
   :path: export
