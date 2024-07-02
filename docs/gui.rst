.. _abaqus_gui_plugins:

###################
Abaqus GUI Plug-ins
###################

.. warning::

   The GUI-related features discussed in this documentation are alpha-state features for early adopters and developer
   testing. Use caution when following this documentation, especially when it comes to modifying your local Abaqus
   environment.

************
GUI Plug-ins
************

Abaqus allows for custom GUI plug-ins to be added to the Abaqus/CAE environment. For more information about Abaqus/CAE
plug-ins and how to make them available to you in Abaqus/CAE, see the `Using plug-ins section of the Abaqus/CAE User's
Guide`_.

Make Turbo-Turtle Plug-ins Available
====================================

.. warning::

   Modifying the Abaqus environment should be considered an advanced usage. See the `Abaqus Environment Documentation`_
   for details of behavior and side effects.

In order for Abaqus to recognize Turbo-Turtle's plugins, you must modify your Abaqus environment with either
``abaqus_v6.env`` or ``custom_v6.env``, either of which can exist in your local home directory or in the working
directory where you will run Abaqus/CAE.

Abaqus looks for the ``plugin_central_dir`` variable to add to the paths where it looks for plugins. Using the absolute
path to your locally installed Turbo-Turtle Abaqus Python package (see :ref:`print_abaqus_path_cli`), you must add the
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

Once your Abaqus environment has been pointed at the Turbo-Turtle Abaqus Python package directory, GUI plug-ins should
be available in Abaqus/CAE through the 'Plug-ins...Turbo-Turtle' drop-down menus. All available Turbo-Turtle plug-ins
are available by a name identical (or nearly identical) to the Turbo-Turtle subcommand names.

Clicking on a plug-in name will launch a dialog box in Abaqus/CAE for user inputs to the plug-in. A help message is
displayed above the sections for user input. In general, the GUI plug-in interfaces are designed to behave the
same way as the Turbo-Turtle :ref:`turbo_turtle_cli`. However, the help message at the top of the dialog box will
describe any nuances specific to the GUI plug-in interface.

Getting More Help for Turbo-Turtle Plug-ins
===========================================

In adition to displaying a help message in the plug-in user interface, Turbo-Turtle plug-ins utilize built-in Abaqus/CAE
features to display more information about a GUI plug-in. In the same way you would access a Turbo-Turtle plug-in
(through the 'Plug-ins' menu), navigate to the 'About Plug-ins' tab at the bottom of the 'Plug-ins' drop-down menu. Here
you can find information for all GUI plug-ins that are available in your Abaqus/CAE environment. Expand
the 'Turbo-Turtle' section and then click the name of the plug-in you need help with. Note that there will be no
information on the 'Turbo-Turtle' tab, but rather within the sub-tabs for different Turbo-Turtle plug-ins.

From each plug-in's sub-tab in the 'About Plug-ins...Turbo-Turtle' menu, you can see author, version, and install
directory information; a 'View' help button; applicable Abaqus/CAE modules for the plug-in; and a description of the
plug-in. Clicking the 'View' help button will launch a web-browser linked to the locally installed version of the HTML
documentation.
