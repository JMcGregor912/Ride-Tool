import numpy as np

# all numpy arrays here which are sent back on a dictionnary results

# basic calculations with setup values
def basic(setup):
    results = {}
    # wheel loads calc
    results['Wtot'] = np.array([np.sum(setup['Wtot_whl']), np.sum(setup['Wtot_whl'][0:2]), np.sum(setup['Wtot_whl'][2:4]), (np.sum(setup['Wtot_whl'][0:2])/np.sum(setup['Wtot_whl']))*100]) # total load [total, FA, RA, %FA], kg
    results['WunSusp'] = np.array([np.sum(setup['WunSusp_whl']), np.sum(setup['WunSusp_whl'][0:2]), np.sum(setup['WunSusp_whl'][2:4]), (np.sum(setup['WunSusp_whl'][0:2])/np.sum(setup['WunSusp_whl']))*100]) # unsuspended masses [total, FA, RA, %FA], kg
    results['WSusp_whl'] = (np.subtract(setup['Wtot_whl'], setup['WunSusp_whl'])) # suspended masses at wheel [FL, FR, RL, RR], kg
    results['WSusp'] = np.array([np.sum(results['WSusp_whl']), np.sum(results['WSusp_whl'][0:2]), np.sum(results['WSusp_whl'][2:4]), (np.sum(results['WSusp_whl'][0:2])/np.sum(results['WSusp_whl']))*100]) # suspended masses [total, FA, RA, %FA], kg
    return results

# calculattions of the ride values
def ride_numbers(setup):
    results = {}
    # ride rates calc
    results['WhlRate'] = (setup['SprRate']*setup['MRdpr']**2) # wheel rate [FA, RA], N/mm
    results['WhlRate_IncTire'] = (results['WhlRate']*setup['TireRate']) / (results['WhlRate']+setup['TireRate']) # wheel rate inc. tire [FA, RA], N/mm

    # rolling torques [FA, RA, %FA]
    results['RollingTorqueSpr'] = ( (setup['Track']**2 * np.tan(1*np.pi/180) * results['WhlRate']) / 2 ) / 1000 # rolling torque due to springs (no tire), Nm/deg
    results['RollingTorqueSpr_IncTire'] = ( (setup['Track']**2 * np.tan(1*np.pi/180) * results['WhlRate_IncTire']) / 2 ) / 1000 # rolling torque due to springs inc. tire, Nm/deg
    results['RollingTorqueArb'] = (setup['Track']**2 * np.tan(1*np.pi/180) * (setup['ArbRate']*setup['MRarb']**2)) / 1000 # rolling torque due to anti roll bars, Nm/deg
    
    results['RollingTorqueTot'] = results['RollingTorqueSpr'] + results['RollingTorqueArb'] # total rolling torque (no tire), Nm/deg
    to_the_FA = results['RollingTorqueTot'][0] / (results['RollingTorqueTot'][0] + results['RollingTorqueTot'][1]) * 100 # repartition on the FA, %FA
    results['RollingTorqueTot'] = np.append(results['RollingTorqueTot'], to_the_FA) # [FA, RA, %FA]

    results['RollingTorqueTot_IncTire'] = results['RollingTorqueSpr_IncTire'] + results['RollingTorqueArb'] # total rolling torque inc. tire, Nm/deg
    to_the_FA = results['RollingTorqueTot_IncTire'][0] / (results['RollingTorqueTot_IncTire'][0] + results['RollingTorqueTot_IncTire'][1]) * 100 # repartition on the FA, %FA
    results['RollingTorqueTot_IncTire'] = np.append(results['RollingTorqueTot_IncTire'], to_the_FA) # [FA, RA, %FA]

    return results