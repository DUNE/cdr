#!/usr/bin/env python3

from pint import UnitRegistry

units = UnitRegistry()
Q = units.Quantity

def tpc_params():
    '''
    TPC related parameters
    '''
    d = dict(
        # docdb 3383
        tpc_drift_distance = Q('3.41 m'),
        tpc_height = Q('6 meter'),
        tpc_width = Q('2.3 meter'),
        tpc_drift_velocity = Q('1.6 mm/microsecond')
    )
    d['tpc_top_surface'] = d['tpc_drift_distance'] * d['tpc_width']    
    d['tpc_volume'] = d['tpc_top_surface'] * d['tpc_height']

    d['tpc_drift_time'] = (d['tpc_drift_distance'] / d['tpc_drift_velocity']).to('millisecond')
    return d

def tpc_params_lbne():
    '''
    TPC related parameters for lbne-fd-closeout TPC
    '''
    d = dict(
        tpc_drift_lbne = Q('3.41 m'),
        tpc_height_lbne = Q('6 meter'),
        tpc_width_lbne = Q('2.3 meter'),
    )
    d['tpc_top_surface_lbne'] = d['tpc_drift_lbne'] * d['tpc_width_lbne']    
    d['tpc_volume_lbne'] = d['tpc_top_surface_lbne'] * d['tpc_height_lbne']
    return d

def daq_params(tpc):
    '''
    DAQ related basic parameters.  Needs TPC parameters
    '''
    d = dict(
        # chapter 2 lbne-fd-closeout
        daq_sample_rate = Q('2 MHz'),
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
    
    d['daq_fs_readout_size'] =(d['daq_bytes_per_sample'] * d['daq_channels'] * d['daq_readout_channel_samples']).to('gigabyte')
    d['daq_fs_readout_rate'] = (d['daq_fs_readout_size'] / d['daq_readout_time']).to('terabyte/second')
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

def beta_params(tpc, daq, lbne):
    'Beta radioactivity from Ar39'
    # beta=Ar39 from lbne-fd-closeout
    d = dict(
        beta_rate_apa = Q('63 kHz') / lbne['tpc_volume_lbne'] * tpc['tpc_volume'],
        beta_event_size = 24 * daq['daq_bytes_per_sample'],
    )
    d['beta_rate'] = (d['beta_rate_apa'] * daq['daq_number_apas']).to('megahertz')
    d['beta_data_rate_apa'] = (d['beta_rate_apa'] * d['beta_event_size']).to('megabyte/second')
    d['beta_data_rate'] = (d['beta_data_rate_apa'] * daq['daq_number_apas']).to('gigabyte/second')
    d['beta_readout_size_apa'] = (d['beta_data_rate_apa'] * daq['daq_readout_time']).to('kilobyte')
    d['beta_readout_size'] = (d['beta_readout_size_apa'] * daq['daq_number_apas']).to('megabyte')
    return d

def cosmics_param(tpc, daq, lbne):
    # cosmics
    d = dict(
        cosmic_muon_rate_apa = Q('6e-7 kHz') /  lbne['tpc_top_surface_lbne'] * tpc['tpc_top_surface'],
        cosmic_muon_event_size = (5e4 * daq['daq_bytes_per_sample']).to('kilobyte'),
    )

    d['cosmic_muon_data_rate_apa'] = (d['cosmic_muon_rate_apa'] * d['cosmic_muon_event_size']).to('byte/second')
    d['cosmic_muon_data_rate'] = (d['cosmic_muon_data_rate_apa'] * daq['daq_number_apas']).to('kilobyte/second')
    return d

def load():
    d = dict(
        tpc = tpc_params(),
        lbne = tpc_params_lbne()
    )
    d['daq'] = daq_params(d['tpc'])
    d['beam'] = beam_params(d['daq'])
    d['beta'] = beta_params(d['tpc'], d['daq'], d['lbne'])
    d['cosmic'] = cosmics_param(d['tpc'], d['daq'], d['lbne'])
    return d

def flatten(d):
    ret = dict()
    for v in d.values():
        ret.update(d)
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
    
def test():
    p = load()
    dump(p)

if '__main__' == __name__:
    test()
