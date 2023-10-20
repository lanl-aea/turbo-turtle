import turbo_turtle._abaqus

def main(model_name, input_file, output_file):
    """Testing wrapper script
    
    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    """
    sphere(model_name, input_file, output_file, part_name='sphere')
    eigth_sphere(model_name, input_file, output_file, part_name='eigth-sphere')
    quarter_sphere(model_name, input_file, output_file, part_name='quarter-sphere')
    half_sphere(model_name, input_file, output_file, part_name='half-sphere')
    seveneigths_sphere(model_name, input_file, output_file, part_name='seveneigths-sphere')
    offset_sphere(model_name, input_file, output_file, part_name='offset-sphere')
    swiss_cheese(model_name, input_file, output_file, part_name='swiss-cheese')

    return


def sphere(model_name, input_file, output_file, part_name='sphere'):
    """Test sphere
    
    Run turboTurtle using the ``sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def eigth_sphere(model_name, input_file, output_file, part_name='eigth-sphere'):
    """Test eigth_sphere
    
    Run turboTurtle using the ``eigth-sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def quarter_sphere(model_name, input_file, output_file, part_name='quarter-sphere'):
    """Test quarter_sphere
    
    Run turboTurtle using the ``quarter-sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def half_sphere(model_name, input_file, output_file, part_name='half-sphere'):
    """Test half_sphere
    
    Run turboTurtle using the ``half-sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def seveneigths_sphere(model_name, input_file, output_file, part_name='seveneigths-sphere'):
    """Test seveneights_sphere
    
    Run turboTurtle using the ``seveneights-sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def offset_sphere(model_name, input_file, output_file, part_name='offset-sphere'):
    """Test offset_sphere
    
    Run turboTurtle using the ``offset-sphere`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [1.0, 1.0, 0.0]
    xpoint = [2.0, 1.0, 0.0]
    zpoint = [1.0, 1.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def swiss_cheese(model_name, input_file, output_file, part_name='swiss-cheese'):
    """Test swiss_cheese
    
    Run turboTurtle using the ``swiss-cheese`` geometry.

    :param str model_name: name of the Abaqus model
    :param str input_file: name of the Abaqus CAE database to open
    :param str output_file: name of the output Abaqus CAE database
    :param str part_name: name of the part in the Abaqus model
    """
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turbo_turtle._abaqus.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)   
    return


if __name__ == "__main__":
    model_name = 'Turbo-Turtle-Tests'
    input_file = 'Turbo-Turtle-Tests'
    output_file = 'Turbo-Turtle-Tests'
    main(model_name, input_file, output_file)
