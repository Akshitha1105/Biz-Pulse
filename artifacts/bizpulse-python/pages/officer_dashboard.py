"""
BizPulse — Government Officer Dashboard
Intelligence alerts, anomaly detection, business search, sector analytics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from data.mock_data import INTELLIGENCE_ALERTS, BUSINESSES, SECTOR_ANALYTICS, DISTRICTS
from engine.anomaly_detection import (
    generate_district_gst_timeseries,
    detect_anomalies_zscore,
    compute_anomaly_summary,
)


SEVERITY_COLORS = {"high": "#d62728", "medium": "#F5A623", "low": "#1f77b4"}
SEVERITY_LABELS = {"high": "HIGH", "medium": "MED", "low": "LOW"}


def render():
    st.title("Government Officer Dashboard")
    st.caption("Rajesh Kumar · Commerce Department, Karnataka · Access Level: Senior Analyst")

    tab1, tab2, tab3 = st.tabs([
        "Intelligence Alerts",
        "Anomaly Detection — GST Trends",
        "Sector Analytics",
    ])

    # ── Tab 1: Intelligence Alerts ──────────────────────────────────────────
    with tab1:
        st.subheader("Active Intelligence Alerts")
        st.caption("AI-generated from real-time analysis of GST, Udyam, and Municipal databases")

        if "dismissed_alerts" not in st.session_state:
            st.session_state.dismissed_alerts = set()

        active_alerts = [
            a for a in INTELLIGENCE_ALERTS
            if a["id"] not in st.session_state.dismissed_alerts
        ]

        if not active_alerts:
            st.success("All alerts have been reviewed and dismissed.")
        else:
            for alert in active_alerts:
                color = SEVERITY_COLORS[alert["severity"]]
                sev_label = SEVERITY_LABELS[alert["severity"]]

                with st.container(border=True):
                    col_badge, col_content, col_action = st.columns([1, 7, 2])
                    with col_badge:
                        st.markdown(
                            f"<span style='background:{color};color:white;padding:4px 8px;"
                            f"border-radius:4px;font-weight:bold;font-size:12px'>{sev_label}</span>",
                            unsafe_allow_html=True,
                        )
                        st.caption(alert["category"])
                    with col_content:
                        st.markdown(f"**{alert['title']}**")
                        st.caption(alert["description"])
                        info_parts = []
                        if alert.get("district"):
                            info_parts.append(f"District: {alert['district']}")
                        if alert.get("sector"):
                            info_parts.append(f"Sector: {alert['sector']}")
                        if alert.get("affected_count"):
                            info_parts.append(f"Affected: {alert['affected_count']} businesses")
                        if info_parts:
                            st.caption(" · ".join(info_parts))
                    with col_action:
                        st.caption(f"Raised: {alert['created_at']}")
                        if st.button("Dismiss", key=f"dismiss_{alert['id']}"):
                            st.session_state.dismissed_alerts.add(alert["id"])
                            st.rerun()

        st.markdown("---")
        st.subheader("Business Search — Real-time Lookup")
        st.caption("Search any business by name, UBID, owner, or city")

        search_query = st.text_input(
            "Search businesses",
            placeholder="Type name, UBID, or city...",
            label_visibility="collapsed",
        )

        results = BUSINESSES
        if search_query:
            q = search_query.lower()
            results = [
                b for b in BUSINESSES
                if q in b["name"].lower()
                or q in b["ubid"].lower()
                or q in b["owner"].lower()
                or q in b["city"].lower()
                or q in b["sector"].lower()
            ]

        st.caption(f"{len(results)} result(s)")

        for b in results:
            status_colors = {
                "Active": "#00D4B4",
                "Action Required": "#F5A623",
                "Non-Compliant": "#d62728",
            }
            sc = status_colors.get(b["status"], "#888")
            with st.expander(
                f"{b['ubid']} — {b['name']} · {b['city']} · {b['sector']}",
                expanded=len(results) == 1,
            ):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**Owner:** {b['owner']}")
                    st.markdown(f"**GSTIN:** {b['gstin'] or 'Not registered'}")
                    st.markdown(f"**Udyam:** {b['udyam'] or 'N/A'}")
                with c2:
                    st.markdown(f"**Compliance Score:** {b['compliance_score']}%")
                    st.progress(b["compliance_score"] / 100)
                    st.markdown(
                        f"**Status:** <span style='color:{sc};font-weight:bold'>{b['status']}</span>",
                        unsafe_allow_html=True,
                    )
                with c3:
                    if b["alerts"]:
                        for a in b["alerts"]:
                            st.warning(a)
                    else:
                        st.success("No active alerts")

    # ── Tab 2: Anomaly Detection ─────────────────────────────────────────────
    with tab2:
        st.subheader("Anomaly Detection — GST Filing Trends")
        st.caption("Time-series z-score analysis on monthly GST filing counts by district")

        selected_district = st.selectbox(
            "Select district",
            DISTRICTS,
            index=DISTRICTS.index("Hubli-Dharwad"),
        )

        df = generate_district_gst_timeseries(selected_district, months=12)
        summary = compute_anomaly_summary(df)
        anomaly_idx = summary["anomaly_indices"]

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Latest Month Filings", f"{summary['latest_value']:,}")
        col_s2.metric("6-Month Average", f"{summary['average_value']:,}")
        col_s3.metric(
            "Recent Change",
            f"{summary['pct_change_recent']:+.1f}%",
            delta_color="inverse" if summary["pct_change_recent"] < 0 else "normal",
        )
        col_s4.metric("Anomalies Detected", summary["anomaly_count"])

        # Trend chart with anomaly markers
        fig = go.Figure()

        # Normal line
        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["filings"],
            name="GST Filings",
            line=dict(color="#00D4B4", width=2.5),
            mode="lines+markers",
            marker=dict(size=7),
        ))

        # Rolling average
        rolling = df["filings"].rolling(window=3, center=True).mean()
        fig.add_trace(go.Scatter(
            x=df["month"],
            y=rolling,
            name="3-Month Rolling Avg",
            line=dict(color="#F5A623", width=1.5, dash="dot"),
            mode="lines",
        ))

        # Anomaly markers
        if anomaly_idx:
            anom_df = df.iloc[anomaly_idx]
            fig.add_trace(go.Scatter(
                x=anom_df["month"],
                y=anom_df["filings"],
                name="Anomaly Detected",
                mode="markers",
                marker=dict(color="#d62728", size=14, symbol="x", line=dict(width=2, color="#d62728")),
            ))

        # Std deviation band
        mean_val = df["filings"].mean()
        std_val = df["filings"].std()
        fig.add_hrect(
            y0=mean_val - std_val,
            y1=mean_val + std_val,
            fillcolor="rgba(0,212,180,0.07)",
            line_width=0,
            annotation_text="±1σ normal range",
            annotation_position="top left",
            annotation_font_color="#888",
        )

        fig.update_layout(
            paper_bgcolor="#0F2040",
            plot_bgcolor="#0F2040",
            font=dict(color="white"),
            xaxis=dict(gridcolor="#1e3050", title="Month"),
            yaxis=dict(gridcolor="#1e3050", title="GST Filings Count"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

        # District comparison
        st.markdown("---")
        st.subheader("Cross-District Comparison — Latest Month")

        comparison_data = []
        for dist in DISTRICTS:
            d_df = generate_district_gst_timeseries(dist, months=12)
            d_summary = compute_anomaly_summary(d_df)
            comparison_data.append({
                "District": dist,
                "Latest Filings": d_summary["latest_value"],
                "6M Average": d_summary["average_value"],
                "% Change": d_summary["pct_change_recent"],
                "Anomalies": d_summary["anomaly_count"],
                "Trend": d_summary["trend"],
            })
        comp_df = pd.DataFrame(comparison_data).sort_values("% Change")

        fig2 = px.bar(
            comp_df,
            x="% Change",
            y="District",
            orientation="h",
            color="% Change",
            color_continuous_scale=["#d62728", "#F5A623", "#00D4B4"],
            labels={"% Change": "Recent % Change in Filings"},
        )
        fig2.add_vline(x=0, line_dash="dash", line_color="white", opacity=0.4)
        fig2.update_layout(
            paper_bgcolor="#0F2040",
            plot_bgcolor="#0F2040",
            font=dict(color="white"),
            height=380,
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: Sector Analytics ──────────────────────────────────────────────
    with tab3:
        st.subheader("Sector Compliance Analytics")
        st.caption("Compliance rate breakdown by district and sector")

        df_sec = pd.DataFrame(SECTOR_ANALYTICS)

        # Bubble chart
        fig3 = px.scatter(
            df_sec,
            x="district",
            y="compliance_rate",
            size="total",
            color="compliance_rate",
            color_continuous_scale=["#d62728", "#F5A623", "#00D4B4"],
            hover_data=["sector", "total"],
            labels={
                "compliance_rate": "Compliance Rate (%)",
                "district": "District",
                "total": "Businesses",
            },
            size_max=50,
        )
        fig3.update_layout(
            paper_bgcolor="#0F2040",
            plot_bgcolor="#0F2040",
            font=dict(color="white"),
            xaxis=dict(gridcolor="#1e3050", tickangle=-30),
            yaxis=dict(gridcolor="#1e3050", range=[55, 105]),
            height=400,
            coloraxis_showscale=True,
        )
        fig3.add_hline(y=80, line_dash="dash", line_color="#F5A623",
                       annotation_text="80% target", annotation_font_color="#F5A623")
        st.plotly_chart(fig3, use_container_width=True)

        # Data table
        st.markdown("**Detailed Breakdown**")
        df_display = df_sec.copy()
        df_display["Compliance Rate"] = df_display["compliance_rate"].map(lambda x: f"{x:.1f}%")
        df_display["Businesses"] = df_display["total"].map(lambda x: f"{x:,}")
        df_display = df_display[["district", "sector", "Compliance Rate", "Businesses"]].rename(
            columns={"district": "District", "sector": "Sector"}
        )
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
        )
