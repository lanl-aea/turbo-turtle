"""Test Turbo-Turtle SCons builders and support functions"""

import pytest
import SCons

from turbo_turtle import scons_extensions


def check_action_string(nodes, post_action, node_count, action_count, expected_string):
    """Verify the expected action string against a builder's target nodes

    :param SCons.Node.NodeList nodes: Target node list returned by a builder
    :param list post_action: list of post action strings passed to builder
    :param int node_count: expected length of ``nodes``
    :param int action_count: expected length of action list for each node
    :param str expected_string: the builder's action string.

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


# TODO: Figure out how to cleanly reset the construction environment between parameter sets
test_builder = {
    "cli_builder": ("cli_builder", {}, 1, 1, ["cli_builder.txt"], ["cli_builder.txt.stdout"]),
    "geometry": ("geometry", {}, 1, 1, ["geometry.txt"], ["geometry.txt.stdout"]),
    "geometry_xyplot": ("geometry_xyplot", {}, 1, 1, ["geometry_xyplot.txt"], ["geometry_xyplot.txt.stdout"]),
    "cylinder": ("cylinder", {}, 1, 1, ["cylinder.txt"], ["cylinder.txt.stdout"]),
    "sphere": ("sphere", {}, 1, 1, ["sphere.txt"], ["sphere.txt.stdout"]),
    "partition": ("partition", {}, 1, 1, ["partition.txt"], ["partition.txt.stdout"]),
    "mesh": ("mesh", {}, 1, 1, ["mesh.txt"], ["mesh.txt.stdout"]),
    "image": ("image", {}, 1, 1, ["image.txt"], ["image.txt.stdout"]),
    "merge": ("merge", {}, 1, 1, ["merge.txt"], ["merge.txt.stdout"]),
    "export": ("export", {}, 1, 1, ["export.txt"], ["export.txt.stdout"]),
}


@pytest.mark.parametrize("builder, kwargs, node_count, action_count, source_list, target_list",
                         test_builder.values(),
                         ids=test_builder.keys())
def test_builder(builder, kwargs, node_count, action_count, source_list, target_list):
    env = SCons.Environment.Environment()
    expected_string = "${cd_action_prefix} ${program} ${subcommand} ${required} ${options} " \
                      "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} " \
                      "${cubit} ${redirect_action_postfix}"

    env.Append(BUILDERS={builder: scons_extensions.cli_builder(**kwargs)})
    nodes = env["BUILDERS"][builder](env, target=target_list, source=source_list)
    check_action_string(nodes, [], node_count, action_count, expected_string)
