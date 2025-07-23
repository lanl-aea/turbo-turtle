import os
import sys
import inspect
import ast


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    input_file,
    output_file,
    x_angle=parsers.image_defaults["x_angle"],
    y_angle=parsers.image_defaults["y_angle"],
    z_angle=parsers.image_defaults["z_angle"],
    image_size=parsers.image_defaults["image_size"],
    model_name=parsers.image_defaults["model_name"],
    part_name=parsers.image_defaults["part_name"],
    color_map=parsers.image_color_map_choices[0],
):
    """Wrap image with file input handling

    :param str input_file: Abaqus input file. Suports ``*.inp`` and ``*.cae``.
    :param str output_file: Output image file. Supports ``*.png`` and ``*.svg``.
    :param float x_angle: Rotation about X-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param float y_angle: Rotation about Y-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param float z_angle: Rotation about Z-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param str color_map: color map key

    :returns: writes image to ``{output_file}``
    """
    import abaqus

    try:
        input_file_extension = os.path.splitext(input_file)[1]
        if input_file_extension.lower() == ".cae":
            with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
                image(
                    output_file,
                    x_angle=x_angle,
                    y_angle=y_angle,
                    z_angle=z_angle,
                    image_size=image_size,
                    model_name=model_name,
                    part_name=part_name,
                    color_map=color_map,
                )
        elif input_file_extension.lower() == ".inp":
            abaqus.mdb.ModelFromInputFile(name=model_name, inputFileName=input_file)
            image(
                output_file,
                x_angle=x_angle,
                y_angle=y_angle,
                z_angle=z_angle,
                image_size=image_size,
                model_name=model_name,
                part_name=part_name,
                color_map=color_map,
            )
        else:
            message = "Uknown file extension {}".format(input_file_extension)
            _mixed_utilities.sys_exit(message)
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))


def image(
    output_file,
    x_angle=parsers.image_defaults["x_angle"],
    y_angle=parsers.image_defaults["y_angle"],
    z_angle=parsers.image_defaults["z_angle"],
    image_size=parsers.image_defaults["image_size"],
    model_name=parsers.image_defaults["model_name"],
    part_name=parsers.image_defaults["part_name"],
    color_map=parsers.image_color_map_choices[0],
):
    """Script for saving a part or assembly view image for a given Abaqus input file.

    The color map is set to color by material. Finally, viewport is set to fit the view to the viewport screen.

    If ``part_name`` is specified, an image of that part will be exported. If no ``part_name`` is specified, the model's
    root assembly will be queried and if empty, all parts in the model will be instanced into the root assembly. Then,
    an image of the root assembly will be exported. The ``input_file`` is not modified to include any generated
    instances.

    :param str output_file: Output image file. Supports ``*.png`` and ``*.svg``.
    :param float x_angle: Rotation about X-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param float y_angle: Rotation about Y-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param float z_angle: Rotation about Z-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python
        method
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param str color_map: color map key

    :returns: writes image to ``{output_file}``

    :raises RuntimeError: if the extension of ``output_file`` is not recognized by Abaqus
    """
    import abaqus
    import abaqusConstants

    output_file_stem, output_file_extension = os.path.splitext(output_file)
    output_file_extension = output_file_extension.lstrip(".")
    if part_name is None:
        model = abaqus.mdb.models[model_name]
        assembly = model.rootAssembly
        if len(assembly.instances.keys()) == 0:
            for new_instance in model.parts.keys():
                part = model.parts[new_instance]
                assembly.Instance(name=new_instance, part=part, dependent=abaqusConstants.ON)
        abaqus.session.viewports["Viewport: 1"].assemblyDisplay.setValues(
            optimizationTasks=abaqusConstants.OFF,
            geometricRestrictions=abaqusConstants.OFF,
            stopConditions=abaqusConstants.OFF,
        )
        abaqus.session.viewports["Viewport: 1"].setValues(displayedObject=assembly)
    else:
        part_object = abaqus.mdb.models[model_name].parts[part_name]
        abaqus.session.viewports["Viewport: 1"].setValues(displayedObject=part_object)

    abaqus.session.viewports["Viewport: 1"].view.rotate(
        xAngle=x_angle, yAngle=y_angle, zAngle=z_angle, mode=abaqusConstants.MODEL
    )
    abaqus.session.viewports["Viewport: 1"].view.fitView()
    abaqus.session.viewports["Viewport: 1"].enableMultipleColors()
    abaqus.session.viewports["Viewport: 1"].setColor(initialColor="#BDBDBD")
    cmap = abaqus.session.viewports["Viewport: 1"].colorMappings[color_map]
    abaqus.session.viewports["Viewport: 1"].setColor(colorMapping=cmap)
    abaqus.session.viewports["Viewport: 1"].disableMultipleColors()
    abaqus.session.printOptions.setValues(vpDecorations=abaqusConstants.OFF)
    abaqus.session.pngOptions.setValues(imageSize=image_size)

    output_format = _abaqus_utilities.return_abaqus_constant_or_exit(output_file_extension)
    if output_format is None:
        error_message = "Abaqus does not recognize the output extension '{}'".format(output_file_extension)
        raise RuntimeError(error_message)

    abaqus.session.printToFile(
        fileName=output_file_stem,
        format=output_format,
        canvasObjects=(abaqus.session.viewports["Viewport: 1"],),
    )


def _validate_color_map(color_map, valid_color_maps):
    """Validate the user-provided color map against a provided list of valid color maps

    :param str color_map: user provided color map
    :param list valid_color_maps: valid color maps to check against

    :raises RuntimError: if user provided color map is invalid
    """
    if color_map not in valid_color_maps:
        error_message = "Error: Color Map option must be one of: {}".format(valid_color_maps)
        raise RuntimeError(error_message)


def _gui_get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._image_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Output File - output image file name (with '.png' or '.svg' extension)
    * Model Name - model to query
    * Part Name - part to query. If blank, assembly view will be queried
    * Color Map - valid Abaqus color map. Choose from: 'Material', 'Section', 'Composite layup', 'Composite ply',
      'Part', 'Part instance', 'Element set', 'Averaging region', 'Element type', 'Default', 'Assembly',
      'Part geometry', 'Load', 'Boundary condition', 'Interaction', 'Constraint', 'Property', 'Meshability',
      'Instance type', 'Set', 'Surface', 'Internal set', 'Internal surface', 'Display group', 'Selection group', 'Skin',
      'Stringer', 'Cell', 'Face'
    * Image Size - size in pixels. Width, Height
    * X-Angle - rotation about x-axis in degrees
    * Y-Angle - rotation about y-axis in degrees
    * Z-Angle - rotation about z-axis in degrees

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``image``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``output_file``: ``str`` type, output file name
    * ``part_name``: ``str`` type, part to query. If ``None`` the assembly view will be queried
    * ``model_name``: ``str`` type, model to query
    * ``color_map``: ``str`` type, valid Abaqus color map
    * ``image_size``: ``list`` type, image size in pixels [width, height]
    * ``x_angle``: ``float`` type, rotation about x-axis in degrees
    * ``y_angle``: ``float`` type, rotation about y-axis in degrees
    * ``z_angle``: ``float`` type, rotation about z-axis in degrees

    :raises RuntimeError: if ``output_file`` is not specified, if ``output_file`` extension is not valid, if
        ``color_map`` is not valid
    """
    import abaqus

    model_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.modelName

    try:
        default_part_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.name
        if default_part_name == "rootAssembly":
            default_color_map = "Assembly"
            default_part_name = ""  # Need to reset to blank string for proper handling in the image() function
        else:
            default_color_map = "Part geometry"
    except AttributeError:
        default_color_map = "Assembly"
        default_part_name = ""

    fields = (
        ("Output File", ""),
        ("Model Name:", model_name),
        ("Part Name:", default_part_name),
        ("Color Map:", default_color_map),
        ("Image Size:", str(parsers.image_defaults["image_size"]).replace("[", "").replace("]", "")),
        ("X-Angle:", str(parsers.image_defaults["x_angle"])),
        ("Y-Angle:", str(parsers.image_defaults["y_angle"])),
        ("Z-Angle:", str(parsers.image_defaults["z_angle"])),
    )

    output_file, model_name, part_name, color_map, image_size, x_angle, y_angle, z_angle = abaqus.getInputs(
        dialogTitle="Turbo Turtle Image",
        label=_mixed_settings._image_gui_help_string,
        fields=fields,
    )

    if model_name is not None:  # Model name will be None is the user hits the "cancel/esc" button
        if not output_file:
            error_message = "Error: You must specify an output file name"
            raise RuntimeError(error_message)

        if not part_name:
            part_name = None  # Blank string needs to be None when passed to image()

        _validate_color_map(color_map, parsers.image_color_map_choices)

        image_size = list(ast.literal_eval(image_size))

        user_inputs = {
            "output_file": output_file,
            "x_angle": float(x_angle),
            "y_angle": float(y_angle),
            "z_angle": float(z_angle),
            "image_size": image_size,
            "model_name": model_name,
            "part_name": part_name,
            "color_map": color_map,
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs required for driving the plugin"""
    _abaqus_utilities.gui_wrapper(inputs_function=_gui_get_inputs, subcommand_function=image, post_action_function=None)


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.image_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                args.input_file,
                args.output_file,
                x_angle=args.x_angle,
                y_angle=args.y_angle,
                z_angle=args.z_angle,
                image_size=args.image_size,
                model_name=args.model_name,
                part_name=args.part_name,
                color_map=args.color_map,
            )
        )
