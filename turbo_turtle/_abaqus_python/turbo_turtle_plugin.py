""" Turbo-Turtle Plugin Driver Script

This script defines Abaqus CAE plugin toolkit options
"""
from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()  # Do this only once

# Partition Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Partition|Help',
    moduleName='turbo_turtle_abaqus.partition', functionName='partition_gui_help()')

# Partition Gui Plugin
toolset.registerKernelMenuButton(
    buttonText='Turbo-Turtle|Partition|Run',
    moduleName='turbo_turtle_abaqus.partition', functionName='partition_gui()',
    applicableModules=('Part', ))
