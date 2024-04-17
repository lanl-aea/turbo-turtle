import argparse

import SCons.Builder
# Importing WAVES internals is marginally preferred over project specific, hardcoded duplication of the WAVES settings
from waves.scons_extensions import _first_target_emitter

from turbo_turtle._settings import _cd_action_prefix
from turbo_turtle._settings import _redirect_action_postfix
from turbo_turtle._settings import _default_abaqus_options
from turbo_turtle._settings import _default_cubit_options
from turbo_turtle._settings import _default_backend
from turbo_turtle import _utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


_exclude_from_namespace = set(globals().keys())


def _get_defaults_dictionary(subcommand):
    defaults_dictionary = f"{subcommand}_defaults".replace("-", "_")
    return getattr(parsers, defaults_dictionary)


def _action(target, source, env):
    """Define the builder action when calling internal package and not the cli

    Requires the ``subcommand`` keyword argument in the SCons task construction environment ``env``.

    :param list target: The target file list of strings
    :param list source: The source file list of SCons.Node.FS.File objects
    :param SCons.Script.SConscript.SConsEnvironment env: The builder's SCons construction environment object
    """
    # Set default kwargs to match parsers.subcommand defaults dictionary
    subcommand = env["subcommand"]
    kwargs = _get_defaults_dictionary(subcommand)

    # Global CLI settings
    kwargs.update({
        "abaqus_command": _default_abaqus_options,
        "cubit_command": _default_cubit_options,
        # TODO: remove deprecated cubit flag
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/130
        "cubit": False,
        "backend": _default_backend
    })

    # Update kwargs with any keys that exist in the environment
    update_keys = set(kwargs.keys()).intersection(env.keys())
    kwargs.update({key: env[key] for key in update_keys})

    # Build the expected namespace object
    kwargs["subcommand"] = subcommand
    # TODO: Required arguments are different for every subcommand. How do we handle different requirements and types?
    kwargs["input_file"] = [path.abspath for path in source]
    kwargs["output_file"] = target[0].abspath
    args = argparse.Namespace(**kwargs)

    # Recover correct wrappers module from main interface
    # TODO: Move to a common function shared with main module. Move to _utilities?
    _wrappers, command = _utilities.set_wrappers_and_command(args)
    if args.subcommand == "geometry-xyplot":
        from turbo_turtle._main import geometry_xyplot
        geometry_xyplot._main(
            args.input_file, args.output_file,
            part_name=args.part_name,
            unit_conversion=args.unit_conversion,
            euclidean_distance=args.euclidean_distance,
            delimiter=args.delimiter,
            header_lines=args.header_lines,
            y_offset=args.y_offset,
            rtol=args.rtol,
            atol=args.atol,
            no_markers=args.no_markers,
            annotate=args.annotate,
            scale=args.scale
        )
    else:
        wrapper_command = getattr(_wrappers, args.subcommand)
        wrapper_command(args, command)


def _api_builder(subcommand):
    """Turbo-Turtle subcommand builder

    .. warning::

       This builder is an early, minimally functional placeholder for future builders. It is intended for developer
       testing and early adopter feedback about design behavior and use cases. The interface and behavior may change
       without warning and without a breaking change in the package version number.

    This builder calls the internal wrapper interfaces associated with Turbo-Turtle subcommands. See the
    :ref:`abaqus_python_api` and :ref:`cubit_python_api` for the available keyword arguments and their Python types.

    Implemented and tested for subcommands:

    * geometry

      * Abaqus: :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.geometry._main`
      * Cubit: :meth:`turbo_turtle._cubit_python.geometry`

    * geometry-xyplot: :meth:`turbo_turtle._main._geometry_xyplot`
    * merge

      * Abaqus: :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.merge._main`
      * Cubit: :meth:`turbo_turtle._cubit_python.merge`

    .. warning::

       Common environment key naming conventions, e.g. ``cubit``, may override builder variables and defaults. If you
       experience unexpected errors or behavior, verify that your construction environment (``env``) doesn't override
       the subcommand CLI variable names.

       For example, it is common to search for an absolute path to an executable and save the path to an environment
       variable as

       .. code-block::

          env["cubit"] = waves.scons_extensions.add_program(["cubit"], env)

       which will override the Turbo-Turtle subcommand ``--cubit`` boolean in the builder. It is best to avoid SCons
       construction environment variable names that clash with the Turbo-Turtle subcommand CLI variables. If this is not
       possible or is impractical, clashing variables can be overridden on a task-by-task basis as

       .. code-block::

          env.TurboTurtleGeometry(target=["vase.cae"], source=["vase.csv"], cubit=False)

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["abaqus"] = waves.scons_extensions.add_program(["abaqus"], env)
       env.Append(BUILDERS={"TurboTurtleGeometry": turbo_turtle.scons_extensions._api_builder("geometry")})
       env.TurboTurtleGeometry(target=["vase.cae"], source=["vase.csv"])

    :param str subcommand: The Turbo-Turtle subcommand to build

    :return: Turbo-Turtle API builder
    :rtype: SCons.Builder.Builder
    """
    kwargs = _get_defaults_dictionary(subcommand)
    # TODO: remove deprecated cubit flag
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/130
    varlist = list(kwargs.keys()) + ["abaqus_command", "cubit_command", "cubit", "backend"]
    internal_builder = SCons.Builder.Builder(
        action=[
            SCons.Action.Action(_action, varlist=varlist)
        ],
        subcommand=subcommand
    )
    return internal_builder


def cli_builder(program="turbo-turtle", subcommand="", required="", options="",
                abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a generic Turbo-Turtle CLI builder.

    This builder provides a template action for the Turbo-Turtle CLI. The default behavior will not do anything unless
    the ``subcommand`` argument is updated to one of the Turbo-Turtle CLI :ref:`cli_subcommands`.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    This builder and any builders created from this template will be most useful if the ``options`` argument places
    SCons substitution variables in the action string, e.g. ``--argument ${argument}``, such that the task definitions
    can modify the options on a per-task basis. Any option set in this manner *must* be provided by the task definition.

    *Builder/Task keyword arguments*

    * ``program``: The Turbo-Turtle command line executable absolute or relative path
    * ``subcommand``: A Turbo-Turtle subcommand
    * ``required``: A space delimited string of subcommand required arguments
    * ``options``: A space delimited string of subcommand optional arguments
    * ``abaqus_command``: The Abaqus command line executable absolute or relative path. When provided as a task
      keyword argument, this must be a space delimited string, not a list.
    * ``cubit_command``: The Cubit command line executable absolute or relative path. When provided as a task keyword
      argument, this must be a space delimited string, not a list.
    * ``backend``: The backend software, e.g. Abaqus or Cubit.
    * ``cd_action_prefix``: Advanced behavior. Most users should accept the defaults.
    * ``redirect_action_postfix``: Advanced behavior. Most users should accept the defaults.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend {backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleCLIBuilder": turbo_turtle.scons_extensions.cli_builder(
               program=env["turbo_turtle],
               subcommand="geometry",
               required="--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}"
           )
       })
       env.TurboTurtleCLIBuilder(
           target=["target.cae"],
           source=["source.csv"],
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software

    :returns: SCons Turbo-Turtle CLI builder
    :rtype: SCons.Builder.Builder
    """  # noqa: E501
    action = ["${cd_action_prefix} ${program} ${subcommand} ${required} ${options} " \
                  "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} " \
                  "--backend ${backend} ${redirect_action_postfix}"]
    builder = SCons.Builder.Builder(
        action=action,
        emitter=_first_target_emitter,
        cd_action_prefix=_cd_action_prefix,
        redirect_action_postfix=_redirect_action_postfix,
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=" ".join(abaqus_command),
        cubit_command=" ".join(cubit_command),
        backend=backend
    )
    return builder


def geometry(program="turbo-turtle", subcommand="geometry",
             required="--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
             options="",
             abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle geometry subcommand CLI builder

    See the :ref:`geometry_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleGeometry": turbo_turtle.scons_extensions.geometry(
               program=env["turbo_turtle],
               options="--part-name ${part_name}"
           )
       })
       env.TurboTurtleGeometry(
           target=["target.cae"],
           source=["source1.csv", "source2.csv"],
           part_name="source1 source2"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def geometry_xyplot(program="turbo-turtle", subcommand="geometry-xyplot",
                    required="--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
                    options="",
                    abaqus_command=_default_abaqus_options,
                    cubit_command=_default_cubit_options,
                    backend=_default_backend):
    """Return a Turbo-Turtle geometry-xyplot subcommand CLI builder

    See the :ref:`geometry_xyplot_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleGeometryXYPlot": turbo_turtle.scons_extensions.geometry_xyplot(
               program=env["turbo_turtle],
               options="--part-name ${part_name}"
           )
       })
       env.TurboTurtleGeometryXYPlot(
           target=["target.png"],
           source=["source1.csv", "source2.csv"],
           part_name="source1 source2"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def cylinder(program="turbo-turtle", subcommand="cylinder",
             required="--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius} " \
                      "--height ${height}",
             options="",
             abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle cylinder subcommand CLI builder

    See the :ref:`cylinder_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    Unless the ``required`` argument is overridden, the following task keyword arguments are *required*:

    * ``inner_radius``
    * ``outer_radius``
    * ``height``

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleCylinder": turbo_turtle.scons_extensions.cylinder(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleCylinder(
           target=["target.cae"],
           source=["SConstruct"],
           inner_radius=1.,
           outer_radius=2.,
           height=1.
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def sphere(program="turbo-turtle", subcommand="sphere",
           required="--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius}",
           options="",
           abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle sphere subcommand CLI builder

    See the :ref:`sphere_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    Unless the ``required`` argument is overridden, the following task keyword arguments are *required*:

    * ``inner_radius``
    * ``outer_radius``

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleSphere": turbo_turtle.scons_extensions.sphere(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleSphere(
           target=["target.cae"],
           source=["SConstruct"],
           inner_radius=1.,
           outer_radius=2.
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def partition(program="turbo-turtle", subcommand="partition",
              required="--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
              options="",
              abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle partition subcommand CLI builder

    See the :ref:`partition_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtlePartition": turbo_turtle.scons_extensions.partition(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtlePartition(
           target=["target.cae"],
           source=["source.cae"],
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def mesh(program="turbo-turtle", subcommand="mesh",
         required="--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath} --element-type ${element_type}",
         options="",
         abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle mesh subcommand CLI builder

    See the :ref:`mesh_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    Unless the ``required`` argument is overridden, the following task keyword arguments are *required*:

    * ``element_type``

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleMesh": turbo_turtle.scons_extensions.mesh(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleMesh(
           target=["target.cae"],
           source=["source.cae"],
           element_type="C3D8R"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def image(program="turbo-turtle", subcommand="image",
          required="--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
          options="",
          abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle image subcommand CLI builder

    See the :ref:`image_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleImage": turbo_turtle.scons_extensions.image(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleImage(
           target=["target.png"],
           source=["source.cae"],
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def merge(program="turbo-turtle", subcommand="merge",
          required="--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
          options="",
          abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle merge subcommand CLI builder

    See the :ref:`merge_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleMerge": turbo_turtle.scons_extensions.merge(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleMerge(
           target=["target.cae"],
           source=["source1.cae", "source2.cae"],
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def export(program="turbo-turtle", subcommand="export",
           required="--input-file ${SOURCE.abspath}",
           options="",
           abaqus_command=_default_abaqus_options, cubit_command=_default_cubit_options, backend=_default_backend):
    """Return a Turbo-Turtle export subcommand CLI builder

    See the :ref:`export_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={
           "TurboTurtleExport": turbo_turtle.scons_extensions.export(
               program=env["turbo_turtle]
           )
       })
       env.TurboTurtleExport(
           target=["target.inp"],
           source=["source.cae"],
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param bool backend: The backend software
    """  # noqa: E501
    return cli_builder(program=program, subcommand=subcommand, required=required, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def turbo_turtle_sphere(
    program="turbo-turtle", subcommand="sphere",
    options="--output-file ${TARGETS[0].abspath} " \
            "--inner-radius ${inner_radius} --outer-radius ${outer_radius} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"], cubit_command=["cubit"], cubit=False
):
    """Turbo-Turtle sphere subcommand builder from template :meth:`turbo_turtle.scons_extensions.cli_builder`

    .. warning::

       This builder will be deprecated in favor of :meth:`turbo_turtle.scons_extensions.sphere`.

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
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={"TurboTurtleSphere": turbo_turtle.scons_extensions.turbo_turtle_sphere()})
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
    # TODO: Remove these builders for version 1.0
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/127
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    message = "The 'turbo_turtle.scons_extensions.turbo_turtle_sphere' builder will be deprecated in a future " \
              "version. Use the 'turbo_turtle.scons_extensions.sphere' builder instead."
    warnings.warn(message, DeprecationWarning)
    if cubit is True:
        backend = "cubit"
    else:
        backend = "abaqus"
    return cli_builder(program=program, subcommand=subcommand, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


def turbo_turtle_partition(
    program="turbo-turtle", subcommand="partition",
    options="--input-file ${SOURCES[0].abspath} --output-file ${TARGETS[0].abspath} " \
            "--model-name ${model_name} --part-name ${part_name}",
    abaqus_command=["abaqus"], cubit_command=["cubit"], cubit=False
):
    """Turbo-Turtle sphere subcommand builder from template :meth:`turbo_turtle.scons_extensions.cli_builder`

    .. warning::

       This builder will be deprecated in favor of :meth:`turbo_turtle.scons_extensions.partition`.

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
       env["turbo_turtle"] = waves.scons_extensions.add_program(["turbo-turtle"], env)
       env.Append(BUILDERS={"TurboTurtlePartition": turbo_turtle.scons_extensions.turbo_turtle_partition()})
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
    # TODO: Remove these builders for version 1.0
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/127
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    message = "The 'turbo_turtle.scons_extensions.turbo_turtle_partition' builder will be deprecated in a future " \
              "version. Use the 'turbo_turtle.scons_extensions.partition' builder instead."
    warnings.warn(message, DeprecationWarning)
    if cubit is True:
        backend = "cubit"
    else:
        backend = "abaqus"
    return cli_builder(program=program, subcommand=subcommand, options=options,
                       abaqus_command=abaqus_command, cubit_command=cubit_command, backend=backend)


_module_objects = set(globals().keys()) - _exclude_from_namespace
__all__ = [name for name in _module_objects if not name.startswith("_")]
