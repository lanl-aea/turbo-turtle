###################
Abaqus GUI Plug-ins
###################

.. warning::
   
   The GUI-related features discussed in this documentation are alpha-state features for early adopteres and developer
   testing. Use caution when following this documentation, especially when it comes to modifying your local Abaqus 
   environment.

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
