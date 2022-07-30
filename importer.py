import numpy as np
import pandas as pd

#interpolation in panda dataframe with request value y:row1 and y1:row0(-1) and y2:row2(+1)
def interpol_mma(df_x, df_y):
    df_x = np.array(df_x)
    df_y = np.array(df_y)
    y = df_y[0]+(df_x[1]-df_x[0])*(df_y[2]-df_y[0])/(df_x[2]-df_x[0])
    return y

# setup information hard coded
def setup_hc():
    setup = {}
    setup['carinfo'] = "RSR19" # car information
    setup['WB'] = [2522.0] # wheelbase, mm
    setup['Track'] = [1525.0, 1710.0] # track at axle [FA, RA], mm
    setup['RH'] = [51.0, 58.5] # ride height at axle [FA, RA], mm
    setup['RCH'] = [12.42, 38.57] # roll center height [FA, RA], mm
    setup['MRdpr'] = [0.665, 0.812] # motion ratio damper [FA, RA], -
    setup['MRarb'] = [1.052, 0.572] # motion ratio anti roll bar [FA, RA], -
    setup['LoadRad'] = [325.8, 340.3] # loaded radius [FA, RA], mm
    setup['SprRate'] = [240.0, 250.0] # spring stiffness [FA, RA], N/mm
    setup['ArbRate'] = [26.4, 28.9] # anti roll bar rate [FA, RA], N/mm
    setup['TireRate'] = [334.0, 339.0] # tire stiffness [FA, RA], N/mm
    setup['Wtot_whl'] = [339.7, 338.5, 363.7, 345.1] # total masses at wheel [FL, FR, RL, RR], kg
    setup['WunSusp_whl'] = [50.5, 50.5, 50.6, 50.6] # unsuspended masses at wheel [FL, FR, RL, RR], kg
    setup['CoGtot0RH'] = [284.0] # CoG height without any RH, mm
    return setup

# import setup from a txt file --> setup.txt
def setup_txt():
    setup = {}
    # iterate through all the lines
    for line in open('data/setup.txt').readlines():
        if not '=' in line: continue # skip this line if it doesn't look like an assignment
        line = line.replace(" ", "").replace("[", "").replace("]", "") # remove all white spaces and brakets into the line first
        left, right = line.split('=', 1) # split it into left and right pieces
        right = right[0:right.index("#")] # remove everything after comments
        if left != "carinfo":
            right = np.fromstring(right, dtype = float, sep=",") # put it into an array with coma separator
        setup[left] = right # keep it around in a dictionary
    return setup

# anti roll bar csv importer
def anti_roll_bar_csv(axle):
    df = pd.read_csv(f'data/anti_roll_bar_{axle}.csv', sep=";")
    return df

# anti roll bar rate to position identifier into csv
def anti_roll_bar_pos(ArbRate, df_arb):
    df = df_arb.loc[df_arb['Stiffness'] == ArbRate] # put ARB position corresponding to the rate (into setup)
    ArbPos = df.iat[0,0] # save the value
    return ArbPos

# anti roll bar position to rate identifier into csv
def anti_roll_bar_rate(ArbPos, df_arb):
    df = df_arb.loc[df_arb['Setting'] == ArbPos] # put ARB rate corresponding to the position
    ArbRate = df.iat[0,1] # save the value
    return ArbRate

# kinematic csv importer
def kinematic_csv(axle):
    df = pd.read_csv(f'data/kinematic_{axle}.csv', sep=";")
    return df

def kinematic_values(RH, df_kin):
    df = pd.DataFrame({'RH':[RH]}) # setup RH into a dataframe
    df_kin = df_kin.append(df) # add the setup RH value into the dataframe at the end
    df_kin = df_kin.sort_values(by=['RH']) # sort the values using RH column
    df_kin = df_kin.drop_duplicates(subset=['RH'], keep='first') # keep the first value if matchin values in RH (setup RH = table RH)
    df_kin = df_kin.reset_index(drop= True) # reset the index correctly
    rh_index = int(df_kin[df_kin['RH']==RH].index[0]) # identify the index of the setup RH in the table
    df_kin = df_kin.loc[[rh_index-1, rh_index, rh_index+1]] # build dataframe with row+1 and row-1
    MRdrp = interpol_mma(df_kin['RH'], df_kin['MRdpr'])
    MRarb = interpol_mma(df_kin['RH'], df_kin['MRarb'])
    RCH = interpol_mma(df_kin['RH'], df_kin['RCH'])
    return MRdrp, MRarb, RCH