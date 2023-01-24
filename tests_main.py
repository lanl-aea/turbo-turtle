import tests_geometry
import tests_partition

def main():
    """Turbo Turtle Tests Driver

    Run this script to demonstrate turboTurtle on a varietry of example problems
    """
    model_name = 'Turbo-Turtle-Tests'
    input_file = 'Turbo-Turtle-Tests'
    output_file = 'Turbo-Turtle-Tests'
    tests_geometry.main(model_name, output_file)
    tests_partition.main(model_name, input_file, output_file)
    return

if __name__ == "__main__":
    main()
