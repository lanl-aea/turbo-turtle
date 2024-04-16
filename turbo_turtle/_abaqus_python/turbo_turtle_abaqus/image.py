import os
import sys
import shutil
import inspect
import argparse
import tempfile


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers
import _mixed_utilities
import _abaqus_utilities


def main(input_file, output_file,
         x_angle=parsers.image_defaults["x_angle"],
         y_angle=parsers.image_defaults["y_angle"],
         z_angle=parsers.image_defaults["z_angle"],
         image_size=parsers.image_defaults["image_size"],
         model_name=parsers.image_defaults["model_name"],
         part_name=parsers.image_defaults["part_name"],
         color_map=parsers.image_color_map_choices[0]):
    """Wrap image with file input handling

    :param str input_file: Abaqus input file. Suports ``*.inp`` and ``*.cae``.
    :param str output_file: Output image file. Supports ``*.png`` and ``*.svg``.
    :param float x_angle: Rotation about X-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param float y_angle: Rotation about Y-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param float z_angle: Rotation about Z-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param str color_map: color map key

    :returns: writes image to ``{output_file}``
    """
    import abaqus

    input_file_extension = os.path.splitext(input_file)[1]
    if input_file_extension.lower() == ".cae":
        with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
            shutil.copyfile(input_file, copy_file.name)
            abaqus.openMdb(pathName=copy_file.name)
            image(output_file, x_angle=x_angle, y_angle=y_angle, z_angle=z_angle, image_size=image_size,
                  model_name=model_name, part_name=part_name, color_map=color_map)
    elif input_file_extension.lower() == ".inp":
        abaqus.mdb.ModelFromInputFile(name=model_name, inputFileName=input_file)
        image(output_file, x_angle=x_angle, y_angle=y_angle, z_angle=z_angle, image_size=image_size,
              model_name=model_name, part_name=part_name, color_map=color_map)
    else:
        message = "Uknown file extension {}".format(input_file_extension)
        _mixed_utilities.sys_exit(message)


def image(output_file,
          x_angle=parsers.image_defaults["x_angle"],
          y_angle=parsers.image_defaults["y_angle"],
          z_angle=parsers.image_defaults["z_angle"],
          image_size=parsers.image_defaults["image_size"],
          model_name=parsers.image_defaults["model_name"],
          part_name=parsers.image_defaults["part_name"],
          color_map=parsers.image_color_map_choices[0]):
    """Script for saving a part or assembly view image for a given Abaqus input file.

    The color map is set to color by material. Finally, viewport is set to fit the view to the viewport screen.

    If ``part_name`` is specified, an image of that part will be exported. If no ``part_name`` is specified, the model's
    root assembly will be queried and if empty, all parts in the model will be instanced into the root assembly. Then,
    an image of the root assembly will be exported. The ``input_file`` is not modified to include any generated
    instances.

    :param str output_file: Output image file. Supports ``*.png`` and ``*.svg``.
    :param float x_angle: Rotation about X-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python method
    :param float y_angle: Rotation about Y-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python method
    :param float z_angle: Rotation about Z-axis in degrees for ``abaqus.session.viewports[].view.rotate`` Abaqus Python method
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param str color_map: color map key

    :returns: writes image to ``{output_file}``
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
        abaqus.session.viewports['Viewport: 1'].assemblyDisplay.setValues(
            optimizationTasks=abaqusConstants.OFF,
            geometricRestrictions=abaqusConstants.OFF,
            stopConditions=abaqusConstants.OFF)
        abaqus.session.viewports['Viewport: 1'].setValues(displayedObject=assembly)
    else:
        part_object = abaqus.mdb.models[model_name].parts[part_name]
        abaqus.session.viewports['Viewport: 1'].setValues(displayedObject=part_object)

    abaqus.session.viewports['Viewport: 1'].view.rotate(xAngle=x_angle, yAngle=y_angle, zAngle=z_angle, mode=abaqusConstants.MODEL)
    abaqus.session.viewports['Viewport: 1'].view.fitView()
    abaqus.session.viewports['Viewport: 1'].enableMultipleColors()
    abaqus.session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap = abaqus.session.viewports['Viewport: 1'].colorMappings[color_map]
    abaqus.session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    abaqus.session.viewports['Viewport: 1'].disableMultipleColors()
    abaqus.session.printOptions.setValues(vpDecorations=abaqusConstants.OFF)
    abaqus.session.pngOptions.setValues(imageSize=image_size)

    output_format = _abaqus_utilities.return_abaqus_constant_or_exit(output_file_extension)
    if output_format is None:
        _mixed_utilities.sys_exit("Abaqus does not recognize the output extension '{}'".format(output_file_extension))

    abaqus.session.printToFile(
        fileName=output_file_stem,
        format=output_format,
        canvasObjects=(abaqus.session.viewports['Viewport: 1'], )
    )


if __name__ == "__main__":

    parser = parsers.image_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.input_file,
        args.output_file,
        x_angle=args.x_angle,
        y_angle=args.y_angle,
        z_angle=args.z_angle,
        image_size=args.image_size,
        model_name=args.model_name,
        part_name=args.part_name,
        color_map=args.color_map,
    ))
