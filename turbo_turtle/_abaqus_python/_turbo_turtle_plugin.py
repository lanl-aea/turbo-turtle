"""Turbo-Turtle Plugin Driver Script

This script defines Abaqus CAE plugin toolkit options
"""

import inspect
import os
import sys

filename = inspect.getfile(lambda: None)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402

from abaqusGui import *  # noqa: E402,F403

# Do this only once
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()  # noqa: F405

# Cylinder Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Cylinder",
    moduleName="turbo_turtle_abaqus.cylinder",
    functionName="_gui()",
    applicableModules=("Part",),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._cylinder_gui_help_string,
)

# Sphere Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Sphere",
    moduleName="turbo_turtle_abaqus.sphere",
    functionName="_gui()",
    applicableModules=("Part",),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._sphere_gui_help_string,
)

# Geometry Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Geometry",
    moduleName="turbo_turtle_abaqus.geometry",
    functionName="_gui()",
    applicableModules=("Part",),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._geometry_gui_help_string,
)

# Partition Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Partition",
    moduleName="turbo_turtle_abaqus.partition",
    functionName="_gui()",
    applicableModules=("Part",),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._partition_gui_help_string,
)

# Mesh Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Mesh",
    moduleName="turbo_turtle_abaqus.mesh_module",
    functionName="_gui()",
    applicableModules=("Mesh",),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._mesh_gui_help_string,
)

# Image Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Image",
    moduleName="turbo_turtle_abaqus.image",
    functionName="_gui()",
    applicableModules=(
        "Part",
        "Assembly",
    ),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._image_gui_help_string,
)


# Export Gui Plugin
toolset.registerKernelMenuButton(
    buttonText="Turbo-Turtle|Export",
    moduleName="turbo_turtle_abaqus.export",
    functionName="_gui()",
    applicableModules=(
        "Assembly",
        "Mesh",
    ),
    icon=afxCreateIcon("turboTurtleIcon.png"),  # noqa: F405
    helpUrl=_mixed_settings._gui_docs_file,
    author=_mixed_settings._author,
    description=_mixed_settings._export_gui_help_string,
)
