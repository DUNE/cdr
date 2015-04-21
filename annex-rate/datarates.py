#!/usr/bin/env python
'''
Estimate data rates.
'''

from dune.params.data import Param
from dune.params.units import Q

def filter(ps):
    '''
    Take a ParamSet, return a new one loaded with derived rate-related parameters.
    '''

    # TPC
    ps.add(Param('tpc_drift_time', ps.tpc_drift_distance / ps.tpc_drift_velocity, 
                 'millisecond', 'Drift time'))

    # DAQ
    ps.add(Param('daq_readout_time', ps.daq_drifts_per_readout * ps.tpc_drift_time,
                 'millisecond', 'DAQ readout time'))
    ps.add(Param('daq_readout_channel_samples', Q(int(ps.daq_sample_rate * ps.daq_readout_time)),
                 '', 'Samples/readout/channel'))
    ps.add(Param('daq_channels_per_detector', Q(int(ps.daq_channels_per_apa * ps.tpc_apa_per_detector)),
                 '', 'Channels per detector'))

    # Global DUNE
    ps.add(Param('dune_number_apas', ps.tpc_apa_per_detector * ps.dune_number_detectors,
                 name='Total number of APAs'))
    
    ps.add(Param('dune_number_channels', Q(int(ps.daq_channels_per_detector * ps.dune_number_detectors)),
                 '', 'Total channels in DUNE'))
    ps.add(Param('dune_fs_readout_size', ps.daq_bytes_per_sample * ps.dune_number_channels * ps.daq_readout_channel_samples,
                 'gigabyte', 'Full-stream DUNE readout size'))
    ps.add(Param('dune_fs_readout_rate', ps.dune_fs_readout_size / ps.daq_readout_time,
                 'terabyte/second', 'Full-stream DUNE readout data rate'))
           
    ps.add(Param('dune_fs_readout_size_second', ps.dune_fs_readout_rate * Q('second'),
                 'terabyte', 'Full-stream DUNE 1 second data volume'))
    ps.add(Param('dune_fs_readout_size_minute', ps.dune_fs_readout_rate * Q('minute'),
                 'petabyte', 'Full-stream DUNE 1 minute data volume'))
    ps.add(Param('dune_fs_readout_size_year', ps.dune_fs_readout_rate * Q('year'),
                 'exabyte', 'Full-stream DUNE 1 year data volume'))

    # Beam related
    ps.add(Param('beam_high_data_rate', ps.beam_event_size * ps.beam_event_occupancy * ps.beam_rep_rate * ps.beam_run_fraction,
                 'gigabyte/year', 'DUNE data rate for beam neutrino interactions'))
    ps.add(Param('beam_fs_data_rate', ps.dune_fs_readout_size * ps.beam_rep_rate * ps.beam_run_fraction,
                 'exabyte/year', 'DUNE full-stream, in-spill data rate'))

    # Cosmics
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

    ps.add(Param('cosmic_muon_rate', ps.dune_number_detectors * ps.tpc_full_width * ps.tpc_full_length * ps.cosmic_muon_flux * ps.cosmic_muon_correction,
                 '1/year', 'DUNE cosmic muon rate'))
    ps.add(Param('cosmic_muon_data_rate', ps.cosmic_muon_rate * ps.cosmic_muon_event_size,
                 'gigabyte/year', 'DUNE cosmic muon data rate'))

    return ps
    
