import streamlit as st
import pandas as pd
import math
import time
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Universal Lab Assistant", page_icon="🧪", layout="wide")

# --- INITIALIZE SESSION STATE (The App's Memory) ---
if 'logbook' not in st.session_state:
    st.session_state.logbook = pd.DataFrame(columns=["Timestamp", "Module", "Result"])

def add_to_log(module, result):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[now, module, result]], columns=["Timestamp", "Module", "Result"])
    st.session_state.logbook = pd.concat([st.session_state.logbook, new_entry], ignore_index=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧪 Lab Navigation")
menu = st.sidebar.selectbox("Select Department:", 
    ["Dashboard Home", 
     "Biochemistry (C1V1)", 
     "Microbiology & Graphs", 
     "Tissue Culture", 
     "Forensics (DNA)", 
     "Master Mix Generator", 
     "Unit Converter", 
     "Centrifuge (RPM/G)", 
     "Lab Timers", 
     "View Daily Log",
     "Lab Budget & Prices"])

st.sidebar.markdown("---")
st.sidebar.write(f"📊 **Logged Actions:** {len(st.session_state.logbook)}")

# --- 1. DASHBOARD HOME ---
if menu == "Dashboard Home":
    st.title("🧪 Universal Lab Assistant")
    st.subheader("Welcome, Scientist!")
    st.write("Your central hub for cross-disciplinary research and automated data logging.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Online")
    col2.metric("Environment", "Cloud/Mobile")
    col3.metric("Version", "1.6")
    
    st.info("Choose a module from the sidebar to start your session.")

# --- 2. BIOCHEMISTRY ---
elif menu == "Biochemistry (C1V1)":
    st.title("🧪 Biochemistry: Solution Prep")
    st.write("Calculate dilution factors using the $C_1V_1 = C_2V_2$ formula.")
    
    c1 = st.number_input("Stock Concentration (M)", value=1.0, format="%.4f")
    c2 = st.number_input("Target Concentration (M)", value=0.1, format="%.4f")
    v2 = st.number_input("Target Volume (mL)", value=100.0)
    
    if st.button("Calculate Dilution"):
        v1 = (c2 * v2) / c1
        result_text = f"Add {v1:.4g} mL of stock to {v2 - v1:.4g} mL of diluent."
        st.success(f"✅ **{result_text}**")
        add_to_log("Biochem", result_text)

# --- 3. MICROBIOLOGY & GRAPHS ---
elif menu == "Microbiology & Graphs":
    st.title("🧫 Microbiology: Growth Analysis")
    
    tab1, tab2 = st.tabs(["Generation Time", "Growth Curve Plotter"])
    
    with tab1:
        n0 = st.number_input("Starting Bacteria Count (N0)", value=1000)
        nt = st.number_input("Final Bacteria Count (Nt)", value=100000)
        t_elapsed = st.number_input("Time Elapsed (minutes)", value=120)
        
        if st.button("Calculate Growth Stats"):
            n_gen = (math.log10(nt) - math.log10(n0)) / math.log10(2)
            gen_time = t_elapsed / n_gen
            st.metric("Number of Generations", f"{n_gen:.2f}")
            st.metric("Doubling Time (g)", f"{gen_time:.2f} mins")
            add_to_log("Microbio", f"Doubling time: {gen_time:.2f} mins")

    with tab2:
        st.subheader("Interactive Growth Curve")
        
        times = st.text_input("Time Points (comma separated)", "0, 30, 60, 90, 120, 150")
        readings = st.text_input("OD600 Readings (comma separated)", "0.05, 0.08, 0.15, 0.35, 0.65, 0.85")
        
        try:
            t_list = [float(x.strip()) for x in times.split(",")]
            r_list = [float(x.strip()) for x in readings.split(",")]
            if len(t_list) == len(r_list):
                df_growth = pd.DataFrame({"Time (min)": t_list, "OD600": r_list})
                fig = px.line(df_growth, x="Time (min)", y="OD600", markers=True, title="Bacterial Growth Profile")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Time and Readings must have same count!")
        except:
            st.warning("Enter numerical values separated by commas.")

# --- 4. TISSUE CULTURE ---
elif menu == "Tissue Culture":
    st.title("🧫 Tissue Culture: Cell Seeding")
    
    current_density = st.number_input("Current Density (cells/mL)", value=1000000)
    target_count = st.number_input("Total Cells Needed", value=500000)
    final_vol = st.number_input("Final Media Volume (mL)", value=10.0)
    
    if st.button("Calculate Seeding"):
        vol_cells = target_count / current_density
        vol_media = final_vol - vol_cells
        if vol_cells > final_vol:
            st.error("Suspension too dilute for this final volume!")
        else:
            res = f"Seed {vol_cells:.3f} mL cells into {vol_media:.3f} mL media."
            st.success(res)
            add_to_log("Tissue Culture", res)

# --- 5. FORENSICS ---
elif menu == "Forensics (DNA)":
    st.title("🧬 Forensics: DNA Normalization")
    initial = st.number_input("Extract Concentration (ng/µL)", value=15.0)
    target = st.number_input("Target DNA Input (ng)", value=1.0)
    total_v = st.number_input("Total Reaction Volume (µL)", value=15.0)
    
    if st.button("Calculate DNA Volume"):
        v_dna = target / initial
        if v_dna < 1.0:
            st.warning("Volume too low for direct pipetting (<1µL). Pre-dilute 1:10.")
        res = f"DNA: {v_dna:.3f}µL | Buffer: {total_v - v_dna:.3f}µL"
        st.success(res)
        add_to_log("Forensics", res)

# --- 6. MASTER MIX GENERATOR ---
elif menu == "Master Mix Generator":
    st.title("🧪 Master Mix Generator")
    num_samples = st.number_input("Actual Samples", value=10)
    total_samples = num_samples * 1.10 # 10% extra
    st.info(f"Calculating for {total_samples:.1f} reactions (including 10% buffer).")
    
    water = st.number_input("Water per rxn (µL)", value=12.5)
    buffer = st.number_input("Buffer per rxn (µL)", value=2.5)
    enzyme = st.number_input("Enzyme per rxn (µL)", value=0.5)
    
    if st.button("Generate Recipe"):
        res = f"W:{water*total_samples:.1f}µL, B:{buffer*total_samples:.1f}µL, E:{enzyme*total_samples:.1f}µL"
        st.success(f"**Total Mix:** {res}")
        add_to_log("Master Mix", res)

# --- 7. UNIT CONVERTER ---
elif menu == "Unit Converter":
    st.title("🔄 Universal Unit Converter")
    mw = st.number_input("Molecular Weight (g/mol)", value=180.16)
    molarity = st.number_input("Molarity (mM)", value=1.0)
    result = molarity * mw
    st.metric("Mass Concentration", f"{result:.2f} mg/L (µg/mL)")
    add_to_log("Converter", f"{molarity}mM = {result:.2f}mg/L")

# --- 8. CENTRIFUGE ---
elif menu == "Centrifuge (RPM/G)":
    st.title("🌀 Centrifuge: RPM to RCF")
    
    radius = st.number_input("Rotor Radius (cm)", value=10.0)
    rpm = st.number_input("Speed (RPM)", value=5000)
    rcf = 0.00001118 * radius * (rpm**2)
    st.metric("Relative Centrifugal Force (G)", f"{rcf:.1f} x g")
    if st.button("Log G-Force"):
        add_to_log("Centrifuge", f"{rpm}RPM = {rcf:.1f}G")

# --- 9. LAB TIMERS ---
elif menu == "Lab Timers":
    st.title("⏱️ Lab Timers")
    task = st.text_input("Step Name", "Incubation")
    mins = st.number_input("Duration (minutes)", 1)
    
    if st.button("Start Timer"):
        secs = mins * 60
        bar = st.progress(0)
        for i in range(secs):
            time.sleep(1)
            bar.progress((i+1)/secs)
        st.balloons()
        st.success(f"🔔 {task} Finished!")
        add_to_log("Timer", f"{task} complete")

# --- 10. VIEW DAILY LOG ---
elif menu == "View Daily Log":
    st.title("📋 Activity Logbook")
    if st.session_state.logbook.empty:
        st.write("No logs for this session yet.")
    else:
        st.dataframe(st.session_state.logbook, use_container_width=True)
        csv = st.session_state.logbook.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", csv, "lab_log.csv", "text/csv")
        
        if st.button("Clear Session"):
            st.session_state.logbook = pd.DataFrame(columns=["Timestamp", "Module", "Result"])
            st.rerun()

# --- 11. BUDGET ---
elif menu == "Lab Budget & Prices":
    st.title("💰 Reagent Pricing")
    data = {
        "Reagent": ["TE Buffer", "Taq Polymerase", "FBS", "Trypsin", "DMEM Media"],
        "Price ($)": [0.05, 12.50, 0.85, 0.12, 0.08],
        "Unit": ["per mL", "per reaction", "per mL", "per mL", "per mL"]
    }
    st.table(pd.DataFrame(data))