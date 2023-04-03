import pyspedas
from pyspedas.themis.cotrans.gse2sse import gse2sse
from pyspedas.themis.state.slp import slp
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord

state_vars = pyspedas.themis.state(probe='d', trange=['2013-11-5', '2013-11-6'])
slp_vars = slp(trange=['2013-11-5', '2013-11-6'])

gse2sse('thd_pos_gse','slp_sun_pos','slp_lun_pos','thd_pos_sse_test',isgsetosse=True, ignore_input_coord=True)

