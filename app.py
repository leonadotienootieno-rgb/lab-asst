import streamlit as st
import pandas as pd

# Set Page Config
st.set_page_config(page_title="Universal Lab Assistant", page_icon="🧪")

st.title("🧪 Universal Lab Assistant")
st.sidebar.header("Lab Departments")

# Menu Selection
menu = st.sidebar.selectbox("Go to:", 
    ["Dashboard Home", "Biochemistry", "Microbiology", "Tissue Culture", "Forensics", "Lab Budget & Prices"])

# 1. HOME / DASHBOARD
if menu == "Dashboard Home":
    st.subheader("Welcome, Scientist!")
    st.write("This tool assists in cross-disciplinary biological calculations and protocol management.")
    st.info("Select a department from the sidebar to begin your calculations.")
    

# 2. BIOCHEMISTRY
elif menu == "Biochemistry":
    st.header("Biochemistry: Solution Prep")
    tab1, tab2 = st.tabs(["Molarity (C1V1)", "Serial Dilution"])
    
    with tab1:
        c1 = st.number_input("Stock Concentration (M)", value=1.0)
        c2 = st.number_input("Target Concentration (M)", value=0.1)
        v2 = st.number_input("Target Volume (mL)", value=100.0)
        
        if st.button("Calculate Buffer"):
            v1 = (c2 * v2) / c1
            st.success(f"Add **{v1:.4g} mL** of stock to **{v2 - v1:.4g} mL** of diluent.")

# 3. MICROBIOLOGY
elif menu == "Microbiology":
    st.header("Microbiology: Growth Dynamics")
    n0 = st.number_input("Starting Bacteria Count (N0)", value=1000)
    nt = st.number_input("Final Bacteria Count (Nt)", value=100000)
    time = st.number_input("Time Elapsed (minutes)", value=120)
    
    if st.button("Calculate Generation Time"):
        import math
        n_gen = (math.log10(nt) - math.log10(n0)) / math.log10(2)
        gen_time = time / n_gen
        st.metric("Number of Generations", f"{n_gen:.2f}")
        st.metric("Doubling Time (g)", f"{gen_time:.2f} mins")
        # [attachment_0](attachment)

# 4. FORENSICS
elif menu == "Forensics":
    st.header("Forensics: DNA Normalization")
    initial = st.number_input("Extract Concentration (ng/µL)", value=15.0)
    target = st.number_input("Target Input (ng)", value=1.0) # Usually 1ng for PCR
    total_v = st.number_input("Reaction Volume (µL)", value=15.0)
    
    v_dna = target / initial
    if st.button("Generate DNA Recipe"):
        if v_dna < 1.0:
            st.error(f"Volume ({v_dna:.4f} µL) is too low for a P2 pipette!")
            st.warning("Action: Perform a 1:10 pre-dilution of your extract.")
        else:
            st.success(f"Mix **{v_dna:.3f} µL** DNA with **{total_v - v_dna:.3f} µL** TE Buffer.")

# 5. BUDGET
elif menu == "Lab Budget & Prices":
    st.header("Reagent Price List")
    # Small sample table
    data = {
        "Reagent": ["TE Buffer", "Taq Polymerase", "FBS", "Trypsin"],
        "Price ($)": [0.05, 12.50, 0.85, 0.12],
        "Unit": ["per mL", "per reaction", "per mL", "per mL"]
    }
    df = pd.DataFrame(data)
    st.table(df)
    st.info("Total project spend can be calculated by linking these values to your saved history.")