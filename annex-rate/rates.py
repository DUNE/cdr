#!/usr/bin/env python3
import numpy as np

from pint import UnitRegistry

units = UnitRegistry()
Q = units.Quantity

def tpc_params():
    '''
    TPC related parameters
    '''
    d = dict(
        # cdr
        tpc_full_height = Q('12.0 meter'),
        tpc_full_width = Q('14.5 meter'),
        tpc_full_length = Q('58.0 meter'),
        # docdb 3383
        tpc_drift_distance = Q('3.41 m'),
        tpc_height = Q('6.0 meter'),
        tpc_width = Q('2.3 meter'),
        tpc_drift_velocity = Q('1.6 mm/microsecond')
    )

    d['tpc_drift_time'] = (d['tpc_drift_distance'] / d['tpc_drift_velocity']).to('millisecond')
    return d

def daq_params(tpc):
    '''
    DAQ related basic parameters.  Needs TPC parameters
    '''
    d = dict(
        # chapter 2 lbne-fd-closeout
        daq_sample_rate = Q('2.0 MHz'),
        # giles
        daq_drifts_per_readout = 2.4,
        daq_bytes_per_sample = Q('12 bits').to('byte'),
        daq_channels_per_apa = 2560,
        daq_apa_per_detector = 150,
        daq_number_detectors = 4,
    )
    d['daq_number_apas'] = d['daq_apa_per_detector'] * d['daq_number_detectors']
    
    d['daq_readout_time'] = d['daq_drifts_per_readout'] * tpc['tpc_drift_time']
    d['daq_readout_channel_samples'] = int(d['daq_sample_rate'] * d['daq_readout_time'])

    d['daq_channels_10kt'] = d['daq_channels_per_apa'] * d['daq_apa_per_detector']
    d['daq_channels'] = d['daq_channels_10kt'] * d['daq_number_detectors']
    
    d['daq_fs_readout_size'] = (d['daq_bytes_per_sample'] * d['daq_channels'] * d['daq_readout_channel_samples']).to('gigabyte')

    d['daq_fs_readout_rate'] = (d['daq_fs_readout_size'] / d['daq_readout_time']).to('terabyte/second')
    d['daq_fs_readout_size_second'] = (d['daq_fs_readout_rate']*Q('second')).to('terabyte')
    d['daq_fs_readout_size_minute'] = (d['daq_fs_readout_rate']*Q('minute')).to('petabyte')
    d['daq_fs_readout_size_year'] = (d['daq_fs_readout_rate']*Q('year')).to('exabyte')

    return d


def beam_params(daq):
    'Define beam parametes'
    d = dict(
        beam_rep_rate = Q('1 Hz'),
        beam_run_fraction = float(Q('2e7 seconds/year')),
        beam_event_size = Q('10 megabyte'),
        # 40kton, oscillated from table  4.1 of sci opp
        beam_event_rate = Q('40000/year').to('1/day') ,
    )
    d['beam_high_data_rate'] = d['beam_event_size'] * d['beam_event_rate']
    #print 'High energy beam data = %s' % beam_high_data.to('gigabyte/year')
    d['beam_fs_data_rate'] = (daq['daq_fs_readout_size'] * d['beam_rep_rate'] * d['beam_run_fraction']).to('petabyte/year')
    #print 'FS in-spill data = %s' % beam_all_data.to('petabyte/year')
    return d

def beta_params(tpc, daq):
    'Beta radioactivity from Ar39'
    # beta=Ar39 from lbne-fd-closeout
    d = dict(
        beta_rate_apa = Q('63 kHz') * 40.0/34.0,
        beta_event_size = 24 * daq['daq_bytes_per_sample'],
    )
    d['beta_rate'] = (d['beta_rate_apa'] * daq['daq_number_apas']).to('megahertz')
    d['beta_data_rate_apa'] = (d['beta_rate_apa'] * d['beta_event_size']).to('megabyte/second')
    d['beta_data_rate'] = (d['beta_data_rate_apa'] * daq['daq_number_apas']).to('gigabyte/second')
    d['beta_readout_size_apa'] = (d['beta_data_rate_apa'] * daq['daq_readout_time']).to('kilobyte')
    d['beta_readout_size'] = (d['beta_readout_size_apa'] * daq['daq_number_apas']).to('megabyte')
    return d

def cosmics_param(tpc, daq):
    # cosmics


# Vitaly Kudryavtsev <v.kudryavtsev@sheffield.ac.uk> writes:
#
# Muon flux at LBNE site (which I assume to be the same as DUNE site) is
# 5.66*10^(-9) cm^(-2) s^(-1) through a spherical detector with an
# uncertainty of about 10% (I hope).
# If you take this flux and multiply by the hosizontal area of the
# cryostat/TPC or whatever you want to calculate the flux through, you
# can get an event rate with an accuracy of about 50% (most muons are
# coming from near vertical directions). If you add another coefficient
# of 1.3-1.4 you will get a rate to within 10-15% accuracy.
#
# As an example, accurate calculations of muon rate on a surface of a
# box 100*40*50 m^3 give an event rate of about 9.7*10^6 muons per year,
# which is close to the flux * horizontal area * 1.36.

    d = dict(
        # see above comment, The 4 is to naively account for 4 10kton detectors
        cosmic_muon_rate = 4*(1.36* Q('5.66e-9 Hz/cm**2') * tpc['tpc_full_width'] * tpc['tpc_full_length']).to('1/year'),
        cosmic_muon_event_size = (5e4 * daq['daq_bytes_per_sample']).to('kilobyte'),
    )

    d['cosmic_muon_data_rate'] = (d['cosmic_muon_rate'] * d['cosmic_muon_event_size']).to('gigabyte/year')
    return d

def load():
    d = dict()
    d['tpc'] = tpc_params()
    d['daq'] = daq_params(d['tpc'])
    d['beam'] = beam_params(d['daq'])
    d['beta'] = beta_params(d['tpc'], d['daq'])
    d['cosmic'] = cosmics_param(d['tpc'], d['daq'])
    return d

def flatten(d):
    ret = dict()
    for v in d.values():
        ret.update(v)
    return ret

def report(params, template):
    f = flatten(params)
    text = template.format(**f)
    return text

def dump(params):
    for cat,d in sorted(params.items()):
        print '\n%s:' % cat.upper()
        for k,v in sorted(d.items()):
            print '%30s %s' % (k,v)
    
pint2latex = {
    '1':'1',
    'byte':r'\byte',
    'kilobyte':r'\kilo\byte',
    'megabyte':r'\mega\byte',
    'gigabyte':r'\giga\byte',
    'petabyte':r'\peta\byte',
    'terabyte':r'\tera\byte',
    'exabyte': r'\exa\byte',
    'hertz':   r'\hertz',
    'kilohertz':r'\kilo\hertz',
    'megahertz':r'\mega\hertz',
    'millisecond':  r'\milli\second',
    'microsecond':  r'\micro\second',
    'second':  r'\second',
    'day' :    r'\day',
    'year':    r'\year',
    'meter':   r'\meter',
    'millimeter':   r'\milli\meter',
}    
    

def wash_latex(flat):
    flat = dict(flat)           # copy
    ret = dict()

    # truncate some numbers to facilitiate nicer formatting
    flat['daq_fs_readout_size'] = np.round(flat['daq_fs_readout_size'], 1)
    flat['daq_fs_readout_rate'] = np.round(flat['daq_fs_readout_rate'], 1)
    flat['daq_fs_readout_size_second'] = np.round(flat['daq_fs_readout_size_second'], 2)
    flat['daq_fs_readout_size_minute'] = np.round(flat['daq_fs_readout_size_minute'], 3)
    flat['daq_fs_readout_size_year'] = np.round(flat['daq_fs_readout_size_year'], 1)

    for k,v in flat.items():
        if type(v) == float or type(v) == int:
            ret[k] = r'\num{%s}' % v
            continue

        m = v.magnitude
        u = str(v.units)
        l = ' / '.join([pint2latex[p.strip()] for p in u.split('/')])
        ret[k] = r'\SI{%s}{%s}' % (m,l)
    return ret

import os.path as osp
mydir=osp.dirname(__file__)

def latex_fundamental_table(washed):
    t = r'''
\begin{{tabular}}[h]{{l|r}}
\hline
Full height & {tpc_full_height} \\
Full width & {tpc_full_width} \\
Full length & {tpc_full_length} \\
detectors & {daq_number_detectors} \\
\hline
channel/APA & {daq_channels_per_apa} \\
APA/detector & {daq_apa_per_detector} \\
Active height (APA) & {tpc_height} \\
Active width (APA) & {tpc_width} \\
Drift distance & {tpc_drift_distance} \\
Voltage & \SI{{500}}{{\volt}} \\
\hline
Drift velocity & {tpc_drift_velocity} \\
Drift time & {tpc_drift_time} \\
\hline
bytes/sample & \num{{12}}/\num{{8}} \\
sample rate & {daq_sample_rate} \\
\# drifts/readout & {daq_drifts_per_readout} \\
\hline
readout time & {daq_readout_time} \\
samples/readout & {daq_readout_channel_samples} \\
\hline
\end{{tabular}}
'''.format(**washed)
    with open(osp.join(mydir,'fundamental-table.tex'), 'w') as fp:
        fp.write(t)
    return t
    
    pass

def latex_full_stream_table(washed):
    t = r'''
  \begin{{tabular}}[h]{{l r}}
\hline
% 23.56992 TiB
FS readout size & {daq_fs_readout_size}\\
FS second & {daq_fs_readout_size_second}\\
FS minute & {daq_fs_readout_size_minute}\\
FS year & {daq_fs_readout_size_year}\\
\hline
  \end{{tabular}}
'''.format(**washed)
    with open(osp.join(mydir,'full-stream-table.tex'), 'w') as fp:
        fp.write(t)
    return t


def test():
    params = load()
    dump(params)

    flat = flatten(params)
    washed = wash_latex(flat)
    latex_fundamental_table(washed)
    latex_full_stream_table(washed)


if '__main__' == __name__:
    test()
