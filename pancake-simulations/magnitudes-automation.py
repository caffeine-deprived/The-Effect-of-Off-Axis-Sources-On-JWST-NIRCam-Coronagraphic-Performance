""" 
Klaus Stephenson
Created March, 2024

Description: An automated PanCAKE script utilized to generate simulations of off-axis reference sources at different magnitudes and arcsecond separations
"""

if __name__ == '__main__':
    import pancake
    import matplotlib.pyplot as plt
    import math
    def calculate_magnitude(relative_brightness):
        """
        Args:
            relative_brightness - a fractional number representing the off-axis reference source/'companion' relative brightness relative to on-axis source
        
        Output: 
            magnitude - number in proper magnitude format
        """
        reference_magnitude = 6.77 #since we used HIP65426 with a magnitude of 6.77; this number should be changed to reflect the on-axis source mag
        magnitude = reference_magnitude - 2.5 * math.log10(relative_brightness)
        return magnitude
    
    
    for r in range(0, 7):  # r here is arcsecodn separation, this number is from 0 to 7 because 0/2=0, 1/2=0.5, 2/0.5= 1, etc until 6/2=3. (7 is excluded)
        r_value = r / 2.0 #value of 'r' in steps of 0.5"
        
        for i in range(4, 7):  #the range reflects the magnitude of i, which the inverse of is the relative brightness so 4=1/1000, 5=1/10,000, etc. 
            relative_brightness = 1 / (10 ** i)
            magnitude = calculate_magnitude(relative_brightness)
            #naming variables dynamically based on relative brightness and 'r' value
            save_file = f"./R{r_value}-M{(10 ** i):,}.fits"
            save_prefix = f"R{r_value}-M{(10 ** i):,}-RDI-subtraction"
            print(f'---------------------------------------------------------\n\n \n running R{r_value}-M{(10 ** i):,} \n \n \n---------------------------------------------------------')
            #above line is just to help keep track of progress when this program is left to run overnight
            target = pancake.scene.Scene('Target')
            target.add_source('HIP 65426', kind='simbad')
            reference = pancake.scene.Scene('Reference')
            reference.add_source('HIP 65426', kind='simbad')
            reference.add_source('Companion', kind='grid', r=r_value, spt='a2v', norm_val=magnitude, norm_unit='vegamag', norm_bandpass='2mass_ks')
            seq = pancake.sequence.Sequence()
            seq.add_observation(target, exposures=[('F444W', 'DEEP8', 18, 5 )], nircam_mask='MASK335R', rolls=[0])
            seq.add_observation(reference, exposures=[('F444W', 'DEEP8', 18, 5)], nircam_mask='MASK335R', scale_exposures=target)
            
            results = seq.run(save_file=save_file, ta_error='saved')
            pancake.analysis.contrast_curve(results, target='Target',references='Reference', subtraction='RDI', save_prefix=save_prefix, klip_subsections=10, klip_annuli=10, sub_only=False, regis_err='saved')
            #regis_err='saved' -- PanCAKE simulates realistic aligning of images on sky; When this is saved PanCAKE eliminate the error/discontinuities between alignments
            #'sub-only' parameter causes contrast curve function to skip the contrast calculation and only do the subtraction, saving runtime
