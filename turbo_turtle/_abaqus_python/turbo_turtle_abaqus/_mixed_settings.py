import inspect
import os
import sys

_filename = inspect.getfile(lambda: None)
_parent = os.path.dirname(_filename)
_project_root_abspath = os.path.dirname(os.path.dirname(os.path.abspath(_parent)))

_author = "Kyle Brindley (kbrindley@lanl.gov), Thomas Roberts (tproberts@lanl.gov)"

_docs_directory = os.path.join(_project_root_abspath, 'docs')
_file_prefix = "file://"
_gui_docs_file = _file_prefix + os.path.join(_docs_directory, "gui.html")

_cylinder_gui_help_string = """
GUI-INPUTS
==========
* Part Name - part name for the cylinder being created.
* Model Name - parts will be created in a new model with this name
* Inner Radius - inner radius of the cylinder
* Outer Radius - outer radius of the cylinder
* Height - height of the cylinder
* Revolution Angle - revolution angle for a 3D part in degrees
* Y-Offset - offset along the global y-axis
"""

_geometry_gui_help_string = """
GUI-INPUTS
==========
* Input File(s) - glob statement or comma separated list of files (NO SPACES) with points in x-y coordinates
* Part Name(s) - part names for the parts being created. If ``None`` or blank, then part name is determined by the
  input files. This must either ``None`` or blank, a single part name, or a comma separated list of
  part names (NO SPACES)
* Model Name - parts will be created in a new model with this name
* Unit Conversion - unit conversion multiplication factor
* Euclidean Distance - connect points with a straight line if the distance between them is larger than this
* Planar Geometry Switch - switch to indicate that the 2D model is planar not axisymmetric (``True`` for planar)
* Revolution Angle - revolution angle for a 3D part in degrees
* Delimiter - delimiter character between columns in the input file(s)
* Header Lines - number of header lines to skip in the input file(s)
* Y-Offset - offset along the global y-axis
* rtol - relative tolerance used by ``numpy.isclose``. If ``None`` or blank, use numpy defaults
* atol - absolute tolerance used by ``numpy.isclose``. If ``None`` or blank, use numpy defaults
"""

_partition_gui_help_string = """
GUI-INPUTS
==========
* Center - center location of the geometry
* X-Vector - location on the x-axis local to the geometry
* Z-Vector - location on the z-axis local to the geometry
* Part Name(s) - part name(s) to partition as a comma separated list (NO SPACES). This can also be a glob statement
* Copy and Paste Parameters - copy and paste the parameters printed to the Abaqus Python terminal to make
  re-use of previous partition parameters easier
"""
