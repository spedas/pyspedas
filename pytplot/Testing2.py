import pytplot
pytplot.store_data('orbit', data={'x':[1497830400, 1466380800], 'y':[3354.4, 3355.45]})
pytplot.store_data('orbit2', data={'x':[1497830400, 1466380800], 'y':[3354.4, 3355.45]})
pytplot.store_data('orbit3', data={'x':[1497830400, 1466380800], 'y':[3354.4, 3355.45]})
 
pytplot.tplot_names()
 
pytplot.tplot_rename("orbit2", "orbitb")
 
pytplot.tplot_names()





#for instrument in insitu
#	check if instrument == true
#	for parameter in instrument?