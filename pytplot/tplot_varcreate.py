
def tplot_varcreate(start_date,end_date):
	import pydivide
	import pytplot
	pydivide.download_files(start_date,end_date)
	insitu,iuvs = pydivide.read(start_date,end_date)
	pytplot.store_data("mvn_kp::hplus_density",data={'x':insitu['Time'], 'y': insitu['SWEA']['HPLUS_Density']})