"""
Take a tplot variable containing positional data, 
trace magnetic field lines to the north ionosphere, south ionosphere, or equator,
then map those points to a basemap
"""
from pyspedas import cotrans, get_data, xyz_to_polar,ttrace2endpoint, tplotxy3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
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
    def __init__(self):
        self._params = Tplot_Map_Param_Set()
        self._params.basemap         = {"projection":"ortho","lat_0":0,"lon_0":0}
        self._params.drawmapboundary = {"fill_color":"white"} #{"fill_color":"lightskyblue"}
        self._params.fillcontinents  = {"color":"white","lake_color":"white"} #{"color":"palegreen","lake_color":"lightskyblue"}
        self._params.drawcoastlines  = {"linewidth":0.25}
        self._params.nightshade      = {"date":dt.datetime.now(),"alpha":0.5}
        self._params.add_linepath    = {}#{"color":"m"}
        self._params.add_marker      = {"color":"m"}
        self._params.add_cap         = {"color":"m"}
        
        # TODO: make meridians into magnetic coordinates
        self._params.drawmeridians   = {"meridians":np.arange(0,360,10)}
        self._params.drawparallels   = {"circles":np.arange(-90,90,10)}
        
        #self._plot_list = []
        self.build_map()

    def build_map(self):
        # TODO: auroral oval plot?
        #plt.cla()
        super().__init__(**self._params.basemap)
        return
    
    def show(self): 
        self.build_map()
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

    # TODO: all methods: verify that kwargs get passed to function parameters correctly
    def add_meridians(self,**draw_meridians_kwargs):
        self._params.drawmeridians.update(draw_meridians_kwargs)
        self.build_map()
        return

    def add_nightshade(self,**nightshade_kwargs):
        self._params.nightshade.update(nightshade_kwargs)
        self.nightshade(**self._params.nightshade)
        return

    # TODO: all methods need default color sequence 
    # QUESTION: does plot() need to be added to include color sequence? 
    def add_linepath(self, x, y,**add_linepath_kwargs):
        self._params.add_linepath.update(add_linepath_kwargs)
        self.plot(x,y,**self._params.add_linepath)
        return
    
    def add_marker(self, x, y, **add_marker_kwargs):
        self._params.add_marker.update(add_marker_kwargs)
        self.plot(x,y,**self._params.add_marker)
        return

    def add_cap(self, x, y,**add_cap_kwargs):
        self._params.add_cap.update(add_cap_kwargs)
        self.plot(x,y,**self._params.add_cap)
        return

def tplot_map(tmap:Tplot_Map | None = None, display:bool = False, **basemap_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
    tmap._params.basemap.update(basemap_kwargs)
    tmap.build_map()
    if display:
        tmap.show()
    return tmap

# TODO accept list of strings or np.ndarray and iterate over list
def add_tracks(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **tracks_plot_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
    #tmap = tplot_map(tmap=tmap)
    if isinstance(coords,str):
        tvar_data = get_data(coords)
        coords = tvar_data.y
    # expects input coordinates in form of radius, longitude, latitude
    x,y = tmap(coords[:,2],coords[:,1])
    tmap.add_linepath(x,y,**tracks_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_markers(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **markers_plot_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
    #tmap = tplot_map(tmap=tmap)
    if isinstance(coords,str):
        tvar_data = get_data(coords)
        coords = tvar_data.y
    # expects input coordinates in form of radius, longitude, latitude
    x,y = tmap(coords[:,2],coords[:,1])
    # TODO: update tmap track plot parameters using tracks_plot_kwargs
    # TODO: need way to pass tmap plot parameters to plot function
    # TODO: do we need to use scatter or plot (with line options turned off?)
    tmap.plot(x,y,markers_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def add_station_fovs(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **station_fov_plot_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
    #tmap = tplot_map(tmap=tmap)
    if isinstance(coords,str):
        tvar_data = get_data(coords)
        coords = tvar_data.y
    # expects input coordinates in form of radius, longitude, latitude
    x,y = tmap(coords[:,2],coords[:,1])
    # TODO: update tmap track plot parameters using tracks_plot_kwargs
    # TODO: need way to pass tmap plot parameters to plot function
    # TODO: do we need to use scatter or plot (with line options turned off?)
    tmap.add_cap(x,y,station_fov_plot_kwargs)
    if display:
        tmap.show()
    return tmap

def geodetic_correction(lat_deg,f=(1/298.26)):
        """
        Convert geocentric latitude to geodetic latitude using squashing factor f
        """
        lat_rad = np.deg2rad(lat_deg)
        lad_corrected_rad = np.arctan( (1-f)**2 * np.tan(lat_rad) )
        lad_corrected_deg = np.rad2deg(lad_corrected_rad)
        return lad_corrected_deg

def cartesian2geodeticpolar(data: str | np.ndarray) -> np.ndarray:
    """
    Get positional data from tplot variable, then convert data coordinates to 
    geodetic polar coordinates
    """
    from pyspedas.tplot_tools import store_data
    make_tvars=False
    if isinstance(data, str):
        make_tvars = True
        name_in = data
        d = get_data(name_in)
        data = d.y
    data_polar = xyz_to_polar(data)
    out = np.zeros(data.shape)
    # radius from center:
    out[:,0] = data_polar[:,0]
    # latitude:
    out[:,1] = geodetic_correction(data_polar[:,1])
    # signed longitude
    out[:,2] = data_polar[:,2]
    if make_tvars:
        store_data(name_in + '_radius', data={'x':d.times, 'y':out[:,0]})
        store_data(name_in + '_geod_lat', data={'x': d.times, 'y': out[:, 1]})
        store_data(name_in + '_signed_lon', data={'x': d.times, 'y': out[:, 2]})
        return
    else:
        return out

def tvar_to_geodeticpolar(tvar:str, in_coord_str:str='gsm'):
    """
    Take a tplot variable of arbitrary coordinate system and convert to geodetic 
    polar
    """
    # TODO: should this return array or simply create new tplot variable? 
    tvar_geo = tvar + "_geo"
    cotrans(name_in=tvar,name_out=tvar_geo,coord_in=in_coord_str,coord_out="geo")
    # convert Cartesian GEO/ECEF data to geodetic polar:
    geo_data = get_data(tvar_geo)
    data_geod_polar = cartesian2geodeticpolar(data=geo_data.y)
    return data_geod_polar

def tvar_to_foottracks(tvar_to_trace:list[str] | str, in_coord_str:str='gsm', **ttrace2endpoint_kwargs) -> list: 
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
        # TODO: finish adding name building options from ttrace2endpoint.py
        match ttrace2endpoint_kwargs["endpoint"]:
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
        match ttrace2endpoint_kwargs["model_str"]:
            case "t89":
                footname_str += "89"
        footname_str += footname_str_pre + "foot" + footname_str_suf
        tracename_str += tracename_str_part + ttrace2endpoint_kwargs["model_str"]
        ttrace2endpoint(
            tvar,
            foot_name=footname_str, 
            trace_name=tracename_str,
            km=True,
            **ttrace2endpoint_kwargs)
        # compute geodetic polar foottracks from tplot variable positional data
        data_geod_polar = tvar_to_geodeticpolar(tvar=footname_str, in_coord_str=in_coord_str)
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

if __name__ == "__main__":
    from pyspedas.projects.themis import state
    date_str = '2007-03-23'
    state(trange=[date_str,date_str], probe='a')
    state(trange=[date_str,date_str], probe='d')
    #tmap = Tplot_Map()
    tmap = tplot_map(lat_0=50,lon_0=-120)
    
    tmap = tplot_trace_tvars_to_tmap(tmap=tmap,tvar=['tha_pos_gsm','thd_pos_gsm'])
    tmap.drawmapboundary()
    tmap.fillcontinents()
    tmap.drawcoastlines(linewidth=0.25)
    #self.drawmeridians(**self._params.drawmeridians)
    #self.drawparallels(**self._params.drawparallels)
    #self.nightshade(**self._params.nightshade)
    tmap.add_nightshade(date=dt.datetime.strptime(date_str+" 00:00:00",'%Y-%m-%d %H:%M:%S'))
    


    # Add ground station markers
    #tplot_map_add_markers(map_obj, marker_latitude_list, marker_longitude_list, marker_symbol, marker_color)

    # Add field of view circles for each ground station
    # Hopefully there are convenience features to plot the circles projected appropriately without generating our own long-lat traces for each FOV
    #tplot_map_add_station_fov(map_obj, marker_latitude_list, marker_longitud_list, fov_radius, linestyle)
    
    tmap.show()