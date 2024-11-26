"""Thin unpacking of the command line argparse namespace into full function interfaces"""

from turbo_turtle import _cubit_python


def geometry(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.geometry`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _cubit_python.geometry(
        args.input_file,
        args.output_file,
        planar=args.planar,
        part_name=args.part_name,
        unit_conversion=args.unit_conversion,
        euclidean_distance=args.euclidean_distance,
        delimiter=args.delimiter,
        header_lines=args.header_lines,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
        rtol=args.rtol,
        atol=args.atol,
    )


def cylinder(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.cylinder`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _cubit_python.cylinder(
        args.inner_radius,
        args.outer_radius,
        args.height,
        args.output_file,
        part_name=args.part_name,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
    )


def sphere(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.sphere`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _cubit_python.sphere(
        args.inner_radius,
        args.outer_radius,
        args.output_file,
        input_file=args.input_file,
        quadrant=args.quadrant,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
        part_name=args.part_name,
    )


def partition(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.partition`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    _cubit_python.partition(
        args.input_file,
        output_file=args.output_file,
        center=args.center,
        xvector=args.xvector,
        zvector=args.zvector,
        part_name=args.part_name,
        big_number=args.big_number,
    )


def sets(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.sets`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    _cubit_python.sets(
        args.input_file,
        output_file=args.output_file,
        part_name=args.part_name,
        face_sets=args.face_sets,
        edge_sets=args.edge_sets,
        vertex_sets=args.vertex_sets,
    )


def mesh(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.mesh`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _cubit_python.mesh(
        args.input_file,
        args.element_type,
        output_file=args.output_file,
        part_name=args.part_name,
        global_seed=args.global_seed,
        edge_seeds=args.edge_seeds,
    )


def merge(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.merge`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    _cubit_python.merge(
        args.input_file,
        args.output_file,
    )


def export(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.export`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    _cubit_python.export(
        args.input_file,
        part_name=args.part_name,
        element_type=args.element_type,
        destination=args.destination,
        output_type=args.output_type,
    )


def image(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.image`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path.
    """
    _cubit_python.image(
        args.input_file,
        args.output_file,
        command,
        x_angle=args.x_angle,
        y_angle=args.y_angle,
        z_angle=args.z_angle,
        image_size=args.image_size,
    )
