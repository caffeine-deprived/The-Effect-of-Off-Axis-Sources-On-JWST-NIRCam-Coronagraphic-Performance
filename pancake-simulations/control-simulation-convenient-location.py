""" 
Klaus Stephenson
Created February, 2024

Description: A custom PanCAKE script utilized as a control scenario for a lot of the magnitude sensitivity loss calculations performed
"""
if __name__ == '__main__':
    import pancake
    import matplotlib.pyplot as plt
    import math
    target = pancake.scene.Scene('Target')
    target.add_source('HIP 65426', kind='simbad') #on-axis target source
    reference = pancake.scene.Scene('Reference')
    reference.add_source('HIP 65426', kind='simbad') #on-axis reference soruce
    #no planet
    seq = pancake.sequence.Sequence()
    seq.add_observation(target, exposures=[('F444W', 'DEEP8', 18, 5 )], nircam_mask='MASK335R', rolls=[0])
    seq.add_observation(reference, exposures=[('F444W', 'DEEP8', 18, 5)], nircam_mask='MASK335R', scale_exposures=target)
    
    results = seq.run(save_file='./control-scenario.fits', ta_error='saved') 
    pancake.analysis.contrast_curve(results, target='Target',references='Reference',  subtraction='RDI', save_prefix=('control-scenario-RDI-subtraction'), klip_subsections=10, klip_annuli=10, sub_only=False,regis_err='saved')
    #'sub-only' paramenter causes contrast curve function to skip the contrast calculation and only do the subtraction, saving runtime

    