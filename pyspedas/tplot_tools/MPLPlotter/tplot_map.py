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

# TODO: need way to handle when argument of "None" is intentional and affects map.
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
        # TODO: we can't keep track of every additional plot being made; we can only provide default 
        #       options for an initial map to be drawn
        # TODO: include legend?
            
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
            self.map_options.update(map_options)
        self.plot_order = self.map_options.keys()
        if view != "":
            self.modify_view(new_view=view)
        self.build_map()

    def build_map(self):
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
        self.build_map()
        plt.show()
        return

    def modify_view(self,new_view:str):
        # TODO: update coordinates to reasonable values
        if isinstance(self.map_options["basemap"],dict):
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

    # TODO: add is_lat, is_lon bools? Add checks
    # TODO: check ranges of latitude and longitude values
    # TODO: should this also accept lists where each element is a number (not str/ndarray)?
    def _parse_input_coords(
            self,coords: str | np.ndarray | list[str] | list[np.ndarray],
            is_lat: bool = False, is_lon: bool = False) -> list[np.ndarray]:
        if not isinstance(coords,list):
            coords = [coords]
        coord_data_list = []
        for coord_obj in coords:
            coord_data = coord_obj
            if isinstance(coord_obj, str):
                # load data from tplot:
                coord_data = get_data(coord_obj)
            # TODO: one of the dimensions MUST be 2; verify. UNLESS is_lat or is_lon is set; then one of the dimensions must be size 0 or 1
            coord_data_list.append(coord_data)
        return coord_data_list

    def _add_linepath(self, x, y,**plot_linepath_kwargs):
        self._params.add_linepath.update(plot_linepath_kwargs)
        self.plot(x,y,**self._params.add_linepath)
        return
    
    def _add_marker(self, x, y, **plot_marker__kwargs):
        self._params.add_marker.update(plot_marker__kwargs)
        self.plot(x,y,**self._params.add_marker)
        return

    def _make_circular_caps():
        return

    def _add_cap(self, x, y,**plot_cap_kwargs):
        self._params.add_cap.update(plot_cap_kwargs)
        self.plot(x,y,**self._params.add_cap)
        return

    # TODO: what if we want to draw multiple sets of meridians? With different options?
    def add_meridians(
            self,lon_vals: str | np.ndarray,
            linestyle: str | None = None,
            linecolor: str | None = None,
            north_pole_loc:tuple=(90,0),
            **drawmeridians_kwargs):
        
        lon_vals = self._parse_input_coords(coords = lon_vals, is_lon=True)
        # TODO: verify args are valid drawmeridians options
        if not isinstance(self.map_options.get("drawmeridians"),dict):
            self.map_options["drawmeridians"] = dict()
        self.map_options["drawmeridians"].update({
            "linestyle":linestyle,
            "linecolor":linecolor
        })
        self.map_options["drawmeridians"].update(drawmeridians_kwargs)
        # TODO: if first element in north_pole_loc is not 90, rotate meridian values. Try rotpole? Or manually rotating the coordinates?

        self.build_map()
        return

    def add_parallels(
            self,lat_vals: str | np.ndarray,
            linestyle: str | None = None,
            linecolor: str | None = None,
            north_pole_loc:tuple=(90,0),
            **drawparallels_kwargs):
        return

    def add_track(self,coords,color,linestyle,**plot_kwargs):
        for coord_set in coords:
            # expects input coordinates in form of radius, longitude, latitude
            x,y = tmap(coord_set[:,2],coord_set[:,1])
            tmap.add_linepath(x,y,**tracks_plot_kwargs)
        return

    def add_markers(self,coords,marker_symbol,marker_color,**scatter_kwargs):
        for coord in coords:
            # expects input coordinates in form of radius, longitude, latitude
            x,y = tmap(coord[2],coord[1])
            # TODO: do we need to use scatter or plot (with line options turned off?)
            tmap.add_marker(x,y,**markers_plot_kwargs)
        return

    def add_station_fov(self,coords,fov_angle = 80.0,fov_radius="",linestyle="",fill_color="",**station_fov_plot_kwargs):
        # TODO: need to determine plot option for station FOV. 
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
        return

    def trace_tvars_to_tmap(
        tmap:Tplot_Map | None,
        tvar:list[str] | str,
        display:bool = False,
        fig_fp:str="") -> Tplot_Map:

        tmap = tplot_map(tmap=tmap)
        
        for tvar_name in tvar:
            # Compute traces:
            computed_trace = _trace_tvars_to_foottracks(tvar_to_trace = tvar_name, model_str = "t89", endpoint = "ionosphere-north")
            tmap = add_tracks(tmap=tmap, coords=computed_trace[0], label = tvar_name)
        if display:
            tmap.show()
        if fig_fp != "":
            plt.savefig(fig_fp)
        return tmap

def _trace_tvars_to_foottracks(tvar_to_trace:list[str] | str, **ttrace2endpoint_kwargs) -> list:
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

# TODO: Basemap can accept axes object; tplot_map can accept existing axes object, or create one if axes object does not already exist.
def tplot_map(
        projection:   str | None = None,
        center:     tuple | None = None,
        range:      tuple | None = None,
        land_color:   str | None = None,
        ocean_color:  str | None = None,
        view = "",
        display:bool = False,
        map_options: dict | None = None, 
        **basemap_kwargs) -> Tplot_Map:
    """
    Creates a tplot map object
    
    Display a map, specifying the projection, lat_long ranges, map dimensions, colors, etc

    map_options is a dict containing options for every intended plot type (including initial Basemap), and supercedes input options. 
    """
    if map_options is None:
        # TODO: verify args are valid basemap options
        map_options = {
            "basemap":{    
                "projection"  : projection,
                "center"      : center,
                "range"       : range,
                "land_color"  : land_color,
                "ocean_color" : ocean_color}}
        if isinstance(map_options["basemap"],dict):
            map_options["basemap"].update(basemap_kwargs)
            if all(map_options["basemap"].values()) == None:
                map_options = None
    tmap = Tplot_Map(view=view,map_options=map_options)
    if display:
        tmap.show()
    return tmap

# TODO: remove
if __name__ == "__main__":
    """
    # Display a map, specifying the projection, lat_long ranges, map dimensions, colors, etc
    map_obj = tplot_map(projection='Mercator', center=something, range=something_else, land_color=land_color, ocean_color=ocean_color)

    # Plot the meridians, with options for line styles, colors, which values to plot)
    tplot_map_add_meridians(map_obj, lat_values=list_of_lats, long_values=list_of_longitudes, linestyle, linecolor)

    # Add the day/night boundary
    tplot_map_add_terminator(map_obj, alpha=alpha, ....).  # I don't recall exactly how this works in basemap but the feature exists

    # Add ground tracks
    tplot_map_add_track(map_obj, themis_a_long_lat, color=themis_a_color, linestyle=linestyle)
    tplot_map_add_track(map_obj, themis_d_long_lat, color=themis_d_color, linestyle=linestyle)

    # Add ground station markers
    tplot_map_add_markers(map_obj, marker_latitude_list, marker_longitude_list, marker_symbol, marker_color)

    # Add field of view circles for each ground station
    # Hopefully there are convenience features to plot the circles projected appropriately without generating our own long-lat traces for each FOV
    tplot_map_add_station_fov(map_obj, marker_latitude_list, marker_longitud_list, fov_radius, linestyle)

    # Display the map after adding all the elements
    map_obj.show()
    """
    map_obj = tplot_map()
    map_obj.show()
    print("Done!")