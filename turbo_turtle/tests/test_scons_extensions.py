"""Test Turbo-Turtle SCons builders and support functions"""

import pytest
import SCons

from turbo_turtle import scons_extensions
from turbo_turtle._settings import _default_abaqus_options
from turbo_turtle._settings import _default_cubit_options
from turbo_turtle._settings import _default_backend


def check_nodes(nodes, post_action, node_count, action_count, expected_string, expected_env_kwargs):
    """Verify the expected action string against a builder's target nodes

    :param SCons.Node.NodeList nodes: Target node list returned by a builder
    :param list post_action: list of post action strings passed to builder
    :param int node_count: expected length of ``nodes``
    :param int action_count: expected length of action list for each node
    :param str expected_string: the builder's action string.
    :param dict expected_env_kwargs: the builder's expected environment keyword arguments

    .. note::

       The method of interrogating a node's action list results in a newline separated string instead of a list of
       actions. The ``expected_string`` should contain all elements of the expected action list as a single, newline
       separated string. The ``action_count`` should be set to ``1`` until this method is updated to search for the
       finalized action list.
    """
    for action in post_action:
        expected_string = expected_string + f"\ncd ${{TARGET.dir.abspath}} && {action}"
    assert len(nodes) == node_count
    for node in nodes:
        node.get_executor()
        assert len(node.executor.action_list) == action_count
        assert str(node.executor.action_list[0]) == expected_string
        for key, value in expected_env_kwargs.items():
            assert node.env[key] == value


# TODO: Figure out how to cleanly reset the construction environment between parameter sets
test_cli_builder = {
    "cli_builder": (
        "cli_builder",
        {},
        1,
        1,
        ["cli_builder.txt"],
        ["cli_builder.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
        },
    ),
    "cli_builder with subcommand": (
        "cli_builder",
        {"subcommand": "subcommand"},
        1,
        1,
        ["cli_builder_with_subcommand.txt"],
        ["cli_builder_with_subcommand.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "subcommand",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
        },
    ),
}


@pytest.mark.parametrize(
    "builder, kwargs, node_count, action_count, source_list, target_list, builder_env",
    test_cli_builder.values(),
    ids=test_cli_builder.keys(),
)
def test_cli_builder(builder, kwargs, node_count, action_count, source_list, target_list, builder_env):
    env = SCons.Environment.Environment()
    expected_string = (
        "${cd_action_prefix} ${program} ${subcommand} ${required} ${options} "
        "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
        "--backend ${backend} ${redirect_action_postfix}"
    )

    env.Append(BUILDERS={builder: scons_extensions.cli_builder(**kwargs)})
    nodes = env["BUILDERS"][builder](env, target=target_list, source=source_list)
    check_nodes(nodes, [], node_count, action_count, expected_string, builder_env)


test_builders = {
    "geometry": (
        "geometry",
        {},
        1,
        1,
        ["geometry.txt"],
        ["geometry.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "geometry",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
        },
    ),
    "geometry_xyplot": (
        "geometry_xyplot",
        {},
        1,
        1,
        ["geometry_xyplot.txt"],
        ["geometry_xyplot.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "geometry-xyplot",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
        },
    ),
    "cylinder": (
        "cylinder",
        {},
        1,
        1,
        ["cylinder.txt"],
        ["cylinder.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "cylinder",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius} "
            "--height ${height}",
        },
    ),
    "sphere": (
        "sphere",
        {},
        1,
        1,
        ["sphere.txt"],
        ["sphere.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "sphere",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--output-file ${TARGET.abspath} --inner-radius ${inner_radius} --outer-radius ${outer_radius}",
        },
    ),
    "partition": (
        "partition",
        {},
        1,
        1,
        ["partition.txt"],
        ["partition.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "partition",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
        },
    ),
    "mesh": (
        "mesh",
        {},
        1,
        1,
        ["mesh.txt"],
        ["mesh.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "mesh",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath} --element-type ${element_type}",
        },
    ),
    "image": (
        "image",
        {},
        1,
        1,
        ["image.txt"],
        ["image.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "image",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCE.abspath} --output-file ${TARGET.abspath}",
        },
    ),
    "merge": (
        "merge",
        {},
        1,
        1,
        ["merge.txt"],
        ["merge.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "merge",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCES.abspath} --output-file ${TARGET.abspath}",
        },
    ),
    "export": (
        "export",
        {},
        1,
        1,
        ["export.txt"],
        ["export.txt.stdout"],
        {
            "program": "turbo-turtle",
            "subcommand": "export",
            "abaqus_command": " ".join(_default_abaqus_options),
            "cubit_command": " ".join(_default_cubit_options),
            "backend": _default_backend,
            "required": "--input-file ${SOURCE.abspath}",
        },
    ),
}


@pytest.mark.parametrize(
    "builder, kwargs, node_count, action_count, source_list, target_list, builder_env",
    test_builders.values(),
    ids=test_builders.keys(),
)
def test_builders(builder, kwargs, node_count, action_count, source_list, target_list, builder_env):
    env = SCons.Environment.Environment()
    expected_string = (
        "${cd_action_prefix} ${program} ${subcommand} ${required} ${options} "
        "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
        "--backend ${backend} ${redirect_action_postfix}"
    )

    builder_function = getattr(scons_extensions, builder)
    env.Append(BUILDERS={builder: builder_function(**kwargs)})
    nodes = env["BUILDERS"][builder](env, target=target_list, source=source_list)
    check_nodes(nodes, [], node_count, action_count, expected_string, builder_env)
