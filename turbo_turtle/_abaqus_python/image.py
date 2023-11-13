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
import _utilities


def main(input_file, output_file,
         x_angle=parsers.image_default_x_angle,
         y_angle=parsers.image_default_y_angle,
         z_angle=parsers.image_default_z_angle,
         image_size=parsers.image_default_image_size,
         model_name=parsers.image_default_model_name,
         part_name=parsers.image_default_part_name,
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
              model_name=model_name, part_name=lart_name, color_map=color_map)
    else:
        message = "Uknown file extension {}".format(input_file_extension)
        _utilities.sys_exit(message)


def image(output_file,
          x_angle=parsers.image_default_x_angle,
          y_angle=parsers.image_default_y_angle,
          z_angle=parsers.image_default_z_angle,
          image_size=parsers.image_default_image_size,
          model_name=parsers.image_default_model_name,
          part_name=parsers.image_default_part_name,
          color_map=parsers.image_color_map_choices[0]):
    """Script for saving an assembly view image (colored by material) for a given Abaqus input file.

    The color map is set to color by material. Finally, viewport is set to fit the view to the viewport screen.

    If the model assembly has no instances, use ``part_name`` to generate one. The ``input_file`` is not modified to
    include this generated instance.

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
    import abaqusConstants

    output_file_stem, output_file_extension = os.path.splitext(output_file)
    assembly = abaqus.mdb.models[model_name].rootAssembly
    if len(assembly.instances.keys()) == 0:
        part = abaqus.mdb.models[model_name].parts[part_name]
        assembly.Instance(name=part_name, part=part, dependent=abaqusConstants.ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=abaqusConstants.OFF, geometricRestrictions=abaqusConstants.OFF, stopConditions=abaqusConstants.OFF)
    session.viewports['Viewport: 1'].setValues(displayedObject=assembly)
    session.viewports['Viewport: 1'].view.rotate(xAngle=x_angle, yAngle=y_angle, zAngle=z_angle, mode=abaqusConstants.MODEL)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].enableMultipleColors()
    session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap=session.viewports['Viewport: 1'].colorMappings[color_map]
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    session.viewports['Viewport: 1'].disableMultipleColors()
    session.printOptions.setValues(vpDecorations=abaqusConstants.OFF)
    session.pngOptions.setValues(imageSize=image_size)
    session.printToFile(fileName=output_file_stem, format=get_abaqus_image_constant(output_file_extension),
        canvasObjects=(session.viewports['Viewport: 1'], ))


def get_abaqus_image_constant(file_extension):
    """
    Function for converting a string for an image file extension (e.g. ``.png``) to the corresponding
    ``abaqusConstants`` value.
    """
    import abaqusConstants

    switcher = {
        '.PNG': abaqusConstants.PNG,
        '.SVG': abaqusConstants.SVG
    }

    return switcher.get(file_extension.upper(), "")


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
        color_map=args.color_map
    ))
