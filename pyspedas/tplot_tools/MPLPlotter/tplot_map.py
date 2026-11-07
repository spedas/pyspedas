"""
Take a tplot variable containing positional data, 
trace magnetic field lines to the north ionosphere, south ionosphere, or equator,
then map those points to a basemap
"""




from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import datetime as dt

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

# TODO: add auroral oval plot
class Tplot_Map(Basemap):
    """
    A Tplot_Map object which inherits from Basemap,
    but with attributes containing plotting function 
    parameters, initialized to defaults.

    Each plotting function parameter (stored in the 
    Tplot_Map_Param_Set object) is a dictionary which 
    is expanded by the corresponding function as kwargs.

    The Tplot_Map.build_map() function makes the function 
    calls in-order to ensure that the base map is drawn 
    correctly (but does re-plot any traces/markers 
    added manually). 

    Usage:
    >> tmap = Tplot_Map()
    >> tmap
    <__main__.Tplot_Map object at 0x000002A3E931AF20>
    >> tmap.params
    <__main__.Tplot_Map_Param_Set object at 0x000002A3E9318400>
    >> tmap.params.fillcontinents
    {'color': 'palegreen', 'lake_color': 'lightskyblue'}
    >> tmap.params.fillcontinents['color'] = 'red'
    >> tmap.params.fillcontinents
    {'color': 'red', 'lake_color': 'lightskyblue'}
    >> tmap.params.fillcontinents = {'color':'green'}
    >> tmap.params.fillcontinents
    {'color':'green'}
    """
    def __init__(
            self, 
            view:         str | None = None, 
            ax:          Axes | None = None, 
            option_dict: dict | None = None, 
            **basemap_kwargs):
        
        self._params = Tplot_Map_Param_Set()
        self._params.basemap         = {"projection":"ortho","lat_0":0,"lon_0":0}
        self._params.drawmapboundary = {"fill_color":"white"} #{"fill_color":"lightskyblue"}
        self._params.fillcontinents  = {"color":"white","lake_color":"white"} #{"color":"palegreen","lake_color":"lightskyblue"}
        self._params.drawcoastlines  = {"linewidth":0.25}
        self._params.nightshade      = {"date":dt.datetime.now(),"alpha":0.5}
        self._params.add_linepath    = dict()#{"color":"m"}
        self._params.add_marker      = {"color":"r","linestyle":"","marker":"d"}
        self._params.add_cap         = {"color":"m"}
        # TODO: make meridians into magnetic coordinates
        self._params.drawmeridians   = {"meridians":np.arange(0,360,10)}
        self._params.drawparallels   = {"circles":np.arange(-90,90,10)}

        self.default_map_options = {
            "basemap":self._params.basemap,
            "drawmapboundary":self._params.drawmapboundary,
            "fillcontinents":self._params.fillcontinents,
            "drawcoastlines":self._params.drawcoastlines,
            "nightshade":self._params.nightshade,
            "add_linepath":self._params.add_linepath,
            "add_marker":self._params.add_marker,
            "add_cap":self._params.add_cap,
        }

        self._params.basemap.update(basemap_kwargs)
        self._params.basemap["ax"]=ax

        # TODO: need to update position values to suitable locations
        if view is not None:
            self.view = view
            match self.view:
                case "North America":
                    option_dict["basemap"].update({"lat_0":0,"lon_0":0})
                case "Northern Europe":
                    option_dict["basemap"].update({"lat_0":0,"lon_0":0})
                case "North Polar":
                    option_dict["basemap"].update({"lat_0":0,"lon_0":0})
                case "South Polar":
                    option_dict["basemap"].update({"lat_0":0,"lon_0":0})

        if option_dict is not None:
            for map_plottype,plot_options in option_dict.items():
                match map_plottype:
                    case "basemap":
                        self._params.basemap.update(plot_options)
                        self.default_map_options["basemap"].update(plot_options)
                    case "drawmapboundary":
                        self._params.drawmapboundary.update(plot_options)
                        self.default_map_options["drawmapboundary"].update(plot_options)
                    case "fillcontinents":
                        self._params.fillcontinents.update(plot_options)
                        self.default_map_options["fillcontinents"].update(plot_options)
                    case "drawcoastlines":
                        self._params.drawcoastlines.update(plot_options)
                        self.default_map_options["drawcoastlines"].update(plot_options)
                    case "nightshade":
                        self._params.nightshade.update(plot_options)
                        self.default_map_options["nightshade"].update(plot_options)
                    case "add_linepath":
                        self._params.add_linepath.update(plot_options)
                        self.default_map_options["add_linepath"].update(plot_options)
                    case "add_marker":
                        self._params.add_marker.update(plot_options)
                        self.default_map_options["add_marker"].update(plot_options)
                    case "add_cap":
                        self._params.add_cap.update(plot_options)
                        self.default_map_options["add_cap"].update(plot_options)

        #self._plot_list = []
        super().__init__(**self._params.basemap)
        self.fig = self.ax.figure

    def show(self): 
        plt.show()
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

    def _parse_input_coords(
        self,coords: str | np.ndarray | list[str] | list[np.ndarray],
        is_lat: bool = False, is_lon: bool = False) -> list[np.ndarray]:
        from pyspedas import get_data
        if not isinstance(coords,list):
            coords = [coords]
        coord_data_list = []
        for coord_obj in coords:
            coord_data = coord_obj
            if isinstance(coord_obj, str):
                # load data from tplot:
                coord_data = get_data(coord_obj)
            # TODO: one of the dimensions MUST be 2; verify. 
            # UNLESS is_lat or is_lon is set; then one of the
            # dimensions must be size 0 or 1
            coord_data_list.append(coord_data)
        return coord_data_list

    def add_map_boundary(self,**drawmapboundary_kwargs):
        self._params.drawmapboundary.update(drawmapboundary_kwargs)
        self.drawmapboundary(**self._params.drawmapboundary)
        return

    def add_fillcontinents(self,**fillcontinents_kwargs):
        self._params.fillcontinents.update(fillcontinents_kwargs)
        self.fillcontinents(**self._params.fillcontinents)
        return
    
    def add_coastlines(self,**drawcoastlines_kwargs):
        self._params.drawcoastlines.update(drawcoastlines_kwargs)
        self.drawcoastlines(**self._params.drawcoastlines)
        return

    def add_meridians(self,**drawmeridians_kwargs):
        self._params.drawmeridians.update(drawmeridians_kwargs)
        self.drawmeridians(**self._params.drawmeridians)
        return

    def add_parallels(self,**drawparallels_kwargs):
        self._params.drawparallels.update(drawparallels_kwargs)
        self.drawparallels(**self._params.drawparallels)
        return

    def add_nightshade(self,**nightshade_kwargs):
        self._params.nightshade.update(nightshade_kwargs)
        self.nightshade(**self._params.nightshade)
        return

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

    def add_tracks(self,coords: str | np.ndarray, **tracks_plot_kwargs):
        coords = self._parse_input_coords(coords=coords)
        
        for coord_set in coords:
            # expects input coordinates in form of radius, longitude, latitude
            x,y = self(coord_set[:,2],coord_set[:,1])
            self.add_linepath(x,y,**tracks_plot_kwargs)
        return

    def add_markers(self,coords: str | np.ndarray | list[np.ndarray], **markers_plot_kwargs):
        coords = self._parse_input_coords(coords=coords)    
        for coord in coords:
            # expects input coordinates in form of radius, longitude, latitude
            x,y = self(coord[2],coord[1])
            # TODO: do we need to use scatter or plot (with line options turned off?)
            self.add_marker(x,y,**markers_plot_kwargs)
        return

    def add_station_fovs(self,coords: str | np.ndarray | list[np.ndarray], fov_angle = 80.0, **station_fov_plot_kwargs):
        from pyspedas import geodetic_correction as cotrans_geodetic_correction
        coords = self._parse_input_coords(coords=coords)    
                
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
    
            x,y = self(alon,cotrans_geodetic_correction(alat))
            self.add_cap(x,y,**station_fov_plot_kwargs)
        return

    def tplot_trace_tvars_to_tmap(self,tvar:list[str] | str):
        for tvar_name in tvar:
            # Compute traces:
            computed_trace = tvar_to_foottracks(tvar_to_trace = tvar_name, model_str = "t89", endpoint = "ionosphere-north")
            self.add_tracks(coords=computed_trace[0], label = tvar_name)
        return



def tvar_to_foottracks(tvar_to_trace:list[str] | str, in_coord_str:str='gsm', **ttrace2endpoint_kwargs) -> list: 
    """
    Take one or more tplot variable names, trace to an endpoint, and compute 
    geodetic polar foottracks from tplot variable positional data
    """
    from pyspedas import get_data, ttrace2endpoint
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar

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
        data_geod_polar = cotrans_cartesian2geodeticpolar(data=geo_data.y)
        foot_name_list.append(data_geod_polar)
    return foot_name_list

def tplot_map(
        tmap:   Tplot_Map | None = None, 
        projection:   str | None = None,
        center:     tuple | None = None,
        range:      tuple | None = None,
        land_color:   str | None = None,
        ocean_color:  str | None = None,
        view:         str | None = None,
        option_dict: dict | None = None,
        ax:          Axes | None = None, 
        display:bool = False, 
        **basemap_kwargs) -> Tplot_Map:
    """"Create a Tplot_Map object, with initialization options"""
    
    if tmap is not None:
        if ax is None:
            ax=tmap.ax
        if option_dict is None:
            option_dict=tmap.default_map_options
        if view is None:
            view = tmap.view
    
    if ax is None:
        # create axes object if none is passed:
        fig, ax = plt.subplots()

    if any([projection,center,range]) is not None:
        if basemap_kwargs is None:
            basemap_kwargs = dict()

        if projection is not None:
            basemap_kwargs.update({"projection":projection})
        
        if isinstance(center,tuple):
            if len(center) != 2:
                raise ValueError("Option 'center' must be tuple of length 2")
            else:
                basemap_kwargs.update({"lat_0":center[0],"lon_0":center[1]})

        if isinstance(range,tuple):
            if len(range) != 4:
                raise ValueError("Option 'range' must be tuple of length 4")
            else:
                basemap_kwargs.update({
                    "llcrnrlat":range[0],
                    "llcrnrlon":range[1],
                    "urcrnrlat":range[2],
                    "urcrnrlon":range[3],})
    
    if land_color is not None or ocean_color is not None:
        if option_dict is None:
            option_dict=dict()
        if land_color is not None:
            option_dict.update({
                "fillcontinents":{"color":land_color}
                })
        if ocean_color is not None:
            option_dict.update({
                "fillcontinents":{"lake_color":ocean_color},
                "drawmapboundary":{"fill_color":ocean_color}
                })

    tmap = Tplot_Map(
        view=view,
        ax=ax,
        option_dict=option_dict,
        **basemap_kwargs)
    
    if display:
        tmap.show()
    
    return tmap

# Deprecated methods:
def add_tracks(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **tracks_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_tracks(coords=coords,**tracks_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_markers(coords: str | np.ndarray | list[np.ndarray], tmap:Tplot_Map | None = None, display:bool = False, **markers_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_markers(coords=coords, **markers_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_station_fovs(coords: str | np.ndarray | list[np.ndarray], fov_angle = 80.0, tmap:Tplot_Map | None = None, display:bool = False, **station_fov_plot_kwargs) -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    if tmap is None:
        tmap = Tplot_Map()
    tmap.add_station_fovs(coords=coords, fov_angle = fov_angle, **station_fov_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def geodetic_correction(lat_deg,f=(1/298.26)):
    """
    Obsolete, deprecated (moved to separate script)

    Convert geocentric latitude to geodetic latitude using squashing factor f
    """
    from pyspedas import geodetic_correction as cotrans_geodetic_correction
    return cotrans_geodetic_correction(lat_deg=lat_deg,f=f)

def cartesian2geodeticpolar(data: str | np.ndarray) -> np.ndarray:
    """
    Obsolete, deprecated (moved to separate script)

    Get positional data from tplot variable, then convert data coordinates to 
    geodetic polar coordinates
    """
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar
    return cotrans_cartesian2geodeticpolar(data=data)

def tvar_to_geodeticpolar(tvar:str, in_coord_str:str='gsm'):
    """
    Obsolete, deprecated

    Take a tplot variable of arbitrary coordinate system and convert to geodetic 
    polar
    """
    from pyspedas import cotrans, get_data
    from pyspedas import cartesian2geodeticpolar as cotrans_cartesian2geodeticpolar
    # TODO: should this return array or simply create new tplot variable? 
    tvar_geo = tvar + "_geo"
    cotrans(name_in=tvar,name_out=tvar_geo,coord_in=in_coord_str,coord_out="geo")
    # convert Cartesian GEO/ECEF data to geodetic polar:
    geo_data = get_data(tvar_geo)
    data_geod_polar = cotrans_cartesian2geodeticpolar(data=geo_data.y)
    return data_geod_polar

def tplot_trace_tvars_to_tmap(
        tmap:Tplot_Map | None,
        tvar:list[str] | str,
        display:bool = False,
        fig_fp:str="") -> Tplot_Map:
    """Deprecated, method moved to Tplot_Map class object"""
    
    tmap = tplot_map(tmap=tmap)
    tmap.tplot_trace_tvars_to_tmap(tvar=tvar)

    if display:
        tmap.show()
    if fig_fp != "":
        plt.savefig(fig_fp)
    return tmap
