import turboTurtle

def main(model_name, input_file, output_file):
    
    sphere(model_name, input_file, output_file, part_name='sphere')
    eigth_sphere(model_name, input_file, output_file, part_name='eigth-sphere')
    quarter_sphere(model_name, input_file, output_file, part_name='quarter-sphere')
    half_sphere(model_name, input_file, output_file, part_name='half-sphere')
    seveneigths_sphere(model_name, input_file, output_file, part_name='seveneigths-sphere')
    offset_sphere(model_name, input_file, output_file, part_name='offset-sphere')
    swiss_cheese(model_name, input_file, output_file, part_name='swiss-cheese')

    return


def sphere(model_name, input_file, output_file, part_name='sphere'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def eigth_sphere(model_name, input_file, output_file, part_name='eigth-sphere'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def quarter_sphere(model_name, input_file, output_file, part_name='quarter-sphere'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def half_sphere(model_name, input_file, output_file, part_name='half-sphere'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def seveneigths_sphere(model_name, input_file, output_file, part_name='seveneigths-sphere'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def offset_sphere(model_name, input_file, output_file, part_name='offset-sphere'):
    center = [1.0, 1.0, 0.0]
    xpoint = [2.0, 1.0, 0.0]
    zpoint = [1.0, 1.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
    return


def swiss_cheese(model_name, input_file, output_file, part_name='swiss-cheese'):
    center = [0.0, 0.0, 0.0]
    xpoint = [1.0, 0.0, 0.0]
    zpoint = [0.0, 0.0, 1.0]
    plane_angle = 45.0
    partitions = {}
    turboTurtle.main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)   
    return


if __name__ == "__main__":
    model_name = 'Turbo-Turtle-Tests'
    input_file = 'Turbo-Turtle-Tests'
    output_file = 'Turbo-Turtle-Tests'
    main(model_name, input_file, output_file)
