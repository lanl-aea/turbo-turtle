""" Turbo-Turtle Plugin Driver Script

This script defines Abaqus CAE plugin toolkit options
"""
import inspect
import os
import sys

filename = inspect.getfile(lambda: None)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
from turbo_turtle_abaqus import _mixed_settings

from abaqusGui import *


toolset = getAFXApp().getAFXMainWindow().getPluginToolset()  # Do this only once

# Cylinder Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Cylinder',
    moduleName='turbo_turtle_abaqus.cylinder', functionName='_gui()',
    applicableModules=('Part', ),
    icon=afxCreateIcon('turboTurtleIcon.png'),
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._cylinder_gui_help_string)

# Geometry Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Geometry',
    moduleName='turbo_turtle_abaqus.geometry', functionName='_gui()',
    applicableModules=('Part', ),
    icon=afxCreateIcon('turboTurtleIcon.png'),
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._geometry_gui_help_string)

# Partition Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Partition',
    moduleName='turbo_turtle_abaqus.partition', functionName='_gui()',
    applicableModules=('Part', ),
    icon=afxCreateIcon('turboTurtleIcon.png'),
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._partition_gui_help_string)
