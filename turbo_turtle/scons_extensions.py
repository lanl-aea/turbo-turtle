import SCons.Builder

# Importing WAVES internals is marginally preferred over project specific, hardcoded duplication of the WAVES settings
from waves.scons_extensions import _first_target_emitter

from turbo_turtle._settings import _cd_action_prefix
from turbo_turtle._settings import _redirect_action_postfix
from turbo_turtle._settings import _default_abaqus_options
from turbo_turtle._settings import _default_cubit_options
from turbo_turtle._abaqus_python import parsers


def _geometry_action(target, source, env):
    """Define the geometry builder action when calling internal package and not the cli

    :param list target: The target file list of strings
    :param list source: The source file list of SCons.Node.FS.File objects
    :param SCons.Script.SConscript.SConsEnvironment env: The builder's SCons construction environment object
    """
    # TODO: recover defaults from parsers without re-creating. Maybe build defaults as dictionary in parsers module?
    # Set default kwargs to match parsers module
    kwargs = {
        "unit_conversion": parsers.geometry_default_unit_conversion,
        "planar": parsers.geometry_default_planar,
        "euclidean_distance": parsers.geometry_default_euclidean_distance,
        "model_name": parsers.geometry_default_model_name,
        "part_name": parsers.geometry_default_part_name,
        "delimiter": parsers.geometry_default_delimiter,
        "header_lines": parsers.geometry_default_header_lines,
        "revolution_angle": parsers.geometry_default_revolution_angle,
        "y_offset": parsers.geometry_default_y_offset,
        "rtol": parsers.geometry_default_rtol,
        "atol": parsers.geometry_default_atol
    }

    # Global CLI settings
    kwargs.update({
        "abaqus_command": _settings._default_abaqus_options,
        "cubit_command": _settings._default_cubit_options,
        "cubit": False
    })

    # Update kwargs with any keys that exist in the environment
    kwargs.update({key: env[key] for key in kwargs.keys()})

    # Recover correct wrappers module from main interface
    _wrappers, command = _utilities.set_wrappers_and_command(
        kwargs["abaqus_command", kwargs["cubit_command"], kwargs["cubit"]
    )
    wrapper_command = getattr(_wrappers, "geometry")
    wrapper_command(args, command)


def geometry():
    """Turbo-Turtle geometry subcommand builder

    This builder calls the internal interface associated with the :ref:`geometry_cli` subcommand.
    All subcommand options can be provided as per-task keyword arguments

    :return: Turbo-Turtle geometry builder
    :rtype: SCons.Builder.Builder
    """
    geometry_builder = SCons.Builder.Builder(
        action = [
            SCons.Action.Action(_geometry_action, varlist=kwargs.keys())
        ]
        emitter=_first_target_emitter,
    )
    return geometry_builder


def _turbo_turtle(program="turbo-turtle", subcommand="", options="",
                  abaqus_command=["abaqus"], cubit_command=["cubit"], cubit=False):
    """Return a generic Turbo-Turtle builder.

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change in the package version number.

    This builder provides a template action for the Turbo-Turtle CLI. The default behavior will not do anything unless
    the ``subcommand`` argument is updated to one of the Turbo-Turtle CLI :ref:`cli_subcommands`.

    This builder and any builders created from this template will be most useful if the ``options`` argument places
    SCons substitution variables in the action string, e.g. ``--argument ${argument}``, such that the task definitions
    can modify the options on a per-task basis. Any option set in this manner *must* be provided by the task definition.

    *Builder/Task keyword arguments*

    * ``program``: The Turbo-Turtle command line executable absolute or relative path
    * ``subcommand``: A Turbo-Turtle subcommand
    * ``options``: A list of subcommand options
    * ``abaqus_command``: The Abaqus command line executable absolute or relative path. When provided as a builder
          keyword argument, this must be a space delimited string, not a list.
    * ``cubit_command``: The Cubit command line executable absolute or relative path. When provided as a builder keyword
          argument, this must be a space delimited string, not a list.
    * ``cubit``: The flag to use Cubit instead of Abaqus. When provided as a builder keyword argument, this must be
          the string ``"--cubit"`` or an empty string ``""``
    * ``cd_action_prefix``: Advanced behavior. Most users should accept the defaults.
    * ``redirect_action_postfix``: Advanced behavior. Most users should accept the defaults.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${options} --abaqus-command ${abaqus_command} ${redirect_action_postfix}

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str options: A list of subcommand options
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool cubit: Boolean to use Cubit instead of Abaqus

    :returns: SCons Turbo-Turtle builder
    :rtype: SCons.Builder.Builder
    """
    cubit = "--cubit" if cubit else ""
    action = ["${cd_action_prefix} ${program} ${subcommand} ${options} --abaqus-command ${abaqus_command} " \
                  "--cubit-command ${cubit_command} ${cubit} ${redirect_action_postfix}"]
    builder = SCons.Builder.Builder(
        action=action,
        emitter=_first_target_emitter,
        cd_action_prefix=_cd_action_prefix,
        redirect_action_postfix=_redirect_action_postfix,
        program=program,
        subcommand=subcommand,
        options=options,
        abaqus_command=" ".join(abaqus_command),
        cubit_command=" ".join(cubit_command),
        cubit=cubit
    )
    return builder


def turbo_turtle_sphere(
    program="turbo-turtle", subcommand="sphere",
    options="--output-file ${TARGETS[0].abspath} " \
            "--inner-radius ${inner_radius} --outer-radius ${outer_radius} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"], cubit_command=["cubit"], cubit=False
):
    """Turbo-Turtle sphere subcommand builder from template :meth:`turbo_turtle.scons_extensions._turbo_turtle`

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change in the package version number.

    This subcommand does not require an input file. If no input file is provided, use the calling SConscript file as the
    task source file. This builder requires at least one TARGET. The first TARGET file must correspond to the
    ``--output-file`` option. Unless the ``options`` argument is overridden, the following task keyword arguments are
    *required*:

    * ``inner_radius``
    * ``outer_radius``
    * ``model_name``
    * ``part_name``

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
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
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool cubit: Boolean to use Cubit instead of Abaqus

    :returns: SCons Turbo-Turtle sphere builder
    :rtype: SCons.Builder.Builder
    """
    return _turbo_turtle(program=program, subcommand=subcommand, options=options,
                         abaqus_command=abaqus_command, cubit_command=cubit_command, cubit=cubit)


def turbo_turtle_partition(
    program="turbo-turtle", subcommand="partition",
    options="--input-file ${SOURCES[0].abspath} --output-file ${TARGETS[0].abspath} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"], cubit_command=["cubit"], cubit=False
):
    """Turbo-Turtle sphere subcommand builder from template :meth:`turbo_turtle.scons_extensions._turbo_turtle`

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change in the package version number.

    This subcommand requires at least one source file. The first SOURCE file just correspond to the ``--input-file``
    option. This builder requires at least one TARGET file. The TARGET file must correspond to the ``--output-file``
    option. Unless the ``options`` argument is overridden, the following task keyword arguments are *required*:

    * ``model_name``
    * ``part_name``

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo-turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={"TurboTurtlePartition": turbo_turtle.scons_extensions._turbo_turtle_partition()})
       env.TurboTurtlePartition(
           target=["partition.cae"],
           source=["sphere.cae"],
           model_name="sphere",
           part_name="sphere"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str options: A list of subcommand options.
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool cubit: Boolean to use Cubit instead of Abaqus

    :returns: SCons Turbo-Turtle sphere builder
    :rtype: SCons.Builder.Builder
    """
    return _turbo_turtle(program=program, subcommand=subcommand, options=options,
                         abaqus_command=abaqus_command, cubit_command=cubit_command, cubit=cubit)
