"""
Klaus Stephenson
Created June, 2024

really just including this to be transparent on the uncertainty calculation
"""
import statistics
total_values = [ #for example...
    0.1045173258,
    0.1197968051,
    0.09097746015,
    0.09591501206,
    0.1061126813,
    0.1076961681,
    0.1175152287,
    0.111057207,
    0.1060988829,
    0.1127240509,
    0.3484003842,
    0.1168810651,
    0.1046807468,
    0.09668495506,
    0.09918699414,
    0.1133172438,
    0.09732879698,
    0.09743328393,
    0.09190642834,
    0.09531547874
]

local_values = [
    0.9653930664,
    1.025908589,
    1.014956355,
    1.000495911,
    1.021378517,
    1.046029925,
    1.022139311,
    1.062472343,
    1.044299603,
    0.9834751487,
    1.066926837,
    1.005967855,
    0.9998033047,
    1.007115006,
    1.029605746,
    1.006271362,
    1.011998057,
    0.9883576035,
    0.9570909739,
    0.9515675306
]

# find the standard deviation and mean for each list
local_std_dev = statistics.stdev(local_values)
total_std_dev = statistics.stdev(total_values)
print("Local Standard Deviation:", "{:.4f} mag".format(local_std_dev))
print("Total Standard Deviation:", "{:.4f} mag".format(total_std_dev))
