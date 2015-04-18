#!/usr/bin/env python3

from pint import UnitRegistry

units = UnitRegistry()
Q = units.Quantity


# chapter 2 lbne-fd-closeout
sample_rate = Q('2 MHz')
drift_distance = Q('3.41 m')
apa_height = Q('6 meter')
apa_width = Q('2.3 meter')
apa_volume = drift_distance * apa_height * apa_width
apa_top_surface = drift_distance * apa_width

# this is constant and set to lbne-fd-closeout value!
lbne_apa_top_surface = Q('3.41 m')*Q('2.3 meter')
lbne_apa_volume = Q('3.41 m')*Q('6 meter')*Q('2.3 meter')

# docdb 3383
drift_velocity = Q('1.6 mm/microsecond')

# giles
number_drifts = 2.4

drift_time = drift_distance / drift_velocity
readout_time = number_drifts * drift_time.to('ms')
samples_per_readout_per_channel = int(sample_rate * readout_time)

print 'Sample rate = %s' % sample_rate.to('MHz')
print 'Drift distance = %s' % drift_distance.to('meter')
print 'Drift velocity = %s' % drift_velocity.to('millimeter/microsecond')
print 'Drift time = %s' % drift_time.to('ms')
print 'Number of drifts = %s' % number_drifts
print 'Readout time = %s' % readout_time.to(units.millisecond)
print 'Samples/readout/channel = %s' % samples_per_readout_per_channel


bytes_per_sample = Q('12 bits').to('byte')
channels_per_APA = 2560
APA_per_detector = 150
number_detectors = 4

channels = channels_per_APA * APA_per_detector * number_detectors 
readout_size = bytes_per_sample * channels* samples_per_readout_per_channel
readout_rate = readout_size / readout_time.to('second')

print 'Channels = %s' % channels
print 'Readout size = %s' % readout_size.to('gigabyte')
print 'Readout rate = %s' % readout_rate.to('terabyte/second')
print 'Readout rate = %s' % readout_rate.to('terabyte/minute')
print 'Readout rate = %s' % readout_rate.to('exabyte/year')


beam_rep_rate = Q('1 Hz')
beam_run_fraction = Q('2e7 seconds/year')
beam_event_size = Q('10 megabyte')
# 40kton, oscillated from table  4.1 of sci opp
beam_number_high_events = Q('40000/year') 

beam_high_data = beam_event_size * beam_number_high_events
print 'High energy beam data = %s' % beam_high_data.to('gigabyte/year')

beam_all_data = readout_size * beam_rep_rate * beam_run_fraction
print 'Full-stream in-spill data = %s' % beam_all_data.to('petabyte/year')

# beta=Ar39 from lbne-fd-closeout
rad_beta_rate_density = Q('63 kHz') / lbne_apa_volume
rad_beta_rate_apa = rad_beta_rate_density * apa_volume
rad_beta_event_size = 24 * bytes_per_sample
print 'Rad(beta) event size = %s' % rad_beta_event_size
rad_beta_data_rate_apa = rad_beta_rate_apa * rad_beta_event_size
print 'Rad(beta) data rate (per APA) = %s' % rad_beta_data_rate_apa.to('megabyte/second')
rad_beta_readout_apa = rad_beta_data_rate_apa * readout_time
print 'Rad(beta) readout (per APA) = %s' % rad_beta_readout_apa.to('kilobyte')
print 'Rad(beta) data rate (per APA) = %s' % rad_beta_data_rate_apa.to('megabyte/second')
print 'Rad(beta) data rate (per APA) = %s' % rad_beta_data_rate_apa.to('terabyte/year')

rad_beta_readout = rad_beta_readout_apa * APA_per_detector * number_detectors
print 'Rad(beta) readout (40kt) = %s' % rad_beta_readout.to('megabyte')
rad_beta_data_rate = rad_beta_data_rate_apa * APA_per_detector * number_detectors
print 'Rad(beta) data rate (40kt) = %s' % rad_beta_data_rate.to('gigabyte/second')
print 'Rad(beta) data rate (40kt) = %s' % rad_beta_data_rate.to('petabyte/year')

# cosmics
cosmic_muon_rate_flux_apa = Q('6e-7 kHz') /  lbne_apa_top_surface
cosmic_muon_rate_apa = cosmic_muon_rate_flux_apa * apa_top_surface
cosmic_muon_event_size = 5e4 * bytes_per_sample
cosmic_muon_data_rate_apa = cosmic_muon_rate_apa * cosmic_muon_event_size

print 'Cosmic muon event size = %s' % cosmic_muon_event_size.to('kilobyte')
print 'Cosmic muon rate (per APA) = %s ' %  cosmic_muon_data_rate_apa.to('bytes/second')
cosmic_muon_data_rate = cosmic_muon_data_rate_apa * APA_per_detector * number_detectors
print 'Cosmic muon data rate (40kT) = %s ' %  cosmic_muon_data_rate.to('kilobyte/second')
print 'Cosmic muon data rate (40kT) = %s ' %  cosmic_muon_data_rate.to('gigabyte/year')
