"""
Take a tplot variable containing positional data, 
trace magnetic field lines to the north ionosphere, south ionosphere, or equator,
then map those points to a basemap
"""
from pyspedas.projects.themis import state
from pyspedas import cotrans, get_data, xyz_to_polar,ttrace2endpoint, tplotxy3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def tplot_map(tname:str,in_coord_str:str='gsm'):
    tname_in_coord = tname
    tname_geo = tname + "_geo"
    cotrans(name_in=tname_in_coord,name_out=tname_geo,coord_in=in_coord_str,coord_out="geo")
    # convert Cartesian GEO data to ECEF data:
    footpoint_pos_GEO = get_data(tname_geo)
    footpoint_pos_GEO_polar = xyz_to_polar(footpoint_pos_GEO.y)
    footpoint_lat = footpoint_pos_GEO_polar[:,1]
    footpoint_lon = footpoint_pos_GEO_polar[:,2]
    footpoint_lat_rad = footpoint_lat*np.pi/180.0
    f = (1/298.26)
    footpoint_lat_geodetic_rad = np.arctan( (1-f)**2 * np.tan(footpoint_lat_rad) )
    footpoint_lat_geodetic = footpoint_lat_geodetic_rad*180.0/np.pi
    map = Basemap(projection='ortho',lat_0=45, lon_0=-90)
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral',lake_color='aqua')
    map.drawcoastlines()
    x,y = map(footpoint_lon,footpoint_lat_geodetic)
    map.plot(x,y,color='m')
    plt.show()
    plt.savefig('test_basemap_themis.png')
    return


if __name__ == "__main__":
    state(trange=['2007-03-23', '2007-03-23'], probe='a')
    ttrace2endpoint('tha_pos_gsm','t89','ionosphere-north',foot_name='ifoot89_n', trace_name='tha_trace_iono_n_t89',km=True)
    tplot_map(tname='ifoot89_n')

    # Trace to south ionosphere with T89 model
    #ttrace2endpoint('tha_pos_gsm','t89','ionosphere-south',foot_name='ifoot89_s', trace_name='tha_trace_iono_s_t89',km=True)
    #tplotxy3('ifoot89_s',legend_names=['South ionosphere foot points',], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_iono_s_foot.png')
    # Trace to equator with T89 model
    #ttrace2endpoint('tha_pos_gsm','t89','equator',foot_name='eq_foot89', trace_name='tha_trace_equ_t89',km=True)
    #tplotxy3('eq_foot89',legend_names=['Equator foot points'], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_equ_foot.png')
    #tplotxy3('tha_trace_equ_t89',legend_names=['Traces to equator'], colors='blue', reverse_x=True, show_centerbody=True, save_png='tha_equ_traces.png')
    