"""
BizPulse — Business Directory (360° UBID Profiles)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.mock_data import BUSINESSES


STATUS_COLORS = {
    "Active": "🟢",
    "Action Required": "🟡",
    "Non-Compliant": "🔴",
}

COMPLIANCE_ICONS = {
    "compliant": "✅",
    "warning": "⚠️",
    "non_compliant": "❌",
    "not_applicable": "➖",
    "pending": "⏳",
}


def render_compliance_gauge(score: int):
    color = "#00D4B4" if score >= 80 else "#F5A623" if score >= 60 else "#d62728"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Compliance Score", "font": {"color": "white", "size": 14}},
        number={"suffix": "%", "font": {"color": color, "size": 32}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
            "bar": {"color": color},
            "bgcolor": "#0A1628",
            "bordercolor": "#334466",
            "steps": [
                {"range": [0, 60], "color": "#1a0a0a"},
                {"range": [60, 80], "color": "#1a1200"},
                {"range": [80, 100], "color": "#001a12"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        height=220,
        paper_bgcolor="#0F2040",
        margin=dict(l=20, r=20, t=40, b=10),
    )
    return fig


def render_turnover_chart(business: dict):
    months = business["turnover_months"]
    values = business["turnover"]
    forecast = [values[-1] * 1.05, values[-1] * 1.09, values[-1] * 1.13]
    all_months = months + ["Jun (F)", "Jul (F)", "Aug (F)"]
    all_values = values + forecast

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=values,
        name="Actual",
        line=dict(color="#00D4B4", width=3),
        mode="lines+markers",
        marker=dict(size=8),
    ))
    fig.add_trace(go.Scatter(
        x=["May"] + ["Jun (F)", "Jul (F)", "Aug (F)"],
        y=[values[-1]] + forecast,
        name="Forecast",
        line=dict(color="#F5A623", width=2, dash="dash"),
        mode="lines+markers",
        marker=dict(size=7, symbol="diamond"),
    ))
    fig.update_layout(
        paper_bgcolor="#0F2040",
        plot_bgcolor="#0F2040",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#1e3050"),
        yaxis=dict(gridcolor="#1e3050", title="Turnover (Rs. Lakhs)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig


def render_ubid_card(business: dict):
    """Render a styled UBID identity card."""
    status_color = {"Active": "#00D4B4", "Action Required": "#F5A623", "Non-Compliant": "#d62728"}
    color = status_color.get(business["status"], "#00D4B4")

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0A1628 0%, #0F2D50 60%, #0A1628 100%);
        border: 2px solid {color};
        border-radius: 12px;
        padding: 24px 28px;
        font-family: 'Courier New', monospace;
        position: relative;
        box-shadow: 0 4px 24px rgba(0,212,180,0.15);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="color: #888; font-size: 11px; letter-spacing: 3px; text-transform: uppercase;">
                    Government of Karnataka
                </div>
                <div style="color: {color}; font-size: 13px; font-weight: bold; margin-top: 2px; letter-spacing: 2px;">
                    BizPulse · Unified Business Identifier
                </div>
            </div>
            <div style="
                background: {color};
                color: #0A1628;
                padding: 4px 10px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            ">{business['status'].upper()}</div>
        </div>

        <div style="margin-top: 20px;">
            <div style="color: #aaa; font-size: 10px; letter-spacing: 2px;">UBID</div>
            <div style="color: {color}; font-size: 26px; font-weight: bold; letter-spacing: 4px;">
                {business['ubid']}
            </div>
        </div>

        <div style="margin-top: 16px; display: flex; gap: 40px;">
            <div>
                <div style="color: #888; font-size: 10px; letter-spacing: 1px;">BUSINESS NAME</div>
                <div style="color: white; font-size: 15px; font-weight: bold;">{business['name']}</div>
            </div>
            <div>
                <div style="color: #888; font-size: 10px; letter-spacing: 1px;">OWNER</div>
                <div style="color: white; font-size: 15px;">{business['owner']}</div>
            </div>
        </div>

        <div style="margin-top: 12px; display: flex; gap: 40px;">
            <div>
                <div style="color: #888; font-size: 10px;">SECTOR</div>
                <div style="color: #ccc; font-size: 13px;">{business['sector']}</div>
            </div>
            <div>
                <div style="color: #888; font-size: 10px;">CITY</div>
                <div style="color: #ccc; font-size: 13px;">{business['city']}</div>
            </div>
            <div>
                <div style="color: #888; font-size: 10px;">REGISTERED</div>
                <div style="color: #ccc; font-size: 13px;">{business['registration_date']}</div>
            </div>
            <div>
                <div style="color: #888; font-size: 10px;">EMPLOYEES</div>
                <div style="color: #ccc; font-size: 13px;">{business.get('employees', 'N/A')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.title("Business Directory — 360° UBID Profiles")
    st.caption("Full unified profiles for all registered Karnataka businesses")

    # Search/filter bar
    col_search, col_status, col_sector = st.columns([3, 1, 1])
    with col_search:
        search = st.text_input("Search by name, UBID, or owner", placeholder="e.g. Meena, KA-2024-BIZ-002...")
    with col_status:
        status_filter = st.selectbox("Status", ["All", "Active", "Action Required", "Non-Compliant"])
    with col_sector:
        sectors = ["All"] + list({b["sector"] for b in BUSINESSES})
        sector_filter = st.selectbox("Sector", sectors)

    filtered = BUSINESSES
    if search:
        q = search.lower()
        filtered = [b for b in filtered if q in b["name"].lower() or q in b["ubid"].lower() or q in b["owner"].lower()]
    if status_filter != "All":
        filtered = [b for b in filtered if b["status"] == status_filter]
    if sector_filter != "All":
        filtered = [b for b in filtered if b["sector"] == sector_filter]

    st.caption(f"{len(filtered)} business(es) found")
    st.markdown("---")

    if not filtered:
        st.warning("No businesses match your filters.")
        return

    # Business selector
    ubid_options = [f"{b['ubid']} — {b['name']}" for b in filtered]
    selected = st.selectbox("Select a business for the 360° profile", ubid_options)
    selected_ubid = selected.split(" — ")[0]
    business = next(b for b in filtered if b["ubid"] == selected_ubid)

    st.markdown("---")

    # UBID Card
    render_ubid_card(business)

    st.markdown("")

    # Alerts
    if business["alerts"]:
        for alert in business["alerts"]:
            st.warning(f"**Alert:** {alert}")

    st.markdown("---")

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.plotly_chart(render_compliance_gauge(business["compliance_score"]), use_container_width=True)

    with m2:
        st.markdown("**Linked Database IDs**")
        st.code(f"""GSTIN:   {business['gstin'] or 'Not registered'}
Udyam:   {business['udyam'] or 'N/A'}
Licence: {business['municipal_licence'] or 'N/A'}
FSSAI:   {business['fssai'] or 'Not registered'}""")

    with m3:
        st.markdown("**Directors / Partners**")
        for d in business["directors"]:
            st.markdown(f"- {d}")
        st.markdown("**Address**")
        st.caption(business["address"])

    with m4:
        st.markdown("**Compliance Status by Department**")
        for item in business["compliance"]:
            icon = COMPLIANCE_ICONS.get(item["status"], "❓")
            exp_text = f" — expires {item['expires']}" if item.get("expires") else ""
            st.markdown(f"{icon} **{item['department']}**{exp_text}")
            st.caption(f"  {item['note']}")

    st.markdown("---")

    # Turnover chart
    col_t, col_info = st.columns([2, 1])
    with col_t:
        st.markdown("**Turnover Trend + 3-Month Forecast (Rs. Lakhs)**")
        st.plotly_chart(render_turnover_chart(business), use_container_width=True)

    with col_info:
        st.markdown("**Registration Timeline**")
        st.markdown(f"""
        | Event | Date |
        |-------|------|
        | Business registered | {business['registration_date']} |
        | UBID issued | {business['registration_date']} |
        | Last compliance check | 2025-05-01 |
        """)

        turnover = business["turnover"]
        growth = ((turnover[-1] - turnover[0]) / turnover[0] * 100) if turnover[0] else 0
        trend_icon = "📈" if growth > 0 else "📉"
        st.metric("6-Month Turnover Growth", f"{growth:+.1f}%")
        st.metric("Latest Month", f"Rs. {turnover[-1]}L")
        st.metric("Avg Monthly", f"Rs. {sum(turnover)/len(turnover):.1f}L")
