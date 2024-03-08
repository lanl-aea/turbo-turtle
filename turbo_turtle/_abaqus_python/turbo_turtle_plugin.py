""" Turbo-Turtle Plugin Driver Script

This script defines Abaqus CAE plugin toolkit options. For this script to work, the code that this script calls must be 
in the same directory as this script.
"""
from abaqusGui import getAFXApp

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()  # Do this only once

# Partition Gui Plugin
toolset.registerKernelMenuButton(
buttonText='Turbo-Turtle|Partition',
moduleName='turbo_turtle_abaqus.partition', functionName='partition_gui()')
