# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
pytplot.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
pytplot.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
pytplot.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
pytplot.store_data('g', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]]})
pytplot.store_data('h', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]],'v':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})

print('add_across_partial')
pytplot.add_across_partial('b',[[1,2],[3,4]],'b_aap')
print(pytplot.data_quants['b_aap'].data)
  
print('add_across')
pytplot.add_across('d','d_aa')
print(pytplot.data_quants['d_aa'].data)
  
print('add')
pytplot.add('a','c','a+c')
print(pytplot.data_quants['a+c'].data)
  
print('avg_res_data')
pytplot.avg_res_data('d',2,'d2res')
print(pytplot.data_quants['d'].data)
print(pytplot.data_quants['d2res'].data)
pytplot.avg_res_data('h', 7, 'h7res')
print(pytplot.data_quants['h'].data)
print(pytplot.data_quants['h'].spec_bins)
print(pytplot.data_quants['h7res'].data)
print(pytplot.data_quants['h7res'].spec_bins)
  
print('clip')
pytplot.clip('d',2,6,'d_clip')
print(pytplot.data_quants['d_clip'].data)
pytplot.clip('h',2,6,'h_clip')
print(pytplot.data_quants['h_clip'].data)
print(pytplot.data_quants['h_clip'].spec_bins)

print('crop')
pytplot.crop('a','b')
  
print('deflag')
pytplot.deflag('d',[100,90,7,2,57],'d_deflag')
print(pytplot.data_quants['d'].data)
print(pytplot.data_quants['d_deflag'].data)
pytplot.deflag('h',[100,90,7,2,57],'h_deflag')
print(pytplot.data_quants['h_deflag'].data)
print(pytplot.data_quants['h_deflag'].spec_bins)

  
print('derive')
pytplot.derive('b','dbdt')
print(pytplot.data_quants['dbdt'].data)
pytplot.derive('h','dhdt')
print(pytplot.data_quants['dhdt'].data)
print(pytplot.data_quants['dhdt'].spec_bins)
 
print('divide')
pytplot.divide('a','b','a/b')
print(pytplot.data_quants['a/b'].data)
  
print('flatten_full')
pytplot.flatten_full('d','d_ff')
print(pytplot.data_quants['d_ff'].data)
  
print('flatten')
pytplot.flatten('d',8,14,'d_flatten')
print(pytplot.data_quants['d_flatten'].data)
  
print('interp_nan')
pytplot.interp_nan('e','e_nonan',s_limit=5)
print(pytplot.data_quants['e_nonan'].data)

print('interpolate')
pytplot.tinterp('a','c',interp='cubic')
print(pytplot.data_quants['c_interp'].data)
 
print('join_vec')
pytplot.join_vec(['d','e','g'],'deg')
print(pytplot.data_quants['deg'].data)
 
print('multiply')
pytplot.multiply('a','c','ac',interp='linear')
print(pytplot.data_quants['ac'].data)

 
print('resample')
# pytplot.resample('d',[3,4,5,6,7,18],'d_resampled')
# print(pytplot.data_quants['d_resampled'].data)
pytplot.resample('h',[3,4,5,6,7,18],'h_resampled')
print(pytplot.data_quants['h_resampled'].data)
print(pytplot.data_quants['h_resampled'].spec_bins)
 
print('spec_mult')
pytplot.spec_mult('h','h_specmult')
print(pytplot.data_quants['h_specmult'].data)
 
print('split_vec')
pytplot.split_vec('b',['b1','b2','b3'],[0,[1,3],4])
print(pytplot.data_quants['b1'].data)
print(pytplot.data_quants['b2'].data)
print(pytplot.data_quants['b3'].data)
defaultlist = pytplot.split_vec('b')
print(pytplot.data_quants['b'].data)
print(pytplot.data_quants['data_3'].data)
print(defaultlist)
 
print('subtract')
pytplot.subtract('a','c','a-c')
print(pytplot.data_quants['a-c'].data)