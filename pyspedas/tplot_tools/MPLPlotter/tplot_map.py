# TODO: update documentation
"""
Take a tplot variable containing positional data, 
trace magnetic field lines to the north ionosphere, south ionosphere, or equator,
then map those points to a basemap
"""
from pyspedas import get_data, ttrace2endpoint, geodetic_correction, cartesian2geodeticpolar
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

# TODO: what to do about multiple applications of a certain type of plot (e.g. add_markers, then add_markers)? How to save params?
# TODO: add auroral oval plot
class Tplot_Map():
    """
    Object containing tplot_map information, with the
    following attributes:
    * map: Basemap object
    * map_options: arguments for various types of plots
        which can be applied to the map attribute. If
        the value for a map_options key is set to 'None',
        then that type of plot won't be made when the map
        is built.
    """
    def __init__(self,view: str = "",map_options: dict | None = None):
        """
        view overwrites lat_0 and lon_0 in "basemap" map_options
        """
        self.date = dt.datetime.now()
        self.map = Basemap()
        # TODO: default params should be None for nightshade, linepath, add_marker, add_cap, drawmeridians, and drawparallels
        # TODO: need magnetic meridians and parallels
        # TODO: labels for geographic and magnetic meridians and parallels?
        self.map_options = {
            "basemap"         : {"projection":"ortho","lat_0":0,"lon_0":0},
            "drawmapboundary" : {"fill_color":"white"},
            "fillcontinents"  : {"color":"white","lake_color":"white"},
            "drawcoastlines"  : {"linewidth":0.25},
            "drawmeridians"   : {"meridians":np.arange(0,360,10)},
            "drawparallels"   : {"circles":np.arange(-90,90,10)},
            "nightshade"      : None, # {"date":dt.datetime.now(),"alpha":0.5}
            "add_linepath"    : None, # {}
            "add_marker"      : None, # {"color":"r","linestyle":"","marker":"d"}
            "add_cap"         : None, # {"color":"m"}
        }
        if map_options is not None:
            self.map_options = map_options
        self.plot_order = self.map_options.keys()
        if view != "":
            self.modify_view(new_view=view)
        self.build_map()

    def build_map(self):
        # TODO: should run through self.params keys, match key to action
        for plot_type in self.plot_order:
            plot_opts = self.map_options.get(plot_type)
            if plot_opts is not None:
                if not isinstance(plot_opts,dict):
                    # TODO test:
                    raise TypeError(f"Value for {plot_type} map_option must be dict; instead, was {plot_opts.type}")
                match plot_type:
                    case "basemap": 
                        self.map = Basemap(**plot_opts)
                    case "drawmapboundary":
                        self.map.drawmapboundary(**plot_opts)
                    case "fillcontinents":
                        self.map.fillcontinents(**plot_opts)
                    case "drawcoastlines":
                        self.map.drawcoastlines(**plot_opts)
                    case "drawmeridians":
                        self.map.drawmeridians(**plot_opts)
                    case "drawparallels":
                        self.map.drawparallels(**plot_opts)
                    case "nightshade":
                        self.map.nightshade(**plot_opts)

        self.map = Basemap(**self.map_options["basemap"])
        return
    
    def show(self): 
        # TODO, include legend?
        self.build_map()
        plt.show()
        return

    def modify_view(self,new_view:str):
        # TODO: update coordinates to reasonable values
        if self.map_options["basemap"] is not None:
            match new_view:
                case "North America":
                    self.map_options["basemap"].update({"lat_0":0,"lon_0":0})
                case "Northern Europe":
                    self.map_options["basemap"].update({"lat_0":0,"lon_0":0})
                case "North Polar":
                    self.map_options["basemap"].update({"lat_0":0,"lon_0":0})
                case "South Polar":
                    self.map_options["basemap"].update({"lat_0":0,"lon_0":0})
        self.build_map()
        return
    
    def modify_plot_order(self,new_plot_order: list[str]):
        self.plot_order = new_plot_order
        return

    def _parse_input_coords(self,coords: str | np.ndarray | list[str] | list[np.ndarray]) -> list[np.ndarray]:
        if not isinstance(coords,list):
            coords = [coords]
        coord_data_list = []
        for coord_obj in coords:
            coord_data = coord_obj
            if isinstance(coord_obj, str):
                # load data from tplot:
                coord_data = get_data(coord_obj)
            # TODO: one of the dimensions MUST be 2; verify
            coord_data_list.append(coord_data)
        return coord_data_list

    # tplot_map_add_meridians(map_obj, lat_values=list_of_lats, long_values=list_of_longitudes, linestyle, linecolor)
    # tplot_map_add_terminator(map_obj, alpha=alpha, ....)
    # tplot_map_add_track(map_obj, themis_a_long_lat, color=themis_a_color, linestyle=linestyle)
    # tplot_map_add_track(map_obj, themis_d_long_lat, color=themis_d_color, linestyle=linestyle)
    # tplot_map_add_markers(map_obj, marker_latitude_list, marker_longitude_list, marker_symbol, marker_color)
    # tplot_map_add_station_fov(map_obj, marker_latitude_list, marker_longitud_list, fov_radius, linestyle)

    

    def add_linepath(self, x, y,**plot_linepath_kwargs):
        self._params.add_linepath.update(plot_linepath_kwargs)
        self.plot(x,y,**self._params.add_linepath)
        return
    
    def add_marker(self, x, y, **plot_marker__kwargs):
        self._params.add_marker.update(plot_marker__kwargs)
        self.plot(x,y,**self._params.add_marker)
        return

    def add_cap(self, x, y,**plot_cap_kwargs):
        self._params.add_cap.update(plot_cap_kwargs)
        self.plot(x,y,**self._params.add_cap)
        return

def _make_circular_caps():
    return
def _trace_tvars_to_foottracks():
    return

def tplot_map(
        projection:str = "Mercator",
        center = (0,0),
        range = (0,0,0,0),
        land_color = "White",
        ocean_color = "White",
        view = "",
        display:bool = False,
        params_dict: dict | None = None, 
        **basemap_kwargs) -> Tplot_Map:
    """
    Creates a tplot map object
    
    Display a map, specifying the projection, lat_long ranges, map dimensions, colors, etc
    """
    # TODO: verify args are valid basemap options
    params = {"basemap":{}}
    params["basemap"]["projection"]  = projection,
    params["basemap"]["center"]      = center,
    params["basemap"]["range"]       = range,
    params["basemap"]["land_color"]  = land_color,
    params["basemap"]["ocean_color"] = ocean_color,
    if params_dict is not None:
        params = params_dict
    params["basemap"].update(basemap_kwargs)
    tmap = Tplot_Map(view=view,params=params)
    if display:
        tmap.show()
    return tmap


# TODO: move add_markers, tplot_trace_tvars_to_tmap, add_station_fovs to Tplot_Map object

def add_tracks(coords: str | np.ndarray | list[np.ndarray], tmap:Tplot_Map | None = None, display:bool = False, **tracks_plot_kwargs) -> Tplot_Map:
    if not isinstance(coords,list):
        if isinstance(coords,str):
            tvar_data = get_data(coords)
            coords = tvar_data.y
        coords = [coords]

    for coord_set in coords:
        # expects input coordinates in form of radius, longitude, latitude
        x,y = tmap(coord_set[:,2],coord_set[:,1])
        tmap.add_linepath(x,y,**tracks_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_markers(coords: str | np.ndarray | list[np.ndarray], tmap:Tplot_Map | None = None, display:bool = False, **markers_plot_kwargs) -> Tplot_Map:
    _tmap_init()
    if not isinstance(coords,list):
        if isinstance(coords,str):
            tvar_data = get_data(coords)
            coords = tvar_data.y
        coords = [coords]

    for coord in coords:
        # expects input coordinates in form of radius, longitude, latitude
        x,y = tmap(coord[2],coord[1])
        # TODO: do we need to use scatter or plot (with line options turned off?)
        tmap.add_marker(x,y,**markers_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_station_fovs(coords: str | np.ndarray | list[np.ndarray], fov_angle = 80.0, tmap:Tplot_Map | None = None, display:bool = False, **station_fov_plot_kwargs) -> Tplot_Map:
    _tmap_init()
    if not isinstance(coords,list):
        if isinstance(coords,str):
            tvar_data = get_data(coords)
            coords = tvar_data.y
        coords = [coords]

    azi = np.arange(0,361)
    r_e = 6378.0 # Earth radius, in km
    z = 120.0 # altitude of emission, in km
    zeta = fov_angle # zenith angle (degrees?)
    theta = np.rad2deg(np.arcsin((r_e/(r_e+z))*np.sin(np.deg2rad(zeta)))) # second angle of triangle
    alpha = zeta - theta
    surface_arclength = np.deg2rad(alpha)*r_e

    for coord in coords:
        alat = 90.0 - np.rad2deg(surface_arclength/r_e)
        alon = 180-azi
        latp = coord[1]
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
        alon=coord[2]-alon

        x,y = tmap(alon,geodetic_correction(alat))
        tmap.add_cap(x,y,**station_fov_plot_kwargs)
    if display:
        tmap.show()
    return tmap


def tvar_to_foottracks(tvar_to_trace:list[str] | str, **ttrace2endpoint_kwargs) -> list: 
    """
    Take one or more tplot variable names, trace to an endpoint, and compute 
    geodetic polar foottracks from tplot variable positional data
    """
    if isinstance(tvar_to_trace,str):
        tvar_to_trace = [tvar_to_trace]
    foot_name_list = []
    for tvar in tvar_to_trace:
        footname_str = tvar
        tracename_str = tvar + "_trace"
        if ttrace2endpoint_kwargs.get("endpoint") is None:
            ttrace2endpoint_kwargs["endpoint"] = "ionosphere-north"
        match ttrace2endpoint_kwargs.get("endpoint"):
            case "ionosphere-north": 
                footname_str_pre="i"
                footname_str_suf="_n"
                tracename_str_part="_iono_n_"
            case "ionosphere-south":
                footname_str_pre="i"
                footname_str_suf="_s"
                tracename_str_part="_iono_s_"
            case "equator":
                footname_str_pre="eq_"
                footname_str_suf=""
                tracename_str_part="_equ"
        if ttrace2endpoint_kwargs.get("model_str") is None:
            ttrace2endpoint_kwargs["model_str"] = "t89"
        footname_str += ttrace2endpoint_kwargs["model_str"]
        footname_str += footname_str_pre + "foot" + footname_str_suf
        tracename_str += tracename_str_part + ttrace2endpoint_kwargs["model_str"]
        ttrace2endpoint(
            tvar=tvar,
            foot_name=footname_str, 
            foot_out_coord="GEO",
            trace_name=tracename_str,
            km=True,
            **ttrace2endpoint_kwargs)
        # compute geodetic polar foottracks from tplot variable positional data
        geo_data = get_data(footname_str)
        data_geod_polar = cartesian2geodeticpolar(data=geo_data.y)
        foot_name_list.append(data_geod_polar)
    return foot_name_list

def tplot_trace_tvars_to_tmap(
        tmap:Tplot_Map | None,
        tvar:list[str] | str,
        display:bool = False,
        fig_fp:str="") -> Tplot_Map:
    tmap = tplot_map(tmap=tmap)
    
    for tvar_name in tvar:
        # Compute traces:
        computed_trace = tvar_to_foottracks(tvar_to_trace = tvar_name, model_str = "t89", endpoint = "ionosphere-north")
        tmap = add_tracks(tmap=tmap, coords=computed_trace[0], label = tvar_name)
    if display:
        tmap.show()
    if fig_fp != "":
        plt.savefig(fig_fp)
    return tmap
