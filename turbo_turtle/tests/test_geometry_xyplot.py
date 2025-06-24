from unittest.mock import patch

import numpy
import matplotlib

from turbo_turtle import geometry_xyplot
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


def test_geometry_xyplot():
    kwargs = {}
    coordinates_list = [numpy.array([[0.0, 0.0], [1.0, 1.0]])]
    figure = geometry_xyplot.geometry_xyplot(coordinates_list, **kwargs)
    assert isinstance(figure, matplotlib.pyplot.Figure)

    kwargs = {"annotate": True}
    with patch("matplotlib.pyplot.annotate") as mock_annotate:
        figure = geometry_xyplot.geometry_xyplot(coordinates_list, **kwargs)
    mock_annotate.assert_called()

    kwargs = {"scale": True}
    with patch("matplotlib.axes.Axes.set_aspect") as mock_set_aspect:
        figure = geometry_xyplot.geometry_xyplot(coordinates_list, **kwargs)
    mock_set_aspect.assert_called_once_with("equal", adjustable="box")


def test_main():
    kwargs = {}
    expected_call_kwargs = {
        "unit_conversion": parsers.geometry_xyplot_defaults["unit_conversion"],
        "euclidean_distance": parsers.geometry_xyplot_defaults["euclidean_distance"],
        "y_offset": parsers.geometry_xyplot_defaults["y_offset"],
        "rtol": parsers.geometry_xyplot_defaults["rtol"],
        "atol": parsers.geometry_xyplot_defaults["atol"],
        "no_markers": parsers.geometry_xyplot_defaults["no_markers"],
        "annotate": parsers.geometry_xyplot_defaults["annotate"],
        "scale": parsers.geometry_xyplot_defaults["scale"],
    }
    with (
        patch("turbo_turtle._abaqus_python.turbo_turtle_abaqus._mixed_utilities.return_genfromtxt_or_exit"),
        patch("matplotlib.pyplot.Figure.savefig"),
        patch("turbo_turtle.geometry_xyplot.geometry_xyplot") as mock_plot,
    ):
        geometry_xyplot._main(["dummy.in"], ["dummy.out"], **kwargs)
    assert mock_plot.call_args.kwargs == expected_call_kwargs
