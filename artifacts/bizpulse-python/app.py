"""
BizPulse — AI-Powered Business Identity & Intelligence Platform
Karnataka, India · Hackathon Prototype

Federated Architecture:
  - No data migration between departments
  - Entity resolution via fuzzy matching + PAN cross-reference
  - UBID graph (simulated Neo4j) for unified identity
  - Real-time anomaly detection on compliance timeseries
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

st.set_page_config(
    page_title="BizPulse — Karnataka UBID Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from pages.overview import render as render_overview
from pages.entity_resolution import render as render_entity_resolution
from pages.business_directory import render as render_business_directory
from pages.officer_dashboard import render as render_officer_dashboard
from pages.owner_portal import render as render_owner_portal

# ── Sidebar Navigation ────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 16px 0;">
        <div style="font-size: 28px; font-weight: 900; color: #00D4B4; letter-spacing: 2px;">
            BizPulse
        </div>
        <div style="font-size: 11px; color: #888; letter-spacing: 1px; margin-top: 2px;">
            KARNATAKA · UBID PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigate",
        options=[
            "Platform Overview",
            "Entity Resolution Engine",
            "Business Directory",
            "Officer Dashboard",
            "Business Owner Portal",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("""
    <div style="font-size: 11px; color: #666; padding: 8px 0;">
        <b style="color: #888;">Architecture</b><br>
        · Federated Data (no migration)<br>
        · Entity Resolution (RapidFuzz)<br>
        · UBID Graph (Neo4j)<br>
        · Kafka CDC sync<br>
        · Anomaly Detection (z-score)<br>
        · NIC Cloud, Karnataka
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size: 11px; color: #555; text-align: center;">
        Hackathon Prototype · May 2025<br>
        Government of Karnataka
    </div>
    """, unsafe_allow_html=True)

# ── Page Routing ──────────────────────────────────────────────────────────────

if page == "Platform Overview":
    render_overview()
elif page == "Entity Resolution Engine":
    render_entity_resolution()
elif page == "Business Directory":
    render_business_directory()
elif page == "Officer Dashboard":
    render_officer_dashboard()
elif page == "Business Owner Portal":
    render_owner_portal()
