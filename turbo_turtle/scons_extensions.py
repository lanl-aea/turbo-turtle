import SCons.Builder
# Importing WAVES internals is marginally preferred over project specific, hardcoded duplication of the WAVES settings
from waves._settings import _cd_action_prefix
from waves._settings import _redirect_action_postfix
from waves.scons_extensions import _first_target_emitter


def _turbo_turtle(program="turbo-turtle", subcommand="", options="", abaqus_command=["abaqus"]):
    """Return a generic Turbo-Turtle builder.

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change version number.

    This builder provides a template action for the Turbo-Turtle CLI. The default behavior will not do anything unless
    the ``subcommand`` argument is updated as one of the Turbo-Turtle CLI subcommands:
    https://aea.re-pages.lanl.gov/python-projects/turbo-turtle/cli.html#sub-commands

    This builder and any builders created from this template will be most useful if the ``options`` argument places
    SCons substitution variables in the action string, e.g. ``--argument ${argument}``, such that the task definitions
    can modify the options on a per-task basis. Any option set in this manner *must* be provided by the task definition.

    *Builder/Task keyword arguments*

    * ``program``: The Turbo-Turtle command line executable absolute or relative path
    * ``subcommand``: A Turbo-Turtle subcommand
    * ``options``: A list of subcommand options
    * ``abaqus_command``: The Abaqus command line executable absolute or relative path. When provided as a keyword
          argument, this should be a space delimited string, not a list.
    * ``cd_action_prefix``: Advanced behavior. Most users should accept the defaults.
    * ``redirect_action_postfix``: Advanced behavior. Most users should accept the defaults.

    .. code-block:: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${options} --abaqus-command ${abaqus_command} ${redirect_action_postfix}

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str options: A list of subcommand options
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options

    :returns: SCons Turbo-Turtle builder
    :rtype: SCons.Builder.Builder
    """
    action = ["${cd_action_prefix} ${program} ${subcommand} ${options} --abaqus-command ${abaqus_command} ${redirect_action_postfix}"]
    builder = SCons.Builder.Builder(
        action=action,
        emitter=_first_target_emitter,
        cd_action_prefix=_cd_action_prefix,
        redirect_action_postfix=_redirect_action_postfix,
        program=program,
        subcommand=subcommand,
        options=options,
        abaqus_command=" ".join(abaqus_command)
    )
    return builder


def _turbo_turtle_sphere(
    program="turbo-turtle", subcommand="sphere",
    options="--output-file ${TARGETS[0].abspath} " \
            "--inner-radius ${inner_radius} --outer-radius ${outer_radius} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"]
):
    """Turbo-Turtle sphere subcommand builder

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change version number.

    This subcommand does not require an input file. If no input file is provided, use the calling SConscript file as the
    task source file. Unless the ``options`` argument is overridden, the following task keyword arguments are *required*:

    * ``inner_radius``
    * ``outer_radius``
    * ``model_name``
    * ``part_name``

    .. code-block:: SConstruct

       import waves
       import turbo_turtle.scons_extensions
       env = Environment()
       env["turbo-turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={"TurboTurtleSphere": turbo_turtle.scons_extensions._turbo_turtle_sphere()})
       env.TurboTurtleSphere(
           target=["sphere.cae"],
           source=["SConstruct"],
           inner_radius=1.,
           outer_radius=2.,
           model_name="sphere",
           part_name="sphere"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str options: A list of subcommand options.

    :returns: SCons Turbo-Turtle sphere builder
    :rtype: SCons.Builder.Builder
    """
    return _turbo_turtle(program=program, subcommand=subcommand, options=options, abaqus_command=abaqus_command)


def _turbo_turtle_partition(
    program="turbo-turtle", subcommand="partition",
    options="--input-file ${SOURCES[0].abspath} --output-file ${TARGETS[0].abspath} " \
            "--center ${center} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"]
):
    """Turbo-Turtle sphere subcommand builder

    This subcommand requires at least one source file. Unless the ``options`` argument is overridden, the following task
    keyword arguments are *required*:

    * ``center``: When provided as a keyword argument, this must be a space delimited string
    * ``model_name``
    * ``part_name``

    .. code-block:: SConstruct

       import waves
       import turbo_turtle.scons_extensions
       env = Environment()
       env["turbo-turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={"TurboTurtlePartition": turbo_turtle.scons_extensions._turbo_turtle_partition()})
       env.TurboTurtleSphere(
           target=["partition.cae"],
           source=["sphere.cae"],
           center="0. 0. 0.",
           model_name="sphere",
           part_name="sphere"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str options: A list of subcommand options.

    :returns: SCons Turbo-Turtle sphere builder
    :rtype: SCons.Builder.Builder
    """
    return _turbo_turtle(program=program, subcommand=subcommand, options=options, abaqus_command=abaqus_command)
