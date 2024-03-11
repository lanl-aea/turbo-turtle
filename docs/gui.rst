############################
Abaqus Python & GUI Plug-ins
############################

.. warning::
   
   The GUI-related features discussed in this documentation are alpha-state features for early adopteres and developer
   testing. Use caution when following this documentation, especially when it comes to modifying your local Abaqus and 
   Python environments.

*********************
Abaqus Python Package
*********************

Turbo-Turtle's Abaqus python package can be imported into your own custom Abaqus python scripts should you wish to use 
the internal API rather than running turbo-turtle via command line. The :ref:`print_abaqus_path_cli` documentation 
describes how to retrieve the absolute path to Turbo-Turtle's Abaqus Python compatible package.

Directory Structure
===================

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
========================

.. warning::
   
   Modifying your local python environment can have unexpected consequences. Proceed with caution.
   
In order for the turbo-turtle Abaqus python API to be importable, the package parent directory must be on your 
``PYTHONPATH``. You can use the following command to add to your ``PYTHONPATH`` enviornment variable prior to executing 
Abaqus CAE:
   
   .. code-block::

      PYTHONPATH=$(turbo_turtle print-abaqus-path):$PYTHONPATH abq2023 cae -noGui myScript.py

Importing Turbo-Turtle Modules
==============================

Turbo-Turtle's Abaqus python package has been design for you to make import statements at the package level. This 
removes the risks of clashing with the Abaqus python namespace when importing turbo-turtle modules. In your python 
script, you can use an import statement like shown below (assuming the ``_abaqus_python`` package directory is on your 
``PYTHONPATH``).

.. code-block:: Python

   import turbo_turtle_abaqus.partition
   
   turbo_turtle_abaqus.partition.main()

************
GUI Plug-ins
************

Abaqus allows for custom GUI plug-ins to be added to the Abaqus/CAE environment. For more information about Abaqus/CAE 
plug-ins and how to make them available to you in Abaqus/CAE, see the **Using plug-ins** section of your Abaqus/CAE 
User's Guide.

Make Turbo-Turtle Plug-ins Available
====================================

.. warning::

   Modifying your local Abaqus environment can have unexpected consequences. Proceed with caution.

In order for Abaqus to recognize turbo-turtle's plugins, you must modify your Abaqus environment with either 
``abaqus_v6.env`` or ``custom_v6.env``, either of which can exist in your local home directory or in the working 
directory where you will run Abaqus/CAE.

Abaqus looks for the ``plugin_central_dir`` variable to add to the paths where it looks for plugins. Using the absolute 
path to your locally installed turbo-turtle Abaqus python package (see :ref:`print_abaqus_path_cli`), you must add the 
following to your ``abaqus_v6.env`` file:

.. code-block:: Python
   :caption: abaqus_v6.env

   plugin_central_dir = "/path/to/turbo_turtle/_abaqus_python"

Included below is a shell command that can be used to append to your ``abaqus_v6.env`` file in the current working 
directory. Note that if you wish to change your home directory's ``abaqus_v6.env`` file, you only need to modify the 
command below with the path to the Abaqus evironment file (i.e. ``~/abaqus_v6.env``).

.. code-block::

   echo plugin_central_dir = \"$(turbo-turtle print-abaqus-path)\" >> abaqus_v6.env

Running Turbo-Turtle Plug-ins
=============================

Once your Abaqus environment has been pointed at the turbo-turtle Abaqus python package directory, GUI plug-ins should 
be available in Abaqus/CAE through the 'Plug-ins...Turbo-Turtle' drop-down menus. Click on the Plug-in you would like to 
run, and a dialogue box will pop up in your GUI session.

GUI Plug-in Documentation
=========================

Follow the links below to find API documentation for the currently supported Abaqus/CAE GUI plugins:

* :ref:`abaqus_python_partition_api`
