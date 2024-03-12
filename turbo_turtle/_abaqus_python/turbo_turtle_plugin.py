""" Turbo-Turtle Plugin Driver Script

This script defines Abaqus CAE plugin toolkit options
"""
from abaqusGui import *

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()  # Do this only once

# Geometry Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Geometry',
    moduleName='turbo_turtle_abaqus.geometry', functionName='_gui()',
    applicableModules=('Part', ),
    icon=afxCreateIcon('turboTurtleIcon.png'))

# Partition Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Partition',
    moduleName='turbo_turtle_abaqus.partition', functionName='_gui()',
    applicableModules=('Part', ),
    icon=afxCreateIcon('turboTurtleIcon.png'))
