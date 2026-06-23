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
        self._params.add_marker      = {"color":"r","linestyle":"","marker":"d"}
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

def tplot_map(tmap:Tplot_Map | None = None, display:bool = False, **basemap_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
    tmap._params.basemap.update(basemap_kwargs)
    tmap.build_map()
    if display:
        tmap.show()
    return tmap

def add_tracks(coords: str | np.ndarray, tmap:Tplot_Map | None = None, display:bool = False, **tracks_plot_kwargs) -> Tplot_Map:
    if tmap is None:
        tmap = Tplot_Map()
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
    if tmap is None:
        tmap = Tplot_Map()
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
    if tmap is None:
        tmap = Tplot_Map()
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
        #data_geod_polar = tvar_to_geodeticpolar(tvar=footname_str, in_coord_str=in_coord_str)
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
    from pyspedas.projects.themis.ground import gmag

    date_str = '2026-02-03'
    state(trange=[date_str,date_str], probe='a')
    state(trange=[date_str,date_str], probe='d')
    
    # Initialize map:
    tmap = tplot_map(lat_0=50,lon_0=-100)
    #tmap._params.drawmapboundary = {"fill_color":"lightskyblue"}
    #tmap._params.fillcontinents = {"color":"palegreen","lake_color":"lightskyblue"}
    
    # Add ground tracks:
    tmap = tplot_trace_tvars_to_tmap(tmap=tmap,tvar=['tha_pos_gsm','thd_pos_gsm'])
    
    # Add ground station markers
    #tplot_map_add_markers(map_obj, marker_latitude_list, marker_longitude_list, marker_symbol, marker_color)
    themis_gmag_dict = gmag.Themis_gmag()
    for station_dict in themis_gmag_dict.get_gmag_list():
        if station_dict['variom'] == 'Y':
            tmap = add_markers(coords=np.array([0,float(station_dict['lat']),float(station_dict['lng'])]),tmap=tmap,label=station_dict['ccode'],ms=3)

    # Add field of view circles for each ground station
    tmap = add_station_fovs(coords=[np.array([0,48,-128]),np.array([0,30,-110])], tmap=tmap)

    tmap.add_map_boundary()
    tmap.add_fillcontinents()
    tmap.add_coastlines(linewidth=0.25)
    tmap.add_nightshade(date=dt.datetime.strptime(date_str+" 15:00:00",'%Y-%m-%d %H:%M:%S'))
    
    tmap.show()
    print("done")