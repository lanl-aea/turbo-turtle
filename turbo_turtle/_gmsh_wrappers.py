"""Unpack command-line argparse namespace into full function interfaces.

The wrapper functions must have the API form

.. code-block::

   def wrapper(args: argparse.Namespace, command: str) -> None:
       pass

The ``command`` argument is required for compatibility with :mod:`turbo_turtle._abaqus_wrappers` and
:mod:`turbo_turtle._cubit_wrappers`.
"""

import argparse
import typing

from turbo_turtle import _gmsh_python


def geometry(args: argparse.Namespace, command: str) -> None:  # noqa: ARG001
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.geometry`.

    Unpack the argument namespace into the full function interface. The ``command`` argument is required for
    compatibility with :mod:`turbo_turtle._abaqus_wrappers` and :mod:`turbo_turtle._cubit_wrappers`.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.geometry(
        args.input_file,
        args.output_file,
        planar=args.planar,
        model_name=args.model_name,
        part_name=args.part_name,
        unit_conversion=args.unit_conversion,
        euclidean_distance=args.euclidean_distance,
        delimiter=args.delimiter,
        header_lines=args.header_lines,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
        rtol=args.rtol,
        atol=args.atol,
    )


def cylinder(args: argparse.Namespace, command: str) -> None:  # noqa: ARG001
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.cylinder`.

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.cylinder(
        args.inner_radius,
        args.outer_radius,
        args.height,
        args.output_file,
        model_name=args.model_name,
        part_name=args.part_name,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
    )


def sphere(args: argparse.Namespace, command: str) -> None:  # noqa: ARG001
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.sphere`.

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.sphere(
        args.inner_radius,
        args.outer_radius,
        args.output_file,
        input_file=args.input_file,
        quadrant=args.quadrant,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
        model_name=args.model_name,
        part_name=args.part_name,
    )


def partition(args: argparse.Namespace, command: str) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("partition subcommand is not yet implemented")


def sets(args: argparse.Namespace, command: str) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("sets subcommand is not yet implemented")


def mesh(args: argparse.Namespace, command: str) -> None:  # noqa: ARG001
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.mesh`.

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.mesh(
        args.input_file,
        args.element_type,
        output_file=args.output_file,
        model_name=args.model_name,
        part_name=args.part_name,
        global_seed=args.global_seed,
        edge_seeds=args.edge_seeds,
    )


def merge(args: argparse.Namespace, command: str) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("merge subcommand is not yet implemented")


def export(args: argparse.Namespace, command: str) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("export subcommand is not yet implemented")


def image(args: argparse.Namespace, command: str) -> None:  # noqa: ARG001
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.image`.

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.image(
        args.input_file,
        args.output_file,
        x_angle=args.x_angle,
        y_angle=args.y_angle,
        z_angle=args.z_angle,
        image_size=args.image_size,
    )
