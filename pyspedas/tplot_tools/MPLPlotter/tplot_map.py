"""
Take a tplot variable containing positional data, 
trace magnetic field lines to the north ionosphere, south ionosphere, or equator,
then map those points to a basemap
"""
from pyspedas import cotrans, get_data, xyz_to_polar,ttrace2endpoint, tplotxy3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

params_tmap_default={
    "params_traces": {"model_str":"t89","endpoint":"ionosphere-north"},
    "params_basemap":{"projection":"ortho","lat_0":0,"lon_0":0},
    "params_map_boundary":{"fill_color":"aqua"},
    "params_fill_conts":{"color":"coral","lake_color":"aqua"},
    "params_draw_coastlines":{},
    "params_plot":{"color":"m"}
}

def tplot_map(tvar:str, tmap:Basemap | None, in_coord_str:str='gsm',params_tmap_in:dict={}) -> Basemap:
    """
    take a tplot variable, convert to GEO coordinates, 
    convert to polar, 
    correct for geodetic coordinates, 
    and then create a basemap object to display the trace
    """
    tvar_geo = tvar + "_geo"
    cotrans(name_in=tvar,name_out=tvar_geo,coord_in=in_coord_str,coord_out="geo")
    # convert Cartesian GEO/ECEF data to geodetic polar:
    data_geo = get_data(tvar_geo)
    data_geod_polar = conv2geodeticpolar(data_geo.y)

    params_tmap = construct_args_dict(params_tmap_default,params_tmap_in)
    # If tmap isn't passed as an argument, construct a default tmap:
    if tmap is None:
        tmap = init_tmap(params_tmap)

    x,y = tmap(data_geod_polar[:,2],data_geod_polar[:,1])
    tmap.plot(x,y,**params_tmap["params_plot"])
    return tmap

def init_tmap(params_tmap:dict={}) -> Basemap:
    tmap_args = construct_args_dict(params_tmap_default,params_tmap)
    tmap = Basemap(**tmap_args["params_basemap"])
    tmap.drawmapboundary(**tmap_args["params_map_boundary"])
    tmap.fillcontinents(**tmap_args["params_fill_conts"])
    tmap.drawcoastlines(**tmap_args["params_draw_coastlines"])
    return tmap

def geodetic_correction(lat_deg,f=(1/298.26)):
    """
    Convert geocentric latitude to geodetic latitude using squashing factor f
    """
    lat_rad = np.deg2rad(lat_deg)
    lad_corrected_rad = np.arctan( (1-f)**2 * np.tan(lat_rad) )
    lad_corrected_deg = np.rad2deg(lad_corrected_rad)
    return lad_corrected_deg

def conv2geodeticpolar(data):
    """
    Get positional data from tplot variable, 
    then convert data coordinates to geodetic polar coordinates
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
       store_data(name_in+'_radius', data={'x':d.times, 'y':out[:,0]})
       store_data(name_in + '_geod_lat', data={'x': d.times, 'y': out[:, 1]})
       store_data(name_in + '_signed_lon', data={'x': d.times, 'y': out[:, 2]})
       return
    else:
        return out 

def create_traces(
        tvar_to_trace:list | str,
        params_traces_in:dict=params_tmap_default["params_traces"]) -> list: 
    
    params_traces=construct_args_dict(params_tmap_default["params_traces"],params_traces_in)

    if type(tvar_to_trace) is str:
        tvar_to_trace = [tvar_to_trace]

    foot_name_list = []
    for tvar in tvar_to_trace:
        footname_str = tvar
        tracename_str = tvar + "_trace"
        match params_traces["endpoint"]:
            case "ionosphere-north": 
                footname_str_pre="i"
                footname_str_suf="n"
                tracename_str_part="iono_n_"
        match params_traces["model_str"]:
            case "t89":
                footname_str += "89"
        footname_str += footname_str_pre + "foot" + footname_str_suf
        tracename_str += tracename_str_part + params_traces["model_str"]
        ttrace2endpoint(
            tvar,
            foot_name=footname_str, 
            trace_name=tracename_str,
            km=True,**params_traces)
        foot_name_list.append(footname_str)
    return foot_name_list

def construct_args_dict(accepted_args:dict,kwargs_dict:dict):
    """
    Method to construct argument dictionary using 
    """
    args_dict = kwargs_dict.copy()
    for expected_arg in accepted_args:
        if expected_arg not in kwargs_dict:
            args_dict[expected_arg] = accepted_args.get(expected_arg)
    return args_dict

def tplot_map_from_list(
        tvar_to_trace:list | str,
        figure_fp:str="",
        in_coord_str:str='gsm',
        params_tmap_in:dict={}):
    params_tmap=construct_args_dict(params_tmap_default,params_tmap_in)
    # take list of tvars (like generated from state), create footpoint traces has new tvariables
    foot_name_list = create_traces(tvar_to_trace,params_traces_in=params_tmap["params_traces"])
    # take list of trace tvars and add traces to tplot map:
    tmap = init_tmap(params_tmap=params_tmap)
    for trace_tvar in foot_name_list:
        tmap = tplot_map(trace_tvar,tmap=tmap,in_coord_str=in_coord_str,params_tmap_in=params_tmap)
    plt.show()
    if figure_fp != "":
        plt.savefig(figure_fp)
    return

if __name__ == "__main__":
    from pyspedas.projects.themis import state
    state(trange=['2007-03-23', '2007-03-23'], probe='a')
    tplot_map_from_list(['tha_pos_gsm'])
    #'ionosphere-south',foot_name='ifoot89_s'
    #'equator',foot_name='eq_foot89'
