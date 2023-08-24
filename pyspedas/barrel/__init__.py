from .load import load

def sspc(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='sspc', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def mspc(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='mspc', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def fspc(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='fspc',trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def rcnt(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='rcnt', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def magn(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='magn', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def ephm(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='ephm', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def hkpg(trange=['2013-01-17', '2013-01-19'], 
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
   
    return load(datatype='hkpg', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)
