"""Read cProfile files and plot.

Files *must* use extensions ``*.cprofile.{lazy,eager}``

.. warning::

   requires Python >=3.9

.. code-block::

   $ python -m cProfile -m profiler.cprofile.lazy -m turbo_turtle._main
   $ EAGER_IMPORT=eager python -m cProfile -m profiler.cprofile.eager -m turbo_turtle._main
   $ python profile_package.py profiler.cprofile.{eager,lazy} -o profiler.png
"""
import pstats
import pathlib
import argparse

import numpy
import xarray
import matplotlib.pyplot


def get_parser() -> argparse.Namespace():
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
        default=None,
        help="Output file to save as figure. Must use an extension supported by matplotlib. (default: %(default)s)"
    )
    return parser


def smallest_stem(path):
    # Python >=3.9 for the ``.removesuffix`` method
    return str(path.name).removesuffix("".join(path.suffixes))


def main():
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

    figure = matplotlib.pyplot.figure()
    dataset.plot.scatter(x="file", y="total time", hue="disposition", add_legend=True, add_colorbar=False)

    if args.output is not None:
        figure.savefig(args.output)
    else:
        matplotlib.pyplot.show()


if __name__ == "__main__":
    main()
