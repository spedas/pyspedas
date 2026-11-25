"""
Tests for pyspedas/tplot_tools/MPLPlotter/tplot_map.py.

These tests need the optional ``basemap`` extra (``pip install pyspedas[maps]``).

The tests are grouped by the part of tplot_map.py they exercise:

- convert_coords_to_geod_lonlat_list(): turning tplot variables or arrays into
  (longitude, geodetic latitude) arrays for plotting.
- Tplot_Map(): map creation, the ``map_options`` dictionary, view presets and
  validation of the Basemap projection arguments.
- The Tplot_Map wrappers for Basemap features (coastlines, countries, ...).
- The Tplot_Map plotting methods that accept tplot variables
  (add_paths, add_markers, add_caps).
- tplot_map(): the convenience function for creating a Tplot_Map.
- The deprecated module-level functions kept for backward compatibility.
- An end-to-end example using THEMIS data (needs network access).
"""

import os
import io
import logging
import unittest
import warnings
import contextlib
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt

from pyspedas import (
    store_data,
    get_data,
    del_data,
    cotrans,
    time_double,
    geodetic_correction,
    cartesian2geodeticpolar,
)
from pyspedas.config import CONFIG
from pyspedas.tplot_tools.MPLPlotter.tplot_map import (
    Tplot_Map,
    tplot_map,
    convert_coords_to_geod_lonlat_list,
    add_tracks as deprecated_add_tracks,
    add_markers as deprecated_add_markers,
    add_station_fovs as deprecated_add_station_fovs,
    geodetic_correction as deprecated_geodetic_correction,
    cartesian2geodeticpolar as deprecated_cartesian2geodeticpolar,
    tvar_to_geodeticpolar as deprecated_tvar_to_geodeticpolar,
)

# Whether to display plots during testing
global_display = CONFIG["testing"]["global_display"]
# Directory to save testing output files
output_dir = CONFIG["testing"]["output_dir"]
save_dir = os.path.join(output_dir, "tplot_map")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Default map_options of a Tplot_Map created without any options
# (the 'ax' entries added when an Axes is supplied are left out here).
DEFAULT_BASEMAP_OPTIONS = {"projection": "ortho", "lat_0": 0, "lon_0": 0}
PLOT_TYPES = [
    "basemap",
    "drawcoastlines",
    "drawcountries",
    "fillcontinents",
    "drawmapboundary",
    "drawmeridians",
    "drawparallels",
    "nightshade",
    "add_paths",
    "add_markers",
    "add_caps",
]

# A small square of (geodetic latitude, longitude) points, in degrees,
# all of which are visible on the default globe centered at (0, 0).
SQUARE_LAT_LON = np.array([
    [0.0, 0.0],
    [30.0, 0.0],
    [30.0, 30.0],
    [0.0, 30.0],
    [0.0, 0.0],
])


def without_ax(options):
    """Return a copy of a plot options dict without the 'ax' entry."""
    return {key: value for key, value in options.items() if key != "ax"}


def blank_map(**kwargs):
    """
    Create a Tplot_Map on a new Axes with none of the default features drawn.

    Returns the map and its Axes, so tests can count what gets drawn.
    """
    fig, ax = plt.subplots()
    tmap = Tplot_Map(ax=ax, override_defaults=True, **kwargs)
    return tmap, ax


def angular_distance_deg(lat1, lon1, lat2, lon2):
    """Great-circle angle, in degrees, between points given in degrees."""
    lat1, lon1, lat2, lon2 = (np.deg2rad(a) for a in (lat1, lon1, lat2, lon2))
    cos_angle = (np.sin(lat1) * np.sin(lat2)
                 + np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2))
    return np.rad2deg(np.arccos(np.clip(cos_angle, -1.0, 1.0)))


class TplotMapTestCase(unittest.TestCase):
    """Shared set up and clean up: start with no tplot variables or figures."""

    def setUp(self):
        del_data("*")

    def tearDown(self):
        del_data("*")
        plt.close("all")


class ConvertCoordsTestCases(TplotMapTestCase):
    """convert_coords_to_geod_lonlat_list() for each input type and option."""

    def test_geodetic_lat_lon_array(self):
        """Geodetic (lat, lon) input comes back as (lon, lat), unchanged in value."""
        result = convert_coords_to_geod_lonlat_list(SQUARE_LAT_LON, coord_type="geod_lat_lon")
        self.assertEqual(len(result), 1)
        np.testing.assert_allclose(result[0][:, 0], SQUARE_LAT_LON[:, 1])
        np.testing.assert_allclose(result[0][:, 1], SQUARE_LAT_LON[:, 0], atol=1e-10)

    def test_geocentric_lat_lon_array(self):
        """Geocentric latitudes are corrected to geodetic latitudes."""
        result = convert_coords_to_geod_lonlat_list(SQUARE_LAT_LON, coord_type="geoc_lat_lon")[0]
        np.testing.assert_allclose(result[:, 0], SQUARE_LAT_LON[:, 1])
        np.testing.assert_allclose(result[:, 1], geodetic_correction(SQUARE_LAT_LON[:, 0]))

    def test_spherical_coordinates(self):
        """(radius, lat, lon) input: the radius is dropped."""
        radius = np.full((SQUARE_LAT_LON.shape[0], 1), 7000.0)
        r_lat_lon = np.hstack([radius, SQUARE_LAT_LON])

        geodetic = convert_coords_to_geod_lonlat_list(r_lat_lon, coord_type="geod_spherical")[0]
        np.testing.assert_allclose(geodetic[:, 0], SQUARE_LAT_LON[:, 1])
        np.testing.assert_allclose(geodetic[:, 1], SQUARE_LAT_LON[:, 0], atol=1e-10)

        geocentric = convert_coords_to_geod_lonlat_list(r_lat_lon, coord_type="geoc_spherical")[0]
        np.testing.assert_allclose(geocentric[:, 0], SQUARE_LAT_LON[:, 1])
        np.testing.assert_allclose(geocentric[:, 1], geodetic_correction(SQUARE_LAT_LON[:, 0]))

    def test_cartesian_geo(self):
        """Cartesian GEO positions agree with pyspedas.cartesian2geodeticpolar()."""
        xyz = np.array([
            [1.0, 0.0, 0.0],   # on the equator at longitude 0
            [0.0, 1.0, 0.0],   # on the equator at longitude 90
            [1.0, 0.0, 1.0],   # geocentric latitude 45 at longitude 0
        ])
        result = convert_coords_to_geod_lonlat_list(xyz, coord_type="cart_GEO")[0]
        expected = cartesian2geodeticpolar(data=xyz)  # columns: r, geodetic lat, lon
        np.testing.assert_allclose(result[:, 0], expected[:, 2], atol=1e-10)
        np.testing.assert_allclose(result[:, 1], expected[:, 1], atol=1e-10)
        np.testing.assert_allclose(result[:2, 0], [0.0, 90.0], atol=1e-10)
        np.testing.assert_allclose(result[2, 1], geodetic_correction(45.0))

    def test_list_of_cartesian_geo_arrays(self):
        """Every array in a list of cart_GEO arrays is converted, not only the first."""
        first = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        second = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
        result = convert_coords_to_geod_lonlat_list([first, second], coord_type="cart_GEO")
        self.assertEqual(len(result), 2)
        expected = cartesian2geodeticpolar(data=second)
        np.testing.assert_allclose(result[1][:, 0], expected[:, 2], atol=1e-10)
        np.testing.assert_allclose(result[1][:, 1], expected[:, 1], atol=1e-10)

    def test_tplot_variable_and_mixed_list(self):
        """Strings are read as tplot variables, and lists may mix variables and arrays."""
        store_data("square_points", data={
            "x": time_double(["2020-01-01/00:00:00", "2020-01-01/00:01:00",
                              "2020-01-01/00:02:00", "2020-01-01/00:03:00",
                              "2020-01-01/00:04:00"]),
            "y": SQUARE_LAT_LON,
        })
        from_tvar = convert_coords_to_geod_lonlat_list("square_points")
        from_array = convert_coords_to_geod_lonlat_list(SQUARE_LAT_LON)
        np.testing.assert_allclose(from_tvar[0], from_array[0])

        mixed = convert_coords_to_geod_lonlat_list([SQUARE_LAT_LON, "square_points"])
        self.assertEqual(len(mixed), 2)
        np.testing.assert_allclose(mixed[0], mixed[1])

    def test_angle_units(self):
        """Radians and arcminutes give the same result as degrees."""
        in_degrees = convert_coords_to_geod_lonlat_list(SQUARE_LAT_LON, coord_type="geoc_lat_lon")[0]

        in_radians = convert_coords_to_geod_lonlat_list(
            np.deg2rad(SQUARE_LAT_LON), coord_type="geoc_lat_lon", angle_meas="radians")[0]
        np.testing.assert_allclose(in_radians, in_degrees, atol=1e-10)

        # 60 arcminutes = 1 degree
        in_arcminutes = convert_coords_to_geod_lonlat_list(
            SQUARE_LAT_LON * 60.0, coord_type="geoc_lat_lon", angle_meas="arcminutes")[0]
        np.testing.assert_allclose(in_arcminutes, in_degrees, atol=1e-10)

    def test_co_latitude(self):
        """A geocentric co-latitude of 30 degrees is a geocentric latitude of 60 degrees."""
        result = convert_coords_to_geod_lonlat_list(
            np.array([[30.0, 10.0], [120.0, 20.0]]), coord_type="geoc_lat_lon", co_latitude=True)[0]
        np.testing.assert_allclose(result[:, 0], [10.0, 20.0])
        np.testing.assert_allclose(result[:, 1], geodetic_correction(np.array([60.0, -30.0])))

    def test_one_dimensional_input(self):
        """A 1-D array is treated as a single record, with a warning."""
        with self.assertLogs(level=logging.WARNING) as captured:
            result = convert_coords_to_geod_lonlat_list(np.array([30.0, 10.0]))
        self.assertTrue(any("one dimensional" in record.getMessage() for record in captured.records))
        self.assertEqual(result[0].shape, (1, 2))
        np.testing.assert_allclose(result[0], [[10.0, 30.0]], atol=1e-10)

    def test_single_record_two_dimensional_input(self):
        """A 2-D array holding one record (one station) is accepted."""
        result = convert_coords_to_geod_lonlat_list(np.array([[30.0, 10.0]]))
        np.testing.assert_allclose(result[0], [[10.0, 30.0]], atol=1e-10)

    def test_invalid_inputs(self):
        """Invalid options and badly shaped data raise ValueError."""
        bad_calls = {
            "unknown coord_type": dict(coords=SQUARE_LAT_LON, coord_type="gsm"),
            "unknown angle_meas": dict(coords=SQUARE_LAT_LON, angle_meas="gradians"),
            "3 columns for lat_lon": dict(coords=np.zeros((4, 3)), coord_type="geod_lat_lon"),
            "2 columns for spherical": dict(coords=np.zeros((4, 2)), coord_type="geod_spherical"),
            "4 columns": dict(coords=np.zeros((4, 4))),
            "3-D array": dict(coords=np.zeros((4, 2, 2))),
            "too few elements": dict(coords=np.array([1.0])),
        }
        for description, kwargs in bad_calls.items():
            with self.subTest(description):
                with self.assertRaises(ValueError):
                    convert_coords_to_geod_lonlat_list(**kwargs)


class TplotMapInitTestCases(TplotMapTestCase):
    """Creating a Tplot_Map and setting up its map_options."""

    def test_default_map(self):
        """The default map has the documented options and draws its features."""
        fig, ax = plt.subplots()
        tmap = Tplot_Map(ax=ax)

        self.assertEqual(list(tmap.map_options.keys()), PLOT_TYPES)
        self.assertEqual(without_ax(tmap.map_options["basemap"]), DEFAULT_BASEMAP_OPTIONS)
        self.assertEqual(without_ax(tmap.map_options["drawcoastlines"]), {"linewidth": 0.25})
        self.assertEqual(without_ax(tmap.map_options["drawcountries"]), {"linewidth": 0.25})
        self.assertEqual(without_ax(tmap.map_options["fillcontinents"]),
                         {"color": "white", "lake_color": "white"})
        self.assertEqual(without_ax(tmap.map_options["drawmapboundary"]), {"fill_color": "white"})
        np.testing.assert_array_equal(tmap.map_options["drawmeridians"]["meridians"], np.arange(0, 360, 10))
        np.testing.assert_array_equal(tmap.map_options["drawparallels"]["circles"], np.arange(-90, 90, 10))
        self.assertEqual(tmap.map_options["nightshade"], {})

        # Coastlines and countries (collections), meridians and parallels
        # (lines) and filled continents (patches) were drawn on the Axes.
        self.assertGreater(len(ax.collections), 0)
        self.assertGreater(len(ax.lines), 0)
        self.assertGreater(len(ax.patches), 0)

    def test_axes_and_figure(self):
        """A supplied Axes is stored, with its Figure, and passed to each drawn feature."""
        fig, ax = plt.subplots()
        tmap = Tplot_Map(ax=ax)
        self.assertIs(tmap.ax, ax)
        self.assertIs(tmap.fig, fig)
        for plot_type, options in tmap.map_options.items():
            with self.subTest(plot_type):
                if options:
                    self.assertIs(options["ax"], ax)

    def test_view_presets(self):
        """Each view preset sets the map center (lat_0, lon_0)."""
        expected_centers = {
            "North America": (50, 260),
            "Northern Europe": (65, 20),
            "North Polar": (90, 0),
            "South Polar": (-90, 0),
        }
        for view, (lat_0, lon_0) in expected_centers.items():
            with self.subTest(view):
                tmap, ax = blank_map(view=view)
                self.assertEqual(tmap.view, view)
                self.assertEqual(tmap.map_options["basemap"]["lat_0"], lat_0)
                self.assertEqual(tmap.map_options["basemap"]["lon_0"], lon_0)

    def test_basemap_keywords(self):
        """Extra keywords go to Basemap; a view preset takes priority over them."""
        tmap, ax = blank_map(lat_0=30, lon_0=-100)
        self.assertEqual(tmap.map_options["basemap"]["lat_0"], 30)
        self.assertEqual(tmap.map_options["basemap"]["lon_0"], -100)
        # The Basemap projection really is centered there:
        np.testing.assert_allclose(tmap(-100, 30), (tmap.urcrnrx / 2, tmap.urcrnry / 2))

        tmap, ax = blank_map(view="North Polar", lat_0=30, lon_0=-100)
        self.assertEqual(tmap.map_options["basemap"]["lat_0"], 90)
        self.assertEqual(tmap.map_options["basemap"]["lon_0"], 0)

    def test_option_dict_updates_defaults(self):
        """option_dict changes only the options it names; the other defaults are kept."""
        fig, ax = plt.subplots()
        tmap = Tplot_Map(ax=ax, option_dict={
            "fillcontinents": {"lake_color": "lightskyblue"},
            "drawmapboundary": {"fill_color": "lightskyblue"},
        })
        self.assertEqual(without_ax(tmap.map_options["fillcontinents"]),
                         {"color": "white", "lake_color": "lightskyblue"})
        self.assertEqual(without_ax(tmap.map_options["drawmapboundary"]),
                         {"fill_color": "lightskyblue"})
        self.assertEqual(without_ax(tmap.map_options["drawcoastlines"]), {"linewidth": 0.25})

    def test_option_dict_draws_nightshade(self):
        """Setting nightshade options at creation draws the day-night shading."""
        date = dt.datetime(2020, 6, 21, 12, 0, 0)
        tmap, ax = blank_map(option_dict={"nightshade": {"date": date, "alpha": 0.5}})
        self.assertEqual(without_ax(tmap.map_options["nightshade"]), {"date": date, "alpha": 0.5})
        self.assertGreater(len(ax.collections), 0)

    def test_override_defaults(self):
        """With override_defaults, only 'basemap' and the option_dict entries remain."""
        tmap, ax = blank_map(option_dict={"fillcontinents": {"lake_color": "lightskyblue"}})
        self.assertEqual(without_ax(tmap.map_options["basemap"]), DEFAULT_BASEMAP_OPTIONS)
        self.assertEqual(without_ax(tmap.map_options["fillcontinents"]), {"lake_color": "lightskyblue"})
        for plot_type in PLOT_TYPES:
            if plot_type not in ("basemap", "fillcontinents"):
                with self.subTest(plot_type):
                    self.assertEqual(tmap.map_options[plot_type], {})

        # With no option_dict at all, nothing is drawn.
        tmap, ax = blank_map()
        self.assertEqual(len(ax.collections) + len(ax.lines) + len(ax.patches), 0)

    def test_projection_names(self):
        """Projections may be given by Basemap short name or by full name."""
        corners = dict(llcrnrlon=-50, llcrnrlat=-50, urcrnrlon=50, urcrnrlat=50)
        for name in ["merc", "mercator", "Mercator"]:
            with self.subTest(name):
                tmap, ax = blank_map(projection=name, **corners)
                self.assertEqual(tmap.map_options["basemap"]["projection"], "merc")
                self.assertEqual(tmap.projection, "merc")

    def test_invalid_projection(self):
        """An unknown projection raises ValueError."""
        fig, ax = plt.subplots()
        with self.assertRaises(ValueError):
            Tplot_Map(ax=ax, projection="not_a_projection")

    def test_projection_argument_warnings(self):
        """Missing or invalid Basemap arguments for a projection are logged."""
        with self.assertLogs(level=logging.WARNING) as captured:
            blank_map(projection="merc")
        self.assertTrue(any("missing some corners" in record.getMessage()
                            for record in captured.records))

        with self.assertLogs(level=logging.WARNING) as captured:
            blank_map(width=1.0e7)
        self.assertTrue(any("invalid arguments" in record.getMessage()
                            for record in captured.records))

    def test_print_map_options(self):
        """print_map_options() prints every plot type and its options."""
        tmap, ax = blank_map(option_dict={"drawcoastlines": {"linewidth": 3}})
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            tmap.print_map_options()
        text = printed.getvalue()
        self.assertTrue(text.startswith("Current Map Options:"))
        for plot_type in PLOT_TYPES:
            self.assertIn(f"'{plot_type}' :", text)
        self.assertIn("'linewidth': 3", text)

    def test_deprecated_params_mirror_map_options(self):
        """The deprecated params attribute still mirrors map_options."""
        fig, ax = plt.subplots()
        tmap = Tplot_Map(ax=ax)
        self.assertEqual(tmap.params.basemap, tmap.map_options["basemap"])
        self.assertEqual(tmap.params.drawcoastlines, tmap.map_options["drawcoastlines"])
        tmap.add_coastlines(linewidth=2)
        self.assertEqual(tmap.params.drawcoastlines["linewidth"], 2)


class TplotMapFeatureTestCases(TplotMapTestCase):
    """The Tplot_Map wrappers for Basemap features."""

    def test_add_coastlines(self):
        tmap, ax = blank_map()
        tmap.add_coastlines(linewidth=3, linestyle="dashed", color="b")
        self.assertEqual(tmap.map_options["drawcoastlines"],
                         {"linewidth": 3, "linestyle": "dashed", "color": "b"})
        self.assertEqual(len(ax.collections), 1)

    def test_add_countries(self):
        tmap, ax = blank_map()
        tmap.add_countries(linewidth=3, linestyle="dashed", color="b")
        self.assertEqual(tmap.map_options["drawcountries"],
                         {"linewidth": 3, "linestyle": "dashed", "color": "b"})
        self.assertEqual(len(ax.collections), 1)

    def test_add_fillcontinents(self):
        tmap, ax = blank_map()
        tmap.add_fillcontinents(color="darkgreen", lake_color="darkblue", alpha=0.5)
        self.assertEqual(tmap.map_options["fillcontinents"],
                         {"color": "darkgreen", "lake_color": "darkblue", "alpha": 0.5})
        self.assertGreater(len(ax.patches), 0)

    def test_add_mapboundary(self):
        tmap, ax = blank_map()
        tmap.add_mapboundary(linewidth=3, color="r", fill_color="lightskyblue")
        self.assertEqual(tmap.map_options["drawmapboundary"],
                         {"linewidth": 3, "color": "r", "fill_color": "lightskyblue"})
        self.assertEqual(len(ax.patches), 1)

    def test_add_meridians(self):
        tmap, ax = blank_map()
        meridians = np.arange(0, 360, 30)
        tmap.add_meridians(meridians=meridians, linewidth=3, color="r", dashes=[1, 0],
                           labels=[1, 1, 1, 1], labelstyle="+/-", textcolor="b")
        options = tmap.map_options["drawmeridians"]
        np.testing.assert_array_equal(options["meridians"], meridians)
        self.assertEqual(options["linewidth"], 3)
        self.assertEqual(options["labelstyle"], "+/-")
        self.assertGreater(len(ax.lines), 0)

    def test_add_parallels(self):
        tmap, ax = blank_map()
        circles = np.arange(-60, 90, 30)
        tmap.add_parallels(circles=circles, linewidth=3, color="r", dashes=[1, 0],
                           labels=[1, 0, 0, 0], labelstyle="+/-", textcolor="b")
        options = tmap.map_options["drawparallels"]
        np.testing.assert_array_equal(options["circles"], circles)
        self.assertEqual(options["textcolor"], "b")
        self.assertGreater(len(ax.lines), 0)

    def test_add_nightshade(self):
        tmap, ax = blank_map()
        date = dt.datetime(2020, 6, 21, 12, 0, 0)
        tmap.add_nightshade(date=date, color="b", delta=0.5, alpha=0.65)
        self.assertEqual(tmap.map_options["nightshade"],
                         {"date": date, "color": "b", "delta": 0.5, "alpha": 0.65})
        self.assertGreater(len(ax.collections), 0)

    def test_repeated_calls_accumulate_options(self):
        """A later call keeps options from an earlier call unless it changes them."""
        tmap, ax = blank_map()
        tmap.add_coastlines(linewidth=3)
        tmap.add_coastlines(color="r")
        self.assertEqual(tmap.map_options["drawcoastlines"], {"linewidth": 3, "color": "r"})


class TplotMapPlotTestCases(TplotMapTestCase):
    """add_paths, add_markers and add_caps, with arrays and tplot variables."""

    def setUp(self):
        super().setUp()
        # The same square, shifted by 15 degrees, stored as a tplot variable.
        store_data("second_square", data={
            "x": time_double(["2020-01-01/00:00:00", "2020-01-01/00:01:00",
                              "2020-01-01/00:02:00", "2020-01-01/00:03:00",
                              "2020-01-01/00:04:00"]),
            "y": SQUARE_LAT_LON + 15.0,
        })

    def assert_line_at(self, tmap, line, lat_lon):
        """Check that a drawn line passes through the given (lat, lon) points."""
        x, y = tmap(lat_lon[:, 1], lat_lon[:, 0])
        np.testing.assert_allclose(line.get_xdata(), x, rtol=1e-6)
        np.testing.assert_allclose(line.get_ydata(), y, rtol=1e-6)

    def test_add_paths(self):
        """One line per coordinate set, through the projected points."""
        tmap, ax = blank_map()
        tmap.add_paths(coords=[SQUARE_LAT_LON, "second_square"], color="b", marker="d",
                       markersize=8, linestyle="dashed", linewidth=3)
        self.assertEqual(tmap.map_options["add_paths"], {
            "color": "b", "marker": "d", "markersize": 8,
            "linestyle": "dashed", "linewidth": 3, "latlon": True,
        })
        self.assertEqual(len(ax.lines), 2)
        self.assert_line_at(tmap, ax.lines[0], SQUARE_LAT_LON)
        self.assert_line_at(tmap, ax.lines[1], get_data("second_square").y)
        self.assertEqual(ax.lines[0].get_color(), "b")
        self.assertEqual(ax.lines[0].get_linestyle(), "--")

    def test_add_paths_cartesian_tplot_variable(self):
        """A tplot variable of cart_GEO positions is drawn at its geodetic footprint."""
        lat_lon = np.array([[10.0, 0.0], [20.0, 10.0], [30.0, 20.0]])
        r_lat_lon = np.hstack([np.full((3, 1), 7000.0), lat_lon])
        store_data("cartesian_track", data={
            "x": time_double(["2020-01-01/00:00", "2020-01-01/00:01", "2020-01-01/00:02"]),
            "y": cartesian2geodeticpolar(data=r_lat_lon, inverse=True),
        })
        tmap, ax = blank_map()
        tmap.add_paths(coords="cartesian_track", coord_type="cart_GEO")
        self.assertEqual(len(ax.lines), 1)
        self.assert_line_at(tmap, ax.lines[0], lat_lon)

    def test_add_markers(self):
        """One scatter collection per coordinate set, at the projected points."""
        tmap, ax = blank_map()
        sizes = [64, 16, 25, 9, 4]
        tmap.add_markers(coords=[SQUARE_LAT_LON, "second_square"], color="g", marker="o",
                         marker_size=sizes, marker_edge_widths=2, marker_edge_colors="k", alpha=0.5)
        options = tmap.map_options["add_markers"]
        self.assertEqual(options["c"], "g")
        self.assertEqual(options["marker"], "o")
        self.assertEqual(options["s"], sizes)
        self.assertEqual(options["linewidths"], 2)
        self.assertEqual(options["edgecolors"], "k")
        self.assertEqual(options["alpha"], 0.5)

        self.assertEqual(len(ax.collections), 2)
        x, y = tmap(SQUARE_LAT_LON[:, 1], SQUARE_LAT_LON[:, 0])
        np.testing.assert_allclose(ax.collections[0].get_offsets(), np.column_stack([x, y]), rtol=1e-6)
        np.testing.assert_allclose(ax.collections[0].get_sizes(), sizes)

    def test_single_point_projection_without_scalar_conversion_warning(self):
        """One-point markers and paths project without NumPy scalar warnings."""
        point = np.array([[65.0, -150.0]])  # geodetic latitude, longitude
        for projection in ("merc", "ortho"):
            for method in ("add_markers", "add_paths"):
                with self.subTest(projection=projection, method=method):
                    options = {"projection": projection}
                    if projection == "merc":
                        options.update(lat_ts=0, llcrnrlon=-166, llcrnrlat=59,
                                       urcrnrlon=-136, urcrnrlat=74)
                    else:
                        options.update(lon_0=-150, lat_0=65)
                    tmap, ax = blank_map(**options)
                    with warnings.catch_warnings():
                        warnings.filterwarnings(
                            "error", category=DeprecationWarning,
                            message="Conversion of an array with ndim > 0 to a scalar",
                        )
                        getattr(tmap, method)(point, marker="o", color="orange")
                        expected = tmap(-150.0, 65.0)
                        if method == "add_markers":
                            actual = ax.collections[-1].get_offsets()
                        else:
                            actual = ax.lines[-1].get_xydata()
                    np.testing.assert_allclose(actual, np.array([expected]))

    def test_add_markers_colormap(self):
        """Marker colors may come from data values with a colormap."""
        tmap, ax = blank_map()
        values = np.arange(SQUARE_LAT_LON.shape[0])
        tmap.add_markers(coords=SQUARE_LAT_LON, color=values, cmap="viridis")
        self.assertEqual(ax.collections[0].get_cmap().name, "viridis")
        np.testing.assert_allclose(ax.collections[0].get_array(), values)

    def test_add_caps(self):
        """One circle per point, every circle point the same angle from its center."""
        centers = np.array([[20.0, 10.0], [45.0, -30.0], [-40.0, 60.0]])  # (lat, lon)
        tmap, ax = blank_map()
        tmap.add_caps(coords=centers, linestyle="dashed", color="r")
        self.assertEqual(tmap.map_options["add_caps"], {"linestyle": "dashed", "color": "r"})
        self.assertEqual(len(ax.lines), centers.shape[0])

        # The cap edge is where a ground observer sees an altitude of 120 km at
        # the zenith angle fov_angle (80 degrees by default), on an Earth radius
        # of 6378 km, as set in add_caps().
        earth_radius, altitude, zenith = 6378.0, 120.0, 80.0
        expected_radius = zenith - np.rad2deg(np.arcsin(
            earth_radius / (earth_radius + altitude) * np.sin(np.deg2rad(zenith))))

        for line, (lat, lon) in zip(ax.lines, centers):
            with self.subTest(center=(lat, lon)):
                lons, lats = tmap(line.get_xdata(), line.get_ydata(), inverse=True)
                distance = angular_distance_deg(
                    geodetic_correction(lats, inverse=True), lons,
                    geodetic_correction(lat, inverse=True), lon)
                np.testing.assert_allclose(distance, expected_radius, rtol=1e-6)

    def test_add_caps_fov_angle(self):
        """A smaller fov_angle draws a smaller cap."""
        tmap, ax = blank_map()
        center = np.array([[0.0, 0.0]])
        tmap.add_caps(coords=np.vstack([center, center]))  # default fov_angle=80
        tmap.add_caps(coords=np.vstack([center, center]), fov_angle=60.0)
        wide_x = np.ptp(ax.lines[0].get_xdata())
        narrow_x = np.ptp(ax.lines[2].get_xdata())
        self.assertLess(narrow_x, wide_x)

    def test_add_caps_tplot_variable(self):
        """Caps can be centered on the points of a tplot variable."""
        tmap, ax = blank_map()
        tmap.add_caps(coords="second_square")
        self.assertEqual(len(ax.lines), get_data("second_square").y.shape[0])


class TplotMapFunctionTestCases(TplotMapTestCase):
    """The tplot_map() convenience function."""

    def test_creates_axes(self):
        """Without an Axes, tplot_map() makes one and returns a Tplot_Map."""
        tmap = tplot_map()
        self.assertIsInstance(tmap, Tplot_Map)
        self.assertIsNotNone(tmap.ax)
        self.assertIs(tmap.fig, tmap.ax.figure)

    def test_center(self):
        """center is (lon_0, lat_0)."""
        tmap = tplot_map(center=(-100, 40))
        self.assertEqual(tmap.map_options["basemap"]["lon_0"], -100)
        self.assertEqual(tmap.map_options["basemap"]["lat_0"], 40)

    def test_range_lat_lon(self):
        """range is (llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat) by default."""
        tmap = tplot_map(projection="mercator", range=(-40, 10, 130, 70))
        basemap_options = tmap.map_options["basemap"]
        self.assertEqual(basemap_options["projection"], "merc")
        self.assertEqual(
            [basemap_options[key] for key in ["llcrnrlon", "llcrnrlat", "urcrnrlon", "urcrnrlat"]],
            [-40, 10, 130, 70])
        np.testing.assert_allclose([tmap.llcrnrlon, tmap.llcrnrlat, tmap.urcrnrlon, tmap.urcrnrlat],
                                   [-40, 10, 130, 70])

    def test_range_xy(self):
        """With range_is_xy, range is (llcrnrx, llcrnry, urcrnrx, urcrnry) in map units."""
        tmap = tplot_map(range=(-2e6, -1e6, 2e6, 1e6), range_is_xy=True)
        basemap_options = tmap.map_options["basemap"]
        self.assertEqual(
            [basemap_options[key] for key in ["llcrnrx", "llcrnry", "urcrnrx", "urcrnry"]],
            [-2e6, -1e6, 2e6, 1e6])
        # Basemap shifts the corners by the Earth radius, but the map is still 4e6 by 2e6.
        np.testing.assert_allclose([tmap.urcrnrx - tmap.llcrnrx, tmap.urcrnry - tmap.llcrnry],
                                   [4e6, 2e6])

    def test_land_and_water_colors(self):
        """land_color fills the continents; water_color fills lakes and oceans."""
        tmap = tplot_map(land_color="darkgreen", water_color="darkblue")
        self.assertEqual(tmap.map_options["fillcontinents"]["color"], "darkgreen")
        self.assertEqual(tmap.map_options["fillcontinents"]["lake_color"], "darkblue")
        self.assertEqual(tmap.map_options["drawmapboundary"]["fill_color"], "darkblue")

    def test_view(self):
        tmap = tplot_map(view="North America")
        self.assertEqual(tmap.map_options["basemap"]["lat_0"], 50)
        self.assertEqual(tmap.map_options["basemap"]["lon_0"], 260)

    def test_override_defaults(self):
        tmap = tplot_map(override_defaults=True)
        for plot_type in PLOT_TYPES[1:]:
            with self.subTest(plot_type):
                self.assertEqual(tmap.map_options[plot_type], {})

    def test_reuse_existing_map(self):
        """A new map built from an existing one keeps its Axes, view and options."""
        first = tplot_map(view="Northern Europe", land_color="tan")
        second = tplot_map(tmap=first)
        self.assertIs(second.ax, first.ax)
        self.assertEqual(second.view, "Northern Europe")
        self.assertEqual(second.map_options["basemap"]["lat_0"], 65)
        self.assertEqual(second.map_options["fillcontinents"]["color"], "tan")

    def test_invalid_center_and_range(self):
        with self.assertRaises(ValueError):
            tplot_map(center=(0, 0, 0))
        with self.assertRaises(ValueError):
            tplot_map(range=(0, 0, 10))

    def test_save_map(self):
        """A full map can be saved as an image."""
        tmap = tplot_map(projection="merc", resolution="c", range=(-170, 35, -45, 75),
                         land_color="palegreen", water_color="lightskyblue")
        tmap.add_coastlines(linewidth=0.25)
        filename = os.path.join(save_dir, "tplot_map_basic.png")
        plt.savefig(filename, dpi=100)
        self.assertTrue(os.path.isfile(filename))
        if global_display:
            tmap.show()


class DeprecatedFunctionTestCases(TplotMapTestCase):
    """
    Module-level functions replaced by Tplot_Map methods or pyspedas.cotrans_tools.

    RULES.md: deprecated routines keep working and log a warning containing "deprecated".
    """

    def assert_deprecation_logged(self, captured):
        self.assertTrue(any("deprecated" in record.getMessage().lower()
                            for record in captured.records))

    def test_add_tracks(self):
        tmap, ax = blank_map()
        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_add_tracks(coords=SQUARE_LAT_LON, tmap=tmap)
        self.assert_deprecation_logged(captured)
        self.assertIs(result, tmap)
        self.assertEqual(len(ax.lines), 1)

    def test_add_markers(self):
        tmap, ax = blank_map()
        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_add_markers(coords=SQUARE_LAT_LON, tmap=tmap)
        self.assert_deprecation_logged(captured)
        self.assertIs(result, tmap)
        self.assertEqual(len(ax.collections), 1)

    def test_add_station_fovs(self):
        tmap, ax = blank_map()
        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_add_station_fovs(coords=SQUARE_LAT_LON, tmap=tmap)
        self.assert_deprecation_logged(captured)
        self.assertIs(result, tmap)
        self.assertEqual(len(ax.lines), SQUARE_LAT_LON.shape[0])

    def test_geodetic_correction(self):
        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_geodetic_correction(50.0)
        self.assert_deprecation_logged(captured)
        self.assertAlmostEqual(result, geodetic_correction(50.0))

    def test_cartesian2geodeticpolar(self):
        xyz = np.array([[1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_cartesian2geodeticpolar(xyz)
        self.assert_deprecation_logged(captured)
        np.testing.assert_allclose(result, cartesian2geodeticpolar(data=xyz))

    def test_tvar_to_geodeticpolar(self):
        """Same result as cotrans() to GEO followed by cartesian2geodeticpolar()."""
        store_data("position_gsm", data={
            "x": time_double(["2020-01-01/00:00", "2020-01-01/12:00"]),
            "y": np.array([[7000.0, 0.0, 0.0], [0.0, 7000.0, 3000.0]]),
        })
        cotrans(name_in="position_gsm", name_out="expected_geo", coord_in="gsm", coord_out="geo")
        expected = cartesian2geodeticpolar(data=get_data("expected_geo").y)

        with self.assertLogs(level=logging.WARNING) as captured:
            result = deprecated_tvar_to_geodeticpolar("position_gsm", in_coord_str="gsm")
        self.assert_deprecation_logged(captured)
        np.testing.assert_allclose(result, expected)


class ThemisMapTestCases(TplotMapTestCase):
    """End-to-end example with THEMIS data (downloads data; needs network access)."""

    def test_themis_ground_tracks_and_stations(self):
        from pyspedas.projects.themis import state
        from pyspedas.projects.themis.ground.gmag import Themis_gmag

        trange = ["2007-03-23", "2007-03-24"]
        state(trange=trange, probe=["a", "d"], varnames=["tha_pos_gsm", "thd_pos_gsm"])

        # Spacecraft positions in GEO, then sub-satellite points on the map.
        for probe in ["a", "d"]:
            cotrans(name_in=f"th{probe}_pos_gsm", name_out=f"th{probe}_pos_geo",
                    coord_in="gsm", coord_out="geo")
        tmap = tplot_map(view="North America", land_color="palegreen", water_color="lightskyblue")
        lines_before = len(tmap.ax.lines)
        tmap.add_paths(coords=["tha_pos_geo", "thd_pos_geo"], coord_type="cart_GEO", color="b")
        self.assertEqual(len(tmap.ax.lines), lines_before + 2)
        track = tmap.ax.lines[-1]
        expected = cartesian2geodeticpolar(data=get_data("thd_pos_geo").y)
        x, y = tmap(expected[:, 2], expected[:, 1])
        np.testing.assert_allclose(track.get_xdata(), x, rtol=1e-6)

        # THEMIS ground magnetometer stations with variometers, and their fields of view.
        stations = [station for station in Themis_gmag().get_gmag_list()
                    if station["variom"] == "Y"]
        self.assertGreater(len(stations), 0)
        station_lat_lon = np.array([[float(s["lat"]), float(s["lng"])] for s in stations])
        collections_before = len(tmap.ax.collections)
        tmap.add_markers(coords=station_lat_lon, marker_size=9)
        self.assertEqual(len(tmap.ax.collections), collections_before + 1)

        lines_before = len(tmap.ax.lines)
        tmap.add_caps(coords=station_lat_lon[:3], color="r")
        self.assertEqual(len(tmap.ax.lines), lines_before + 3)

        tmap.add_nightshade(date=dt.datetime(2007, 3, 23, 15, 0, 0))

        filename = os.path.join(save_dir, "tplot_map_full.png")
        plt.savefig(filename, dpi=100)
        self.assertTrue(os.path.isfile(filename))
        if global_display:
            tmap.show()

if __name__ == "__main__":
    unittest.main()
