import argparse


def sphere_parser(basename="sphere.py"):

    default_input_file = None
    default_quadrant = "both"
    default_angle = 360.
    default_center = (0., 0.)
    default_model_name = "Model-1"
    default_part_name = "sphere"

    prog = "abaqus cae -noGui {} --".format(basename)
    cli_description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower " \
                      "(+X-Y), or both quadrants."

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--input-file', type=str, default=default_input_file,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=("both", "upper", "lower"), default=default_quadrant,
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--angle', type=float, default=default_angle,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--center', nargs=2, type=float, default=default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser
