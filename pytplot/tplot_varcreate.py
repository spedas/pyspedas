
def tplot_varcreate(startdate,enddate):
	import pydivide
	import pytplot
	#pydivide.download_files(start_date = startdate,end_date = enddate)
	insitu = pydivide.read(startdate,enddate)
	print(insitu)
	print(insitu["EUV"])
	inst_list = ["EUV","LPW","STATIC","SWEA","SWIA","MAG","SEP","NGIMS"]
	for instrument in inst_list:
		for obs in insitu[instrument]:
			obs_specific = "mvn_kp::"+obs
			pytplot.store_data(obs_specific,data={'x':insitu['Time'], 'y': insitu[instrument][obs]})
			print(instrument)
			print(obs)
tplot_varcreate("2016-06-06","2016-06-07")