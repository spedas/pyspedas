import pydivide
import pytplot
from pytplot import tplot_common
#pydivide.download_files(start_date='2015-12-25',end_date='2015-12-27')
#pydivide.download_files(start_date='2015-12-25',end_date='2015-12-27',iuvs=True)
#insitu,iuvs = pydivide.read('2015-12-26')

#pytplot.options(3,"ylog",1)
#
pytplot.options('swia_counts', 'ylog', 1)

name = tplot_common.data_quants.keys()[3]
#insitu2 = pydivide.insitu_search(insitu, 'inbound')