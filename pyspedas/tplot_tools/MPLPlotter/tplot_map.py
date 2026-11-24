from mpl_toolkits.basemap import Basemap, _projnames, projection_params
import logging
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import datetime as dt
import string

class Tplot_Map_Param_Set():
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or 0
    def __set__(self, obj, value:dict) -> None:
        new_val = obj.__dict__.get(self.name).copy()
        for key,val in value.items():
            new_val[key] = val
        obj.__dict__[self.name] = new_val

# TODO: let color keywords be matplotlib color type options
# TODO: add auroral oval plot
class Tplot_Map(Basemap):
    """
    Create maps and add plots using tplot variables.
    
    The initialization creates the map, and class methods
    are used to add plots. Allows for customization of the
    default map format (see `options_dict` in Parameters and 
    `map_options` in Attributes). 

    The default map adds map boundaries, fills continents, 
    and draws coastlines, countries, meridians, and parallels
    as plots to the initial map, as well as adding a 
    day-night terminator shading if that option is already set.
    If any of these types of plots are not desired for the initial
    map, the `options_dict` will need to be provided at initialization
    with the options for the unwanted plot types set to None (see 
    `options_dict` in Parameters for more details). The 
    `override_defaults` argument will also need to be set to True (
    see `override_defaults` in Parameters for more details).

    Parameters
    ----------
    view : str or None, {'North America', 'Northern Europe', 'North Polar', 'South Polar', None}
        Presets for map center position. Defaults to None.
    ax : Axes, optional
        Existing Axes object to which Tplot_Map plots will be 
        attached. If none are provided, uses basemap module 
        defaults.
    option_dict : dict, optional
        Modifies `map_options` before plotting. The `option_dict`
        must have a similar format to `map_options` (see 
        `map_options` for further details). 
    override_defaults : bool, optional
        If `override_defaults` is True, the default plot options 
        in `map_options` will be completely replaced by the plot 
        options in `option_dict`. Otherwise, options for a given
        plot type only be changed if those options are specified 
        in `option_dict`. Set to False by default.
    **basemap_kwargs
        Keyword arguments for initializing Basemap objects. 
        See Basemap() for more details.

    Attributes
    ----------
    ax : Axes
        Existing Axes object to which Tplot_Map plots will be 
        attached. If none are provided, uses basemap module 
        defaults.
    fig : Figure | SubFigure
        Existing Figure which `ax` is built in.
    map_options : dict
        Dictionary where each key is the name of a plot type, and 
        each value is a plot options dictionary. For the plot
        options dictionaries, each key is an argument 
        name (e.g. 'lat_0'), and each value is the method argument
        (e.g 0). The Examples section contains a demonstration for
        viewing the current value of `map_options`. Order of plot
        type keys determines order in which initial basemap plots
        are made. The `print_map_options()` method displays what
        the format and current parameters of `map_options`.

    Methods
    -------
    show()
        Displays current Tplot_Map object.
    print_map_options()
        Print the `map_options` attribute in a readable format.
    add_coastlines(linewidth:float | None=None,linestyle:str | None=None,color:str | None=None,**drawcoastlines_kwargs)
        Draw coastlines onto the map.
    add_countries(linewidth: float | None = None, linestyle: str | None = None, color: str | None = None, **drawcountries_kwargs):
        Draw country borders onto the map.
    add_fillcontinents(color: str | None = None, lake_color: str | None = None, alpha: float | None = None,**fillcontinents_kwargs)
        Fill landmasses and lakes with colors.
    add_mapboundary(linewidth: float | None = None, color: str | None = None, fill_color:  str | None = None, **drawmapboundary_kwargs)
        Draw map borders and fill ocean color.
    add_meridians(meridians : np.ndarray | None = None, linewidth: float | None = None, color: str | None = None, dashes: list | None = None,labels: list | None = None, labelstyle: str | None = None, textcolor: str | None = None,**drawmeridians_kwargs)
        Draw meridional lines along specified longitudes.
    add_parallels(circles: np.ndarray | None = None, linewidth: float | None = None, color: str | None = None, dashes: list | None = None, labels: list | None = None, labelstyle: str | None = None,textcolor: str | None = None, **drawparallels_kwargs)
        Draw parallels lines along specified latitudes.
    add_nightshade(date : dt.datetime | None = dt.datetime.now(), color: str | None = None, delta: float | None = None,alpha: float | None = None, **nightshade_kwargs)
        Draw shaded region to represent nighttime.
    add_paths(coords: str | np.ndarray | list[str] | list[np.ndarray], coord_type: str = 'geod_lat_lon', co_latitude: bool = False, angle_meas: str = 'degrees',color=None, marker=None, markersize=None, linestyle=None, linewidth=None, **plot_kwargs)
        Draw line of points, optionally using tplot variable
    add_markers(coords: str | np.ndarray | list[str] | list[np.ndarray],coord_type: str = 'geod_lat_lon', co_latitude: bool = False, angle_meas: str = 'degrees',color = None, marker = None, marker_size = None, marker_edge_widths = None, marker_edge_colors = None,cmap = None, norm = None, alpha = None, **scatter_kwargs)
        Plot set of coordinates with optionally varying marker sizes and colors.    
    add_caps(coords: str | np.ndarray | list[str] | list[np.ndarray], fov_angle = 80.0,coord_type: str = 'geod_lat_lon', co_latitude: bool = False, angle_meas: str = 'degrees',color=None, marker=None, linestyle=None, linewidth=None, markersize=None, **plot_kwargs)
        Draw circles around a set of coordinates, optionally using tplot variable

    Notes
    -----
    Tplot_Map inherits from Basemap, so standard Basemap class functions
    and usage are accessible using the Tplot_Map object. Please see 
    Basemap() for more details.

    The Tplot_Map class methods which wrap Basemap methods update
    the `map_options` dictionary, and also enable the use of tplot
    variables in map plots.

    If an option used by Basemap or its class methods aren't provided
    in `map_options`, the default option value in the Basemap method is
    used instead.

    Examples
    --------
    
    Create a default Tplot_Map object:
    
    >>> tmap = Tplot_Map()    

    Create Tplot_Map object with a view over northern Europe:
    
    >>> print(Tplot_Map(view='Northern Europe').map_options["basemap"])
    {'projection': 'ortho', 'lat_0': 65, 'lon_0': 20}

    Create Tplot_Map object with a day-night boundary and modified water colors:
    
    >>> import datetime as dt
    >>> tmap = Tplot_Map(option_dict={"nightshade":{"date":dt.datetime(2026, 11, 19, 11, 8, 21),"alpha":0.5},"fillcontinents":{"lake_color": "lightskyblue"},"drawmapboundary":{"fill_color":"lightskyblue"}})
    >>> print(tmap.map_options["nightshade"])
    {'date': datetime.datetime(2026, 11, 19, 11, 8, 21), 'alpha': 0.5}
    >>> print(tmap.map_options["fillcontinents"])
    {'color': 'white', 'lake_color': 'lightskyblue'}
    >>> print(tmap.map_options["drawmapboundary"])
    {'fill_color': 'lightskyblue'}
    >>> tmap.show()  # doctest: +SKIP

    Override `map_options` using `option_dict`:

    >>> tmap = Tplot_Map(override_defaults=True,option_dict={"basemap":{"projection":"mercator"},"fillcontinents":{"lake_color": "lightskyblue"}})
    >>> tmap.print_map_options()
    Current Map Options:
    {
     'basemap' : {'projection': 'merc'},
     'drawcoastlines' : {},
     'drawcountries' : {},
     'fillcontinents' : {'lake_color': 'lightskyblue'},
     'drawmapboundary' : {},
     'drawmeridians' : {},
     'drawparallels' : {},
     'nightshade' : {},
     'add_paths' : {},
     'add_markers' : {},
     'add_caps' : {},
    }
    """
    def __init__(
            self, 
            view:         str | None = None, 
            ax:          Axes | None = None, 
            option_dict: dict | None = None,
            override_defaults: bool = False,
            **basemap_kwargs):

        # Define projection options, construct 
        # projection options dict from basemap
        # projection params
        self._projection_params = projection_params
        self._corners_latlon = ["llcrnrlon","llcrnrlat","urcrnrlon","urcrnrlat"]
        self._corners_xy = ["llcrnrx","llcrnry","urcrnrx","urcrnry"]
        self._center = ["lon_0","lat_0"]
        self._center_1 = ["lon_1","lat_1"]
        self._center_2 = ["lon_2","lat_2"]
        self._invalid_projection_params = dict()
        self._convert_projection_params()

        self.ax = None
        self.fig = None
        if ax is not None:
            self.ax = ax
            self.fig = self.ax.figure

        # TODO: provide meridians in magnetic coordinates as well
        # Define default options for map methods:
        self.map_options = {
            "basemap": {"projection":"ortho","lat_0":0,"lon_0":0},
            "drawcoastlines":{"linewidth":0.25},
            "drawcountries":{"linewidth":0.25},
            "fillcontinents":{"color":"white","lake_color":"white"},
            "drawmapboundary":{"fill_color":"white"},
            "drawmeridians":{"meridians":np.arange(0,360,10)},
            "drawparallels":{"circles":np.arange(-90,90,10)},
            "nightshade":{},
            "add_paths":{},
            "add_markers":{"color":"r","marker":"d"},
            "add_caps":{},
        }

        # Handle basemap_kwargs, if any:
        self.map_options["basemap"].update(basemap_kwargs)
        
        # If view is set, override basemap kwargs for centering position
        self.view = view
        if self.view is not None:
            match self.view:
                case "North America":
                    self.map_options["basemap"]["lat_0"] = 50
                    self.map_options["basemap"]["lon_0"] = 260
                case "Northern Europe":
                    self.map_options["basemap"]["lat_0"] = 65
                    self.map_options["basemap"]["lon_0"] = 20
                case "North Polar":
                    self.map_options["basemap"]["lat_0"] = 90
                    self.map_options["basemap"]["lon_0"] = 0
                case "South Polar":
                    self.map_options["basemap"]["lat_0"] = -90
                    self.map_options["basemap"]["lon_0"] = 0
                case _:
                    raise ValueError(f'Received view = "{self.view}"; must be one of: "North America", "Northern Europe", "North Polar", "South Polar"')

        if option_dict is None:
            option_dict = {}
                
        for key in self.map_options.keys():
            if key in option_dict.keys():
                if override_defaults:
                    self.map_options[key] = option_dict[key]
                else:
                    self.map_options[key].update(option_dict[key])
            else:
                if override_defaults and key != "basemap":
                    self.map_options[key] = {}
        
        # Validate basemap inputs, and provide warnings if inputs are not valid:
        self._validate_basemap_params()

        # Deprecated; retained for compatibility: 
        self._params = Tplot_Map_Param_Set()
        
        # Use map_options to update self._params, and make initial plots:
        for map_plottype in self.map_options.keys():
            # If plot_options are defined, create plot from
            # corresponding map_plottype:
            if self.map_options.get(map_plottype) is not None and self.map_options.get(map_plottype) != {}:
                if self.ax is not None:
                    self.map_options[map_plottype]["ax"] = self.ax
                if map_plottype in ["basemap","drawmapboundary","fillcontinents","drawcoastlines","drawcountries","drawmeridians","drawparallels","nightshade"]:
                    self._add_plot_feature(map_plottype)
            self._overwrite_params(map_plottype)

    # Display methods:
    def show(self): 
        """
        Displays current Tplot_Map object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------        
        
        Display the default Tplot_Map:
        
        >>> Tplot_Map().show()  # doctest: +SKIP
        """
        plt.show()
        return

    def print_map_options(self):
        """
        Print the `map_options` attribute in a readable format.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------        
        
        Print default `map_options`:
            
        >>> Tplot_Map().print_map_options()  # doctest: +NORMALIZE_WHITESPACE
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0},
         'drawcoastlines' : {'linewidth': 0.25},
         'drawcountries' : {'linewidth': 0.25},
         'fillcontinents' : {'color': 'white', 'lake_color': 'white'},
         'drawmapboundary' : {'fill_color': 'white'},
         'drawmeridians' : {'meridians': array([  0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100, 110, 120,
            130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250,
            260, 270, 280, 290, 300, 310, 320, 330, 340, 350])},
         'drawparallels' : {'circles': array([-90, -80, -70, -60, -50, -40, -30, -20, -10,   0,  10,  20,  30,
            40,  50,  60,  70,  80])},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {'color': 'r', 'marker': 'd'},
         'add_caps' : {},
        }      
        """
        outstr = "Current Map Options:\n{\n"
        for key in self.map_options.keys():
            outstr = outstr + " '" + f"{key}" + "' : " + f"{self.map_options[key]}" + ",\n"
        outstr = outstr + "}"
        print(outstr)
        return

    # Basemap wrapper methods:
    def add_coastlines(
            self,
            linewidth: float | None = None,
            linestyle:   str | None = None,
            color:       str | None = None,
            **drawcoastlines_kwargs):
        """
        Draw coastlines onto the map.
        
        Parameters
        ----------
        linewidth : float, optional
            Thickness of line drawn around coasts. If None, uses 
            `map_options` or Basemap `drawcoastlines` defaults.
        linestyle : str, optional
            Indicates which line format option will be used 
            (e.g. 'solid','dashed',etc...). If None, uses 
            `map_options` or Basemap `drawcoastlines` defaults.
        color : str, optional
            Indicates which color the line drawn around coasts will 
            be (e.g. black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `drawcoastlines` defaults.
        **drawcoastlines_kwargs
            Keyword arguments for other basemap `drawcoastlines` method options.

        Notes
        -----
        Wrapper for Basemap `drawcoastlines` method.
        Saves input options to `map_options` attribute.

        Returns
        -------
        None

        Examples
        --------

        Draw a map using only blue dashed line coastlines:

        >>> tmap = Tplot_Map(option_dict={},override_defaults=True)
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.add_coastlines(linewidth = 3,linestyle = 'dashed',color = 'b')
        >>> print(tmap.map_options["drawcoastlines"])
        {'linewidth': 3, 'linestyle': 'dashed', 'color': 'b'}
        >>> tmap.show()  # doctest: +SKIP
        """
        if linewidth is not None:
            drawcoastlines_kwargs.update({'linewidth':linewidth})
        if linestyle is not None:
            drawcoastlines_kwargs.update({'linestyle':linestyle})
        if color is not None:
            drawcoastlines_kwargs.update({'color':color})
        self._add_plot_feature(plot_type="drawcoastlines",plot_type_kwargs=drawcoastlines_kwargs)
        return

    def add_countries(
            self,
            linewidth: float | None = None,
            linestyle:   str | None = None,
            color:       str | None = None,
            **drawcountries_kwargs):
        """
        Draw country borders onto the map.
                
        Parameters
        ----------
        linewidth : float, optional
            Thickness of line drawn around country borders. If None, uses 
            `map_options` or Basemap `drawcountries` defaults.
        linestyle : str, optional
            Indicates which line format option will be used 
            (e.g. 'solid','dashed',etc...). If None, uses 
            `map_options` or Basemap `drawcountries` defaults.
        color : str, optional
            Indicates which color the line drawn around coasts will 
            be (e.g. black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `drawcountries` defaults.
        **drawcountries_kwargs
            Keyword arguments for the basemap `drawcountries` method.

        Notes
        -----
        Wrapper for Basemap `drawcountries` method.
        Saves input options to `map_options` attribute.

        Returns
        -------
        None

        Examples
        --------

        Draw a map using only blue dashed line country borders:

        >>> tmap = Tplot_Map(option_dict={},override_defaults=True)
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.add_countries(linewidth = 3,linestyle = 'dashed',color = 'b')
        >>> print(tmap.map_options["drawcountries"])
        {'linewidth': 3, 'linestyle': 'dashed', 'color': 'b'}
        >>> tmap.show()  # doctest: +SKIP
        """
        if linewidth is not None:
            drawcountries_kwargs.update({'linewidth':linewidth})
        if linestyle is not None:
            drawcountries_kwargs.update({'linestyle':linestyle})
        if color is not None:
            drawcountries_kwargs.update({'color':color})
        self._add_plot_feature(plot_type="drawcountries",plot_type_kwargs=drawcountries_kwargs)
        return

    def add_fillcontinents(
            self,
            color :      str | None = None,
            lake_color : str | None = None,
            alpha :    float | None = None,
            **fillcontinents_kwargs):
        """
        Fill landmasses and lakes with colors.
                                
        Parameters
        ----------
        color : str, optional
            Fills landmasses.
        lake_color : str, optional
            Fills lakes within landmasses. 
        alpha : float, optional
            Sets transparency for landmass polygons, allowing the map 
            background (see method `add_mapboundary`) to show through.
        **fillcontinents_kwargs
            Keyword arguments for the basemap `fillcontinents` method.

        Notes
        -----
        Wrapper for Basemap `fillcontinents` method.
        Saves input options to `map_options` attribute.
        
        Returns
        -------
        None

        Examples
        --------

        Draw landmasses in dark green, lakes in dark blue, with a transparency alpha of 0.5 (leaving the oceans white):

        >>> tmap = Tplot_Map(option_dict={},override_defaults=True)
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.add_fillcontinents(color = 'darkgreen',lake_color = 'darkblue',alpha = 0.5)
        >>> print(tmap.map_options["fillcontinents"])
        {'color': 'darkgreen', 'lake_color': 'darkblue', 'alpha': 0.5}
        >>> tmap.show()  # doctest: +SKIP
        """
        if color is not None:
            fillcontinents_kwargs.update({'color':color})
        if lake_color is not None:
            fillcontinents_kwargs.update({'lake_color':lake_color})
        if alpha is not None:
            fillcontinents_kwargs.update({'alpha':alpha})
        self._add_plot_feature(plot_type="fillcontinents",plot_type_kwargs=fillcontinents_kwargs)
        return

    def add_mapboundary(
            self,
            linewidth: float | None = None,
            color:       str | None = None,
            fill_color:  str | None = None,
            **drawmapboundary_kwargs):
        """
        Draw map borders and fill ocean color.
                        
        Parameters
        ----------
        linewidth : float, optional
            Thickness of line drawn around the outer edge of the map. If None, uses 
            `map_options` or Basemap `drawmapboundary` defaults.
        color : str, optional
            Indicates color of the map boundary line drawn (e.g. 
            black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `drawmapboundary` defaults.
            Defaults to black.
        fill_color : str, optional
            Fills map background (ocean color). If None, uses 
            `map_options` or Basemap `drawmapboundary` defaults.
            Defaults to white.
        **drawmapboundary_kwargs
            Keyword arguments for the basemap `drawmapboundary` method.

        Notes
        -----
        Wrapper for Basemap `drawmapboundary` method.
        Saves input options to `map_options` attribute.

        Returns
        -------
        None

        Examples
        --------

        Draw a light blue featureless globe with a red border:

        >>> tmap = Tplot_Map(option_dict={},override_defaults=True)
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.add_mapboundary(linewidth = 3,color = 'r',fill_color = 'lightskyblue')
        >>> print(tmap.map_options["drawmapboundary"])
        {'linewidth': 3, 'color': 'r', 'fill_color': 'lightskyblue'}
        >>> tmap.show()  # doctest: +SKIP
        """
        if linewidth is not None:
            drawmapboundary_kwargs.update({'linewidth':linewidth})
        if color is not None:
            drawmapboundary_kwargs.update({'color':color})
        if fill_color is not None:
            drawmapboundary_kwargs.update({'fill_color':fill_color})
        self._add_plot_feature(plot_type="drawmapboundary",plot_type_kwargs=drawmapboundary_kwargs)
        return
    
    # TODO: add support for tplot variables in meridians and parallels
    def add_meridians(
            self,
            meridians : np.ndarray | None = None,
            linewidth :      float | None = None,
            color :            str | None = None,
            dashes :          list | None = None,
            labels :          list | None = None,
            labelstyle :       str | None = None,
            textcolor :        str | None = None,
            **drawmeridians_kwargs):
        """
        Draw meridional lines along specified longitudes.
                                
        Parameters
        ----------
        meridians : np.ndarray
            Array containing longitudes to locate meridional lines. Expects 
            longitudes in degrees. 
        linewidth : float, optional
            Thickness of line drawn around the outer edge of the map. If None, uses 
            `map_options` or Basemap `drawmeridians` defaults.
        color : str, optional
            Indicates color of the meridional lines drawn (e.g. 
            black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `drawmeridians` defaults.
            Defaults to black.
        dashes : list, optional
            Dash pattern for meridians (default [1,1], i.e.
            1 pixel on, 1 pixel off). If None, uses 
            `map_options` or Basemap `drawmeridians` defaults.
        labels : list, optional          
            List of 4 values (default [0,0,0,0]) that control
            whether meridians are labelled where they intersect
            the left, right, top or bottom of the plot. For
            example labels=[1,0,0,1] will cause meridians
            to be labelled where they intersect the left and
            and bottom of the plot, but not the right and top.
            If None, uses `map_options` or Basemap 
            `drawmeridians` defaults.
        labelstyle : string, optional
            If set to "+/-", east and west longitudes are
            labelled with "+" and "-", otherwise they are
            labelled with "E" and "W".
        textcolor : str, optional,
            Color of text used to label meridians where they 
            intersect with the map border (e.g. black text 
            uses the 'k' string). If None, uses `map_options` 
            or Basemap `drawmeridians` defaults. 
        **drawmeridians_kwargs
            Keyword arguments for the basemap `drawmeridians` method.

        Notes
        -----
        Wrapper for Basemap `drawmeridians` method.
        Saves input options to `map_options` attribute.

        Returns
        -------
        None

        Examples
        --------

        Draw solid red meridians every 30 degrees, with blue 
        labels placed along all edges of the plot where the longitude
        intersects with the map boundary:

        >>> tmap = Tplot_Map(view="Northern Europe",override_defaults=True,projection="mercator",llcrnrlon=-40,llcrnrlat=10,urcrnrlon=130,urcrnrlat=70)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_meridians(meridians=np.arange(0,360,30),linewidth=3,color = 'r',dashes = [1,0],labels = [1,1,1,1],labelstyle="+/-",textcolor='b')
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'merc', 'lat_0': 65, 'lon_0': 20, 'llcrnrlon': -40, 'llcrnrlat': 10, 'urcrnrlon': 130, 'urcrnrlat': 70},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {'meridians': array([  0,  30,  60,  90, 120, 150, 180, 210, 240, 270, 300, 330]), 'linewidth': 3, 'color': 'r', 'dashes': [1, 0], 'labels': [1, 1, 1, 1], 'labelstyle': '+/-', 'textcolor': 'b'},
         'drawparallels' : {},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.show()  # doctest: +SKIP
        """
        if meridians is not None:
            drawmeridians_kwargs.update({'meridians':meridians})
        if linewidth is not None:
            drawmeridians_kwargs.update({'linewidth':linewidth})
        if color is not None:
            drawmeridians_kwargs.update({'color':color})
        if dashes is not None:
            drawmeridians_kwargs.update({'dashes':dashes})
        if labels is not None:
            drawmeridians_kwargs.update({'labels':labels})
        if labelstyle is not None:
            drawmeridians_kwargs.update({'labelstyle':labelstyle})
        if textcolor is not None:
            drawmeridians_kwargs.update({'textcolor':textcolor})    
        self._add_plot_feature(plot_type="drawmeridians",plot_type_kwargs=drawmeridians_kwargs)
        return

    def add_parallels(
            self,
            circles :   np.ndarray | None = None,
            linewidth :      float | None = None,
            color :            str | None = None,
            dashes :          list | None = None,
            labels :          list | None = None,
            labelstyle :       str | None = None,
            textcolor :        str | None = None,
            **drawparallels_kwargs):
        """
        Draw parallels lines along specified latitudes.
                                        
        Parameters
        ----------
        circles : np.ndarray
            Array containing latitudes to locate parallels. Expects 
            latitudes in degrees. 
        linewidth : float, optional
            Thickness of line drawn around the outer edge of the map. If None, uses 
            `map_options` or Basemap `drawparallels` defaults.
        color : str, optional
            Indicates color of the parallels drawn (e.g. 
            black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `drawparallels` defaults.
            Defaults to black.
        dashes : list, optional
            Dash pattern for parallels (default [1,1], i.e.
            1 pixel on, 1 pixel off). If None, uses 
            `map_options` or Basemap `drawparallels` defaults.
        labels : list, optional          
            List of 4 values (default [0,0,0,0]) that control
            whether parallels are labelled where they intersect
            the left, right, top or bottom of the plot. For
            example labels=[1,0,0,1] will cause parallels
            to be labelled where they intersect the left and
            and bottom of the plot, but not the right and top.
            If None, uses `map_options` or Basemap 
            `drawparallels` defaults.
        labelstyle : string, optional
            If set to "+/-", north and south latitudes are
            labelled with "+" and "-", otherwise they are
            labelled with "N" and "S".
        textcolor : str, optional,
            Color of text used to label parallels where they 
            intersect with the map border (e.g. black text 
            uses the 'k' string). If None, uses `map_options` 
            or Basemap `drawparallels` defaults. 
        **drawparallels_kwargs
            Keyword arguments for the basemap `drawparallels` method.

        Notes
        -----
        Wrapper for Basemap `drawparallels` method.
        Saves input options to `map_options` attribute.
        

        Returns
        -------
        None

        Examples
        --------

        Draw solid red parallels every 30 degrees, with blue 
        labels placed along all edges of the plot where the longitude
        intersects with the map boundary:

        >>> tmap = Tplot_Map(view="Northern Europe",option_dict={},override_defaults=True,projection="mercator",llcrnrlon=-40,llcrnrlat=10,urcrnrlon=130,urcrnrlat=70)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_parallels(circles=np.arange(0,90,30),linewidth=3,color = 'r',dashes = [1,0],labels = [1,1,1,1],labelstyle="+/-",textcolor='b')
        >>> tmap.print_map_options()
        Current Map Options:
        {
         'basemap' : {'projection': 'merc', 'lat_0': 65, 'lon_0': 20, 'llcrnrlon': -40, 'llcrnrlat': 10, 'urcrnrlon': 130, 'urcrnrlat': 70},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {'circles': array([ 0, 30, 60]), 'linewidth': 3, 'color': 'r', 'dashes': [1, 0], 'labels': [1, 1, 1, 1], 'labelstyle': '+/-', 'textcolor': 'b'},
         'nightshade' : {},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.show()  # doctest: +SKIP
        """
        if circles is not None:
            drawparallels_kwargs.update({'circles':circles})
        if linewidth is not None:
            drawparallels_kwargs.update({'linewidth':linewidth})
        if color is not None:
            drawparallels_kwargs.update({'color':color})
        if dashes is not None:
            drawparallels_kwargs.update({'dashes':dashes})
        if labels is not None:
            drawparallels_kwargs.update({'labels':labels})
        if labelstyle is not None:
            drawparallels_kwargs.update({'labelstyle':labelstyle})
        if textcolor is not None:
            drawparallels_kwargs.update({'textcolor':textcolor})
        self._add_plot_feature(plot_type="drawparallels",plot_type_kwargs=drawparallels_kwargs)
        return

    def add_nightshade(
            self,
            date : dt.datetime | None = None,
            color :        str | None = None,
            delta :      float | None = None,
            alpha :      float | None = None,
            **nightshade_kwargs):
        """
        Draw shaded region to represent nighttime.
                                                
        Parameters
        ----------
        date : DateTime, optional
            Specifies time from which regions in darkness will be inferred. 
        color : str, optional
            Indicates color of the shading (e.g. 
            black lines can use the 'k' string). If None, uses 
            `map_options` or Basemap `nightshade` defaults.
            Defaults to black.
        delta : float, optional
            Day/night terminator is computed with a
            a resolution of ``delta`` degrees 
            (default 0.25).If None, uses `map_options` 
            or Basemap `nightshade` defaults.
        alpha : float, optional
            Alpha transparency for shading (default 0.5, so
            map background shows through).If None, uses 
            `map_options` or Basemap `nightshade` defaults.
        **nightshade_kwargs
            Keyword arguments for the basemap `nightshade` method.

        Notes
        -----
        Wrapper for Basemap `nightshade` method.
        Saves input options to `map_options` attribute.
        
        Returns
        -------
        None

        Examples
        --------

        Shade the nighttime of a globe centered over North America using the
        current time, with the shading being done in blue, a degree resolution 
        of 0.5, and a transparency of 65%:

        >>> tmap = Tplot_Map(view="North America",override_defaults=True)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_nightshade(color='b',delta=0.5,alpha=0.65)
        >>> tmap.print_map_options()  # doctest: +ELLIPSIS
        Current Map Options:
        {
         'basemap' : {'projection': 'ortho', 'lat_0': 50, 'lon_0': 260},
         'drawcoastlines' : {},
         'drawcountries' : {},
         'fillcontinents' : {},
         'drawmapboundary' : {},
         'drawmeridians' : {},
         'drawparallels' : {},
         'nightshade' : {'date': datetime.datetime(...), 'color': 'b', 'delta': 0.5, 'alpha': 0.65},
         'add_paths' : {},
         'add_markers' : {},
         'add_caps' : {},
        }
        >>> tmap.show()  # doctest: +SKIP
        """
        if date is None:
            date = dt.datetime.now()
        nightshade_kwargs.update({'date':date})
        if color is not None:
            nightshade_kwargs.update({'color':color})
        if delta is not None:
            nightshade_kwargs.update({'delta':delta})
        if alpha is not None:
            nightshade_kwargs.update({'alpha':alpha})
        self._add_plot_feature(plot_type="nightshade",plot_type_kwargs=nightshade_kwargs)
        return

    # Plotting methods which accept tplot variables:
    def add_paths(
            self,
            coords: str | np.ndarray | list[str] | list[np.ndarray], 
            coord_type: str = 'geod_lat_lon',
            co_latitude: bool = False,
            angle_meas: str = 'degrees',
            color=None, 
            marker=None, 
            markersize=None,
            linestyle=None,
            linewidth=None, 
            **plot_kwargs):
        """
        Draw line of points, optionally using tplot variable

        Parameters
        ----------
        coords : str or np.ndarray or list of str or list of np.ndarray
            Coordinate data to convert to geodetic coordinate data. If
            `coords` or each element of `coords` (if `coords` is a list)
            are of the string type, then attempts to load data from a tplot
            variable, using the string as the tplot variable name. Otherwise,
            attempts to transform the coordinate data directly. 
        coord_type : {'geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO'}
            Indicates how the input coordinates should be interpreted. The 
            first and second (and third, if applicable) components of the
            data will be interpreted as the following for each `coord_type`:
            geod_lat_lon : Geodetic latitude, Longitude
            geoc_lat_lon : Geocentric Latitude, Longitude
            geod_spherical : Radius, Geodetic Latitude, Longitude
            geoc_spherical : Radius, Geocentric Latitude, Longitude
            cart_GEO : X, Y, Z in ECEF coordinates 

            Defaults to 'geod_lat_lon'
        co_latitude : bool, optional
            Indicates if input latitude is a co-latitude. Here,
            co-latitude is defined as angle between the position vector and
            axis of Earth's rotation. Default is False
        angle_meas : {'degrees', 'radians', 'arcminutes'}
            Indicates unit of measurement of input latitude and longitude 
            coordinates. Defaults to 'degrees'
        color : string or tuple of float or tuple of string and float, optional
            Indicates line color (e.g. black lines can use 
            the 'k' string). If None, uses `map_options` 
            or Basemap `add_paths` defaults. Defaults to black.
        marker : string or Path or MarkerStyle, optional
            Indicates style of marker along line path. Defaults
            to None, skipping markers being drawn.
        markersize : float, optional
            Sets size of markers.
        linestyle : string or tuple, optional
            Indicates how line path is drawn (e.g. 'dashed'). 
            Defaults to solid line.
        linewidth : float, optional
            Sets width of line path.
        **plot_kwargs
            Keyword arguments for the basemap `plot` method.
        
        Notes
        -----
        Wrapper for Basemap `plot` method, intended for
        use with traces. Saves input options to 
        `map_options` attribute.
        
        Returns
        -------
        None

        Examples
        --------

        Draw two squares on a mercator projection map, once using
        a numpy array, and another using a tplot variable. 
    
        >>> import numpy as np
        >>> from pyspedas import store_data
        >>> arr_path_points = np.array([
        ...     (0,0),
        ...     (30,0),
        ...     (30,30),
        ...     (0,30),
        ...     (0,0),
        ... ])
        >>> tplot_path_points = "second square"
        >>> store_data(
        ...     name=tplot_path_points,
        ...     data = {
        ...         'x': [1,2,3,4,5],
        ...         'y': np.array([
        ...             (15,15),
        ...             (45,15),
        ...             (45,45),
        ...             (15,45),
        ...             (15,15),
        ...         ])
        ...     },
        ... )
        True
        >>> squares_coords = [arr_path_points,tplot_path_points]
        >>> tmap = Tplot_Map(override_defaults=True,projection="mercator",llcrnrlon=-50,urcrnrlon=50,llcrnrlat=-50,urcrnrlat=50)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_paths(coords=squares_coords,marker='d',markersize=8,linestyle='dashed',linewidth=3)
        >>> tmap.show()  # doctest: +SKIP
        """
        if color is not None:
            plot_kwargs.update({"color":color})
        if marker is not None:
            plot_kwargs.update({"marker":marker})
        if linestyle is not None:
            plot_kwargs.update({"linestyle":linestyle})
        if linewidth is not None:
            plot_kwargs.update({"linewidth":linewidth})
        if markersize is not None:
            plot_kwargs.update({"markersize":markersize})
        plot_kwargs.update({"latlon":True})
        self.map_options["add_paths"].update(plot_kwargs)

        self._overwrite_params("add_paths")
        for coord_set in convert_coords_to_geod_lonlat_list(coords=coords,coord_type=coord_type,co_latitude=co_latitude,angle_meas=angle_meas):
            self.plot(coord_set[:,0],coord_set[:,1],**self.map_options.get("add_paths"))
        return

    def add_markers(
            self,
            coords: str | np.ndarray | list[str] | list[np.ndarray],
            coord_type: str = 'geod_lat_lon',
            co_latitude: bool = False,
            angle_meas: str = 'degrees',
            color = None,
            marker = None,
            marker_size = None,
            marker_edge_widths = None,
            marker_edge_colors = None,
            cmap = None,
            norm = None,
            alpha = None,
            **scatter_kwargs):
        """
        Plot set of coordinates with optionally varying marker sizes and colors.
        
        Parameters
        ----------
        coords : str or np.ndarray or list of str or list of np.ndarray
            Coordinate data to convert to geodetic coordinate data. If
            `coords` or each element of `coords` (if `coords` is a list)
            are of the string type, then attempts to load data from a tplot
            variable, using the string as the tplot variable name. Otherwise,
            attempts to transform the coordinate data directly.
        coord_type : {'geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO'}
            Indicates how the input coordinates should be interpreted. The 
            first and second (and third, if applicable) components of the
            data will be interpreted as the following for each `coord_type`:
            geod_lat_lon : Geodetic latitude, Longitude
            geoc_lat_lon : Geocentric Latitude, Longitude
            geod_spherical : Radius, Geodetic Latitude, Longitude
            geoc_spherical : Radius, Geocentric Latitude, Longitude
            cart_GEO : X, Y, Z in ECEF coordinates

            Defaults to 'geod_lat_lon'
        co_latitude : bool, optional
            Indicates if input latitude is a co-latitude. Here,
            co-latitude is defined as angle between the position vector and
            axis of Earth's rotation. Default is False
        angle_meas : {'degrees', 'radians', 'arcminutes'}
            Indicates unit of measurement of input latitude and longitude 
            coordinates. Defaults to 'degrees'
        color : array-like or list of color or color, optional
            The marker colors. See `pyplot.scatter` for more details.
        marker : MarkerStyle, optional
            The marker style. See `pyplot.scatter` for more details.
        marker_size : float or array-like, shape (n, ), optional
            The marker size in points**2 (typographic points are 1/72 in.). 
            See `pyplot.scatter` for more details.
        marker_edge_widths : float or array-like, optional
            The linewidth of the marker edges. See `pyplot.scatter` for more details.
        marker_edge_colors : {'face', 'none', None} or color or list of color, optional
            The edge color of the marker. See `pyplot.scatter` for more details.
        cmap : str or Colormap, optional
            The Colormap instance or registered colormap name used to map scalar 
            data to colors. See `pyplot.scatter` for more details.
        norm : str or Normalize, optional
            The normalization method used to scale scalar data to the [0, 1] range before 
            mapping to colors using cmap. See `pyplot.scatter` for more details.
        alpha : float, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).
        **scatter_kwargs
            Keyword arguments for the basemap `scatter` method.
            
        Notes
        -----
        Wrapper for Basemap `scatter` method, intended for
        use with coordinate points. Saves input options to 
        `map_options` attribute.

        If plotting points of the same marker size and color,
        it is more efficient to use the `add_paths` method,
        with the line style set to 'none' and by setting the 
        marker option.
        
        Returns
        -------
        None

        Examples
        --------

        Draw two sets of point markers: one using 
        a numpy array and another using a tplot variable.
        Have the first set be a different color from the 
        second set, and have the size of the markers 
        vary, with points of the same index having the
        same size:

        >>> import numpy as np
        >>> from pyspedas import store_data
        >>> arr_path_points = np.array([
        ...     (0,0),
        ...     (30,0),
        ...     (30,30),
        ...     (0,30),
        ... ])
        >>> tplot_path_points = "second square"
        >>> store_data(
        ...     name=tplot_path_points,
        ...     data = {
        ...         'x': [1,2,3,4],
        ...         'y': np.array([
        ...             (15,15),
        ...             (45,15),
        ...             (45,45),
        ...             (15,45),
        ...         ])
        ...     },
        ... )
        True
        >>> squares_coords = [arr_path_points,tplot_path_points]
        >>> tmap = Tplot_Map(override_defaults=True,projection="mercator",llcrnrlon=-50,urcrnrlon=50,llcrnrlat=-50,urcrnrlat=50)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_markers(coords=squares_coords,marker='d',marker_size=[64,16,25,9])
        >>> tmap.show()  # doctest: +SKIP
        """
        if color is not None:
            scatter_kwargs.update({"c":color})
        if marker is not None:
            scatter_kwargs.update({"marker":marker})
        if marker_size is not None:
            scatter_kwargs.update({"s":marker_size})
        if marker_edge_widths is not None:
            scatter_kwargs.update({"linewidths":marker_edge_widths})
        if marker_edge_colors is not None:
            scatter_kwargs.update({"edgecolors":marker_edge_colors})
        if cmap is not None:
            scatter_kwargs.update({"cmap":cmap})
        if norm is not None:
            scatter_kwargs.update({"norm":norm})
        if alpha is not None:
            scatter_kwargs.update({"alpha":alpha})
        self.map_options["add_markers"].update(scatter_kwargs)
        self._overwrite_params("add_markers")
        for coord_set in convert_coords_to_geod_lonlat_list(coords=coords,coord_type=coord_type,co_latitude=co_latitude,angle_meas=angle_meas):
            self.scatter(coord_set[:,0],coord_set[:,1],**self.map_options.get("add_markers"),latlon=True)
        return

    # TODO: add option for km radius
    def add_caps(
            self,
            coords: str | np.ndarray | list[str] | list[np.ndarray],
            fov_angle = 80.0,
            coord_type: str = 'geod_lat_lon',
            co_latitude: bool = False,
            angle_meas: str = 'degrees',
            color=None, 
            marker=None, 
            linestyle=None,
            linewidth=None, 
            markersize=None, 
            **plot_kwargs):
        """
        Draw circles around a set of coordinates, optionally using tplot variable
        
        Parameters
        ----------
        coords : str or np.ndarray or list of str or list of np.ndarray
            Coordinate data to convert to geodetic coordinate data. If
            `coords` or each element of `coords` (if `coords` is a list)
            are of the string type, then attempts to load data from a tplot
            variable, using the string as the tplot variable name. Otherwise,
            attempts to transform the coordinate data directly. 
        fov_angle : float, optional
            Sets "zenith angle" when calculating circle around center point.
            Smaller fov_angle values result in smaller radii for the circles
            around the stations.
        coord_type : {'geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO'}
            Indicates how the input coordinates should be interpreted. The 
            first and second (and third, if applicable) components of the
            data will be interpreted as the following for each `coord_type`:
            geod_lat_lon : Geodetic latitude, Longitude
            geoc_lat_lon : Geocentric Latitude, Longitude
            geod_spherical : Radius, Geodetic Latitude, Longitude
            geoc_spherical : Radius, Geocentric Latitude, Longitude
            cart_GEO : X, Y, Z in ECEF coordinates 

            Defaults to 'geod_lat_lon'
        co_latitude : bool, optional
            Indicates if input latitude is a co-latitude. Here,
            co-latitude is defined as angle between the position vector and
            axis of Earth's rotation. Default is False
        angle_meas : {'degrees', 'radians', 'arcminutes'}
            Indicates unit of measurement of input latitude and longitude 
            coordinates. Defaults to 'degrees'
        color : string or tuple of float or tuple of string and float, optional
            Indicates line color (e.g. black lines can use 
            the 'k' string). If None, uses `map_options` 
            or Basemap `add_paths` defaults. Defaults to black.
        marker : string or Path or MarkerStyle, optional
            Indicates style of marker along line path. Defaults
            to None, skipping markers being drawn.
        markersize : float, optional
            Sets size of markers.
        linestyle : string or tuple, optional
            Indicates how line path is drawn (e.g. 'dashed'). 
            Defaults to solid line.
        linewidth : float, optional
            Sets width of line path.
        **plot_kwargs
            Keyword arguments for the basemap `plot` method.
        
        Notes
        -----
        Formatting uses Basemap `plot` options. 
        Saves input options to `map_options` attribute. 
        
        Algorithm to compute the path coordinates of FOV 
        circle based on a formula from Taff, Celestial 
        mechanics.
        
        Returns
        -------
        None

        Examples
        --------

        Draw two sets of caps onto a globe, drawing one set 
        of caps using a numpy array, and another using a 
        tplot variable: 
    
        >>> import numpy as np
        >>> from pyspedas import store_data
        >>> arr_path_points = np.array([
        ...     (0,0),
        ...     (30,0),
        ...     (30,30),
        ...     (0,30),
        ...     (0,0),
        ... ])
        >>> tplot_path_points = "second_cap_set"
        >>> store_data(
        ...     name=tplot_path_points,
        ...     data = {
        ...         'x': [1,2,3,4,5],
        ...         'y': np.array([
        ...             (15,15),
        ...             (45,15),
        ...             (45,45),
        ...             (15,45),
        ...             (15,15),
        ...         ])
        ...     },
        ... )
        True
        >>> caps_coords = [arr_path_points,tplot_path_points]
        >>> tmap = Tplot_Map(override_defaults=True)
        >>> tmap.add_coastlines()
        >>> tmap.add_countries()
        >>> tmap.add_caps(coords=caps_coords,linestyle='dashed',linewidth=1)
        >>> tmap.show()  # doctest: +SKIP
        """
        from pyspedas import geodetic_correction as cotrans_geodetic_correction
        
        if color is not None:
            plot_kwargs.update({"color":color})
        if marker is not None:
            plot_kwargs.update({"marker":marker})
        if linestyle is not None:
            plot_kwargs.update({"linestyle":linestyle})
        if linewidth is not None:
            plot_kwargs.update({"linewidth":linewidth})
        if markersize is not None:
            plot_kwargs.update({"markersize":markersize})
        self.map_options["add_caps"].update(plot_kwargs)
        self._overwrite_params("add_caps")
        
        azi = np.arange(0,361)
        r_e = 6378.0 # Earth radius, in km
        z = 120.0 # altitude of emission, in km
        zeta = fov_angle # zenith angle (degrees)
        theta = np.rad2deg(np.arcsin((r_e/(r_e+z))*np.sin(np.deg2rad(zeta)))) # second angle of triangle
        alpha = zeta - theta
        surface_arclength = np.deg2rad(alpha)*r_e
    
        for coord_set in convert_coords_to_geod_lonlat_list(coords=coords,coord_type=coord_type,co_latitude=co_latitude,angle_meas=angle_meas):
            for i in np.arange(0,coord_set.shape[0]):
                coord = coord_set[i,:]
                
                alat = 90.0 - np.rad2deg(surface_arclength/r_e)
                alon = 180-azi
                latp = cotrans_geodetic_correction(lat_deg=coord[1],inverse=True) # coord[1]
                lonp = 180.0
                t0 = np.deg2rad(90.0-latp)
                t1 = np.deg2rad(90.0-alat)
                p0 = np.deg2rad(lonp)
                p1 = np.deg2rad(alon)
                zz = np.cos(t0)*np.cos(t1)+np.sin(t0)*np.sin(t1)*np.cos(p1-p0)
                zz[zz < -1.0] = -1.0
                zz[zz >  1.0] =  1.0
                xx=np.sin(t1)*np.sin(p1-p0)
                yy=np.sin(t0)*np.cos(t1)-np.cos(t0)*np.sin(t1)*np.cos(p1-p0)
                alat = r_e * np.arccos(zz)
                alon = alat
                alon = np.rad2deg(np.arctan(xx/yy))
                alat = 90.0 - np.rad2deg(alat/r_e)
                alon=coord[0]-alon
        
                x,y = self(alon,cotrans_geodetic_correction(alat))
                self.plot(x,y,**self.map_options.get("add_caps"))
        return

    # Helper functions:
    def _overwrite_params(self,map_plottype:str):
        param_opts = self.map_options.get(map_plottype)
        match map_plottype:
            case "basemap":
                self._params.basemap = param_opts
            case "drawmapboundary":
                self._params.drawmapboundary = param_opts
            case "fillcontinents":
                self._params.fillcontinents = param_opts
            case "drawcountries":
                self._params.add_countries = param_opts
            case "drawcoastlines":
                self._params.drawcoastlines = param_opts
            case "nightshade":
                self._params.nightshade = param_opts
            case "drawmeridians":
                self._params.drawmeridians = param_opts
            case "drawparallels":
                self._params.drawparallels = param_opts
            case "add_lineplot":
                self._params.add_lineplot = param_opts
            case "add_marker":
                self._params.add_marker = param_opts
            case "add_cap":
                self._params.add_cap = param_opts
        return

    def _convert_projection_params(self):
        updated_proj_params = dict()
        invalid_projection_params = dict()
        for proj_key, proj_params in self._projection_params.items():
            match proj_params:
                case 'corners only (no width/height)':
                    updated_proj_params[proj_key] = self._corners_latlon + self._corners_xy
                    invalid_projection_params[proj_key] = ["width","height"]
                case 'corners plus lat_ts (no width/height)':
                    updated_proj_params[proj_key] = self._corners_latlon + self._corners_xy + ["lat_ts"]
                    invalid_projection_params[proj_key] = ["width","height"]
                case 'lon_0,lat_0,k_0':
                    updated_proj_params[proj_key] = self._center + ["k_0"]
                    invalid_projection_params[proj_key] = []
                case 'lon_0,lat_0,lat_1,lat_2,lon_1,lon_2,no_rot,k_0':
                    updated_proj_params[proj_key] = self._center + self._center_1 + self._center_2 + ["no_rot","k_0"]
                    invalid_projection_params[proj_key] = []
                case 'corners only plus lat_ts (no width/height)':
                    updated_proj_params[proj_key] = self._corners_latlon + self._corners_xy + ["lat_ts"]
                    invalid_projection_params[proj_key] = ["width","height"]
                case 'lon_0,lat_0,lat_1,lat_2,k_0':
                    updated_proj_params[proj_key] = self._center + ["lat_1","lat_2","k_0"]
                    invalid_projection_params[proj_key] = []
                case 'lon_0,lat_0':
                    updated_proj_params[proj_key] = self._center
                    invalid_projection_params[proj_key] = []
                case 'bounding_lat,lon_0,lat_0,no corners or width/height':
                    updated_proj_params[proj_key] = self._center + ["boundinglat"]
                    invalid_projection_params[proj_key] = ["width","height"] + self._corners_latlon + self._corners_xy
                case 'lon_0,lat_0,lat_1,lat_2':
                    updated_proj_params[proj_key] = self._center + ["lat_1","lat_2"]
                    invalid_projection_params[proj_key] = []
                case 'lon_0,lat_0,lat_1':
                    updated_proj_params[proj_key] = self._center + ["lat_1"]
                    invalid_projection_params[proj_key] = []
                case 'lon_0,lat_0,lat_ts,k_0':
                    updated_proj_params[proj_key] = self._center + ["lat_ts","k_0"]
                    invalid_projection_params[proj_key] = []
                case 'lon_0,lat_0,llcrnrx,llcrnry,urcrnrx,urcrnry,no width/height':
                    updated_proj_params[proj_key] = self._center + self._corners_xy
                    invalid_projection_params[proj_key] = ["width","height"]
                case 'lon_0,satellite_height,llcrnrx,llcrnry,urcrnrx,urcrnry,no width/height':
                    updated_proj_params[proj_key] = ["lon_0","satellite_height"] + self._corners_xy
                    invalid_projection_params[proj_key] = ["width","height"]
                case 'lon_0,lat_0,no corners or width/height':
                    updated_proj_params[proj_key] = self._center
                    invalid_projection_params[proj_key] = ["width","height"] + self._corners_latlon + self._corners_xy
                case 'lon_0,o_lat_p,o_lon_p,corner lat/lon or corner x,y (no width/height)':
                    updated_proj_params[proj_key] = ["lon_0","o_lat_p","o_lon_p"] + self._corners_latlon + self._corners_xy
                    invalid_projection_params[proj_key] = ["width","height"]
        self._projection_params = updated_proj_params
        self._invalid_projection_params = invalid_projection_params
        return

    def _validate_basemap_params(self):
        this_projection = self.map_options["basemap"].get("projection")
        if this_projection is not None:
            if this_projection not in _projnames.keys():
                # check inverse projection
                _projnames_inverse = dict([(value, key) for key, value in _projnames.items()])
                if string.capwords(this_projection) in _projnames_inverse.keys():
                    self.map_options["basemap"]["projection"] = _projnames_inverse[string.capwords(this_projection)]
                    this_projection = self.map_options["basemap"].get("projection")
                else:
                    raise ValueError(f"Option 'projection' must be one of: {_projnames.keys()} or {_projnames_inverse.keys()}")

            # check arguments:
            this_projection_param_set = set(self._projection_params[this_projection])
            projection_param_diff = this_projection_param_set - set(self.map_options["basemap"].keys())
            projection_includes_corners_latlon = len(set(self._corners_latlon) - this_projection_param_set) == 0
            projection_includes_corners_xy = len(set(self._corners_xy) - this_projection_param_set) == 0
            projection_includes_all_corners = projection_includes_corners_latlon and projection_includes_corners_xy
            args_include_corners_latlon = len(set(self._corners_latlon) - set(self.map_options["basemap"].keys())) == 0
            args_include_corners_xy = len(set(self._corners_xy) - set(self.map_options["basemap"].keys())) == 0
            args_include_some_corners = args_include_corners_latlon or args_include_corners_xy
            args_include_invalid_params = len(set(self._invalid_projection_params[this_projection]) - self.map_options["basemap"].keys()) < len(set(self._invalid_projection_params[this_projection]))
            
            if len(projection_param_diff) > 0:
                if projection_includes_all_corners and not args_include_some_corners:
                    logging.warning("Basemap init is missing some corners arguments; visual may differ from expected.")
                else:
                    # Check if parameters are optional.
                    if this_projection_param_set - set(self.map_options['basemap'].keys()) != set(['llcrnrx','llcrnry','urcrnrx','urcrnry']):
                        logging.warning(f"Required arguments are missing: {this_projection_param_set - set(self.map_options['basemap'].keys())}" )
            if args_include_invalid_params:
                logging.warning(f"Basemap init contains invalid arguments: {set(self._invalid_projection_params[this_projection]) - self.map_options['basemap'].keys()}")
        return

    def _add_plot_feature(self,plot_type:str,plot_type_kwargs:dict = {}):
        self.map_options[plot_type].update(plot_type_kwargs)
        self._overwrite_params(plot_type)
        match plot_type:
            case "basemap":
                super().__init__(**self.map_options.get(plot_type))
            case "drawcoastlines":
                self.drawcoastlines(**self.map_options.get(plot_type))
            case "drawcountries":
                self.drawcountries(**self.map_options.get(plot_type))
            case "drawmapboundary":
                self.drawmapboundary(**self.map_options.get(plot_type))
            case "drawmeridians":
                self.drawmeridians(**self.map_options.get(plot_type))
            case "drawparallels":
                self.drawparallels(**self.map_options.get(plot_type))
            case "fillcontinents":
                self.fillcontinents(**self.map_options.get(plot_type))
            case "nightshade":
                self.nightshade(**self.map_options.get(plot_type))
        return

    @property
    def params(self):
        """The params property."""
        return self._params
    @params.setter
    def params(self, value):
        self._params = value
    @params.deleter
    def params(self):
        del self._params

    # End Tplot_Map class definition

def convert_coords_to_geod_lonlat_list(
        coords: str | np.ndarray | list[str] | list[np.ndarray],
        coord_type: str = 'geod_lat_lon',
        co_latitude: bool = False,
        angle_meas: str = 'degrees'
        ) -> list[np.ndarray]:
    """
    Takes tplot variable(s) or numpy array(s), and packages the data into arrays of longitude and latitude.
    
    For every tplot variable or numpy array, it parses the data, 
    assuming a given coordinate format, into an array 

    Takes tplot variable, list of tplot variables, numpy 
    array, or list of numpy arrays and packages position 
    data as a list of longitudes and latitudes (which 
    basemap expects).
    
    Parameters
    ----------
    coords : str or np.ndarray or list of str or list of np.ndarray
        Coordinate data to convert to geodetic coordinate data. If
        `coords` or each element of `coords` (if `coords` is a list)
        are of the string type, then attempts to load data from a tplot
        variable, using the string as the tplot variable name. Otherwise,
        attempts to transform the coordinate data directly. 
    coord_type : {'geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO'}
        Indicates how the input coordinates should be interpreted. The 
        first and second (and third, if applicable) components of the
        data will be interpreted as the following for each `coord_type`:
        geod_lat_lon : Geodetic latitude, Longitude
        geoc_lat_lon : Geocentric Latitude, Longitude
        geod_spherical : Radius, Geodetic Latitude, Longitude
        geoc_spherical : Radius, Geocentric Latitude, Longitude
        cart_GEO : X, Y, Z in ECEF coordinates

        Defaults to 'geod_lat_lon'
    co_latitude : bool, optional
        Indicates if input latitude is a co-latitude. Here,
        co-latitude is defined as angle between the position vector and
        axis of Earth's rotation. Default is False
    angle_meas : {'degrees', 'radians', 'arcminutes'}
        Indicates unit of measurement of input latitude and longitude 
        coordinates. Defaults to 'degrees' 
    
    Returns
    -------
    lonlat_data_list, list
        Two-dimensional Numpy arrays where the first 
        index corresponds to the record/observation, 
        and the second index corresponds to each 
        coordinate (longitude and geodetic latitude, 
        respectively). Longitude and latitude are
        reported in degrees.

    Notes
    -----
    This method is primarily used by the Tplot_Map
    plotting methods to parse the positional input 
    argument, so that they can accept tplot 
    variables or numpy arrays (or lists of either). 
    While it is generally unnecessary to call this 
    method on its own, it is provided for convenience
    when handling positional data of common formats.

    Examples
    --------
    
    Take a set of geocentric coordinates from a numpy
    array and tplot variable and convert them into 
    geodetic coordinates:

    >>> import numpy as np
    >>> from pyspedas import store_data
    >>> arr_path_points = np.array([
    ...     (0,0),
    ...     (30,0),
    ...     (30,30),
    ...     (0,30),
    ...     (0,0),
    ... ])
    >>> tplot_path_points = "second_set"
    >>> store_data(
    ...     name=tplot_path_points,
    ...     data = {
    ...         'x': [1,2,3,4,5],
    ...         'y': np.array([
    ...             (15,15),
    ...             (45,15),
    ...             (45,45),
    ...             (15,45),
    ...             (15,15),
    ...         ])
    ...     },
    ... )
    True
    >>> coords = [arr_path_points,tplot_path_points]
    >>> print(convert_coords_to_geod_lonlat_list(coords=coords,coord_type="geoc_lat_lon"))  # doctest: +NORMALIZE_WHITESPACE
    [array([[ 0.        ,  0.        ],
       [ 0.        , 30.16692229],
       [30.        , 30.16692229],
       [30.        ,  0.        ],
       [ 0.        ,  0.        ]]), array([[15.        , 15.09649162],
       [15.        , 45.19242142],
       [45.        , 45.19242142],
       [45.        , 15.09649162],
       [15.        , 15.09649162]])]
    """
    from pyspedas import get_data
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar
    from pyspedas import geodetic_correction as cotrans_geodetic_correction

    if coord_type not in ['geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO']:
        raise ValueError("coord_type must be one of: 'geod_lat_lon','geoc_lat_lon','geod_spherical','geoc_spherical','cart_GEO'")
    coord_type_in = coord_type
    # Create list of coordinate data to parse:
    coords_list = []
    if isinstance(coords,list):
        coords_list = coords
    else:
        coords_list = [coords]

    geod_lonlat_list = []
    for coord_obj in coords_list:
        coord_type = coord_type_in
        # Initially assume list contains arrays:
        coord_data = coord_obj
        if isinstance(coord_obj,str):
            # If list is of tplot variables; load data into arrays instead:
            coord_data = (get_data(coord_obj)).y

        ndim = len(coord_data.shape)
        if coord_data.size < 2:
            raise ValueError(f"Positional data must have at least 2 elements; got {len(coord_data)}")
        if ndim == 1:
            logging.warning("Received one dimensional data; assuming single record of coordinates...")
            coord_data = np.array([coord_data])
            ndim = len(coord_data.shape)
        
        if ndim != 2:
            raise ValueError(f"Positional data must be two dimensional; got: {ndim}")
        elif coord_data.shape[1] not in [2,3]:
            raise ValueError(f"Second dimension of data must be of length 2 or 3; got {coord_data.shape[1]}")
        else:
            req_col_l = 3
            if coord_type in ['geod_lat_lon','geoc_lat_lon']:
                req_col_l = 2
            if coord_data.shape[1] != req_col_l:
                raise ValueError(f"Coordinate type {coord_type} requires second dimension to be length {req_col_l}; instead, was {coord_data.shape[1]}")

            if coord_type == 'cart_GEO':
                # X, Y, Z in ECEF coordinates
                coord_data = cotrans_cartesian2geodeticpolar(data=coord_data)
                coord_type = 'geod_spherical'
            
            coord_data_lon = coord_data[:,-1]
            if coord_data.shape[1] == 3:
                coord_data_lat = coord_data[:,1]
            else:
                coord_data_lat = coord_data[:,0]

            if angle_meas != 'degrees':
                if angle_meas not in ["radians","arcminutes"]:
                    raise ValueError("Argument angle_meas must be one of: 'degrees', 'radians', 'arcminutes'")
                if angle_meas == "radians":
                    coord_data_lon = np.rad2deg(coord_data_lon)
                    coord_data_lat = np.rad2deg(coord_data_lat)
                else:
                    # Data is in arcminutes
                    coord_data_lon = coord_data_lon / 60
                    coord_data_lat = coord_data_lat / 60

            if co_latitude:
                coord_data_lat = 90-coord_data_lat
            
            if coord_type in ['geoc_lat_lon','geoc_spherical']:
                coord_data_lat_geoc = coord_data_lat
            else:
                coord_data_lat_geoc = cotrans_geodetic_correction(coord_data_lat,inverse=True)
            
            coord_data_lat_geod = cotrans_geodetic_correction(coord_data_lat_geoc)

            geod_lonlat_list.append( np.array([ coord_data_lon , coord_data_lat_geod ]).transpose() )
    return geod_lonlat_list

def tplot_map(
        tmap:   Tplot_Map | None = None, 
        projection:   str | None = None,
        center:     tuple | None = None,
        range:      tuple | None = None,
        land_color:   str | None = None,
        water_color:  str | None = None,
        view:         str | None = None,
        option_dict: dict | None = None,
        override_defaults : bool = False,
        ax:          Axes | None = None, 
        range_is_xy: bool = False,
        display:bool = False, 
        **basemap_kwargs) -> Tplot_Map:
    # TODO: make sure coordinates are interpreted as lon, lat, not the other way around
    """
    Create a Tplot_Map object, with convenient initialization options
    
    Parameters
    ----------
    tmap : Tplot_Map, optional
        Existing Tplot_Map object to use as the basis for the 
        created Tplot_Map object. If none are provided, creates
        new Tplot_Map object from scratch.
    projection : str, optional
        Basemap projection parameter
    center : tuple of floats, optional
        Shortcut for assigning map center, where
        the tuple has the form: (lon_0, lat_0)
    range : tuple, optional
        Shortcut for specifying the corners of the map.
        If `range_is_xy` is False, takes the form:
        (llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat)
        If `range_is_xy` is True, takes the form:
        (llcrnrx, llcrnry, urcrnrx, urcrnry)
    land_color : string, optional
        Specifies color for land masses
    water_color : string, optional
        Specifies color for oceans and lakes
    view : str or None, {'North America', 'Northern Europe', 'North Polar', 'South Polar', None}
        Presets for map center position. Defaults to None.
    ax : Axes, optional
        Existing Axes object to which Tplot_Map plots will be 
        attached. If none are provided, creates one.
    option_dict : dict, optional
        Modifies `map_options` (see `Tplot_Map`) before plotting. 
        The `option_dict` must have a similar format to `map_options`. 
    override_defaults : bool, optional
        If `override_defaults` is True, the default plot options 
        in `map_options` (see `Tplot_Map`) will be completely 
        replaced by the plot options in `option_dict`. Otherwise, 
        options for a given plot type can only be changed if those options 
        are specified in `option_dict`. Set to False by default.
    range_is_xy : bool, optional
        Indicates whether range should be interpreted
        as map coordinates or not. Defaults to False.
    display : bool, optional
        Indicates whether or not the map object should be
        shown after it has been created. Defaults to False.
    **basemap_kwargs
        Other keyword arguments for the Basemap class constructor.

    Returns
    -------
    Tplot_Map
        Created Tplot_Map object

    Examples
    --------
    
    Create default map and display plot options:

    >>> tmap = tplot_map()
    >>> tmap.print_map_options()  # doctest: +NORMALIZE_WHITESPACE
    Current Map Options:
    {
     'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0, 'ax': <Axes: >},
     'drawcoastlines' : {'linewidth': 0.25, 'ax': <Axes: >},
     'drawcountries' : {'linewidth': 0.25, 'ax': <Axes: >},
     'fillcontinents' : {'color': 'white', 'lake_color': 'white', 'ax': <Axes: >},
     'drawmapboundary' : {'fill_color': 'white', 'ax': <Axes: >},
     'drawmeridians' : {'meridians': array([  0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100, 110, 120,
        130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250,
        260, 270, 280, 290, 300, 310, 320, 330, 340, 350]), 'ax': <Axes: >},
     'drawparallels' : {'circles': array([-90, -80, -70, -60, -50, -40, -30, -20, -10,   0,  10,  20,  30,
            40,  50,  60,  70,  80]), 'ax': <Axes: >},
     'nightshade' : {},
     'add_paths' : {},
     'add_markers' : {'color': 'r', 'marker': 'd', 'ax': <Axes: >},
     'add_caps' : {},
    }

    Create map with mercator projection, centered on Northern Europe:

    >>> tmap = tplot_map(view="Northern Europe",projection="mercator",range=(-40,10,130,70),display=True)  # doctest: +SKIP

    Create a globe centered over North America where the oceans are blue and the land is green:

    >>> tmap = tplot_map(view="North America",water_color='darkblue',land_color='darkgreen',display=True)  # doctest: +SKIP
    
    Create blank Tplot_Map object (useful if default plot types are not 
    desired--still requires Basemap params):
    
    >>> tmap = tplot_map(override_defaults=True)
    >>> tmap.print_map_options()
    Current Map Options:
    {
     'basemap' : {'projection': 'ortho', 'lat_0': 0, 'lon_0': 0, 'ax': <Axes: >},
     'drawcoastlines' : {},
     'drawcountries' : {},
     'fillcontinents' : {},
     'drawmapboundary' : {},
     'drawmeridians' : {},
     'drawparallels' : {},
     'nightshade' : {},
     'add_paths' : {},
     'add_markers' : {},
     'add_caps' : {},
    }
    """
    
    if tmap is not None:
        if ax is None:
            ax=tmap.ax
        if option_dict is None:
            option_dict=tmap.map_options
        if view is None:
            view = tmap.view
    
    if ax is None:
        # create axes object if none is passed:
        fig, ax = plt.subplots()

    if basemap_kwargs is None:
        basemap_kwargs = dict()

    if isinstance(projection,str):
        basemap_kwargs.update({"projection":projection})
    
    if isinstance(center,tuple):
        if len(center) != 2:
            raise ValueError("Option 'center' must be tuple of length 2")
        else:
            basemap_kwargs.update({"lon_0":center[0],"lat_0":center[1]})

    if isinstance(range,tuple):
        if len(range) != 4:
            raise ValueError("Option 'range' must be tuple of length 4")
        else:
            if range_is_xy:
                basemap_kwargs.update({
                    "llcrnry":range[1],
                    "llcrnrx":range[0],
                    "urcrnry":range[3],
                    "urcrnrx":range[2],})
            else:
                basemap_kwargs.update({
                    "llcrnrlat":range[1],
                    "llcrnrlon":range[0],
                    "urcrnrlat":range[3],
                    "urcrnrlon":range[2],})
    
    if land_color is not None or water_color is not None:
        if option_dict is None:
            option_dict=dict()
        if option_dict.get("fillcontinents") is None:
            option_dict["fillcontinents"] = dict()
        if land_color is not None:
            option_dict["fillcontinents"].update({"color":land_color})
        if water_color is not None:
            option_dict["fillcontinents"].update({"lake_color":water_color})
            if option_dict.get("drawmapboundary") is None:
                option_dict["drawmapboundary"] = dict()
            option_dict["drawmapboundary"].update({"fill_color":water_color})

    tmap = Tplot_Map(
        view=view,
        ax=ax,
        option_dict=option_dict,
        override_defaults=override_defaults,
        **basemap_kwargs)
    
    if display:
        tmap.show()
    
    return tmap

# Deprecated methods:
def add_tracks(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **tracks_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    logging.warning('The "add_tracks()" method is deprecated. Please use "Tplot_Map.add_tracks()" instead.')
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_paths(coords=coords,**tracks_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_markers(coords: str | np.ndarray | list[np.ndarray], tmap:Tplot_Map | None = None, display:bool = False, **markers_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    logging.warning('The "add_markers()" method is deprecated. Please use "Tplot_Map.add_markers()" instead.')
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_markers(coords=coords, **markers_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_station_fovs(coords: str | np.ndarray | list[np.ndarray], fov_angle = 80.0, tmap:Tplot_Map | None = None, display:bool = False, **station_fov_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    logging.warning('The "add_station_fovs()" method is deprecated. Please use "Tplot_Map.add_station_fovs()" instead.')
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_caps(coords=coords, fov_angle = fov_angle, **station_fov_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def geodetic_correction(lat_deg,f=(1/298.26)):
    """
    Obsolete, deprecated (moved to separate script)

    Convert geocentric latitude to geodetic latitude using squashing factor f
    """
    # TODO: revise
    logging.warning('The "geodetic_correction()" method is deprecated. Please use "geodetic_correction" in the "cotrans" package instead.')
    from pyspedas import geodetic_correction as cotrans_geodetic_correction
    return cotrans_geodetic_correction(lat_deg=lat_deg,flattening=f)

def cartesian2geodeticpolar(data: str | np.ndarray) -> np.ndarray:
    """
    Obsolete, deprecated (moved to separate script)

    Get positional data from tplot variable, then convert data coordinates to 
    geodetic polar coordinates
    """
    logging.warning('The "cartesian2geodeticpolar()" method is deprecated. Please use "cartesian2geodeticpolar" in the "cotrans" package instead.')
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar
    return cotrans_cartesian2geodeticpolar(data=data)

def tvar_to_geodeticpolar(tvar:str, in_coord_str:str='gsm'):
    """
    Obsolete, deprecated

    Take a tplot variable of arbitrary coordinate system and convert to geodetic 
    polar
    """
    logging.warning('The "tvar_to_geodeticpolar()" method is deprecated. Please use "convert_coords_to_geod_lonlat_list" instead.')
    from pyspedas import cotrans, get_data
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar
    tvar_geo = tvar + "_geo"
    cotrans(name_in=tvar,name_out=tvar_geo,coord_in=in_coord_str,coord_out="geo")
    # convert Cartesian GEO/ECEF data to geodetic polar:
    geo_data = get_data(tvar_geo)
    data_geod_polar = cotrans_cartesian2geodeticpolar(data=geo_data.y)
    return data_geod_polar
