import os
import sys
import shutil
import inspect
import argparse
import tempfile


default_x_angle = 0.
default_y_angle = 0.
default_z_angle = 0.
default_image_size = (1920, 1080)
default_model_name = "Model-1"
default_part_name = "Part-1"


def main(input_file, output_file, x_angle=default_x_angle, y_angle=default_y_angle, z_angle=default_z_angle,
         image_size=default_image_size, model_name=default_model_name, part_name=default_part_name):
    """Wrap image with file input handling

    :param str input_file: Abaqus input file. Suports ``*.inp`` and ``*.cae``.
    :param str output_file: Output image file. Supports ``*.png`` and ``*.svg``.
    :param float x_angle: Rotation about X-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param float y_angle: Rotation about Y-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param float z_angle: Rotation about Z-axis in degrees for ``session.viewports[].view.rotate`` Abaqus Python method
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model

    :returns: writes image to ``{output_file}``
    """
    import abaqus

    input_file_extension = os.path.splitext(input_file)[1]
    if input_file_extension.lower() == ".cae":
        with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
            shutil.copyfile(input_file, copy_file.name)
            abaqus.openMdb(pathName=copy_file.name)
            image(output_file, x_angle=x_angle, y_angle=y_angle, z_angle=z_angle, image_size=image_size,
                  model_name=model_name, part_name=part_name)
    elif input_file_extension.lower() == ".inp":
        abaqus.mdb.ModelFromInputFile(name=model_name, inputFileName=input_file)
        image(output_file, x_angle=x_angle, y_angle=y_angle, z_angle=z_angle, image_size=image_size,
              model_name=model_name, part_name=part_name)
    else:
        sys.stderr.write("Uknown file extension {}".format(input_file_extension))
        sys.exit(1)


def image(output_file, x_angle=default_x_angle, y_angle=default_y_angle, z_angle=default_z_angle,
          image_size=default_image_size, model_name=default_model_name, part_name=default_part_name):
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

    :returns: writes image to ``{output_file}``
    """
    import abaqus
    import abaqusConstants

    assembly = mdb.models[model_name].rootAssembly
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
    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    session.viewports['Viewport: 1'].disableMultipleColors()
    session.printOptions.setValues(vpDecorations=abaqusConstants.OFF)
    session.pngOptions.setValues(imageSize=image_size)  # This is the aspect ration I found works best for my model
    session.printToFile(fileName=output_file_name, format=get_abaqus_image_constant(output_file_ext),
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


def get_parser():
    file_name = inspect.getfile(lambda: None)
    base_name = os.path.basename(file_name)

    prog = "abaqus cae -noGui {} --".format(base_name)
    cli_description = "Save an image of an Abaqus model"

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)
    parser.add_argument('--input-file', type=str, required=True,
                         help='Abaqus input file. Supports ``*.inp`` and ``*.cae``.')
    parser.add_argument('--output-file', type=str, required=True,
                        help='Output image from the Abaqus viewport. Supports ``*.png`` and ``*.svg``.')
    parser.add_argument('--x-angle', type=float, default=default_x_angle,
                        help='Viewer rotation about X-axis in degrees (default: %(default)s)')
    parser.add_argument('--y-angle', type=float, default=default_y_angle,
                        help='Viewer rotation about Y-axis in degrees (default: %(default)s)')
    parser.add_argument('--z-angle', type=float, default=default_z_angle,
                        help='Viewer rotation about Z-axis in degrees (default: %(default)s)')
    parser.add_argument('--image-size', nargs=2, type=float, default=default_image_size,
                        help="Image size in pixels (X, Y) (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args, unknown = parser.parse_known_args()

    sys.exit(main(
        args.input_file,
        args.output_file,
        x_angle=args.x_angle,
        y_angle=args.y_angle,
        z_angle=args.z_angle,
        image_size=args.image_size,
        model_name=args.model_name,
        part_name=args.part_name
    ))
