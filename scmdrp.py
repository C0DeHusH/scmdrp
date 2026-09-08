import streamlit as st
import pandas as pd

# --- Page Configuration & Custom CSS ---
st.set_page_config(page_title="SCM Delivery Planner", layout="wide", page_icon="🚛")

# Custom CSS for a professional dashboard look AND Frozen (Fixed) Header
st.markdown("""
    <style>
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* --- FROZEN (FIXED) HEADER STYLING --- */
    .fixed-header {
        position: fixed;
        top: 2.875rem; /* Starts below Streamlit's default top menu bar */
        left: 0;
        right: 0;
        background-color: #ffffff;
        z-index: 99999;
        padding: 1rem 3rem 1rem 3rem; 
        border-bottom: 2px solid #e0e0e0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    }
    
    .fixed-header h1 {
        color: #1E3A8A;
        font-weight: 700;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 2.2rem;
        line-height: 1.2;
    }
    
    .fixed-header p {
        color: #334155;
        margin: 5px 0 0 0 !important;
        font-size: 1.1rem;
    }

    /* Dark Mode Compatibility for the Frozen Header */
    @media (prefers-color-scheme: dark) {
        .fixed-header {
            background-color: #0e1117;
            border-bottom: 2px solid #262730;
        }
        .fixed-header h1 { color: #60a5fa; }
        .fixed-header p { color: #cbd5e1; }
        div[data-testid="metric-container"] {
            background-color: #1a1c23;
            border-color: #333;
        }
    }
    </style>
    
    <!-- Render the Frozen Header -->
    <div class="fixed-header">
        <h1>🚛 SCM Delivery Requirements Plan</h1>
        <p>Enterprise Logistics & Fleet Allocation Dashboard</p>
    </div>
    
    <!-- INVISIBLE SPACER: Pushes the Tabs down so they aren't hidden behind the fixed header -->
    <div style="height: 110px;"></div>
""", unsafe_allow_html=True)


# --- Helper Function for Smart Branch-Based Assignment (With Area Priority) ---
def assign_trucks_to_branches(branch_summary_df, trucks_df, area_schedule_df):
    """Assigns trucks per BRANCH, prioritizing Area Schedule Priority first, then by load size."""
    trip_pool = []
    for _, row in trucks_df.iterrows():
        trips = int(row.get("Weekly Trips", 1))
        for i in range(trips):
            trip_pool.append({
                # Clean name without trip consolidation text
                "Truck Desc": row['Truck Desc'], 
                "Max Index": row["Max Index"]
            })
            
    assignments = []
    
    # Merge with area schedule to get priorities
    branch_summary_df = branch_summary_df.merge(area_schedule_df, on="Area", how="left")
    # Default to lowest priority (99) if not defined
    branch_summary_df['Priority Level'] = pd.to_numeric(branch_summary_df['Priority Level'], errors='coerce').fillna(99)
    
    # SORTING LOGIC: Priority Level (1 is highest), then Total Index (Largest load first)
    branch_summary_df = branch_summary_df.sort_values(by=["Priority Level", "Total_Index"], ascending=[True, False])
    
    for _, row in branch_summary_df.iterrows():
        remaining_load = row["Total_Index"]
        assigned_trucks = []
        total_cap = 0
        
        while remaining_load > 0 and trip_pool:
            # Sort pool by smallest capacity to find perfect fits
            trip_pool.sort(key=lambda x: x["Max Index"])
            capable_trucks = [t for t in trip_pool if t["Max Index"] >= remaining_load]
            
            if capable_trucks:
                chosen_truck = capable_trucks[0]
            else:
                # If load exceeds any single truck, grab the largest available
                chosen_truck = trip_pool[-1]
                
            assigned_trucks.append(chosen_truck["Truck Desc"])
            total_cap += chosen_truck["Max Index"]
            remaining_load -= chosen_truck["Max Index"]
            trip_pool.remove(chosen_truck)
            
        under_util = max(0, total_cap - row["Total_Index"])
        overflow = max(0, remaining_load)
        
        priority_lvl = int(row.get("Priority Level", 99))
        
        assignments.append({
            "Priority": priority_lvl,
            "Area": row["Area"],
            "Branch": row["Branch"],
            "Total Branch Index": round(row["Total_Index"], 2),
            "Assigned Trucks": ", ".join(assigned_trucks) if assigned_trucks else "None Available",
            "Total Assigned Cap": total_cap,
            "Underutilized Space": round(under_util, 2),
            "Capacity Overflow": round(overflow, 2)
        })
        
    return pd.DataFrame(assignments), trip_pool

# --- Helper Function for Master Data Management Tabs ---
def render_master_data_manager(df_name, session_key, description):
    """Renders a standardized interface for importing, exporting, and editing master data."""
    st.caption(description)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Export Button
        csv_data = st.session_state[session_key].to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export {df_name} to CSV",
            data=csv_data,
            file_name=f"{df_name.lower().replace(' ', '_')}.csv",
            mime='text/csv',
            use_container_width=True
        )
        
    with col2:
        # Import Expander
        with st.expander(f"📤 Import / Replace {df_name}"):
            st.warning(f"Uploading a new file will **REPLACE** your current {df_name} data.")
            uploaded_md = st.file_uploader(f"Upload CSV/Excel", type=["csv", "xlsx", "xls"], key=f"import_{session_key}", label_visibility="collapsed")
            
            if uploaded_md is not None:
                if st.button("Confirm Replacement", key=f"btn_{session_key}", type="primary"):
                    try:
                        if uploaded_md.name.endswith('.csv'):
                            new_df = pd.read_csv(uploaded_md)
                        else:
                            new_df = pd.read_excel(uploaded_md)
                            
                        # Clean column names (strip whitespace)
                        new_df.columns = [str(c).strip() for c in new_df.columns]
                        
                        st.session_state[session_key] = new_df
                        st.success("✅ Master Data Updated Successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                        
    # Data Editor
    st.session_state[session_key] = st.data_editor(
        st.session_state[session_key], 
        num_rows="dynamic", 
        use_container_width=True, 
        hide_index=True,
        key=f"editor_{session_key}"
    )

# --- Initialize Session State for Master Data ---

if 'area_schedule_df' not in st.session_state:
    st.session_state.area_schedule_df = pd.DataFrame(columns=["Area", "Priority Level"])

if 'items_df' not in st.session_state:
    st.session_state.items_df = pd.DataFrame([
        {"Item Description": "ACCESS 125", "Index Size": 1.0},
        {"Item Description": "ACCESS 125 RIDE CONNECT", "Index Size": 1.0},
        {"Item Description": "AVENIS125", "Index Size": 1.0},
        {"Item Description": "BURGMAN STREET", "Index Size": 1.5},
        {"Item Description": "BURGMAN STREET EX", "Index Size": 1.5},
        {"Item Description": "DR160", "Index Size": 1.5},
        {"Item Description": "GIXXER 155", "Index Size": 2.0},
        {"Item Description": "GIXXER SF 155", "Index Size": 2.0},
        {"Item Description": "GIXXER SF 250", "Index Size": 2.0},
        {"Item Description": "GIXXER250", "Index Size": 2.0},
        {"Item Description": "RAIDER150 FI BLADE", "Index Size": 1.0},
        {"Item Description": "RAIDER150 FI PRO", "Index Size": 1.0},
        {"Item Description": "SKYDRIVE CROSSOVER", "Index Size": 1.0},
        {"Item Description": "SKYDRIVE SPORT", "Index Size": 1.0},
        {"Item Description": "SMASH FI(MAGS)", "Index Size": 1.0},
        {"Item Description": "SMASH FI(SPOKE)", "Index Size": 1.0},
        {"Item Description": "SMASH(MAGS)", "Index Size": 1.0},
        {"Item Description": "SMASH(SPOKE)", "Index Size": 1.0},
        {"Item Description": "V-STROM 160", "Index Size": 2.0},
        {"Item Description": "V-STROM 250 SX", "Index Size": 2.0},
        {"Item Description": "WIZARD", "Index Size": 1.0},
        {"Item Description": "BARAKO II (DUAL START)", "Index Size": 1.0},
        {"Item Description": "BARAKO II (KICK START)", "Index Size": 1.0},
        {"Item Description": "BARAKO III FI(DUAL START)", "Index Size": 1.0},
        {"Item Description": "BARAKO III FI(KICK START)", "Index Size": 1.0},
        {"Item Description": "BOXER", "Index Size": 1.0},
        {"Item Description": "BRUSKY125", "Index Size": 1.0},
        {"Item Description": "CT100", "Index Size": 1.0},
        {"Item Description": "CT100B", "Index Size": 1.0},
        {"Item Description": "CT125", "Index Size": 1.0},
        {"Item Description": "KLX150", "Index Size": 1.5},
        {"Item Description": "ADV160", "Index Size": 1.5},
        {"Item Description": "ADV160 ROADSYNC", "Index Size": 1.5},
        {"Item Description": "AIRBLADE 160", "Index Size": 1.5},
        {"Item Description": "BEAT FI PREM", "Index Size": 1.0},
        {"Item Description": "BEAT FI STD", "Index Size": 1.0},
        {"Item Description": "CLICK125 FI", "Index Size": 1.0},
        {"Item Description": "CLICK125 FI SE", "Index Size": 1.0},
        {"Item Description": "CLICK160 FI", "Index Size": 1.5},
        {"Item Description": "CRF150", "Index Size": 1.5},
        {"Item Description": "CRF300", "Index Size": 2.0},
        {"Item Description": "CRF300 RALLY", "Index Size": 2.0},
        {"Item Description": "GIORNO", "Index Size": 1.0},
        {"Item Description": "NAVI", "Index Size": 1.0},
        {"Item Description": "PCX160 ROADSYNC", "Index Size": 1.5},
        {"Item Description": "PCX160 STANDARD", "Index Size": 1.5},
        {"Item Description": "TMX ALPHA FI", "Index Size": 1.0},
        {"Item Description": "TMX150 SUPREMO", "Index Size": 1.0},
        {"Item Description": "WAVE RSX (DRUM)", "Index Size": 1.0},
        {"Item Description": "WAVE RSX(DISC)", "Index Size": 1.0},
        {"Item Description": "WINNER X ABS", "Index Size": 1.0},
        {"Item Description": "WINNER X RC", "Index Size": 1.0},
        {"Item Description": "WINNER X STD", "Index Size": 1.0},
        {"Item Description": "XR150", "Index Size": 1.5},
        {"Item Description": "XRM DUAL SPORTS FI(DS)", "Index Size": 1.0},
        {"Item Description": "XRM MOTARD FI", "Index Size": 1.0},
        {"Item Description": "XRM OFFROAD FI(DSX)", "Index Size": 1.0},
        {"Item Description": "XRM RS", "Index Size": 1.0},
        {"Item Description": "MIO SPORTY", "Index Size": 1.0},
        {"Item Description": "MIO i125", "Index Size": 1.0},
        {"Item Description": "MIO GEAR", "Index Size": 1.0},
        {"Item Description": "FAZZIO", "Index Size": 1.0},
        {"Item Description": "MIO GRAVIS", "Index Size": 1.0},
        {"Item Description": "YTX125", "Index Size": 1.5},
        {"Item Description": "XTZ125", "Index Size": 1.5},
        {"Item Description": "MIO AEROX 155", "Index Size": 1.5},
        {"Item Description": "MIO AEROX S 155", "Index Size": 1.5},
        {"Item Description": "NMAX155 FI ABS", "Index Size": 1.5},
        {"Item Description": "NMAX155 TECHMAX", "Index Size": 1.5},
        {"Item Description": "SNIPER 155 FI", "Index Size": 1.5},
        {"Item Description": "MT15", "Index Size": 1.5},
        {"Item Description": "MT03", "Index Size": 1.5},
        {"Item Description": "R15", "Index Size": 1.5},
        {"Item Description": "R3", "Index Size": 1.5},
        {"Item Description": "SEROW", "Index Size": 1.5},
        {"Item Description": "XSR", "Index Size": 1.5},
        {"Item Description": "PG-01", "Index Size": 1.5},
        {"Item Description": "LEXI 155", "Index Size": 1.5},
        {"Item Description": "YZ250F BSB4", "Index Size": 1.5},
        {"Item Description": "YZ250FX BAJH", "Index Size": 1.5},
        {"Item Description": "YZ250X BRY3", "Index Size": 1.5},
        {"Item Description": "YZ250 BRCB", "Index Size": 1.5},
        {"Item Description": "YZ450F BHRB", "Index Size": 1.5},
        {"Item Description": "WR155", "Index Size": 2.0},
        {"Item Description": "XMAX", "Index Size": 2.0},
        {"Item Description": "WR250F BAKH", "Index Size": 2.0},
        {"Item Description": "WR250F BAKA", "Index Size": 2.0},
        {"Item Description": "WR450F BDB5", "Index Size": 2.0},
        {"Item Description": "WR450F BDB9", "Index Size": 2.0},
        {"Item Description": "PW50 BSL4", "Index Size": 2.0},
        {"Item Description": "YZ125X", "Index Size": 2.0},
        {"Item Description": "YZF-R1M D466", "Index Size": 2.0},
        {"Item Description": "YZF-R7 BEBV", "Index Size": 2.0},
        {"Item Description": "BOLT R-SPEC BDU7", "Index Size": 2.0},
        {"Item Description": "YZF-R7 BEB6", "Index Size": 2.0},
        {"Item Description": "YZ125 B4XC", "Index Size": 2.0},
        {"Item Description": "TMAX TECH MAX BBWD", "Index Size": 3.0},
        {"Item Description": "YZ65 BR8P", "Index Size": 3.0},
        {"Item Description": "MT-10 SP BGG8", "Index Size": 3.0},
        {"Item Description": "TMAX BBV5", "Index Size": 3.0},
        {"Item Description": "TRACER 9 GT BAP4", "Index Size": 3.0},
        {"Item Description": "SUPER TENERE ES BUY5", "Index Size": 3.0},
        {"Item Description": "TENERE 700 BMB3", "Index Size": 3.0},
        {"Item Description": "XSR700 BMC3", "Index Size": 3.5},
        {"Item Description": "MT-07 BATP", "Index Size": 3.5},
        {"Item Description": "MT-09 B7NL", "Index Size": 3.5},
        {"Item Description": "XSR900 BEA8", "Index Size": 3.5},
        {"Item Description": "YZ85 B4BF", "Index Size": 4.0},
        {"Item Description": "SPARE PARTS - SMALL BOX", "Index Size": 0.1},
        {"Item Description": "SPARE PARTS - MEDIUM BOX", "Index Size": 0.25},
        {"Item Description": "SPARE PARTS - LARGE BOX", "Index Size": 0.5},
        {"Item Description": "SPARE PARTS - XLARGE BOX", "Index Size": 1.0},
        {"Item Description": "TIRES BUNDLE - SMALL(25'S)", "Index Size": 0.25},
        {"Item Description": "TIRES BUNDLE - MEDIUM(25'S)", "Index Size": 0.5}
    ])

if 'trucks_df' not in st.session_state:
    st.session_state.trucks_df = pd.DataFrame([
        {"Plate No.": "NFJ 1986", "Max Index": 40.0, "Weekly Trips": 2, "Truck Desc": "ISUZU 6W - 40 Cap"},
        {"Plate No.": "MAD 2439", "Max Index": 24.0, "Weekly Trips": 3, "Truck Desc": "ISUZU 6W - 24 Cap"},
        {"Plate No.": "NBQ 9462", "Max Index": 24.0, "Weekly Trips": 3, "Truck Desc": "ISUZU 6W - 24 Cap"},
        {"Plate No.": "NHE 4554", "Max Index": 36.0, "Weekly Trips": 2, "Truck Desc": "HOWO 6W - 36 Cap"},
        {"Plate No.": "NHE 4604", "Max Index": 36.0, "Weekly Trips": 2, "Truck Desc": "HOWO 6W - 36 Cap"}
    ])

if 'branches_df' not in st.session_state:
    st.session_state.branches_df = pd.DataFrame([
        {"Branches": "HONDA ISULAN", "Area": "AREA I"},
        {"Branches": "HONDA SURALLAH", "Area": "AREA I"},
        {"Branches": "MUTI BANGA", "Area": "AREA I"},
        {"Branches": "MUTI ISULAN", "Area": "AREA I"},
        {"Branches": "MUTI SURALLAH", "Area": "AREA I"},
        {"Branches": "MUTI TACURONG", "Area": "AREA I"},
        {"Branches": "HONDA MARAMAG", "Area": "AREA II"},
        {"Branches": "MUTI DON CARLOS", "Area": "AREA II"},
        {"Branches": "MUTI LAPASAN", "Area": "AREA II"},
        {"Branches": "MUTI MARAMAG", "Area": "AREA II"},
        {"Branches": "MUTI QUEZON", "Area": "AREA II"},
        {"Branches": "MUTI VALENCIA", "Area": "AREA II"},
        {"Branches": "MUTI BULUA", "Area": "AREA II"},
        {"Branches": "MUTI MANOLO", "Area": "AREA II"},
        {"Branches": "MUTI NABUNTURAN", "Area": "AREA III-A"},
        {"Branches": "MUTI PANABO", "Area": "AREA III-A"},
        {"Branches": "MUTI SAMAL", "Area": "AREA III-A"},
        {"Branches": "MUTI TAGUM 3", "Area": "AREA III-A"},
        {"Branches": "MUTI TAGUM 1", "Area": "AREA III-A"},
        {"Branches": "MUTI TAGUM 2", "Area": "AREA III-A"},
        {"Branches": "MUTI TIBUNGCO", "Area": "AREA III-A"},
        {"Branches": "MUTI BANSALAN", "Area": "AREA III-B"},
        {"Branches": "MUTI CABANTIAN", "Area": "AREA III-B"},
        {"Branches": "MUTI CALINAN", "Area": "AREA III-B"},
        {"Branches": "MUTI CATALUNAN GRANDE", "Area": "AREA III-B"},
        {"Branches": "MUTI DIGOS", "Area": "AREA III-B"},
        {"Branches": "MUTI ECOLAND", "Area": "AREA III-B"},
        {"Branches": "MUTI KABACAN", "Area": "AREA IV"},
        {"Branches": "MUTI KIDAPAWAN", "Area": "AREA IV"},
        {"Branches": "MUTI MIDSAYAP", "Area": "AREA IV"},
        {"Branches": "MUTI MLANG", "Area": "AREA IV"},
        {"Branches": "HONDA KORONADAL", "Area": "AREA V"},
        {"Branches": "MUTI 3S", "Area": "AREA V"},
        {"Branches": "MUTI MALUNGON", "Area": "AREA V"},
        {"Branches": "MUTI MARBEL", "Area": "AREA V"},
        {"Branches": "MUTI POLOMOLOK", "Area": "AREA V"},
        {"Branches": "MUTI TUPI", "Area": "AREA V"},
        {"Branches": "MUTI ALABEL", "Area": "AREA V"},
        {"Branches": "HONDA MALUNGON", "Area": "AREA V"},
        {"Branches": "MUTI SAN FRANCISCO", "Area": "AREA VI"},
        {"Branches": "MUTI BUTUAN", "Area": "AREA VI"},
        {"Branches": "MUTI BAYUGAN", "Area": "AREA VI"},
        {"Branches": "MUTI PROSPERIDAD", "Area": "AREA VI"},
        {"Branches": "MUTI CABADBARAN", "Area": "AREA VI"}
    ])

if 'weekly_plan' not in st.session_state:
    st.session_state.weekly_plan = pd.DataFrame(columns=[
        "Date", "Priority", "Area", "Branch", "Unit Allocated", "Quantity", "Assigned Truck(s)", "Total Index Load"
    ])

if 'planner_input' not in st.session_state:
    st.session_state.planner_input = []

if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# --- Application Tabs ---
tab1, tab2, tab3 = st.tabs(["📅 Weekly Master Planner", "📊 Allocation Summary", "⚙️ Master Data Management"])

# --- TAB 1: Weekly Master Planner ---
with tab1:
    
    col_up, col_man = st.columns([1, 1])
    
    with col_up:
        st.subheader("📁 1. Upload Allocation")
        st.caption("Upload **ALloc Template.xlsx**. Grid auto-updates.")
        uploaded_file = st.file_uploader("Select Excel File", type=["xlsx", "xls"], key=f"upload_{st.session_state.uploader_key}", label_visibility="collapsed")
        
        if uploaded_file is not None:
            try:
                df_uploaded = pd.read_excel(uploaded_file)
                mapping = {"Standard Description": "Item", "Qty Transfer": "Qty", "Branch": "Branch", "AREA": "Area"}
                df_mapped = df_uploaded.rename(columns=mapping).dropna(subset=["Item", "Qty"])
                
                # Clean strings to prevent mismatch
                for col in ['Item', 'Branch', 'Area']:
                    if col in df_mapped.columns:
                        df_mapped[col] = df_mapped[col].astype(str).str.strip()
                
                new_entries = df_mapped[["Area", "Branch", "Item", "Qty"]].to_dict('records')
                st.session_state.planner_input.extend(new_entries)
                st.session_state.uploader_key += 1 
                st.success(f"✅ Successfully loaded {len(new_entries)} records!")
                st.rerun()
                    
            except Exception as e:
                st.error(f"File mismatch error: {e}")

    with col_man:
        st.subheader("✍️ 2. Quick Add (Manual)")
        with st.expander("Expand to manually input items"):
            c1, c2 = st.columns(2)
            unique_areas = sorted(st.session_state.branches_df['Area'].dropna().unique())
            
            with c1:
                sel_area = st.selectbox("Area", unique_areas)
                sel_item = st.selectbox("Item", st.session_state.items_df["Item Description"].tolist())
            with c2:
                filtered_branches = st.session_state.branches_df[st.session_state.branches_df['Area'] == sel_area]['Branches'].tolist()
                sel_branch = st.selectbox("Branch", filtered_branches)
                sel_qty = st.number_input("Qty", min_value=1, step=1, value=1)
                
            if st.button("Add Entry", use_container_width=True, type="secondary"):
                st.session_state.planner_input.append({"Area": sel_area, "Branch": sel_branch, "Item": sel_item, "Qty": sel_qty})
                st.rerun() 
                
    st.markdown("---")
    
    st.subheader("📋 3. Loadout Grid")
    current_loadout_df = pd.DataFrame(st.session_state.planner_input)
    
    if not current_loadout_df.empty:
        edited_df = st.data_editor(
            current_loadout_df,
            column_config={
                "Area": st.column_config.SelectboxColumn("Area", options=unique_areas, required=True),
                "Branch": st.column_config.SelectboxColumn("Branch", options=st.session_state.branches_df['Branches'].tolist(), required=True),
                "Item": st.column_config.SelectboxColumn("Item", options=st.session_state.items_df["Item Description"].tolist(), required=True),
                "Qty": st.column_config.NumberColumn("Quantity", min_value=1, step=1)
            },
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="dispatch_grid"
        )
        st.session_state.planner_input = edited_df.to_dict('records')
    else:
        st.info("The loadout is empty. Please upload a template or use the quick add.")
        edited_df = pd.DataFrame(columns=["Area", "Branch", "Item", "Qty"])

    valid_entries = edited_df.dropna(subset=["Branch", "Item"])
    
    # --- ACTIVE AREA SCHEDULE EDITOR ---
    if not valid_entries.empty:
        st.markdown("---")
        st.subheader("⭐ 4. Set Area Priority")
        st.caption("Manually adjust the Priority Level (1 = Highest) exclusively for the areas present in your current loadout.")
        
        active_areas = valid_entries["Area"].unique()
        active_schedule = st.session_state.area_schedule_df[st.session_state.area_schedule_df["Area"].isin(active_areas)].copy()
        
        missing_areas = set(active_areas) - set(active_schedule["Area"])
        if missing_areas:
            missing_df = pd.DataFrame([{"Area": a, "Priority Level": 99} for a in missing_areas])
            active_schedule = pd.concat([active_schedule, missing_df], ignore_index=True)
            
        edited_schedule = st.data_editor(
            active_schedule,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Area": st.column_config.TextColumn("Area", disabled=True),
                "Priority Level": st.column_config.NumberColumn("Priority (1=High)", min_value=1, max_value=99, step=1)
            },
            key="active_schedule_editor"
        )
        
        master_clean = st.session_state.area_schedule_df[~st.session_state.area_schedule_df["Area"].isin(active_areas)]
        st.session_state.area_schedule_df = pd.concat([master_clean, edited_schedule], ignore_index=True)
        
        # Calculate valid items and group by BRANCH
        valid_entries["Qty"] = pd.to_numeric(valid_entries["Qty"], errors='coerce').fillna(0)
        valid_entries = valid_entries[valid_entries["Qty"] > 0]
        valid_entries = valid_entries.merge(st.session_state.items_df, how="left", left_on="Item", right_on="Item Description")
        valid_entries["Total Index"] = valid_entries["Qty"] * valid_entries["Index Size"]
        
        # We group by BRANCH now instead of AREA
        branch_summary = valid_entries.groupby(["Area", "Branch"]).agg(
            Total_Index=('Total Index', 'sum')
        ).reset_index()
        
        insight_df, remaining_pool = assign_trucks_to_branches(branch_summary, st.session_state.trucks_df, edited_schedule)
        
        # Mappings based on Branch
        assignment_mapping = dict(zip(insight_df["Branch"], insight_df["Assigned Trucks"]))
        priority_mapping = dict(zip(insight_df["Area"], insight_df["Priority"]))
        
        st.markdown("---")
        st.subheader("🧠 5. AI Smart Assignment (Per Branch)")
        
        total_index_all = branch_summary["Total_Index"].sum()
        total_fleet_cap = sum(row["Max Index"] * int(row.get("Weekly Trips", 1)) for _, row in st.session_state.trucks_df.iterrows())
        remaining_fleet_cap = sum(t["Max Index"] for t in remaining_pool)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Total Load Index", f"{total_index_all:.2f}")
        c2.metric("🚛 Global Fleet Cap", f"{total_fleet_cap:.2f}")
        c3.metric("🟢 Remaining Cap", f"{remaining_fleet_cap:.2f}")
        
        if total_index_all > total_fleet_cap:
            c4.error(f"🚨 Deficit: {(total_index_all - total_fleet_cap):.2f}")
        else:
            c4.success(f"✅ Surplus Detected")
            
        st.dataframe(
            insight_df.style.background_gradient(subset=['Underutilized Space'], cmap='Blues')
                           .background_gradient(subset=['Capacity Overflow'], cmap='Reds')
                           .set_properties(subset=['Priority'], **{'font-weight': 'bold', 'color': '#1E3A8A'}),
            use_container_width=True, hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_save, col_clear = st.columns([1, 4])
        
        with col_save:
            if st.button("💾 Save to Summary", type="primary", use_container_width=True):
                records = []
                current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                
                for _, row in valid_entries.iterrows():
                    records.append({
                        "Date": current_time,
                        "Priority": priority_mapping.get(row["Area"], 99),
                        "Area": row["Area"],
                        "Branch": row["Branch"],
                        "Unit Allocated": row["Item"],
                        "Quantity": row["Qty"],
                        "Assigned Truck(s)": assignment_mapping.get(row["Branch"], "None"),
                        "Total Index Load": row["Total Index"]
                    })
                
                new_records_df = pd.DataFrame(records)
                st.session_state.weekly_plan = pd.concat([st.session_state.weekly_plan, new_records_df], ignore_index=True)
                st.toast("✅ Allocations saved to Weekly Summary.")
                
        with col_clear:
            if st.button("🗑️ Clear Loadout"):
                st.session_state.planner_input = []
                st.rerun()

# --- TAB 2: Weekly Allocation Summary ---
with tab2:
    st.subheader("📊 Saved Allocations & Reporting")
    
    if not st.session_state.weekly_plan.empty:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                all_areas = sorted(st.session_state.weekly_plan["Area"].unique())
                filter_area = st.multiselect("🔍 Filter by Area", options=all_areas)
            with col2:
                if filter_area:
                    available_branches = sorted(st.session_state.weekly_plan[st.session_state.weekly_plan["Area"].isin(filter_area)]["Branch"].unique())
                else:
                    available_branches = sorted(st.session_state.weekly_plan["Branch"].unique())
                filter_branch = st.multiselect("🔍 Filter by Branch", options=available_branches)
            
            filtered_df = st.session_state.weekly_plan.copy()
            if filter_area:
                filtered_df = filtered_df[filtered_df["Area"].isin(filter_area)]
            if filter_branch:
                filtered_df = filtered_df[filtered_df["Branch"].isin(filter_branch)]
                
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        c1, c2, c3 = st.columns([1, 1, 3])
        with c1:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Export CSV", data=csv, file_name='weekly_allocation_summary.csv', mime='text/csv')
        with c2:
            if st.button("🚨 Clear Summary Database", type="primary"):
                st.session_state.weekly_plan = pd.DataFrame(columns=[
                    "Date", "Priority", "Area", "Branch", "Unit Allocated", "Quantity", "Assigned Truck(s)", "Total Index Load"
                ])
                st.rerun()
    else:
        st.info("No dispatches saved yet. Complete a dispatch plan in the Master Planner.")

# --- TAB 3: Master Data Management ---
with tab3:
    st.subheader("⚙️ System Configuration & Master Data")
    
    sub1, sub2, sub3, sub4 = st.tabs(["📦 Item Library", "🚚 Fleet Config", "🏢 Branch Master", "⭐ Default Priority History"])
    
    with sub1:
        render_master_data_manager(
            df_name="Items Configuration", 
            session_key="items_df", 
            description="Manage item details and their physical index sizes."
        )
        
    with sub2:
        render_master_data_manager(
            df_name="Fleet Details", 
            session_key="trucks_df", 
            description="Manage truck capacity and weekly multi-trip availability."
        )

    with sub3:
        render_master_data_manager(
            df_name="Branch Mapping", 
            session_key="branches_df", 
            description="Map branches to their designated regional areas."
        )
        
    with sub4:
        render_master_data_manager(
            df_name="Historical Priority Levels", 
            session_key="area_schedule_df", 
            description="Review or adjust the saved historical priorities for previously mapped areas."
        )
