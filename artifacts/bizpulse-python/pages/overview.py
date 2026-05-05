"""
BizPulse — Platform Overview / Landing Page
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
from data.mock_data import PLATFORM_STATS, SECTOR_ANALYTICS, BUSINESSES


def animated_metric(label, value, suffix="", delta=None):
    if delta:
        st.metric(label, f"{value}{suffix}", delta=delta)
    else:
        st.metric(label, f"{value}{suffix}")


def render():
    st.title("BizPulse — AI-Powered Business Identity Platform")
    st.caption("Unified Business Identifier (UBID) System · Karnataka, India")

    st.markdown("---")

    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### One Identity for Every Business in Karnataka

        BizPulse solves the critical problem of **fragmented business registrations** across Karnataka's
        government departments — GST, Udyam, Municipal Licences, and FSSAI — by assigning every business
        a **UBID (Unified Business Identifier)**, like Aadhaar for businesses.

        > *"A Hubli textile businesswoman today visits 3 government offices, carries 7 documents,
        > and waits 4 weeks to prove her business is compliant. With BizPulse, she does it in 30 seconds."*
        """)

    with col2:
        st.info("""
        **Architecture Highlights**
        - Federated data — no migration needed
        - AI entity resolution (fuzzy + PAN matching)
        - Real-time sync via Kafka CDC
        - UBID graph on Neo4j
        - NIC Cloud deployment
        """)

    st.markdown("---")
    st.subheader("Platform Statistics — Live")

    # Stats row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    stats = PLATFORM_STATS
    c1.metric("Businesses Unified", f"{stats['total_businesses']:,}")
    c2.metric("UBIDs Issued Today", f"+{stats['unified_today']:,}", delta=f"+{stats['unified_today']:,}")
    c3.metric("Compliance Rate", f"{stats['compliance_rate']}%", delta="+1.2%")
    c4.metric("Active Alerts", stats['active_alerts'], delta="-2", delta_color="inverse")
    c5.metric("Districts Active", stats['districts_active'])
    c6.metric("Departments Integrated", stats['departments_integrated'])

    st.markdown("---")

    # Fragmented → Unified flow diagram
    st.subheader("The UBID Architecture — Federated Data Flow")

    fig = go.Figure()

    # Source databases (left column)
    sources = ["GST Portal\n(GSTN)", "Udyam Registry\n(MSME)", "Municipal DB\n(ULBs)", "FSSAI Registry"]
    source_colors = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd"]
    for i, (src, color) in enumerate(zip(sources, source_colors)):
        fig.add_annotation(
            x=0.05, y=0.85 - i * 0.25,
            text=f"<b>{src}</b>",
            showarrow=False,
            font=dict(size=12, color="white"),
            bgcolor=color,
            bordercolor=color,
            borderwidth=2,
            borderpad=8,
            xref="paper", yref="paper",
        )

    # Integration layer (center)
    fig.add_annotation(
        x=0.5, y=0.5,
        text="<b>BizPulse Integration Layer</b><br>Kafka CDC · Entity Resolution<br>UBID Graph (Neo4j)",
        showarrow=False,
        font=dict(size=13, color="white"),
        bgcolor="#0A1628",
        bordercolor="#00D4B4",
        borderwidth=2,
        borderpad=12,
        xref="paper", yref="paper",
    )

    # Output: UBID
    fig.add_annotation(
        x=0.92, y=0.5,
        text="<b>UBID</b><br>KA-2024-BIZ-XXX<br>Unified Identity",
        showarrow=False,
        font=dict(size=13, color="white"),
        bgcolor="#F5A623",
        bordercolor="#F5A623",
        borderwidth=2,
        borderpad=12,
        xref="paper", yref="paper",
    )

    # Use shapes (lines) for arrows instead of annotations with axref=paper
    # Arrows from sources to integration layer
    for i in range(4):
        y_pos = 0.85 - i * 0.25
        fig.add_shape(
            type="line",
            x0=0.17, y0=y_pos, x1=0.30, y1=0.5,
            xref="paper", yref="paper",
            line=dict(color="#00D4B4", width=1.5, dash="dot"),
        )

    # Arrow from integration layer to UBID
    fig.add_shape(
        type="line",
        x0=0.65, y0=0.5, x1=0.78, y1=0.5,
        xref="paper", yref="paper",
        line=dict(color="#F5A623", width=2),
    )

    fig.update_layout(
        height=320,
        paper_bgcolor="#0F2040",
        plot_bgcolor="#0F2040",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Compliance overview chart
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Compliance Rate by Sector & District")
        df = pd.DataFrame(SECTOR_ANALYTICS)
        fig2 = px.bar(
            df.sort_values("compliance_rate"),
            x="compliance_rate",
            y="sector",
            color="compliance_rate",
            color_continuous_scale=["#d62728", "#F5A623", "#00D4B4"],
            orientation="h",
            labels={"compliance_rate": "Compliance Rate (%)", "sector": "Sector"},
            hover_data=["district", "total"],
        )
        fig2.update_layout(
            height=380,
            paper_bgcolor="#0F2040",
            plot_bgcolor="#0F2040",
            font=dict(color="white"),
            coloraxis_showscale=False,
        )
        fig2.update_xaxes(range=[0, 105])
        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        st.subheader("Registered Businesses by Status")
        status_counts = {
            "Active": sum(1 for b in BUSINESSES if b["status"] == "Active"),
            "Action Required": sum(1 for b in BUSINESSES if b["status"] == "Action Required"),
            "Non-Compliant": sum(1 for b in BUSINESSES if b["status"] == "Non-Compliant"),
        }
        fig3 = go.Figure(go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            hole=0.55,
            marker=dict(colors=["#00D4B4", "#F5A623", "#d62728"]),
        ))
        fig3.update_layout(
            height=380,
            paper_bgcolor="#0F2040",
            font=dict(color="white"),
            showlegend=True,
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Technical Architecture Components")

    arch_cols = st.columns(4)
    components = [
        ("Entity Resolution Engine", "Fuzzy matching (RapidFuzz) + PAN deduplication + address normalization across 4 databases"),
        ("UBID Graph (Neo4j)", "Federated identity graph — links entities without data migration. CDC via Kafka keeps it in sync"),
        ("Anomaly Detection", "Time-series analysis on GST filings, turnover trends, and compliance rates with z-score alerting"),
        ("Compliance Calendar", "Rule-based + ML deadline prediction engine for GST, Udyam, Municipal, and FSSAI obligations"),
    ]
    for col, (title, desc) in zip(arch_cols, components):
        with col:
            st.info(f"**{title}**\n\n{desc}")
