import sys
import pathlib
import argparse
import subprocess


# TODO: write a Python 2/3 compatible parser and argument handler
def get_parser():

    default_center = [0.0, 0.0, 0.0]
    default_xpoint = [1.0, 0.0, 0.0]
    default_zpoint = [0.0, 0.0, 1.0]
    default_plane_angle = 45.0
    default_partitions_x = [0.0, 0.0]
    default_partitions_y = [0.0, 0.0]
    default_partitions_z = [0.0, 0.0]

    cli_description = "Partition a spherical shape into a turtle shell given a small number of locating parameters."

    parser = argparse.ArgumentParser(description=cli_description)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--model-name', type=str, required=True,
                        help="Abaqus model name")
    requiredNamed.add_argument('--part-name', type=str, required=True,
                        help="Abaqus part name")
    requiredNamed.add_argument('--input-file', type=str, required=True,
                        help="Abaqus model database to open")

    parser.add_argument('--output-file', type=str, default=None,
                        help="Abaqus model database to save to. Defaults to the specified --input-file")
    parser.add_argument('--abaqus-command', type=str, default="abq2023",
                        help='Abaqus executable absolute or relative path')

    parser.add_argument('--xpoint', nargs=3, type=float, default=default_xpoint,
                        help="Point on the x-axis (default: %(default)s)")
    parser.add_argument('--center', nargs=3, type=float, default=default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--zpoint', nargs=3, type=float, default=default_zpoint,
                        help="Point on the z-axis (default: %(default)s)")
    parser.add_argument('--plane-angle', type=float, default=default_plane_angle,
                        help="Angle for non-principal partitions (default: %(default)s)")
    parser.add_argument('--x-partitions', type=float, nargs='+', default=default_partitions_x,
                        help="Create a partition offset from the x-principal-plane (default: %(default)s)")
    parser.add_argument('--y-partitions', type=float, nargs='+', default=default_partitions_y,
                        help="Create a partition offset from the y-principal-plane (default: %(default)s)")
    parser.add_argument('--z-partitions', type=float, nargs='+', default=default_partitions_z,
                        help="Create a partition offset from the z-principal-plane (default: %(default)s)")
    return parser


def main():
    package_root = pathlib.Path(__file__).resolve().parent
    abaqus_main = package_root / "_abaqus.py"

    parser = get_parser()
    args, unknown = parser.parse_known_args()

    # TODO: write a Python 2/3 compatible parser and argument handler
    if args.output_file is None:
        args.output_file = args.input_file

    command = f"{args.abaqus_command} cae -noGui {abaqus_main} -- "
    command += f"--model-name {args.model_name} --part-name {args.part_name} --output-file {args.output_file} "
    command += f"--xpoint {' '.join(map(str, args.xpoint))} "
    command += f"--center {' '.join(map(str, args.center))} "
    command += f"--zpoint {' '.join(map(str, args.zpoint))} "
    command += f"--plane-angle {args.plane_angle} "
    command += f"--x-partitions {' '.join(map(str, args.x_partitions))} "
    command += f"--y-partitions {' '.join(map(str, args.y_partitions))} "
    command += f"--z-partitions {' '.join(map(str, args.z_partitions))} "
    print(command)
    command = command.split()
    stdout = subprocess.check_output(command)


if __name__ == "__main__":
    sys.exit(main())
