#!/usr/bin/env python
'''
Estimate data rates.
'''

import numpy as np

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
    ps.add(Param('daq_readout_channel_samples', (ps.daq_sample_rate * ps.daq_readout_time).to_base_units(),
                 '', 'Samples/readout/channel', precision=0))
    ps.add(Param('daq_channels_per_detector', (ps.daq_channels_per_apa * ps.tpc_apa_per_detector).to_base_units(),
                 '', 'Channels per detector', precision=0))

    # Global DUNE
    ps.add(Param('dune_number_apas', ps.tpc_apa_per_detector * ps.dune_number_detectors,
                 name='Total number of APAs'))
    ps.add(Param('dune_detector_mass', ps.tpc_detector_mass * ps.dune_number_detectors,
                 'kilotonne', name='Total fiducial mass', precision=0))

    ps.add(Param('dune_number_channels', ps.daq_channels_per_detector * ps.dune_number_detectors,
                 '', 'Total channels in DUNE', precision=0))


    ps.add(Param('dune_fs_readout_size', (ps.daq_bytes_per_sample * ps.dune_number_channels * ps.daq_readout_channel_samples).to('gigabyte'),
                 'gigabyte', 'Full-stream readout size', precision=1))
    ps.add(Param('dune_fs_readout_rate', ps.dune_fs_readout_size / ps.daq_readout_time,
                 'terabyte/second', 'Full-stream readout data rate', precision=1))
           
    ps.add(Param('dune_fs_readout_size_second', ps.dune_fs_readout_rate * Q('second'),
                 'terabyte', 'Full-stream 1 second data volume', precision=1))
    ps.add(Param('dune_fs_readout_size_minute', ps.dune_fs_readout_rate * Q('minute'),
                 'terabyte', 'Full-stream 1 minute data volume', precision=1))
    ps.add(Param('dune_fs_readout_size_year', ps.dune_fs_readout_rate * Q('year'),
                 'exabyte', 'Full-stream 1 year data volume', precision=1))

    # Beam related
    ps.add(Param('beam_rep_rate', 1.0/ps.beam_spill_cycle,
                 'hertz', 'Beam spill repetition rate', precision=2))
    ps.add(Param('beam_rate', ps.beam_event_occupancy * ps.beam_rep_rate * ps.beam_run_fraction,
                 '1/year', 'Beam neutrino interaction rate', precision=0))

    ps.add(Param('beam_data_rate_fs', ps.beam_rate * ps.dune_fs_readout_size, 
                 'megabyte/second', 'FS readout rate for events with beam interactions', precision=0))
    ps.add(Param('beam_data_year_fs', ps.beam_data_rate_fs * Q('year'),
                 'terabyte', 'Annual FS readout volume for events with beam interactions', precision=0))

    ps.add(Param('beam_high_data_rate', ps.beam_event_size * ps.beam_rate,
                 'kilobyte/second', 'Data rate for beam neutrino interactions', precision=2))
    ps.add(Param('beam_high_data_year', ps.beam_high_data_rate * Q('year'),
                 'gigabyte', 'Annual beam neutrino data volume', precision=0))
    ps.add(Param('beam_fs_data_rate', ps.dune_fs_readout_size * ps.beam_rep_rate * ps.beam_run_fraction,
                 'petabyte/year', 'Full-stream in-spill data rate', precision=0))

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
                 'hertz', 'Cosmic muon event rate', precision=3))
    ps.add(Param('cosmic_muon_data_rate', ps.cosmic_muon_rate * ps.cosmic_muon_event_size,
                 'kilobyte/second', 'Cosmic muon data rate', precision=1))
    ps.add(Param('cosmic_muon_data_year', ps.cosmic_muon_data_rate * Q('year'),
                 'gigabyte', 'Annual cosmic muon data volume', precision=0))

    # Ar39 beta
    ps.add(Param('beta_readout_size', ps.beta_event_size * ps.daq_bytes_per_sample,
                 'byte', 'Ar39 readout size', precision=0))

    ps.add(Param('beta_rate', ps.beta_rate_apa * ps.dune_number_apas, 
                 'megahertz', 'Ar39 event rate', precision=1))

    ps.add(Param('beta_data_rate', ps.beta_rate * ps.beta_readout_size,
                 'gigabyte/second', 'Ar39 data rate', precision=1))

    ps.add(Param('beta_data_year', ps.beta_data_rate * Q('year'),
                 'petabyte', 'Annual Ar39 data volume', precision=0))


    # SNB
    ps.add(Param('snb_event_size_fs', ps.dune_fs_readout_rate * ps.snb_readout_time,
                 'terabyte', 'SNB FS event size', precision=1))
    ps.add(Param('snb_data_rate_fs', ps.snb_event_size_fs * ps.snb_rate,
                 'megabyte/second', 'SNB FS data rate', precision=1))
    ps.add(Param('snb_data_year_fs', ps.snb_data_rate_fs * Q('year'),
                 'terabyte', 'Annual SNB FS data volume', precision=0))

    ps.add(Param('snb_event_size_zs', ps.beta_data_rate * ps.snb_readout_time,
                 'gigabyte', 'SNB ZS event size', precision=1))
    ps.add(Param('snb_data_rate_zs', ps.snb_event_size_zs * ps.snb_rate,
                 'byte/second', 'SNB ZS data rate', precision=0))
    ps.add(Param('snb_data_year_zs', ps.snb_data_rate_zs * Q('year'),
                 'gigabyte', 'Annual SNB ZS data volume', precision=0))




    return ps
    
