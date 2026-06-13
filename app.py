import streamlit as st
import pandas as pd
import math
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Universal Lab Assistant", page_icon="🧪", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'logbook' not in st.session_state:
    st.session_state.logbook = pd.DataFrame(columns=["Timestamp", "Module", "Result", "User_Note"])

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.timer_end = None
    st.session_state.timer_task = ""
    st.session_state.timer_duration = 0

if 'free_calculations' not in st.session_state:
    st.session_state.free_calculations = 0

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

MAX_FREE_CALCULATIONS = 10  # Limit for free tier

def add_to_log(module, result, note=""):
    """Add entry to session logbook"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[now, module, result, note]], 
                             columns=["Timestamp", "Module", "Result", "User_Note"])
    st.session_state.logbook = pd.concat([st.session_state.logbook, new_entry], ignore_index=True)

def check_usage_limit():
    """Track and enforce free tier limits"""
    st.session_state.free_calculations += 1
    if st.session_state.free_calculations > MAX_FREE_CALCULATIONS:
        st.warning(f"⚠️ You've reached the free limit ({MAX_FREE_CALCULATIONS} calculations). Upgrade to Pro for unlimited access!")
        st.info("💎 **Pro Plan:** $4.99/month - Unlimited calculations, protocol templates, data export, and priority support")
        return False
    return True

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🧪 Lab Navigation")
    
    # User status
    if st.session_state.user_email:
        st.success(f"👤 {st.session_state.user_email}")
        if st.button("Logout"):
            st.session_state.user_email = None
            st.rerun()
    else:
        with st.expander("🔐 Sign Up for Pro (Free)"):
            email = st.text_input("Email address")
            if st.button("Start Free Trial"):
                if "@" in email and "." in email:
                    st.session_state.user_email = email
                    st.session_state.free_calculations = 0
                    st.success("✅ Welcome! You have 10 free calculations.")
                    st.rerun()
                else:
                    st.error("Please enter a valid email")
    
    st.markdown("---")
    
    menu = st.selectbox("Select Module:", 
        ["🧪 Dashboard Home", 
         "🧬 Biochemistry (C1V1)", 
         "🧫 Microbiology & Graphs", 
         "🔬 Tissue Culture", 
         "🕵️ Forensics (DNA)", 
         "🧪 Master Mix Generator", 
         "🔄 Unit Converter", 
         "🌀 Centrifuge (RPM/G)", 
         "⏱️ Lab Timers", 
         "📋 Protocol Templates",
         "📊 View Daily Log",
         "💰 Lab Budget & Prices"])
    
    st.markdown("---")
    
    # Usage stats
    st.metric("Calculations Used", 
              f"{st.session_state.free_calculations}/{MAX_FREE_CALCULATIONS}")
    
    # Upgrade prompt
    if st.session_state.free_calculations > 5 and not st.session_state.user_email:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 1rem; border-radius: 0.5rem; color: white;'>
            <h4>🚀 Go Pro</h4>
            <p>Unlimited calculations<br/>Protocol templates<br/>Data export</p>
            <strong>$4.99/month</strong>
        </div>
        """, unsafe_allow_html=True)

# --- 1. DASHBOARD HOME ---
if "Dashboard Home" in menu:
    st.markdown('<h1 class="main-header">🧪 Universal Lab Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Your All-in-One Laboratory Calculation Suite")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Calculations", len(st.session_state.logbook))
    with col2:
        st.metric("🧪 Modules", "12")
    with col3:
        st.metric("☁️ Status", "Online")
    with col4:
        st.metric("📱 Platform", "Web/Mobile")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    qcol1, qcol2, qcol3 = st.columns(3)
    with qcol1:
        if st.button("🧬 Quick Dilution", use_container_width=True):
            st.session_state.quick_action = "dilution"
    with qcol2:
        if st.button("🧫 Growth Curve", use_container_width=True):
            st.session_state.quick_action = "growth"
    with qcol3:
        if st.button("📋 View Protocols", use_container_width=True):
            st.session_state.quick_action = "protocols"
    
    # Featured protocols
    st.markdown("### 📚 Featured Protocol Templates")
    feat_col1, feat_col2 = st.columns(2)
    with feat_col1:
        st.info("**PCR Master Mix**\n\nComplete guide for 50µL reactions with optimization tips")
    with feat_col2:
        st.info("**Cell Culture Passaging**\n\nStep-by-step protocol for adherent cell lines")

# --- 2. BIOCHEMISTRY ---
elif "Biochemistry" in menu:
    st.markdown("## 🧬 Biochemistry: Solution Preparation")
    st.markdown("Calculate precise dilution volumes using $C_1V_1 = C_2V_2$")
    
    with st.form("dilution_form"):
        col1, col2 = st.columns(2)
        with col1:
            c1 = st.number_input("Stock Concentration (M)", value=1.0, format="%.4f", help="Concentration of your stock solution")
            c2 = st.number_input("Target Concentration (M)", value=0.1, format="%.4f", help="Desired final concentration")
        with col2:
            v2 = st.number_input("Target Volume (mL)", value=100.0, min_value=0.1, help="Final volume needed")
            note = st.text_input("Note (optional)", placeholder="e.g., 1M NaCl for Buffer A")
        
        submitted = st.form_submit_button("🧮 Calculate Dilution")
        
        if submitted:
            if not check_usage_limit():
                st.stop()
            
            try:
                if c1 <= 0:
                    st.error("❌ Stock concentration must be greater than zero")
                elif c2 > c1:
                    st.error("❌ Target concentration cannot exceed stock concentration")
                else:
                    v1 = (c2 * v2) / c1
                    
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.metric("Stock Volume Needed", f"{v1:.4f} mL")
                    with col_r2:
                        st.metric("Diluent Volume", f"{v2 - v1:.4f} mL")
                    
                    # Visual representation
                    st.markdown("### 📊 Visual Representation")
                    ratio = v1/v2
                    st.progress(ratio, text=f"Stock: {ratio:.1%} | Diluent: {1-ratio:.1%}")
                    
                    result_text = f"Add {v1:.4g} mL of stock to {v2 - v1:.4g} mL of diluent"
                    st.success(f"✅ **{result_text}**")
                    add_to_log("Biochem Dilution", result_text, note)
                    
                    # Download result
                    result_df = pd.DataFrame({
                        "Parameter": ["Stock Conc", "Target Conc", "Target Volume", "Stock Volume", "Diluent Volume"],
                        "Value": [f"{c1} M", f"{c2} M", f"{v2} mL", f"{v1:.4f} mL", f"{v2-v1:.4f} mL"]
                    })
                    st.download_button("📥 Download Calculation", 
                                     result_df.to_csv(index=False), 
                                     "dilution_calc.csv")
                    
            except Exception as e:
                st.error(f"⚠️ Calculation error: {str(e)}")

# --- 3. MICROBIOLOGY & GRAPHS ---
elif "Microbiology" in menu:
    st.markdown("## 🧫 Microbiology: Growth Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📈 Generation Time", "📊 Growth Curve", "📚 Reference"])
    
    with tab1:
        with st.form("growth_form"):
            col1, col2 = st.columns(2)
            with col1:
                n0 = st.number_input("Initial Count (N₀)", value=1000, min_value=1, 
                                   help="Starting number of bacteria")
                nt = st.number_input("Final Count (Nₜ)", value=100000, min_value=1,
                                   help="Ending number of bacteria")
            with col2:
                t_elapsed = st.number_input("Time Elapsed (min)", value=120, min_value=1)
                note = st.text_input("Note (optional)", placeholder="e.g., E. coli at 37°C")
            
            submitted = st.form_submit_button("🧮 Calculate Growth Parameters")
            
            if submitted:
                if not check_usage_limit():
                    st.stop()
                
                try:
                    n_gen = (math.log10(nt) - math.log10(n0)) / math.log10(2)
                    gen_time = t_elapsed / n_gen
                    growth_rate = 1 / gen_time if gen_time > 0 else 0
                    
                    col_r1, col_r2, col_r3 = st.columns(3)
                    col_r1.metric("Generations", f"{n_gen:.2f}")
                    col_r2.metric("Doubling Time", f"{gen_time:.1f} min")
                    col_r3.metric("Growth Rate", f"{growth_rate:.4f} min⁻¹")
                    
                    st.info(f"📝 **Interpretation:** The population doubles every {gen_time:.1f} minutes")
                    add_to_log("Microbiology Growth", 
                              f"Doubling time: {gen_time:.1f} min", note)
                    
                except Exception as e:
                    st.error(f"⚠️ Calculation error: {str(e)}")
    
    with tab2:
        st.markdown("### 📊 Interactive Growth Curve")
        
        st.markdown("""
        **Enter your time points and OD600 readings:**
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            times = st.text_area("Time Points (min)", "0, 30, 60, 90, 120, 150, 180", 
                               help="One value per line or comma-separated")
        with col2:
            readings = st.text_area("OD600 Readings", "0.05, 0.08, 0.15, 0.35, 0.65, 0.95, 1.10",
                                  help="Must match number of time points")
        
        if st.button("📈 Plot Growth Curve"):
            try:
                t_list = [float(x.strip()) for x in times.replace('\n', ',').split(",") if x.strip()]
                r_list = [float(x.strip()) for x in readings.replace('\n', ',').split(",") if x.strip()]
                
                if len(t_list) != len(r_list):
                    st.error(f"❌ Mismatch: {len(t_list)} time points vs {len(r_list)} readings")
                elif len(t_list) < 2:
                    st.error("❌ Need at least 2 data points")
                else:
                    chart_df = pd.DataFrame({"OD600": r_list}, index=t_list)
                    st.line_chart(chart_df, use_container_width=True)
                    
                    # Calculate growth phase
                    st.markdown("### 📈 Growth Analysis")
                    if len(r_list) > 2:
                        max_growth_idx = r_list.index(max(r_list))
                        st.info(f"🔍 **Max OD600:** {max(r_list):.3f} at t={t_list[max_growth_idx]} min")
                        
                    add_to_log("Growth Curve", f"{len(t_list)} points plotted")
                    
            except ValueError:
                st.error("❌ Please enter valid numbers only")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
    
    with tab3:
        st.markdown("### 📚 Reference Values")
        ref_data = pd.DataFrame({
            "Organism": ["E. coli", "S. aureus", "B. subtilis", "P. aeruginosa", "S. cerevisiae"],
            "Doubling Time (min)": [20, 30, 120, 40, 90],
            "Optimal Temp (°C)": [37, 37, 30, 37, 30],
            "Typical Max OD600": [2.0, 3.0, 2.5, 4.0, 1.5]
        })
        st.dataframe(ref_data, use_container_width=True, hide_index=True)

# --- 4. TISSUE CULTURE ---
elif "Tissue Culture" in menu:
    st.markdown("## 🔬 Tissue Culture: Cell Seeding")
    
    with st.form("seeding_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_density = st.number_input("Cell Density (cells/mL)", value=1000000, 
                                            min_value=1, format="%d")
            target_count = st.number_input("Total Cells Needed", value=500000, 
                                         min_value=1, format="%d")
        with col2:
            final_vol = st.number_input("Final Volume (mL)", value=10.0, min_value=0.1)
            flask_type = st.selectbox("Culture Vessel", 
                                    ["T25 Flask", "T75 Flask", "6-well plate", 
                                     "96-well plate", "100mm dish", "Custom"])
        
        submitted = st.form_submit_button("🧮 Calculate Seeding Volumes")
        
        if submitted:
            if not check_usage_limit():
                st.stop()
            
            try:
                if current_density <= 0:
                    st.error("❌ Cell density must be positive")
                else:
                    vol_cells = target_count / current_density
                    vol_media = final_vol - vol_cells
                    
                    if vol_cells > final_vol:
                        st.error("❌ Cell suspension too dilute! Centrifuge and resuspend in smaller volume.")
                        st.info("💡 **Tip:** Centrifuge at 300g for 5 min, resuspend in fresh media")
                    else:
                        col_r1, col_r2 = st.columns(2)
                        col_r1.metric("Cell Suspension", f"{vol_cells:.3f} mL")
                        col_r2.metric("Fresh Media", f"{vol_media:.3f} mL")
                        
                        # Flask-specific info
                        flask_volumes = {
                            "T25 Flask": 5, "T75 Flask": 15, "6-well plate": 2,
                            "96-well plate": 0.2, "100mm dish": 10
                        }
                        if flask_type in flask_volumes:
                            st.info(f"💡 **{flask_type}** typically holds {flask_volumes[flask_type]} mL")
                        
                        result_text = f"Add {vol_cells:.3f} mL cells to {vol_media:.3f} mL media in {flask_type}"
                        st.success(f"✅ {result_text}")
                        add_to_log("Tissue Culture", result_text)
                        
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# --- 5. FORENSICS ---
elif "Forensics" in menu:
    st.markdown("## 🕵️ Forensics: DNA Normalization")
    
    with st.form("dna_form"):
        col1, col2 = st.columns(2)
        with col1:
            initial = st.number_input("DNA Concentration (ng/µL)", value=15.0, min_value=0.1)
            target = st.number_input("Target DNA Mass (ng)", value=50.0, min_value=0.1)
        with col2:
            total_v = st.number_input("Total Reaction Volume (µL)", value=25.0, min_value=1.0)
            note = st.text_input("Case/Evidence ID (optional)", placeholder="e.g., Evidence-0042")
        
        submitted = st.form_submit_button("🧮 Calculate DNA Volume")
        
        if submitted:
            if not check_usage_limit():
                st.stop()
            
            try:
                v_dna = target / initial
                
                if v_dna < 0.5:
                    st.warning("⚠️ **Volume too low for accurate pipetting**")
                    st.markdown(f"""
                    **Recommended:** Pre-dilute DNA 1:10
                    - Mix 1 µL DNA + 9 µL water
                    - Use 10× more volume from diluted stock
                    - New volume to add: {v_dna*10:.2f} µL
                    """)
                
                col_r1, col_r2, col_r3 = st.columns(3)
                col_r1.metric("DNA Volume", f"{v_dna:.2f} µL")
                col_r2.metric("Buffer/Water", f"{total_v - v_dna:.2f} µL")
                col_r3.metric("Total Volume", f"{total_v:.1f} µL")
                
                result_text = f"DNA: {v_dna:.2f}µL | Diluent: {total_v - v_dna:.2f}µL"
                st.success(f"✅ **PCR Setup:** {result_text}")
                add_to_log("Forensics DNA", result_text, note)
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# --- 6. MASTER MIX GENERATOR ---
elif "Master Mix" in menu:
    st.markdown("## 🧪 Master Mix Generator")
    
    with st.form("master_mix_form"):
        num_samples = st.number_input("Number of Samples", value=8, min_value=1)
        excess = st.slider("Excess (%)", 5, 25, 10, help="Extra volume to account for pipetting errors")
        
        total_rxns = math.ceil(num_samples * (1 + excess/100))
        
        st.info(f"📊 Preparing for **{total_rxns}** reactions ({excess}% excess)")
        
        st.markdown("### Reaction Components (per reaction)")
        col1, col2, col3 = st.columns(3)
        with col1:
            water = st.number_input("Water (µL)", value=13.5, min_value=0.0, step=0.5)
            buffer = st.number_input("Buffer (µL)", value=2.5, min_value=0.0, step=0.5)
        with col2:
            dntps = st.number_input("dNTPs (µL)", value=0.5, min_value=0.0, step=0.5)
            primers_f = st.number_input("Forward Primer (µL)", value=1.0, min_value=0.0, step=0.5)
        with col3:
            primers_r = st.number_input("Reverse Primer (µL)", value=1.0, min_value=0.0, step=0.5)
            enzyme = st.number_input("Polymerase (µL)", value=0.5, min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("🧮 Generate Master Mix")
        
        if submitted:
            if not check_usage_limit():
                st.stop()
            
            components = {
                "Water": water * total_rxns,
                "Buffer": buffer * total_rxns,
                "dNTPs": dntps * total_rxns,
                "Forward Primer": primers_f * total_rxns,
                "Reverse Primer": primers_r * total_rxns,
                "Polymerase": enzyme * total_rxns
            }
            
            total_vol = sum(components.values())
            
            st.markdown("### 📋 Master Mix Recipe")
            
            # Create a nice table
            df_mix = pd.DataFrame({
                "Component": list(components.keys()),
                "Per Rxn (µL)": [water, buffer, dntps, primers_f, primers_r, enzyme],
                f"×{total_rxns} Rxns (µL)": list(components.values()),
                "Check (✓)": [""] * 6
            })
            st.dataframe(df_mix, use_container_width=True, hide_index=True)
            
            st.metric("Total Master Mix Volume", f"{total_vol:.1f} µL")
            
            # Aliquot info
            aliquot_vol = total_vol / num_samples
            st.success(f"✅ Add **{aliquot_vol:.1f} µL** master mix to each of {num_samples} tubes")
            
            add_to_log("Master Mix", f"{total_rxns} rxns, {total_vol:.1f}µL total")
            
            # Download recipe
            st.download_button("📥 Download Recipe", 
                             df_mix.to_csv(index=False), 
                             "master_mix_recipe.csv")

# --- 7. UNIT CONVERTER ---
elif "Unit Converter" in menu:
    st.markdown("## 🔄 Unit Converter")
    
    conversion_type = st.selectbox("Conversion Type", 
        ["Molarity to Mass", "Mass to Moles", "Percentage Solutions"])
    
    if conversion_type == "Molarity to Mass":
        with st.form("molarity_form"):
            col1, col2 = st.columns(2)
            with col1:
                mw = st.number_input("Molecular Weight (g/mol)", value=58.44, 
                                    help="e.g., NaCl = 58.44 g/mol")
                molarity = st.number_input("Molarity (M)", value=1.0, format="%.3f")
            with col2:
                volume = st.number_input("Volume (L)", value=1.0, format="%.3f")
                note = st.text_input("Compound Name (optional)", placeholder="e.g., Sodium chloride")
            
            if st.form_submit_button("🔄 Convert"):
                mass = molarity * mw * volume
                st.metric("Mass Required", f"{mass:.3f} g")
                st.success(f"✅ Dissolve **{mass:.3f} g** in **{volume:.3f} L** for **{molarity} M** solution")
                add_to_log("Unit Converter", f"{molarity}M {note or 'solution'} = {mass:.3f}g")
    
    elif conversion_type == "Percentage Solutions":
        with st.form("percent_form"):
            col1, col2 = st.columns(2)
            with col1:
                percent_type = st.radio("Type", ["% (w/v)", "% (v/v)", "% (w/w)"])
                percentage = st.number_input("Percentage", value=10.0, min_value=0.01, max_value=100.0)
            with col2:
                total_volume = st.number_input("Total Volume (mL)", value=100.0, min_value=0.1)
            
            if st.form_submit_button("🔄 Calculate"):
                if percent_type in ["% (w/v)", "% (v/v)"]:
                    amount = (percentage / 100) * total_volume
                    unit = "g" if percent_type == "% (w/v)" else "mL"
                    st.success(f"✅ Use **{amount:.2f} {unit}** in total volume of **{total_volume:.1f} mL**")
                    add_to_log("Unit Converter", f"{percentage}% ({percent_type}) = {amount:.2f}{unit}")

# --- 8. CENTRIFUGE ---
elif "Centrifuge" in menu:
    st.markdown("## 🌀 Centrifuge: RPM ↔ RCF Converter")
    
    tab1, tab2 = st.tabs(["RPM → RCF", "RCF → RPM"])
    
    with tab1:
        with st.form("rpm_to_rcf"):
            radius = st.number_input("Rotor Radius (cm)", value=10.0, min_value=1.0, 
                                   help="Distance from rotor center to tube bottom")
            rpm = st.number_input("Speed (RPM)", value=5000, min_value=100)
            
            if st.form_submit_button("🌀 Convert to RCF"):
                rcf = 0.00001118 * radius * (rpm ** 2)
                st.metric("RCF (× g)", f"{rcf:.0f}")
                
                # Common applications
                if rcf < 500:
                    st.info("💡 Low speed - Cell pelleting (300-500g)")
                elif rcf < 5000:
                    st.info("💡 Medium speed - Bacteria pelleting (3000-5000g)")
                else:
                    st.info("💡 High speed - Microsome/organelle pelleting (10000-100000g)")
                
                add_to_log("Centrifuge", f"{rpm} RPM = {rcf:.0f} × g at {radius}cm")
    
    with tab2:
        with st.form("rcf_to_rpm"):
            radius2 = st.number_input("Rotor Radius (cm)", value=10.0, min_value=1.0, key="radius2")
            rcf_target = st.number_input("Desired RCF (× g)", value=5000, min_value=1)
            
            if st.form_submit_button("🌀 Convert to RPM"):
                rpm_needed = math.sqrt(rcf_target / (0.00001118 * radius2))
                st.metric("Required RPM", f"{rpm_needed:.0f}")
                add_to_log("Centrifuge", f"{rcf_target}g = {rpm_needed:.0f} RPM at {radius2}cm")

# --- 9. LAB TIMERS ---
elif "Lab Timers" in menu:
    st.markdown("## ⏱️ Lab Timers")
    
    # Multiple timer presets
    presets = {
        "Custom": 0,
        "Quick Spin (30s)": 0.5,
        "Vortex (10s)": 0.17,
        "Incubation (5 min)": 5,
        "Centrifuge (10 min)": 10,
        "PCR Extension (30 min)": 30,
        "Digestion (1 hour)": 60,
        "Overnight (16 hours)": 960
    }
    
    col1, col2 = st.columns([2, 1])
    with col1:
        preset = st.selectbox("Quick Preset", list(presets.keys()))
    with col2:
        if preset != "Custom":
            mins = presets[preset]
            st.metric("Duration", f"{mins} min")
        else:
            mins = st.number_input("Duration (min)", 1, 1, 1440)
    
    task = st.text_input("Task Name", "Incubation")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("▶️ Start", use_container_width=True) and not st.session_state.timer_running:
            st.session_state.timer_running = True
            st.session_state.timer_end = time.time() + (mins * 60)
            st.session_state.timer_task = task
            st.session_state.timer_duration = mins
            st.rerun()
    
    with col_btn2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.timer_running = False
    
    with col_btn3:
        if st.button("⏹️ Reset", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_end = None
            st.session_state.timer_task = ""
            st.rerun()
    
    # Timer display
    if st.session_state.timer_end:
        remaining = max(0, st.session_state.timer_end - time.time())
        
        if st.session_state.timer_running and remaining > 0:
            mins_rem = int(remaining // 60)
            secs_rem = int(remaining % 60)
            
            # Progress bar
            total_duration = st.session_state.timer_duration * 60
            progress = 1 - (remaining / total_duration)
            st.progress(min(progress, 1.0))
            
            # Big timer display
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: #f0f2f6; border-radius: 1rem;'>
                <h1 style='font-size: 4rem; font-family: monospace; color: #1f77b4;'>
                    {mins_rem:02d}:{secs_rem:02d}
                </h1>
                <p style='color: #666;'>{st.session_state.timer_task}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-refresh
            time.sleep(1)
            st.rerun()
            
        elif remaining <= 0 and st.session_state.timer_end:
            st.balloons()
            st.success(f"🔔 **{st.session_state.timer_task} Complete!**")
            add_to_log("Timer", f"{st.session_state.timer_task} finished ({st.session_state.timer_duration} min)")
            st.session_state.timer_running = False
            st.session_state.timer_end = None

# --- 10. PROTOCOL TEMPLATES (NEW PREMIUM FEATURE) ---
elif "Protocol Templates" in menu:
    st.markdown("## 📋 Protocol Templates")
    
    if st.session_state.user_email:
        st.success("✨ Pro Feature: Full protocol library unlocked!")
    else:
        st.warning("🔒 Free tier shows limited protocols. Sign up to unlock all 20+ protocols!")
    
    protocol_categories = {
        "PCR & Molecular Biology": {
            "Standard PCR (50µL)": {
                "components": {
                    "Template DNA": "1-2 µL",
                    "Forward Primer (10µM)": "1 µL",
                    "Reverse Primer (10µM)": "1 µL",
                    "dNTPs (10mM each)": "1 µL",
                    "10X PCR Buffer": "5 µL",
                    "Taq Polymerase (5U/µL)": "0.5 µL",
                    "Nuclease-free Water": "to 50 µL"
                },
                "cycling": "95°C/3min → 35×(95°C/30s, 55°C/30s, 72°C/30s) → 72°C/5min",
                "tips": "Adjust annealing temperature ±5°C based on primer Tm"
            },
            "qPCR Master Mix (20µL)": {
                "components": {
                    "2X SYBR Green Mix": "10 µL",
                    "Forward Primer (10µM)": "0.5 µL",
                    "Reverse Primer (10µM)": "0.5 µL",
                    "cDNA template": "2 µL",
                    "Nuclease-free Water": "7 µL"
                },
                "cycling": "95°C/10min → 40×(95°C/15s, 60°C/1min)",
                "tips": "Always include NTC and standard curve in triplicate"
            }
        },
        "Protein & Electrophoresis": {
            "SDS-PAGE Running Buffer (10X)": {
                "components": {
                    "Tris base": "30.3 g",
                    "Glycine": "144.1 g",
                    "SDS": "10 g",
                    "dH₂O": "to 1 L"
                },
                "storage": "Room temperature, stable for 6 months",
                "tips": "Do NOT adjust pH. Dilute to 1X before use."
            },
            "Coomassie Staining": {
                "components": {
                    "Coomassie R-250": "0.25 g",
                    "Methanol": "45 mL",
                    "Acetic acid": "10 mL",
                    "dH₂O": "45 mL"
                },
                "protocol": "Stain 30 min → Destain (40% MeOH, 10% AcOH) until clear",
                "tips": "Microwave 30s to speed up staining"
            }
        },
        "Cell Culture": {
            "Cell Passaging (Adherent)": {
                "steps": [
                    "Aspirate old media",
                    "Wash with PBS (Ca²⁺/Mg²⁺ free)",
                    "Add 0.25% trypsin-EDTA (2mL for T75)",
                    "Incubate 2-5 min at 37°C",
                    "Tap flask to detach cells",
                    "Add complete media (2X trypsin volume)",
                    "Centrifuge 300g × 5 min",
                    "Resuspend in fresh media",
                    "Split 1:3 to 1:10 depending on cell line"
                ],
                "tips": "Check confluence daily. Most lines passaged at 80-90% confluency"
            }
        }
    }
    
    if not st.session_state.user_email:
        # Free tier: show only PCR
        shown_categories = {"PCR & Molecular Biology": protocol_categories["PCR & Molecular Biology"]}
    else:
        shown_categories = protocol_categories
    
    for category, protocols in shown_categories.items():
        st.markdown(f"### {category}")
        for protocol_name, details in protocols.items():
            with st.expander(f"📄 {protocol_name}"):
                if "components" in details:
                    st.markdown("**Components:**")
                    comp_df = pd.DataFrame(details["components"].items(), 
                                          columns=["Component", "Amount"])
                    st.dataframe(comp_df, hide_index=True, use_container_width=True)
                
                if "cycling" in details:
                    st.markdown(f"**Cycling Conditions:** {details['cycling']}")
                
                if "steps" in details:
                    st.markdown("**Steps:**")
                    for i, step in enumerate(details["steps"], 1):
                        st.markdown(f"{i}. {step}")
                
                if "tips" in details:
                    st.info(f"💡 **Pro Tip:** {details['tips']}")
                
                if "storage" in details:
                    st.markdown(f"**Storage:** {details['storage']}")
                
                # Download individual protocol
                protocol_text = f"{protocol_name}\n\n"
                if "components" in details:
                    protocol_text += "Components:\n"
                    for k, v in details["components"].items():
                        protocol_text += f"  {k}: {v}\n"
                st.download_button("📥 Download", protocol_text, 
                                 f"{protocol_name.lower().replace(' ', '_')}.txt")

# --- 11. VIEW DAILY LOG ---
elif "View Daily Log" in menu:
    st.markdown("## 📊 Session Logbook")
    
    if st.session_state.logbook.empty:
        st.info("📝 No calculations logged yet. Start using the modules to build your log!")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            module_filter = st.multiselect("Filter by Module", 
                                         st.session_state.logbook["Module"].unique().tolist())
        with col2:
            if st.button("📥 Export All as CSV"):
                csv = st.session_state.logbook.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download CSV", csv, "lab_session_log.csv", 
                                 "text/csv", key="download_log")
        
        # Display filtered log
        if module_filter:
            filtered = st.session_state.logbook[st.session_state.logbook["Module"].isin(module_filter)]
        else:
            filtered = st.session_state.logbook
        
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        
        # Stats
        st.markdown(f"**Total entries:** {len(st.session_state.logbook)} | "
                   f"**Modules used:** {st.session_state.logbook['Module'].nunique()}")
        
        if st.button("🗑️ Clear Session Log", type="secondary"):
            st.session_state.logbook = pd.DataFrame(columns=["Timestamp", "Module", "Result", "User_Note"])
            st.rerun()

# --- 12. BUDGET & PRICES ---
elif "Budget" in menu:
    st.markdown("## 💰 Lab Reagent Reference Prices")
    st.caption("Approximate prices for budget planning. Actual costs may vary.")
    
    budget_data = {
        "Molecular Biology": pd.DataFrame({
            "Reagent": ["Taq Polymerase", "dNTPs Mix", "SYBR Green Mix", 
                       "Restriction Enzyme", "T4 DNA Ligase", "DNA Ladder"],
            "Price": ["$0.50/rxn", "$0.30/rxn", "$1.00/rxn", 
                     "$0.80/rxn", "$0.60/rxn", "$2.00/lane"],
            "Supplier Example": ["NEB", "Thermo", "Bio-Rad", "NEB", "NEB", "Invitrogen"]
        }),
        "Cell Culture": pd.DataFrame({
            "Reagent": ["DMEM (500mL)", "FBS (500mL)", "Trypsin-EDTA (100mL)",
                       "Pen/Strep (100mL)", "PBS (500mL)", "DMSO (50mL)"],
            "Price": ["$25", "$250", "$35", "$15", "$10", "$40"],
            "Supplier Example": ["Gibco", "Sigma", "Gibco", "Gibco", "Lonza", "Sigma"]
        }),
        "General Lab": pd.DataFrame({
            "Reagent": ["Ethanol (1L)", "Isopropanol (1L)", "Agarose (100g)",
                       "TEMED (25mL)", "APS (25g)", "Tris Base (500g)"],
            "Price": ["$30", "$25", "$80", "$15", "$10", "$45"],
            "Supplier Example": ["Fisher", "Fisher", "Bio-Rad", "Bio-Rad", "Sigma", "Sigma"]
        })
    }
    
    tabs = st.tabs(list(budget_data.keys()))
    for tab, (category, df) in zip(tabs, budget_data.items()):
        with tab:
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.metric("Estimated Monthly Budget (Small Lab)", "$200-500", 
             help="Covers basic consumables for molecular biology + cell culture work")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"v2.0 | {len(st.session_state.logbook)} actions logged")

if st.session_state.free_calculations >= MAX_FREE_CALCULATIONS:
    st.sidebar.error("🛑 Free limit reached")
    st.sidebar.button("💎 Upgrade to Pro - $4.99/mo", use_container_width=True)
