import streamlit as st
import calcul
import importer

setup = {}
# look for the setup information and make basic calcs
setup = importer.setup_txt()
setup = setup | calcul.basic(setup) # merge the setup and the basic calcs dictionnaries ( | operator merge dictionnaries)

#st.set_page_config(layout="wide")
#st.sidebar.write("Navigation")
#st.markdown('<style>footer {display: none!important};</style>', unsafe_allow_html=True)

st.title(f"Car Information {setup['carinfo']}")
st.header("**Infos in setup.txt**")
st.write("**Global Information**")
st.text(f"Wheel base : {setup['WB'][0]} mm")
st.text(f"CoGtotZ @0RH : {setup['CoGtot0RH'][0]} mm")
colfa, colra = st.columns(2)
with colfa:
    st.write('<p style= "color:#ff9933">Front Axle</p>', unsafe_allow_html=True)
    st.text(f"Track : {setup['Track'][0]} mm")
    st.text(f"RH : {setup['RH'][0]} mm")
    st.text(f"RCH : {setup['RCH'][0]} mm")
    st.text(f"MR dpr : {setup['MRdpr'][0]} -")
    st.text(f"MR arb : {setup['MRarb'][0]} -")
    st.text(f"Loaded Radius : {setup['LoadRad'][0]} mm")
    st.text(f"Spring Rate : {setup['SprRate'][0]} N/mm")
    st.text(f"ARB Rate : {setup['ArbRate'][0]} N/mm")
    st.text(f"Tire Rate : {setup['TireRate'][0]} N/mm")
with colra:
    st.write('<p style= "color:#ff00ff">Rear Axle</p>', unsafe_allow_html=True)
    st.text(f"Track : {setup['Track'][1]} mm")
    st.text(f"RH : {setup['RH'][1]} mm")
    st.text(f"RCH : {setup['RCH'][1]} mm")
    st.text(f"MR dpr : {setup['MRdpr'][1]} -")
    st.text(f"MR arb : {setup['MRarb'][1]} -")
    st.text(f"Loaded Radius : {setup['LoadRad'][1]} mm")
    st.text(f"Spring Rate : {setup['SprRate'][1]} N/mm")
    st.text(f"ARB Rate : {setup['ArbRate'][1]} N/mm")
    st.text(f"Tire Rate : {setup['TireRate'][1]} N/mm")
st.markdown("""---""")
col1, col2 = st.columns(2)
with col1:
    st.write("Total wheel mass in kg")
    st.text(f"FL {setup['Wtot_whl'][0]} | {setup['Wtot_whl'][1]} FR")
    st.text(f"RL {setup['Wtot_whl'][2]} | {setup['Wtot_whl'][3]} RR")
    st.text(f"Tot weight : {round(setup['Wtot'][0],1)} kg")
    st.text(f"FA weight : {round(setup['Wtot'][1],1)} kg")
    st.text(f"RA weight : {round(setup['Wtot'][2],1)} kg")
    st.text(f"Weight distrib : {round(setup['Wtot'][3],1)} %FA")
with col2:
    st.write("Un Suspended mass in kg")
    st.text(f"FL {setup['WunSusp_whl'][0]} | {setup['WunSusp_whl'][1]} FR")
    st.text(f"RL {setup['WunSusp_whl'][2]} | {setup['WunSusp_whl'][3]} RR")
    st.text(f"Tot weight : {round(setup['WunSusp'][0],1)} kg")
    st.text(f"FA weight : {round(setup['WunSusp'][1],1)} kg")
    st.text(f"RA weight : {round(setup['WunSusp'][2],1)} kg")
    st.text(f"Weight distrib : {round(setup['WunSusp'][3],1)} %FA")
st.markdown("""---""")
st.header("**Calc Basic**")
st.write("Suspended mass in kg")
st.text(f"FL {round(setup['WSusp_whl'][0],1)} | {round(setup['WSusp_whl'][1],1)} FR")
st.text(f"RL {round(setup['WSusp_whl'][2],1)} | {round(setup['WSusp_whl'][3],1)} RR")
st.text(f"Tot weight : {round(setup['WSusp'][0],1)} kg")
st.text(f"FA weight : {round(setup['WSusp'][1],1)} kg")
st.text(f"RA weight : {round(setup['WSusp'][2],1)} kg")
st.text(f"Weight distrib : {round(setup['WSusp'][3],1)} %FA")
st.markdown("""---""")
st.header("**Tables**")
col1, col2 = st.columns(2)
with col1:
    st.write("FA ARB table")
    df_fa_arb = importer.anti_roll_bar_csv("front") # csv front anti roll bar
    st.write(df_fa_arb)
    setup['ArbPos_fa'] = importer.anti_roll_bar_pos(setup['ArbRate'][0], df_fa_arb) # take ARB settings from the table identification
    st.text(f"identified : {setup['ArbPos_fa']}")
with col2:
    st.write("RA ARB table")
    df_ra_arb = importer.anti_roll_bar_csv("rear") # csv rear anti roll bar
    st.write(df_ra_arb)
    setup['ArbPos_ra'] = importer.anti_roll_bar_pos(setup['ArbRate'][1], df_ra_arb) # take ARB settings from the table identification
    st.text(f"identified : {setup['ArbPos_ra']}")
col1, col2 = st.columns(2)
with col1:
    st.write("FA KIN table")
    df_fa_kin = importer.kinematic_csv("front") # csv front kinematic
    st.write(df_fa_kin)
    setup['MRdpr'][0], setup['MRarb'][0], setup['RCH'][0] = importer.kinematic_values(setup['RH'][0], df_fa_kin) # take RH / MRdpr / MRarb / RCH settings from the table identification (using RH)
    st.text(f"RH {round(setup['RH'][0], 1)} mm | RCH {round(setup['RCH'][0], 1)}")
    st.text(f"MRdpr {round(setup['MRdpr'][0], 4)}| MRarb {round(setup['MRarb'][0], 4)}")
with col2:
    st.write("RA KIN table")
    df_ra_kin = importer.kinematic_csv("rear") # csv rear kinematic
    st.write(df_ra_kin)
    setup['MRdpr'][1], setup['MRarb'][1], setup['RCH'][1] = importer.kinematic_values(setup['RH'][1], df_ra_kin) # take RH / MRdpr / MRarb / RCH settings from the table identification (using RH)
    st.text(f"RH {round(setup['RH'][1], 1)} mm | RCH {round(setup['RCH'][1], 1)}")
    st.text(f"MRdpr {round(setup['MRdpr'][1], 4)}| MRarb {round(setup['MRarb'][1], 4)}")

# save setup dictionnary into session state
st.session_state = setup
st.markdown("""---""")
st.write("session state :")
st.write(st.session_state)