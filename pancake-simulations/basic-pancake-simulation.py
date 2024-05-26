""" 
Klaus Stephenson
Created September, 2023

Description: A basic PanCAKE script utilized to make individual simulations if say something was improperly calculated, needed double checking,
or if one of the automated scripts forgot something
"""
if __name__ == '__main__':
    import pancake #PanCAKE must currently be called within __name__=='__main__' brackets otherwise will crash
    import matplotlib.pyplot as plt
    import math
    target = pancake.scene.Scene('Target') #initalizing target observation
    target.add_source('HIP 65426', kind='simbad') #inserting on-axis host
    #if an injected planet is needed keep the following 2 lines
    input_file = ''  # where I would input an offline file containing HIP 65426b information
    target.add_source('HIP 65426b', r=1, kind='file', filename=input_file, wave_unit='micron', flux_unit='Jy')  #inserting the planet, 'r=1' indicates that the planet is 1" away from the center of the on-axis host

    reference = pancake.scene.Scene('Reference') #initalizing reference observation
    reference.add_source('HIP 65426', kind='simbad') #inserting on-axis reference source

    seq = pancake.sequence.Sequence() #begin observations
    seq.add_observation(target, exposures=[('F444W', 'DEEP8', 18, 5 )], nircam_mask='MASK335R', rolls=[0]) #target observation, with these specific parameters
    seq.add_observation(reference, exposures=[('F444W', 'DEEP8', 18, 5)], nircam_mask='MASK335R', scale_exposures=target)
    
    results = seq.run(save_file='./example-name.fits', ta_error='saved')
    pancake.analysis.contrast_curve(results, target='Target',references='Reference',  subtraction='RDI', save_prefix=('example-prefix-name'), klip_subsections=10, klip_annuli=10, sub_only=False, regis_err='saved')
    #'sub-only' paramenter causes contrast curve function to skip the contrast calculation and only do the subtraction, saving runtime

    
