import streamlit as st
import calcul
import importer

#take session state
setup_a = st.session_state
setup_b = st.session_state
#import anti roll bar and kinematic csv tables
df_fa_arb = importer.anti_roll_bar_csv("front")
df_ra_arb = importer.anti_roll_bar_csv("rear")
df_fa_kin = importer.kinematic_csv("front")
df_ra_kin = importer.kinematic_csv("rear")

ArbRate_FA_csv = st.sidebar.checkbox("use FA ARB csv", value=True, key="-ArbRate_FA_csv-")
ArbRate_RA_csv = st.sidebar.checkbox("use RA ARB csv", value=True, key="-ArbRate_RA_csv-")
st.title("Ride Tool")
st.header("Setup infos")
cola, colb = st.columns(2)
with cola:
    st.write("Setup A")
    setup_a['RH'][0] = st.number_input("Front RH [mm] : ", min_value=0.0, max_value=100.0, value=setup_a['RH'][0], step=0.5, key='-a_frh-')
    setup_a['MRdpr'][0], setup_a['MRarb'][0], setup_a['RCH'][0] = importer.kinematic_values(setup_a['RH'][0], df_fa_kin) # take RH / MRdpr / MRarb / RCH settings from the table identification (using RH)
    setup_a['RH'][1] = st.number_input("Rear RH [mm] : ", min_value=0.0, max_value=100.0, value=setup_a['RH'][1], step=0.5, key='-a_rrh-')
    setup_a['MRdpr'][1], setup_a['MRarb'][1], setup_a['RCH'][1] = importer.kinematic_values(setup_a['RH'][1], df_ra_kin) # take RH / MRdpr / MRarb / RCH settings from the table identification (using RH)
    setup_a['SprRate'][0] = st.number_input("Front Spring [N/mm] : ", min_value=0.0, max_value=1000.0, value=setup_a['SprRate'][0], step=10.0, key='-a_fspr-')
    setup_a['SprRate'][1] = st.number_input("Rear Spring [N/mm] : ", min_value=0.0, max_value=1000.0, value=setup_a['SprRate'][1], step=10.0, key='-a_rspr-')
    
    if ArbRate_FA_csv == True:
        arb_setting = st.selectbox("Front ARB Pos ", df_fa_arb['Setting'], index=int(df_fa_arb[df_fa_arb['Setting']==setup_a['ArbPos_fa']].index[0]))
        setup_a['ArbPos_fa'] = arb_setting # update ARB position
        setup_a['ArbRate'][0] = importer.anti_roll_bar_rate(arb_setting, df_fa_arb) # take ARB position from selectbox and get the stiffness
        st.text(f"Front ARB Rate : {setup_a['ArbRate'][0]} N/mm")
    if ArbRate_FA_csv == False:
        st.number_input("Front ARB [N/mm]", min_value=0.0, max_value=1000.0, value=setup_a['ArbRate'][0], step=1.0)
    
    if ArbRate_RA_csv == True:
        arb_setting = st.selectbox("Rear ARB Pos ", df_ra_arb['Setting'], index=int(df_ra_arb[df_ra_arb['Setting']==setup_a['ArbPos_ra']].index[0]))
        setup_a['ArbPos_ra'] = arb_setting # update ARB position
        setup_a['ArbRate'][1] = importer.anti_roll_bar_rate(arb_setting, df_ra_arb) # take ARB position from selectbox and get the stiffness
        st.text(f"Rear ARB Rate : {setup_a['ArbRate'][1]} N/mm")
    if ArbRate_RA_csv == False:
        st.number_input("Rear ARB [N/mm]", min_value=0.0, max_value=1000.0, value=setup_a['ArbRate'][1], step=1.0)
    
    if st.button('Send setup'):
        st.markdown("""---""")
        ride_a = calcul.ride_numbers(setup_a) # basic calcs from setup
        st.write("Ride Rates")
        st.text(f"Front Whl Rate = {round(ride_a['WhlRate'][0],1)} N/mm")
        st.text(f"Rear Whl Rate = {round(ride_a['WhlRate'][1],1)} N/mm")
        st.text(f"Front Ride Rate = {round(ride_a['WhlRate_IncTire'][0],1)} N/mm")
        st.text(f"Rear Ride Rate = {round(ride_a['WhlRate_IncTire'][1],1)} N/mm")

        st.write("Rolling Torques")
        st.text(f"Front Rolling Torque = {round(ride_a['RollingTorqueTot'][0],1)} Nm/deg")
        st.text(f"Rear Rolling Torque = {round(ride_a['RollingTorqueTot'][1],1)} Nm/deg")
        st.text(f"%FA = {round(ride_a['RollingTorqueTot'][2],1)} %")
        st.text(f"Front Roll Torque Inc.T= {round(ride_a['RollingTorqueTot_IncTire'][0],1)} Nm/deg")
        st.text(f"Rear Roll Torque Inc.T = {round(ride_a['RollingTorqueTot_IncTire'][1],1)} Nm/deg")
        st.text(f"%FA = {round(ride_a['RollingTorqueTot_IncTire'][2],1)} %")

st.markdown("""---""")
st.write("setup_a :")
st.write(setup_a)
#with colb:
#    st.write("Setup B")
#    st.number_input("Front Spring [N/mm] : ", min_value=0.0, max_value=1000.0, value=setup_b['SprRate'][0], step=10.0, key='-b_fpsr-')
#    st.number_input("Rear Spring [N/mm] : ", min_value=0.0, max_value=1000.0, value=setup_b['SprRate'][1], step=10.0, key='-b_rpsr-')

st.markdown("""---""")
st.write("session state :")
st.write(st.session_state)