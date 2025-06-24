from turbo_turtle import _settings
from turbo_turtle import _utilities


def geometry(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.geometry_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "geometry.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {_utilities.character_delimited_list(args.input_file)} "
    command += f"--output-file {args.output_file} "
    command += f"--unit-conversion {args.unit_conversion} "
    command += f"--euclidean-distance {args.euclidean_distance} "
    if args.planar:
        command += "--planar "
    command += f"--model-name {args.model_name} "
    if args.part_name[0] is not None:
        command += f"--part-name {_utilities.character_delimited_list(args.part_name)} "
    command += f"--delimiter {args.delimiter} "
    command += f"--header-lines {args.header_lines} "
    command += f"--revolution-angle {args.revolution_angle} "
    command += f"--y-offset {args.y_offset} "
    if args.rtol is not None:
        command += f"--rtol {args.rtol} "
    if args.atol is not None:
        command += f"--atol {args.atol} "
    _utilities.run_command(command)


def cylinder(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.cylinder_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "cylinder.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--inner-radius {args.inner_radius} "
    command += f"--outer-radius {args.outer_radius} "
    command += f"--height {args.height} "
    command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} "
    command += f"--part-name {args.part_name} "
    command += f"--revolution-angle {args.revolution_angle} "
    command += f"--y-offset {args.y_offset}"
    _utilities.run_command(command)


def sphere(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.sphere_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "sphere.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--inner-radius {args.inner_radius} --outer-radius {args.outer_radius} "
    command += f"--output-file {args.output_file} "
    if args.input_file is not None:
        command += f"--input-file {args.input_file} "
    command += f"--quadrant {args.quadrant} --revolution-angle {args.revolution_angle} "
    command += f"--y-offset {args.y_offset} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    _utilities.run_command(command)


def partition(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.partition_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "partition.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--center {_utilities.character_delimited_list(args.center)} "
    command += f"--xvector {_utilities.character_delimited_list(args.xvector)} "
    command += f"--zvector {_utilities.character_delimited_list(args.zvector)} "
    command += f"--model-name {args.model_name} --part-name {_utilities.character_delimited_list(args.part_name)} "
    command += f"--big-number {args.big_number}"
    _utilities.run_command(command)


def sets(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.sets_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "sets.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    if args.face_sets is not None:
        face_sets = [[name, f'"{mask}"'] for name, mask in args.face_sets]
        command += _utilities.construct_append_options("--face-set", face_sets) + " "
    if args.edge_sets is not None:
        edge_sets = [[name, f'"{mask}"'] for name, mask in args.edge_sets]
        command += _utilities.construct_append_options("--edge-set", edge_sets) + " "
    if args.vertex_sets is not None:
        vertex_sets = [[name, f'"{mask}"'] for name, mask in args.vertex_sets]
        command += _utilities.construct_append_options("--vertex-set", vertex_sets)
    _utilities.run_command(command)


def mesh(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.mesh_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "mesh_module.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--element-type {args.element_type} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    command += f"--global-seed {args.global_seed} "
    if args.edge_seeds is not None:
        command += _utilities.construct_append_options("--edge-seed", args.edge_seeds)
    _utilities.run_command(command)


def merge(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.merge_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "merge.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {_utilities.character_delimited_list(args.input_file)} "
    command += f"--output-file {args.output_file} "
    command += f"--merged-model-name {args.merged_model_name} "
    if args.model_name[0] is not None:
        command += f"--model-name {_utilities.character_delimited_list(args.model_name)} "
    if args.part_name[0] is not None:
        command += f"--part-name {_utilities.character_delimited_list(args.part_name)}"
    _utilities.run_command(command)


def export(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.export_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "export.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--model-name {args.model_name} --part-name {_utilities.character_delimited_list(args.part_name)} "
    if args.element_type[0] is not None:
        command += f"--element-type {_utilities.character_delimited_list(args.element_type)} "
    command += f"--destination {args.destination} "
    if args.assembly is not None:
        command += f"--assembly {args.assembly}"
    _utilities.run_command(command)


def image(args, command):
    """Python 3 wrapper around the Abaqus Python
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.image_parser` CLI

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: abaqus executable path
    """
    script = _settings._abaqus_python_abspath / "image.py"

    command = f"{command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--output-file {args.output_file} "
    command += f"--x-angle {args.x_angle} "
    command += f"--y-angle {args.y_angle} "
    command += f"--z-angle {args.z_angle} "
    command += f"--image-size {_utilities.character_delimited_list(args.image_size)} "
    command += f"--model-name {args.model_name} "
    if args.part_name is not None:
        command += f"--part-name {args.part_name} "
    command += f"--color-map {args.color_map}"
    _utilities.run_command(command)
