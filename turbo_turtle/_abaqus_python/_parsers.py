"""Python 2/3 compatible parsers for use in both the Abaqus Python scripts and the Turbo-Turtle Python 3 wrappers

Content *must* be compatible with Python 2 and 3. Content should be limited to those things necessary to construct the
CLI parser(s). Other content, such as project/package settings type variables, can be included to minimize the required
``sys.path`` modifications required in the Abaqus Python package/scripts. For now, that means this file does double duty
as the Abaqus Python package settings file and the parsers file.
"""
import argparse


sphere_default_input_file = None
sphere_default_quadrant = "both"
sphere_default_angle = 360.
sphere_default_center = (0., 0.)
sphere_default_model_name = "Model-1"
sphere_default_part_name = "sphere"


def sphere_parser(basename="sphere.py", add_help=True):

    prog = "abaqus cae -noGui {} --".format(basename)
    cli_description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower " \
                      "(+X-Y), or both quadrants."

    if add_help:
        parser = argparse.ArgumentParser(description=cli_description, prog=prog)
    else:
        parser = argparse.ArgumentParser(add_help=add_help)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--input-file', type=str, default=sphere_default_input_file,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=("both", "upper", "lower"), default=sphere_default_quadrant,
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--angle', type=float, default=sphere_default_angle,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--center', nargs=2, type=float, default=sphere_default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=sphere_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=sphere_default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser
