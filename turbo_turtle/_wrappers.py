import subprocess


def geometry(args):
    """Python 3 wrapper around the Abaqus Python geometry CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_geometry.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {' '.join(map(str, args.input_file))} "
    command += f"--output-file {args.output_file} "
    command += f"--unit-conversion {args.unit_conversion} "
    command += f"--euclidian-distance {args.euclidian_distance} "
    if args.planar:
        command += f"--planar "
    command += f"--model-name {args.model_name} "
    command += f"--part-name {' '.join(map(str, args.part_name))} "
    command += f"--delimiter {args.delimiter} "
    command += f"--header-lines {args.header_lines} "
    command += f"--revolution-angle {args.revolution_angle}"
    command = command.split()
    stdout = subprocess.check_output(command)


def sphere(args):
    """Python 3 wrapper around the Abaqus Python sphere CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_sphere.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--inner-radius {args.inner_radius} --outer-radius {args.outer_radius} "
    command += f"--output-file {args.output_file} "
    if args.input_file is not None:
        command += f"--input-file {args.input_file} "
    command += f"--quadrant {args.quadrant} --angle {args.angle} "
    command += f"--center {' '.join(map(str, args.center))} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    command = command.split()
    stdout = subprocess.check_output(command)


def partition(args):
    """Python 3 wrapper around the Abaqus Python partition CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_partition.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    command += f"--xpoint {' '.join(map(str, args.xpoint))} "
    command += f"--center {' '.join(map(str, args.center))} "
    command += f"--zpoint {' '.join(map(str, args.zpoint))} "
    command += f"--plane-angle {args.plane_angle} "
    command += f"--x-partitions {' '.join(map(str, args.x_partitions))} "
    command += f"--y-partitions {' '.join(map(str, args.y_partitions))} "
    command += f"--z-partitions {' '.join(map(str, args.z_partitions))} "
    command = command.split()
    stdout = subprocess.check_output(command)


def mesh(args):
    """Python 3 wrapper around the Abaqus Python mesh CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_mesh.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--element-type {args.element_type} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    command += f"--global-seed {args.global_seed}"
    command = command.split()
    stdout = subprocess.check_output(command)


def export(args):
    """Python 3 wrapper around the Abaqus Python export CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_export.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--model-name {args.model_name} --part-name {' '.join(map(str, args.part_name))} "
    command += f"--element-type {' '.join(map(str, args.element_type))} "
    command += f"--destination {args.destination}"
    command = command.split()
    stdout = subprocess.check_output(command)


def image(args):
    """Python 3 wrapper around the Abaqus Python image CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._abaqus_python_abspath / "_image.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--output-file {args.output_file} "
    command += f"--x-angle {args.x_angle} "
    command += f"--y-angle {args.y_angle} "
    command += f"--z-angle {args.z_angle} "
    command += f"--image-size {' '.join(map(str, args.image_size))} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    command = command.split()
    stdout = subprocess.check_output(command)