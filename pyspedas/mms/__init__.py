"""
This module contains routines for loading MMS data

"""

from functools import wraps

from .mec_ascii.state import mms_load_state
from .fgm.fgm import mms_load_fgm
from .hpca.hpca import mms_load_hpca
from .fpi.fpi import mms_load_fpi
from .scm.scm import mms_load_scm
from .mec.mec import mms_load_mec
from .feeps.feeps import mms_load_feeps
from .eis.eis import mms_load_eis
from .edi.edi import mms_load_edi
from .edp.edp import mms_load_edp
from .dsp.dsp import mms_load_dsp
from .aspoc.aspoc import mms_load_aspoc
from .fsm.fsm import mms_load_fsm
from .fgm.mms_curl import mms_curl
from .fgm.mms_lingradest import mms_lingradest
from .spd_mms_load_bss import spd_mms_load_bss

'''
    the following wrappers allow users to import the load routines using 
    the syntax: 
    
            >>> from pyspedas.mms import fgm
            >>> fgm_data = fgm(...)

        and/or

            >>> import pyspedas
            >>> fgm_data = pyspedas.mms.fgm(...)
'''

@wraps(spd_mms_load_bss)
def bss(*args, **kwargs):
    return spd_mms_load_bss(*args, **kwargs)

@wraps(mms_load_state)
def state(*args, **kwargs):
    return mms_load_state(*args, **kwargs)

@wraps(mms_load_fgm)
def fgm(*args, **kwargs):
    return mms_load_fgm(*args, **kwargs)

@wraps(mms_load_scm)
def scm(*args, **kwargs):
    return mms_load_scm(*args, **kwargs)

@wraps(mms_load_fsm)
def fsm(*args, **kwargs):
    return mms_load_fsm(*args, **kwargs)

@wraps(mms_load_edp)
def edp(*args, **kwargs):
    return mms_load_edp(*args, **kwargs)

@wraps(mms_load_edi)
def edi(*args, **kwargs):
    return mms_load_edi(*args, **kwargs)

@wraps(mms_load_fpi)
def fpi(*args, **kwargs):
    return mms_load_fpi(*args, **kwargs)

@wraps(mms_load_hpca)
def hpca(*args, **kwargs):
    return mms_load_hpca(*args, **kwargs)

@wraps(mms_load_eis)
def eis(*args, **kwargs):
    return mms_load_eis(*args, **kwargs)

@wraps(mms_load_feeps)
def feeps(*args, **kwargs):
    return mms_load_feeps(*args, **kwargs)

@wraps(mms_load_aspoc)
def aspoc(*args, **kwargs):
    return mms_load_aspoc(*args, **kwargs)

@wraps(mms_load_mec)
def mec(*args, **kwargs):
    return mms_load_mec(*args, **kwargs)

@wraps(mms_load_dsp)
def dsp(*args, **kwargs):
    return mms_load_dsp(*args, **kwargs)

@wraps(mms_curl)
def curlometer(*args, **kwargs):
    return mms_curl(*args, **kwargs)

@wraps(mms_lingradest)
def lingradest(*args, **kwargs):
    return mms_lingradest(*args, **kwargs)
