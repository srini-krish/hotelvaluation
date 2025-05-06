import streamlit as st
import numpy as np
import pandas as pd

# --------------------------------------------------
# Base Hotel Assumptions (edited in sidebar)
# --------------------------------------------------
BASE = {
    "Hotel Name": "Maple Grove Inn",
    "Location": "Asheville, NC",
    "Room Count": 18,
    "ADR": 175.0,             
    "Occupancy Rate": 0.62,    
    "Annual Revenue": 710_000.0,
    "Operating Expenses": 480_000.0,  
    "NOI": 230_000.0,  
    "Sale Price (Last Year)": 1_800_000.0,  
    "Market Cap Rate": 0.085,  
    "ADR Multiplier": 7.6,     
    # "Equity %": 0.30,          
    "Equity (Invested)": 10_000.0, 
}

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Valuation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Sidebar – User-Editable Inputs
# --------------------------------------------------
st.sidebar.header("Assumptions")
hotel_name = st.sidebar.text_input("Hotel Name", value=BASE["Hotel Name"])
location = st.sidebar.text_input("Location", value=BASE["Location"])
room_count = st.sidebar.number_input("Room Count", min_value=1, max_value=500, value=BASE["Room Count"], step=1)
adr = st.sidebar.number_input("Average Daily Rate (ADR) [$]", value=BASE["ADR"], step=1.0)
occ = st.sidebar.slider(
    "Occupancy Rate [%]", min_value=30.0, max_value=100.0, value=BASE["Occupancy Rate"] * 100, step=1.0
) / 100.0
cap_rate = st.sidebar.slider(
    "Market Cap Rate [%]", min_value=1.0, max_value=50.0, value=BASE["Market Cap Rate"] * 100, step=0.5
) / 100.0
annual_rev = st.sidebar.number_input("Annual Revenue [$]", value=BASE["Annual Revenue"], step=1000.0)
opex = st.sidebar.number_input("Annual Operating Expenses [$]", value=BASE["Operating Expenses"], step=1000.0)
noi = st.sidebar.number_input("NOI [$]", value=BASE["NOI"], step=1000.0)
sale_price = st.sidebar.number_input("Sale Price (Last Year) [$]", value=BASE["Sale Price (Last Year)"], step=1000.0)
adr_multiplier = st.sidebar.number_input("ADR Multiplier", value=BASE["ADR Multiplier"], step=0.1)
equity_pct = st.sidebar.number_input("Equity (Invested)", value=BASE["Equity (Invested)"], step=1000.0)

# equity_pct = st.sidebar.slider(
#     "Equity Percentage [%]", min_value=10.0, max_value=100.0, value=BASE["Equity %"] * 100, step=5.0
# ) / 100.0



# --------------------------------------------------
# Core Valuation Functions
# --------------------------------------------------
def income_approach(noi: float, c_rate: float) -> float:
    """Direct Capitalization."""
    return round(noi / c_rate,2)

def adr_multiplier_approach(adr_: float, rooms: int, mult: float) -> float:
    """ADR * Rooms * Multiplier."""
    return round(adr_ * rooms * mult,2)

def cash_on_cash(noi: float, value: float, eq_pct: float) -> float:
    return round(noi / (value),2)

def cash_on_cash_return(noi: float, value: float, eq_pct: float) -> float:
    return round(noi / eq_pct,2)


# --------------------------------------------------
# Base-Case Calculations
# --------------------------------------------------

value_income = income_approach(noi, cap_rate)
value_adr = adr_multiplier_approach(adr, room_count, adr_multiplier)


coc_income = cash_on_cash(noi, value_income, equity_pct)
coc_adr = cash_on_cash(noi, value_adr, equity_pct)
coc_return = cash_on_cash_return(noi, value_adr, equity_pct)

st.title(f"{hotel_name} · Valuation Dashboard")
st.subheader(f"Location: {location}")

col1, col2, col3 = st.columns(3)
col1.metric("Net Operating Income (NOI)", f"${noi:,.2f}")
col2.metric("Income Approach Value", f"${value_income:,.2f}")
col3.metric("ADR Multiplier Value", f"${value_adr:,.2f}")

col4, col5 = st.columns(2)
col4.metric("Cash-on-Cash (Income)", f"{coc_income:.3f}")
col5.metric("Cash-on-Cash (ADR)", f"{coc_adr:.3f}")

col6 = st.columns(1)
col4.metric("Cash-on-Cash (Return)", f"{coc_return:.3f}")

with st.expander("📈 Valuation range Analysis", expanded=False):
    st.markdown("Adjust ranges below to explore how key variables affect value.")

    adr_rng = st.slider("ADR Range [$]", 50, 500, (70, 95), step=5)
    occ_rng = st.slider("Occupancy Range [%]", 10, 100, (55, 85), step=5)
    cap_rng = st.slider("Cap Rate Range [%]", 1, 50, (7, 11), step=1)

    adr_vals = np.arange(adr_rng[0], adr_rng[1] + 0.01, 25)
    occ_vals = np.arange(occ_rng[0] / 100, occ_rng[1] / 100 + 0.0001, 0.05)
    cap_vals = np.arange(cap_rng[0] / 100, cap_rng[1] / 100 + 0.0001, 0.01)

    records = []
    for adr_i in adr_vals:
        for occ_i in occ_vals:
            for cap_i in cap_vals:
                rev_i = round(adr_i * room_count * occ_i * 365,2)
                noi_i = round(rev_i - opex,2)
                val_inc_i = income_approach(noi_i, cap_i)
                val_adr_i = adr_multiplier_approach(adr_i, room_count, adr_multiplier)
                records.append({
                    "ADR": adr_i,
                    "Occ": occ_i,
                    "Cap": cap_i,
                    "Rev": rev_i,
                    "NOI": noi_i,
                    "Value_Income": val_inc_i,
                    "Value_ADR": val_adr_i,
                })

    sens_df = pd.DataFrame(records)

    # Display first few rows in an interactive table
    st.dataframe(sens_df.head(500), use_container_width=True)

    # Download button for full Valuation range data
    csv_bytes = sens_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Valuation range CSV", csv_bytes, "valuation_range.csv", "text/csv")