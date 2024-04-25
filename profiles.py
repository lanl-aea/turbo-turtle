"""Read cProfile files and plot.

Files *must* use extensions ``*.cprofile.{lazy,eager}``

.. warning::

   requires Python >=3.9

.. code-block::

   $ python -m cProfile -m profiler.cprofile.lazy -m turbo_turtle._main
   $ EAGER_IMPORT=eager python -m cProfile -m profiler.cprofile.eager -m turbo_turtle._main
   $ python profile_package.py profiler.cprofile.{eager,lazy} -o profiler.png
"""
import typing
import pstats
import pathlib
import argparse

import numpy
import xarray
import matplotlib.pyplot


default_figsize = [10, 5]
default_output = None


def get_parser() -> argparse.Namespace():
    """Get CLI parser

    :returns: profiler.py CLI parser
    """
    parser = argparse.ArgumentParser(
        description="Read multiple cProfile files and plot. Files *must* use extensions ``.cprofile.{lazy,eager}``"
    )
    parser.add_argument(
        "FILE",
        nargs="+",
        help="cProfile output file"
    )
    parser.add_argument(
        "-o", "--output",
        default=default_output,
        help="Output file to save as figure. Must use an extension supported by matplotlib. (default: %(default)s)"
    )
    parser.add_argument(
        "-f", "--figsize",
        nargs=2,
        type=float,
        default=default_figsize,
        help="Matplotlib figure size [width, height] in inches. (default: %(default)s)"
    )
    return parser


def smallest_stem(path: pathlib.Path) -> str:
    """Return the smallest stem from a pathlib Path object by removing all suffixes

    .. warning::

       requires Python >=3.9

    :param path: pathlib Path object to process

    :returns: shortest stem (all suffixes removed)
    """
    # Python >=3.9 for the ``.removesuffix`` method
    return str(path.name).removesuffix("".join(path.suffixes))


def plot(
    dataset: xarray.Dataset,
    figsize: typing.Tuple[float, float] = default_figsize,
    output: typing.Optional[str] = default_output,
    **kwargs
) -> None:
    """Plot Xarray Dataset, optionally saving and output file

    If no output file is specified, open a matplotlib figure window

    :param dataset: Xarray dataset to plot
    :param figsize: Matplotlib figure size argument (width, height) in inches
    :param output: Output file to save. Optional.
    :param **kwargs: ``dataset.plot.scatter`` keyword arguments
    """
    figure = matplotlib.pyplot.figure(figsize=figsize)
    dataset.plot.scatter(**kwargs)
    figure.axes[0].set_xticklabels(labels=dataset["file"].values, rotation=6)
    if output is not None:
        figure.savefig(output)
    else:
        matplotlib.pyplot.show()


def main() -> None:
    """Read cProfile files and plot"""
    parser = get_parser()
    args = parser.parse_args()

    dispositions = [".eager", ".lazy"]
    paths = [pathlib.Path(path) for path in args.FILE]
    stems = list(set([smallest_stem(path)for path in paths]))

    total_time = numpy.zeros([len(stems), len(dispositions)])
    for path in paths:
        stats = pstats.Stats(str(path))

        stem = smallest_stem(path)
        disposition = path.suffixes[-1]
        disposition_index = dispositions.index(disposition)
        stems_index = stems.index(stem)
        total_time[stems_index, disposition_index] = stats.total_tt

    dataset = xarray.Dataset(
        {"total time": (["file", "disposition"], total_time)},
        coords={
            "file": stems,
            "disposition": dispositions
        }
    )
    dataset["total time"].attrs["units"] = "s"
    dataset = dataset.sortby("file")

    plot(dataset, figsize=tuple(args.figsize), output=args.output,
         x="file", y="total time", hue="disposition", add_legend=True, add_colorbar=False)


if __name__ == "__main__":
    main()
