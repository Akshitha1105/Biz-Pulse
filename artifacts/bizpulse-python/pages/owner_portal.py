"""
BizPulse — Business Owner Portal
Compliance calendar, UBID card, upcoming deadlines, document locker
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.mock_data import BUSINESSES, COMPLIANCE_DEADLINES


COMPLIANCE_ICONS = {
    "compliant": "✅",
    "warning": "⚠️",
    "non_compliant": "❌",
    "not_applicable": "➖",
    "pending": "⏳",
}


def render_owner_ubid_card(business: dict):
    status_icons = {"Active": "🟢", "Action Required": "🟡", "Non-Compliant": "🔴"}
    icon = status_icons.get(business["status"], "⚪")

    with st.container(border=True):
        col_title, col_badge = st.columns([4, 1])
        with col_title:
            st.caption("GOVERNMENT OF KARNATAKA  ·  BizPulse Unified Business Identifier Card")
        with col_badge:
            st.markdown(f"**{icon} {business['status']}**")

        st.markdown(f"### `{business['ubid']}`")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Business**  \n{business['name']}")
        with col2:
            st.markdown(f"**Owner**  \n{business['owner']}")

        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown(f"**City**  \n{business['city']}")
        with col4:
            st.markdown(f"**Sector**  \n{business['sector']}")
        with col5:
            st.markdown(f"**Registered Since**  \n{business['registration_date']}")


def render():
    st.title("Business Owner Portal")
    st.caption("Meena Sharma · Meena Textiles, Hubli · UBID: KA-2024-BIZ-002")

    # Active alerts banner
    business = next(b for b in BUSINESSES if b["ubid"] == "KA-2024-BIZ-002")

    if "dismissed_owner_alerts" not in st.session_state:
        st.session_state.dismissed_owner_alerts = set()

    active_alerts = [
        a for a in business["alerts"]
        if a not in st.session_state.dismissed_owner_alerts
    ]
    for alert in active_alerts:
        col_alert, col_dismiss = st.columns([8, 1])
        with col_alert:
            st.warning(f"**Alert:** {alert}")
        with col_dismiss:
            if st.button("✕", key=f"own_dismiss_{alert[:20]}"):
                st.session_state.dismissed_owner_alerts.add(alert)
                st.rerun()

    tab1, tab2, tab3 = st.tabs(["My UBID & Compliance", "Upcoming Deadlines", "My Documents"])

    # ── Tab 1: UBID & Compliance ─────────────────────────────────────────────
    with tab1:
        st.markdown("")
        render_owner_ubid_card(business)

        st.markdown("")
        st.subheader("Compliance Status Across Departments")

        for item in business["compliance"]:
            icon = COMPLIANCE_ICONS.get(item["status"], "❓")
            col_dept, col_status, col_note, col_exp = st.columns([2, 1.5, 4, 2])
            with col_dept:
                st.markdown(f"**{item['department']}**")
            with col_status:
                status_labels = {
                    "compliant": "Compliant",
                    "warning": "Warning",
                    "non_compliant": "Action Required",
                    "not_applicable": "N/A",
                    "pending": "Pending",
                }
                label = status_labels.get(item["status"], item["status"])
                st.markdown(f"{icon} {label}")
            with col_note:
                st.caption(item["note"])
            with col_exp:
                if item.get("expires"):
                    st.caption(f"Expires: {item['expires']}")

        st.markdown("---")

        # Compliance score gauge
        score = business["compliance_score"]
        color = "#00D4B4" if score >= 80 else "#F5A623" if score >= 60 else "#d62728"
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={"reference": 80, "increasing": {"color": "#00D4B4"}, "decreasing": {"color": "#d62728"}},
            title={"text": "Your Compliance Score", "font": {"color": "white"}},
            number={"suffix": " / 100", "font": {"color": color, "size": 36}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
                "bar": {"color": color},
                "bgcolor": "#0A1628",
                "bordercolor": "#334466",
                "steps": [
                    {"range": [0, 60], "color": "#1a0808"},
                    {"range": [60, 80], "color": "#1a1208"},
                    {"range": [80, 100], "color": "#081a10"},
                ],
            },
        ))
        fig.update_layout(height=280, paper_bgcolor="#0F2040", margin=dict(l=30, r=30, t=40, b=20))
        col_g, col_tips = st.columns([1, 1])
        with col_g:
            st.plotly_chart(fig, use_container_width=True)
        with col_tips:
            st.markdown("**How to improve your score**")
            st.markdown("""
            - Renew your **Municipal Licence** before Jun 4, 2025
            - File **GST return** before May 20, 2025
            - Apply for **FSSAI licence** (food businesses require it)
            - Keep all registrations updated in BizPulse
            """)
            st.info("Completing these actions will raise your score to **~89 / 100**")

    # ── Tab 2: Upcoming Deadlines ─────────────────────────────────────────────
    with tab2:
        st.subheader("Compliance Calendar — Upcoming Deadlines")

        urgency_colors = {
            "critical": "#d62728",
            "high": "#F5A623",
            "low": "#00D4B4",
        }

        my_deadlines = [d for d in COMPLIANCE_DEADLINES if "KA-2024-BIZ-002" in d["business"]]

        for deadline in sorted(my_deadlines, key=lambda x: x["due"]):
            color = urgency_colors.get(deadline["urgency"], "#888")
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 2, 2])
                with col1:
                    st.markdown(f"**{deadline['event']}**")
                with col2:
                    st.markdown(f"Due: **{deadline['due']}**")
                with col3:
                    st.markdown(
                        f"<span style='color:{color};font-weight:bold'>{deadline['urgency'].upper()}</span>",
                        unsafe_allow_html=True,
                    )

        st.markdown("---")
        st.subheader("Full Compliance Calendar (All Businesses)")

        all_deadlines_df = pd.DataFrame(COMPLIANCE_DEADLINES)
        all_deadlines_df = all_deadlines_df.sort_values("due")
        all_deadlines_df.columns = [c.replace("_", " ").title() for c in all_deadlines_df.columns]
        st.dataframe(all_deadlines_df, use_container_width=True, hide_index=True)

    # ── Tab 3: My Documents ───────────────────────────────────────────────────
    with tab3:
        st.subheader("My Documents — All Registrations in One Place")
        st.caption("Federated view — documents sourced from 4 departments, no data migration")

        docs = [
            {
                "Document": "GST Certificate",
                "ID": business["gstin"],
                "Issued By": "GST Portal (GSTN)",
                "Status": "Active",
                "Last Updated": "2024-12-01",
            },
            {
                "Document": "Udyam Registration Certificate",
                "ID": business["udyam"],
                "Issued By": "Udyam Registry (MSME)",
                "Status": "Active",
                "Last Updated": "2021-08-03",
            },
            {
                "Document": "Municipal Licence (Shop & Estab.)",
                "ID": business["municipal_licence"],
                "Issued By": "Hubli-Dharwad Municipal Corp.",
                "Status": "Expiring Soon",
                "Last Updated": "2021-09-15",
            },
            {
                "Document": "FSSAI Food Licence",
                "ID": "Not Applied",
                "Issued By": "FSSAI",
                "Status": "Missing",
                "Last Updated": "—",
            },
        ]
        df_docs = pd.DataFrame(docs)
        st.dataframe(df_docs, use_container_width=True, hide_index=True)

        st.info("BizPulse fetches these documents from each department's API in real time. No physical copies needed.")

        st.markdown("**Download Documents**")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                "Download GST Certificate (mock)",
                data=f"GST Certificate\nBusiness: {business['name']}\nGSTIN: {business['gstin']}\nStatus: Active",
                file_name="gst_certificate.txt",
            )
        with col_d2:
            st.download_button(
                "Download Udyam Certificate (mock)",
                data=f"Udyam Certificate\nBusiness: {business['name']}\nUdyam No: {business['udyam']}\nStatus: Active",
                file_name="udyam_certificate.txt",
            )
        with col_d3:
            st.download_button(
                "Download UBID Summary (mock)",
                data=f"UBID Summary\nUBID: {business['ubid']}\nBusiness: {business['name']}\nOwner: {business['owner']}\nCompliance Score: {business['compliance_score']}/100",
                file_name="ubid_summary.txt",
            )
