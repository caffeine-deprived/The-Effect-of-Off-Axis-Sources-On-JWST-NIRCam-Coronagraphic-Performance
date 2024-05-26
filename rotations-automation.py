""" 
Klaus Stephenson
Created March, 2024

Description: An automated PanCAKE script utilized to generate simulations of off-axis reference sources at different rotations and arcsecond separations
"""
def run_simulation(r_value, relative_brightness, theta):
    # Naming variables dynamically based on relative brightness and 'r' value
    save_file = f"./no-planet-R{r_value}-RB{relative_brightness:.0e}-Theta{theta}.fits"
    save_prefix = f"no-planet-R{r_value}-RB{relative_brightness:.0e}-Theta{theta}-RDI-subtraction"

    print(f'---------------------------------------------------------\n\n \n running no-planet-R{r_value}-RB{relative_brightness:.0e} Theta {theta} \n \n \n---------------------------------------------------------')
    #above line is just to help keep track of progress when this program is left to run overnight
    target = pancake.scene.Scene('Target')
    target.add_source('HIP 65426', kind='simbad')
    reference = pancake.scene.Scene('Reference')
    reference.add_source('HIP 65426', kind='simbad')
    #created this script after the magnitudes automation and realized no need to define it as a function
    reference_magnitude = 6.77
    magnitude = reference_magnitude - 2.5 * math.log10(relative_brightness)

    reference.add_source('Companion', kind='grid', theta = theta, r=r_value, spt='a2v', norm_val=magnitude, norm_unit='vegamag', norm_bandpass='2mass_ks')
    #the specified/dynamic parameters here are the theta value, r, and norm_val

    seq = pancake.sequence.Sequence()
    seq.add_observation(target, exposures=[('F444W', 'DEEP8', 18, 5)], nircam_mask='MASK335R', rolls=[0])
    seq.add_observation(reference, exposures=[('F444W', 'DEEP8', 18, 5)], nircam_mask='MASK335R', scale_exposures=target)

    results = seq.run(save_file=save_file, ta_error='saved')
    pancake.analysis.contrast_curve(results, target='Target', references='Reference', subtraction='RDI', save_prefix=save_prefix, klip_subsections=10, klip_annuli=10, sub_only=False, regis_err='saved')

if __name__ == '__main__':
    import math
    import pancake
    import matplotlib.pyplot as plt
    radii = [0.5, 1, 1.5, 2, 2.5, 3]  # Radial separations from 0.5" to 3" in steps of 0.5
    thetas = [0, 90, 180, 270]  # Different angles
    relative_brightness = 1/100000
    for r_value in radii:
        for theta in thetas:
            run_simulation(r_value, relative_brightness, theta)
