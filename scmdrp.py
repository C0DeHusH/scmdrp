import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="SCM Delivery Requirements Plan", layout="wide", page_icon="🏍️")
st.title("🏍️ SCM Delivery Requirements Plan")
st.markdown("---")

# --- Initialize Session State for Master Data (FULL LIST) ---
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
        {"Plate No.": "NFJ 1986 (ISUZU 6W - 40 Cap)", "Max Index": 40.0, "Truck Desc": "NFJ 1986 (ISUZU 6W - 40 Cap)"},
        {"Plate No.": "MAD 2439 (ISUZU 6W - 24 Cap)", "Max Index": 24.0, "Truck Desc": "MAD 2439 (ISUZU 6W - 24 Cap)"},
        {"Plate No.": "NBQ 9462 (ISUZU 6W - 24 Cap)", "Max Index": 24.0, "Truck Desc": "NBQ 9462 (ISUZU 6W - 24 Cap)"},
        {"Plate No.": "NHE 4554 (HOWO/SINOTRUCK 6W - 36 Cap)", "Max Index": 36.0, "Truck Desc": "NHE 4554 (HOWO/SINOTRUCK 6W - 36 Cap)"},
        {"Plate No.": "NHE 4604 (HOWO/SINOTRUCK 6W - 36 Cap)", "Max Index": 36.0, "Truck Desc": "NHE 4604 (HOWO/SINOTRUCK 6W - 36 Cap)"}
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
        "Date", "Initial Truck", "Area", "Branch", "Unit Allocated", "Quantity", "Spillover Truck", "Total Index Load"
    ])

if 'planner_input' not in st.session_state:
    st.session_state.planner_input = []

# --- Create Application Tabs ---
tab1, tab2, tab3 = st.tabs(["📋 Daily Dispatch Planner", "📅 Weekly Allocation Summary", "⚙️ Master Data Management"])

# --- TAB 1: Daily Dispatch Planner ---
with tab1:
    
    with st.container():
        st.subheader("🚛 1. Select Initial Truck")
        primary_truck = st.selectbox("Assign Primary Truck for this Route:", st.session_state.trucks_df["Truck Desc"].tolist(), label_visibility="collapsed")
        truck_capacity = st.session_state.trucks_df.loc[st.session_state.trucks_df['Truck Desc'] == primary_truck, 'Max Index'].values[0]
    
    st.markdown("---")
    
    st.subheader("📦 2. Rapid Data Entry")
    st.caption("Select Area to filter Branches, pick an Item, and click Add. You can edit or delete entries in the grid below.")
    
    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns([2, 2, 3, 1, 1])
        
        with c1:
            unique_areas = sorted(st.session_state.branches_df['Area'].unique())
            sel_area = st.selectbox("1. Select Area", unique_areas)
            
        with c2:
            filtered_branches = st.session_state.branches_df[st.session_state.branches_df['Area'] == sel_area]['Branches'].tolist()
            sel_branch = st.selectbox("2. Select Branch", filtered_branches)
            
        with c3:
            sel_item = st.selectbox("3. Select Item", st.session_state.items_df["Item Description"].tolist())
            
        with c4:
            sel_qty = st.number_input("4. Qty", min_value=1, step=1, value=1)
            
        with c5:
            st.write("") 
            st.write("")
            if st.button("➕ Add", use_container_width=True):
                st.session_state.planner_input.append({
                    "Area": sel_area,
                    "Branch": sel_branch,
                    "Item": sel_item,
                    "Qty": sel_qty
                })
                st.toast(f"✅ Added {sel_qty}x {sel_item} to loadout!")
                st.rerun() 
                
    st.subheader("📝 3. Review & Edit Loadout")
    st.caption("**How to Delete a row:** Click the gray box on the far left of the row, then press your `Delete` key (or click the trash icon in the top right of the grid).")
    
    current_loadout_df = pd.DataFrame(st.session_state.planner_input)
    
    if not current_loadout_df.empty:
        # Made columns editable via dropdowns instead of disabled text
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
            key="dispatch_grid"
        )
        
        st.session_state.planner_input = edited_df.to_dict('records')
    else:
        st.info("Your loadout is empty. Use the rapid entry bar above to add items.")
        edited_df = pd.DataFrame(columns=["Area", "Branch", "Item", "Qty"])

    valid_entries = edited_df.dropna(subset=["Branch", "Item"])
    
    total_index = 0
    if not valid_entries.empty:
        valid_entries = valid_entries[valid_entries["Qty"] > 0]
        valid_entries = valid_entries.merge(st.session_state.items_df, how="left", left_on="Item", right_on="Item Description")
        valid_entries["Total Index"] = valid_entries["Qty"] * valid_entries["Index Size"]
        total_index = valid_entries["Total Index"].sum()
    
    spillover = max(0, total_index - truck_capacity)
    
    if total_index == 0:
        status = "AWAITING LOAD"
    elif spillover > 0:
        status = "⚠️ OVERLOADED - SPILLOVER DETECTED"
    else:
        status = "✅ OPTIMAL LOAD"
        
    auto_truck = "N/A - NO OVERFLOW"
    if spillover > 0:
        available = st.session_state.trucks_df[st.session_state.trucks_df["Max Index"] >= spillover].sort_values(by="Max Index")
        if not available.empty:
            auto_truck = available.iloc[0]["Truck Desc"]
        else:
            auto_truck = "🚨 MULTIPLE ADDITIONAL TRUCKS REQUIRED"

    st.markdown("---")
    st.subheader("📊 4. Real-Time Capacity Status")
    
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Load Index", f"{total_index:.2f}")
        col2.metric("Initial Truck Status", status)
        col3.metric("Spillover Index (Unassigned)", f"{spillover:.2f}")
        col4.metric("Auto-Assigned Additional Truck", auto_truck)
    
    st.markdown("---")
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("💾 Save to Weekly Summary", type="primary", use_container_width=True):
            if not valid_entries.empty:
                records = []
                current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                
                for _, row in valid_entries.iterrows():
                    records.append({
                        "Date": current_time,
                        "Initial Truck": primary_truck,
                        "Area": row["Area"],
                        "Branch": row["Branch"],
                        "Unit Allocated": row["Item"],
                        "Quantity": row["Qty"],
                        "Spillover Truck": auto_truck if spillover > 0 else "None",
                        "Total Index Load": total_index
                    })
                
                new_records_df = pd.DataFrame(records)
                st.session_state.weekly_plan = pd.concat([st.session_state.weekly_plan, new_records_df], ignore_index=True)
                
                # Replaced static success with a pop-up Toast
                st.toast("🎉 Detailed dispatches saved to Weekly Summary successfully!", icon="✅")
            else:
                st.toast("⚠️ No items added to the loadout yet.", icon="⚠️")
                
    with c2:
        if st.button("🗑️ Clear Entire Loadout"):
            st.session_state.planner_input = []
            st.toast("🗑️ Loadout cleared.", icon="✅")
            st.rerun()

# --- TAB 2: Weekly Allocation Summary ---
with tab2:
    st.header("Weekly Allocation Summary")
    st.info("This table tracks granular daily loads including destination branches, areas, and specific unit allocations.")
    
    if not st.session_state.weekly_plan.empty:
        st.dataframe(st.session_state.weekly_plan, use_container_width=True)
        csv = st.session_state.weekly_plan.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Export Detailed Weekly Summary to CSV", data=csv, file_name='weekly_allocation_summary_detailed.csv', mime='text/csv')
    else:
        st.write("No dispatches saved yet. Go to the Daily Dispatch Planner and save a load.")

# --- TAB 3: Master Data Management ---
with tab3:
    st.header("Master Data Editor")
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader("Items & Index")
        st.session_state.items_df = st.data_editor(st.session_state.items_df, num_rows="dynamic", use_container_width=True)
    with c2:
        st.subheader("Fleet Capacity")
        st.session_state.trucks_df = st.data_editor(st.session_state.trucks_df, num_rows="dynamic", use_container_width=True)
    with c3:
        st.subheader("Branches")
        st.session_state.branches_df = st.data_editor(st.session_state.branches_df, num_rows="dynamic", use_container_width=True)