import typing

import SCons.Builder
from waves.scons_extensions import first_target_emitter

from turbo_turtle._settings import _cd_action_prefix
from turbo_turtle._settings import _redirect_action_postfix
from turbo_turtle._settings import _default_abaqus_options
from turbo_turtle._settings import _default_cubit_options
from turbo_turtle._settings import _default_backend


_exclude_from_namespace = set(globals().keys())


def cli_builder(
    program: str = "turbo-turtle",
    subcommand: str = "",
    required: str = "",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software

    :returns: SCons Turbo-Turtle CLI builder
    """  # noqa: E501
    action = [
        (
            "${cd_action_prefix} ${program} ${subcommand} ${required} ${options} "
            "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--backend ${backend} ${redirect_action_postfix}"
        ),
    ]
    builder = SCons.Builder.Builder(
        action=action,
        emitter=first_target_emitter,
        cd_action_prefix=_cd_action_prefix,
        redirect_action_postfix=_redirect_action_postfix,
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=" ".join(abaqus_command),
        cubit_command=" ".join(cubit_command),
        backend=backend,
    )
    return builder


def geometry(
    program: str = "turbo-turtle",
    subcommand: str = "geometry",
    required: str = "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def geometry_xyplot(
    program: str = "turbo-turtle",
    subcommand: str = "geometry-xyplot",
    required: str = "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def cylinder(
    program: str = "turbo-turtle",
    subcommand: str = "cylinder",
    # fmt: off
    required: str = "--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius} "
                    "--height ${height}",
    # fmt: on
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def sphere(
    program: str = "turbo-turtle",
    subcommand: str = "sphere",
    required: str = "--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def partition(
    program: str = "turbo-turtle",
    subcommand: str = "partition",
    required: str = "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def sets(
    program: str = "turbo-turtle",
    subcommand: str = "sets",
    required: str = "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
    """Return a Turbo-Turtle sets subcommand CLI builder

    See the :ref:`sets_cli` CLI documentation for detailed subcommand usage and options.
    Builds subcommand specific options for the :meth:`turbo_turtle.scons_extensions.cli_builder` function.

    At least one target must be specified. The first target determines the working directory for the builder's action.
    The action changes the working directory to the first target's parent directory prior to execution.

    The emitter will assume all emitted targets build in the current build directory. If the target(s) must be built in
    a build subdirectory, e.g. in a parameterized target build, then the first target must be provided with the build
    subdirectory, e.g. ``parameter_set1/my_target.ext``. When in doubt, provide a STDOUT redirect file as a target, e.g.
    ``target.stdout``.

    One of the following options must be added to the ``options`` string or the subcommand will return an error:

    * ``--face-set``
    * ``--edge-set``
    * ``--vertex-set``

    .. code-block::
       :caption: action string construction

       ${cd_action_prefix} ${program} ${subcommand} ${required} ${options} --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} --backend ${backend} ${redirect_action_postfix}

    .. code-block::
       :caption: SConstruct

       import waves
       import turbo_turtle
       env = Environment()
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
       env.Append(BUILDERS={
           "TurboTurtleSets": turbo_turtle.scons_extensions.sets(
               program=env["turbo_turtle],
               options="${face_sets} ${edge_sets} ${vertex_sets}",
           )
       })
       env.TurboTurtleSets(
           target=["target.cae"],
           source=["source.cae"],
           face_sets="--face-set top '[#1 ]' --face-set bottom '[#2 ]'",
           edge_sets="",
           vertex_sets="--vertex-set origin '[#1 ]'"
       )

    :param str program: The Turbo-Turtle command line executable absolute or relative path
    :param str subcommand: A Turbo-Turtle subcommand
    :param str required: A space delimited string of subcommand required arguments
    :param str options: A space delimited string of subcommand optional arguments
    :param list abaqus_command: The Abaqus command line executable absolute or relative path options
    :param list cubit_command: The Cubit command line executable absolute or relative path options
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def mesh(
    program: str = "turbo-turtle",
    subcommand: str = "mesh",
    required: str = "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath} --element-type ${element_type}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def image(
    program: str = "turbo-turtle",
    subcommand: str = "image",
    required: str = "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def merge(
    program: str = "turbo-turtle",
    subcommand: str = "merge",
    required: str = "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


def export(
    program: str = "turbo-turtle",
    subcommand: str = "export",
    required: str = "--input-file ${SOURCE.abspath}",
    options: str = "",
    abaqus_command: typing.List[str] = _default_abaqus_options,
    cubit_command: typing.List[str] = _default_cubit_options,
    backend: str = _default_backend,
) -> SCons.Builder.Builder:
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
       env["turbo_turtle"] = waves.scons_extensions.add_program(env, ["turbo-turtle"])
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
    :param str backend: The backend software
    """  # noqa: E501
    return cli_builder(
        program=program,
        subcommand=subcommand,
        required=required,
        options=options,
        abaqus_command=abaqus_command,
        cubit_command=cubit_command,
        backend=backend,
    )


_module_objects = set(globals().keys()) - _exclude_from_namespace
__all__ = [name for name in _module_objects if not name.startswith("_")]
