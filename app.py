"""
app.py - VryfID NYC Rental Seasonality Intelligence Dashboard

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import (
    manhattan_2024,
    brooklyn_2024,
    nw_queens_2024,
    seasonal_insights,
    vryfid_growth_metrics,
)


st.set_page_config(
    page_title="NYC Rental Seasonality | VryfID Growth Intelligence",
    page_icon="📊",
    layout="wide",
)


df_manhattan = pd.DataFrame(manhattan_2024)
df_brooklyn = pd.DataFrame(brooklyn_2024)
df_queens = pd.DataFrame(nw_queens_2024)


st.title("NYC Rental Market Seasonality Intelligence")
st.markdown(
    "**Prepared for VryfID** | Data: Douglas Elliman / Miller Samuel Monthly Reports (2024)"
)
st.markdown("---")


metrics = vryfid_growth_metrics

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Peak Monthly Leases (Aug)",
    value=f"{metrics['peak_lease_volume']['value']:,}",
    delta="Record high for August",
)
col2.metric(
    label="Winter Trough (Jan)",
    value=f"{metrics['winter_trough_volume']['value']:,}",
    delta="-52% vs peak",
    delta_color="inverse",
)
col3.metric(
    label="Fastest Lease Speed (Jun)",
    value=f"{metrics['summer_days_on_market']['value']} days",
    delta="Lowest on record",
)
col4.metric(
    label="Peak Bidding Wars (Jun)",
    value=f"{metrics['peak_bidding_wars']['value']}%",
    delta="1 in 4 above asking",
)

st.markdown("---")

st.header("1. The Seasonal Demand Cycle")
st.markdown(
    "New lease signings more than **double** from winter to summer. "
    "Manhattan goes from 3,922 leases in January to 8,223 in August."
)

df_leases = df_manhattan.dropna(subset=["new_leases"])

fig_leases = px.bar(
    df_leases,
    x="month",
    y="new_leases",
    text="new_leases",
    color="new_leases",
    color_continuous_scale="teal",
)

fig_leases.update_layout(
    title="Manhattan New Lease Signings by Month (2024)",
    xaxis_title="",
    yaxis_title="New Leases",
    showlegend=False,
    coloraxis_showscale=False,
    height=450,
)

fig_leases.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
)

st.plotly_chart(fig_leases, use_container_width=True)


st.header("2. Rent Stays Flat, Volume Explodes")
st.markdown(
    "The surprise: Manhattan median rent only varies about $234 across the entire year "
    "($4,100 in Mar to $4,334 in Dec). The real seasonal shift is in **volume and speed**, "
    "not price. Lease signings more than double while rent barely moves."
)

df_both = df_manhattan.dropna(subset=["median_rent"])

fig_dual = go.Figure()

df_leases_clean = df_manhattan.dropna(subset=["new_leases"])
fig_dual.add_trace(
    go.Bar(
        x=df_leases_clean["month"],
        y=df_leases_clean["new_leases"],
        name="New Leases",
        marker_color="rgba(13, 148, 136, 0.3)",
        yaxis="y",
    )
)

fig_dual.add_trace(
    go.Scatter(
        x=df_both["month"],
        y=df_both["median_rent"],
        name="Median Rent",
        mode="lines+markers",
        line=dict(color="#0D9488", width=3),
        marker=dict(size=8),
        yaxis="y2",
    )
)

fig_dual.update_layout(
    title="Volume vs Price: The Real Seasonal Story",
    yaxis=dict(title="New Leases", side="left"),
    yaxis2=dict(title="Median Rent ($)", side="right", overlaying="y"),
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
)

st.plotly_chart(fig_dual, use_container_width=True)


st.header("3. Borough-Level Patterns")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Median Rent Comparison")
    
    df_m = df_manhattan[["month", "month_num", "median_rent"]].copy()
    df_m["borough"] = "Manhattan"
    
    df_b = df_brooklyn[["month", "month_num", "median_rent"]].copy()
    df_b["borough"] = "Brooklyn"
    
    df_q = df_queens[["month", "month_num", "median_rent"]].copy()
    df_q["borough"] = "NW Queens"
    
    df_all = pd.concat([df_m, df_b, df_q], ignore_index=True)
    df_all = df_all.dropna(subset=["median_rent"])
    df_all = df_all.sort_values("month_num")
    
    fig_borough = px.line(
        df_all,
        x="month",
        y="median_rent",
        color="borough",
        markers=True,
        color_discrete_map={
            "Manhattan": "#0D9488",
            "Brooklyn": "#3B82F6",
            "NW Queens": "#F59E0B",
        },
    )
    fig_borough.update_layout(
        yaxis_title="Median Rent ($)",
        xaxis_title="",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_borough, use_container_width=True)

with col_right:
    st.subheader("Key Borough Differences")
    st.markdown(
        """
        **Manhattan** ($4,100 - $4,334)
        - Highest absolute rents but flattest seasonal variation
        - Record lease volume in August (8,223), more than double January (3,922)
        - Peak bidding wars: 24% in June, DOM drops to 24 days
        
        **Brooklyn** ($3,495 - $3,695)
        - Most competitive borough: bidding wars hit 29.9% by December
        - Record lease signings in August (4,895)
        - 1 in 4 leases signed above asking even in off-season months
        
        **NW Queens** ($3,200 - $3,541)
        - Most affordable of the three tracked markets
        - Highest percentage of new development listings (25-33%)
        - Inventory nearly doubled year-over-year, fastest growing market
        """
    )


st.markdown("---")
st.header("4. What This Means for VryfID")
st.markdown(
    "The seasonal data reveals specific windows where VryfID's growth efforts "
    "will have maximum impact."
)

for season_name, info in seasonal_insights.items():
    with st.expander(f"**{season_name.title()}** ({info['months']})", expanded=False):
        col_a, col_b = st.columns([1, 2])
        
        with col_a:
            st.markdown(f"**Demand:** {info['demand']}")
            st.markdown(f"**Rent Level:** {info['rent_level']}")
            st.markdown(f"**Competition:** {info['competition']}")
            st.markdown(f"**Inventory:** {info['inventory']}")
        
        with col_b:
            st.info(f"**VryfID Implication:** {info['vryfid_implication']}")


st.markdown("---")
st.header("5. Growth Calendar Recommendations")

q1, q2, q3, q4 = st.columns(4)

with q1:
    st.markdown("### Q1: Jan-Mar")
    st.markdown(" **Prepare**")
    st.markdown(
        "- Build renter profiles during low competition\n"
        "- Onboard landlords/brokers while they have time\n"
        "- Content marketing: 'Get your docs ready before summer'"
    )

with q2:
    st.markdown("### Q2: Apr-Jun")
    st.markdown(" **Push Hard**")
    st.markdown(
        "- Peak acquisition window: renters searching 30-60 days early\n"
        "- Highest ROI on marketing spend\n"
        "- Emphasize speed: 'Apply in minutes, not days'"
    )

with q3:
    st.markdown("### Q3: Jul-Sep")
    st.markdown(" **Convert**")
    st.markdown(
        "- Maximum urgency for users already on platform\n"
        "- Push verified profile completion\n"
        "- Landlord pain is highest: sell screening efficiency"
    )

with q4:
    st.markdown("### Q4: Oct-Dec")
    st.markdown(" **Retain & Prep**")
    st.markdown(
        "- Engage existing users for renewals\n"
        "- Second push to landlords with unfilled inventory\n"
        "- Collect data, iterate, prepare for next spring"
    )


st.markdown("---")
st.caption(
    "Analysis by Atharva Deshmukh | Data sourced from Douglas Elliman / "
    "Miller Samuel Monthly Rental Reports (2024), StreetEasy Market Reports, "
    "and industry research. | Built for VryfID growth planning."
)