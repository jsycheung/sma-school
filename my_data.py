myvis = 'group_1_bin32.ms'
out = listobs(myvis)
titan = 'Titan' # Titan shouldn't be resolved, but the amp vs uvdist shows it's resolved because it resolves part of saturn (titan is only 30" away from Saturn which is also inside the beam)
# if you inspect amp vs channel the amp is also not that flat. 
# can look at observing log
# should have used staralt http://catserver.ing.iac.es/staralt/
# variable names for the sources are case sensitive
flux = 'mwc349a'

bpcal= '3c84'

# Gain calibrators
# NOTE: SMA observations often have 2 gain calibrators. If you only have one, comment out `pcal2' and remove its
# use in `bothpcal`. Similarly, you *could* have more than two, in which case add a `pcal3` and add to `bothpcal`
#  ppropriate!
# For G34
pcal1 = '1743-038'

# For SDC
pcal2= '1924-292'
# A variable to use both gain cals
bothpcal = f"{pcal1},{pcal2}"

# A variable with all the calibrator names for convenience later
calfields= ",".join([bpcal, bothpcal, flux])

# If you have more than 1 science field, separate the source names by a comma in the string.
science_fields = 'G34.30+0.20,SDC35.063-0.726_1'
science_jas = science_fields.split(',')[0]
science_naomi = science_fields.split(',')[1]

# flagmanager(myvis, mode='restore', versionname='original.old.1684270218')

# plotms(vis=myvis, xaxis='channel', yaxis='amp',field=titan, avgtime='1e8', avgscan=False,
#        coloraxis='ant1',iteraxis='spw', ydatacolumn='data',
#        gridrows=4, gridcols=3, yselfscale=True)


# plotms(vis=myvis, xaxis='UVdist', yaxis='amp',field=titan, avgtime='1e8', avgchannel='1000',
#        coloraxis='ant1',iteraxis='spw', ydatacolumn='data',
#        gridrows=4, gridcols=3, yselfscale=True)

# plotms(vis=myvis, xaxis='channel',
#        yaxis='amp',field=bpcal, avgtime='1e8', avgscan=False,
#        coloraxis='Corr',iteraxis='spw', ydatacolumn='data',
#        gridrows=4, gridcols=3, yselfscale=True)
       #Then we see a flat spectrum of amp against channel, can flag some outliers

# What if i forgot to save original? how do i revert? USE unflag

# flagmanager(vis=myvis, mode='save', versionname='original')

# flagdata(vis=myvis, mode='manual', spw='2:305', antenna='Ant4&Ant6', correlation='XX', flagbackup=False)
# flagdata(vis=myvis, mode='manual', spw='2:149', antenna='Ant5&Ant8', correlation='XX', flagbackup=False)
# flagdata(vis=myvis, mode='manual', spw='7:208', antenna='Ant5&Ant8', flagbackup=False)
# flagdata(vis=myvis, mode='manual', spw='1:81', antenna='Ant3&Ant8;Ant5&Ant8', correlation='XX', flagbackup=False)
# mode='unflag' to unflag 
# flagmanager(vis=myvis, mode='save', versionname='bandpass')
# plot amp against time, after avg over channel everything looks fine

import numpy as np
# Factor the data have been downsampled by:
# rechunk = 32

# Original number of channels is 16384 per spw. Divide that by how many we have rechunked.
# chan_num = int(16384 / rechunk)

# Set the fraction of channels to flag at each edge.
# edgechan_frac = 0.025

# Range of channels to flag at the lower edge
# edge_chan_low = int(np.floor(chan_num * edgechan_frac))
# Range of channels to flag at the upper edge
# edge_chan_high = int(np.floor(chan_num * (1. - edgechan_frac)))

# Combine into the format that CASA's flagdata will interpret
# To select all SPWs, we use the "*" wildcard.
# Also note that channel counting starts at "0", so we set the upper limit to be `chan_num-1`
# edgechan = "*:0~{0};{1}~{2}".format(edge_chan_low,
#                                     edge_chan_high, chan_num-1)

# print(edgechan)
# *:0~12;499~511
# flagdata(vis=myvis, mode='manual', spw=edgechan, flagbackup=False)
# flagmanager(vis=myvis, mode='save', versionname='edge_flagging')
flagmanager(vis=myvis, mode='restore', versionname='edge_flagging') # Load completed bandpass flagging

plotms(vis=myvis, xaxis='channel',
       yaxis='amp',field=flux, avgtime='1e8', avgscan=False,
       coloraxis='Corr',iteraxis='spw', ydatacolumn='data',
       gridrows=4, gridcols=3, yselfscale=True)
       # we saw some emission lines, we should just flag those for this particular field i.e. flux calibrator
# remove emission lines (spw3:384,391; spw9:70,78)
flagdata(vis=myvis, mode='manual', field=flux, spw="3:380~395", flagbackup=False)
flagdata(vis=myvis, mode='manual', field=flux, spw="9:65~85", flagbackup=False)


# remove instrumental harmonics (we know because we see it in symmetric spw 1 and 10, and only certain antennas have these, not all)
flagdata(vis=myvis, mode='manual', field=flux, spw="1:84", antenna='Ant3&Ant5', flagbackup=False) # if we see the same anormalities for other cals as well, flag those
flagdata(vis=myvis, mode='manual', field=flux, spw="1:84", antenna='Ant4&Ant8', correlation='YY', flagbackup=False)
flagdata(vis=myvis, mode='manual', field=flux, spw="1:84", antenna='Ant5&Ant8', correlation='YY', flagbackup=False)
flagdata(vis=myvis, mode='manual', field=flux, spw="7:208", antenna='Ant1&Ant8', correlation='YY', flagbackup=False)
flagdata(vis=myvis, mode='manual', field=flux, spw="10:84", antenna='Ant3&Ant5', flagbackup=False)
flagdata(vis=myvis, mode='manual', field=flux, spw="10:84", antenna='Ant5&Ant8', correlation='YY', flagbackup=False)
# we also plotted amp against time and it looks fine

flagmanager(vis=myvis, mode='save', versionname='flux_flagging_amp_channel', comment='amp vs channel')

# now we move on to gain calibrators!
plotms(vis=myvis, xaxis='channel',yaxis='amp',
       field=pcal1,
       avgtime='1e8', avgscan=False,
       coloraxis='Corr',iteraxis='spw', ydatacolumn='data',
       gridrows=4, gridcols=3, yselfscale=True)

flagdata(vis=myvis, mode='manual', spw="4:160", flagbackup=False) 
flagdata(vis=myvis, mode='manual', spw="4:208", flagbackup=False) 
flagdata(vis=myvis, mode='manual', spw="2:273", flagbackup=False)
flagdata(vis=myvis, mode='manual', spw="7:208", flagbackup=False) 
flagdata(vis=myvis, mode='manual', spw="7:160", flagbackup=False) 
flagdata(vis=myvis, mode='manual', spw="1:84", flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='pcal1')

plotms(vis=myvis, xaxis='channel',yaxis='amp',
       field=pcal2,
       avgtime='1e8', avgscan=False,
       coloraxis='Corr',iteraxis='spw', ydatacolumn='data',
       gridrows=4, gridcols=3, yselfscale=True)

flagdata(vis=myvis, mode='manual', spw="10:84", flagbackup=False)
flagmanager(vis=myvis, mode='save', versionname='pcal2')

# setjy
from casatools import table, msmetadata
msmd.open(myvis)
scan_idx = msmd.scannumbers()[0]
all_spws = msmd.spwsforscan(scan_idx)
mean_freq = np.mean([np.mean(msmd.chanfreqs(spw_idx)) for spw_idx in all_spws])
msmd.close()

#the flux we found in the sma calibrator list
flux_stokesI = 2.06

setjy(vis=myvis, field=flux, spw='',
       fluxdensity=[flux_stokesI, 0, 0, 0],
       reffreq=f"{mean_freq/1e9}GHz",
       scalebychan=True,
       standard='manual',
       usescratch=False)

# calibration setup
refant = 'Ant1'

min_solint = 'int'

# phase-only selfcal for bandpass calibrator. because it is point source and bright, phase is 0
phaseshortgaincal_table = '{0}.bpself.gcal'.format(myvis)
if os.path.exists(phaseshortgaincal_table):
    os.system(f'rm -rf {phaseshortgaincal_table}')

gaincal(vis=myvis,caltable=phaseshortgaincal_table,
        field=bpcal,spw="",refant=refant, scan="",
        calmode='p',
        solint=min_solint,
        minsnr=2.0, minblperant=3,
        gaintable=[])

# Plot the table to inspect the calibration solution
plotms(vis=phaseshortgaincal_table,
       xaxis='time',
       yaxis='phase',
       coloraxis='spw',
       iteraxis='antenna',
       ydatacolumn='data',
       gridrows=3, gridcols=3,
       yselfscale=True,
       xconnector='line', timeconnector=True)

# Syntax is: time avg., freq avg.
bpsolint = 'inf,4ch'
bandpass_table = '{0}.bandpass.solnorm_true.bcal'.format(myvis)
if os.path.exists(bandpass_table):
    os.system(f'rm -rf {bandpass_table}')

# smooth some channels CHECK SMOOTHING WINDOW, fit the soln
bandpass(vis=myvis,caltable=bandpass_table,
         bandtype='B', scan="",
         field=bpcal, spw="",
         combine='scan,field',
         refant=refant,
         solint=bpsolint, solnorm=True, minblperant=3,
         fillgaps=10,  # If some channels are flagged above, interpolate over in the BP
         gaintable=[phaseshortgaincal_table])

plotms(vis=bandpass_table,xaxis='freq',
       yaxis='phase',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       gridrows=3, gridcols=3,
       yselfscale=True,)

plotms(vis=bandpass_table,xaxis='freq',
       yaxis='amp',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       gridrows=3, gridcols=3,
       yselfscale=True,)
       # we can see some drop off because we didn't flag all edges

plotms(vis=bandpass_table,xaxis='freq',
       yaxis='amp',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       gridrows=3, gridcols=3,
       yselfscale=True,)

#phase gain calibration
# per-int phase with combining spws across sidebands.
gain_phase_int_table = '{0}.intphase_combinespw.gcal'.format(myvis)
# Receiver 1:
gaincal(vis=myvis,caltable=gain_phase_int_table,
        field=calfields,refant=refant,
        combine='spw',spw='0~5',
        calmode='p',solint=min_solint,minsnr=2.0,minblperant=3,
        gaintable=[bandpass_table])
# Note the same `caltable` name with `append=True`
# Receiver 2:
gaincal(vis=myvis,caltable=gain_phase_int_table, append=True,
        field=calfields, refant=refant,
        combine='spw',spw='6~11',
        calmode='p',solint=min_solint,minsnr=2.0,minblperant=3,
        gaintable=[bandpass_table])

plotms(vis=gain_phase_int_table,xaxis='time',
       yaxis='phase',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       xconnector='line', timeconnector=True,
       gridrows=3, gridcols=3,
       yselfscale=True)
       # good, smooth phase variation against time

# we make another phase gain solution this time average over longer time
long_solint = '300s'
gain_phase_scan_table = '{0}.scanphase_combinespw.gcal'.format(myvis)
# Receiver 1:
gaincal(vis=myvis,caltable=gain_phase_scan_table,
        field=calfields,refant=refant,
        combine='spw',spw='0~5',
        calmode='p',solint=long_solint,minsnr=2.0,minblperant=3,
        gaintable=[bandpass_table])
# Receiver 2:
# Note the same `caltable` name with `append=True`
gaincal(vis=myvis,caltable=gain_phase_scan_table, append=True,
        field=calfields, refant=refant,
        combine='spw',spw='6~11',
        calmode='p',solint=long_solint,minsnr=2.0,minblperant=3,
        gaintable=[bandpass_table])
plotms(vis=gain_phase_scan_table, xaxis='time',
       yaxis='phase',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       xconnector='line', timeconnector=True,
       gridrows=3, gridcols=3,
       yselfscale=True)
       # good, some phase jump towards the end by nothing too crazy

# amplitude gain calibration
this_spwmap = [0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6 ,6]
# we apply phase correction before solving for amp gain
amp_solint = '10min'

gain_amp_scan_table = '{0}.amp.gcal'.format(myvis)

gaincal(vis=myvis,caltable=gain_amp_scan_table,
        field=calfields, spw="", refant=refant,
        combine='',
        spwmap=[[],this_spwmap],
        calmode='a', solint=amp_solint, minsnr=3.0, minblperant=3,
        gaintable=[bandpass_table,
                   gain_phase_int_table])

plotms(vis=gain_amp_scan_table, xaxis='time',
       yaxis='amp',
       coloraxis='spw',iteraxis='antenna',ydatacolumn='data',
       xconnector='line', timeconnector=True,
       gridrows=3, gridcols=3,
       yselfscale=True)

plotms(vis=gain_amp_scan_table,
       xaxis='freq', yaxis='amp',
       coloraxis='field',iteraxis='antenna', ydatacolumn='data',
       xconnector='line', timeconnector=True,
       gridrows=3, gridcols=3,
       yselfscale=True)

# absolute flux calibration
# Apply to all calibrators except the flux calibrator itself.
transfer_fields = [bpcal, bothpcal]

fluxboot_table = '{0}.flux.cal'.format(myvis)
       
fluxresults = fluxscale(vis=myvis,
                        caltable=gain_amp_scan_table,
                        refspwmap=[-1],
                        transfer=transfer_fields,
                        fluxtable=fluxboot_table,
                        reference=flux,
                        fitorder=1,
                        incremental=False)
flagmanager(vis=myvis, mode='save', versionname='beforeapplycal')

# Apply calibrator solutions
# apply to bpcal
applycal(vis=myvis,field=bpcal,
         spw="",
         gaintable=[bandpass_table,
                    gain_phase_int_table,
                    fluxboot_table], # This order for tables is reflected in `interp`, `spwmap`, and `gainfield`
         interp=['linear,linearflag',
                 'linear,linear',
                 'nearest,linear'], # for each field, this is how to average/interpolate the solutions in "time,freq"
         spwmap=[[], this_spwmap, []],
         gainfield=[bpcal, bpcal, bpcal],
         flagbackup=False,
         calwt=False)
# apply to two gain calibrators
for pcal in bothpcal.split(","):

    applycal(vis=myvis,field=pcal,
            spw="",
            gaintable=[bandpass_table,
                       gain_phase_int_table,
                       fluxboot_table],
            interp=['linear,linearflag',
                    'linearPD,linear',
                    'nearest,linear'],
            spwmap=[[], this_spwmap, []],
            gainfield=[bpcal, pcal, pcal],
            flagbackup=False, calwt=False)

# apply to flux calibrators
applycal(vis=myvis,field=flux,
         spw="",
         gaintable=[bandpass_table,
                    gain_phase_int_table,
                    fluxboot_table],
         interp=['nearest','nearestPD','nearest'],
         spwmap=[[], this_spwmap, []],
         gainfield=[bpcal, flux, flux],
         flagbackup=False, calwt=False)

# apply to science fields
applycal(vis=myvis,field=science_fields,
        spw="",
        gaintable=[bandpass_table,
                   gain_phase_scan_table,
                   fluxboot_table],
        interp=['linear,linearflag',
                'linearPD,linear',
                'linear,linear'],
        spwmap=[[], this_spwmap, []],
        gainfield=[bpcal, bothpcal, bothpcal],
        flagbackup=False, calwt=False,
        applymode='calflagstrict')
flagmanager(vis=myvis, mode='save', versionname='afterapplycal')

# inspect calibrated data
plotms(vis=myvis, xaxis='channel',
       yaxis='amp',field=bpcal, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # flat spectrum, good

plotms(vis=myvis, xaxis='channel',
       yaxis='phase',field=bpcal, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # centered at zero, not bad

plotms(vis=myvis, xaxis='time', yaxis='amp',
       field=bpcal,
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # amp vs time approximately constant, the scatter is due to the edge channels

plotms(vis=myvis, xaxis='uvdist', yaxis='amp',
       field=bpcal,
       avgchannel='2048', avgtime='300',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # constant, FT of delta function is constant in visibility space

plotms(vis=myvis, xaxis='channel',
       yaxis='amp',field=pcal1, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)

plotms(vis=myvis, xaxis='channel',
       yaxis='phase',field=pcal1, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # why so scattered? but if i average over channels it is not too bad. if average is centered zero, just that it's not very bright
plotms(vis=myvis, xaxis='time', yaxis='amp',
       field=pcal1,
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='uvdist', yaxis='amp',
       field=pcal1,
       avgchannel='2048', avgtime='300',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)

plotms(vis=myvis, xaxis='channel',
       yaxis='amp',field=pcal2, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='channel',
       yaxis='phase',field=pcal2, avgtime='1e8', avgscan=False,
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='time', yaxis='amp',
       field=pcal2,
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='uvdist', yaxis='amp',
       field=pcal2,
       avgchannel='2048', avgtime='300',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
# for flux cal
plotms(vis=myvis, xaxis='uvdist', yaxis='amp',
       field=flux,
       avgchannel='2048', avgtime='600',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
       # the flux cal is a star, not solar system object, amp vs uvdist is constant
# inspect targets
plotms(vis=myvis, xaxis='freq',
       yaxis='amp',field=science_fields,
       avgtime='1e8', avgscan=True, avgbaseline=True,
       spw='',
       coloraxis='spw', ydatacolumn='corrected',
       gridrows=1, gridcols=1)
plotms(vis=myvis, xaxis='freq',
       yaxis='amp',field='G34.30+0.20',
       avgtime='1e8', avgscan=True, avgbaseline=True,
       spw='',
       coloraxis='spw', ydatacolumn='corrected',
       gridrows=1, gridcols=1)
plotms(vis=myvis, xaxis='freq',
       yaxis='amp',field='SDC35.063-0.726_1',
       avgtime='1e8', avgscan=True, avgbaseline=True,
       spw='',
       coloraxis='spw', ydatacolumn='corrected',
       gridrows=1, gridcols=1)
       # saw a line around 231 GHz
plotms(vis=myvis, xaxis='time', yaxis='amp',
       field=science_fields,
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='time', yaxis='amp',
       field='G34.30+0.20',
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)
plotms(vis=myvis, xaxis='time', yaxis='amp',
       field='SDC35.063-0.726_1',
       avgchannel='2048',
       coloraxis='ant1',iteraxis='spw', ydatacolumn='corrected',
       gridrows=4, gridcols=3, yselfscale=True)

# Questions, why sometimes we apply gain phase int table but not gain phase scan table?
# And we don't apply gain amp scan table because it is already in the fluxboot table?
# Why is phase vs channel for pcal1 corrected so scattered?

# tclean, usage of mask is to see if the point is physical or sidelobe
tclean(vis=myvis, field=bpcal, imagename=f'{bpcal}_test',
       imsize=128, cell='0.6arcsec', specmode='mfs',
       weighting='briggs', robust=0., niter=0)
imview(f'{bpcal}_test.image', out=f'{bpcal}_test_image.jpg')
tclean(vis=myvis, field=pcal1, imagename=f'{pcal1}_test',
       imsize=128, cell='0.6arcsec', specmode='mfs',
       weighting='briggs', robust=0., niter=0)
imview(f'{pcal1}_test.image', out=f'{pcal1}_test_image.jpg')
tclean(vis=myvis, field=pcal2, imagename=f'{pcal2}_test',
       imsize=128, cell='0.6arcsec', specmode='mfs',
       weighting='briggs', robust=0., niter=0)

# flag line emission before making continuum image
plotms(vis=myvis, field=science_jas,
       xaxis='Frequency', yaxis='amp',
	   freqframe='LSRK',
       avgtime='1e20', avgscan=True, coloraxis='spw',
	   )
spw_freqstring = '2:230~375,3:345~425,4:140~225,4:260~415, 5:190~265'