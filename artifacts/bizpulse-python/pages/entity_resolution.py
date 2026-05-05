"""
BizPulse — Entity Resolution Demo
Shows the fuzzy matching + PAN cross-reference + UBID assignment pipeline
"""

import streamlit as st
import pandas as pd
import time
from data.mock_data import FRAGMENTED_RECORDS
from engine.entity_resolution import (
    run_entity_resolution,
    DEMO_UBID_ASSIGNMENTS,
    fuzzy_name_match,
    normalize_name,
)


def render():
    st.title("Entity Resolution Engine")
    st.caption("AI-powered deduplication across fragmented Karnataka government databases")

    st.markdown("""
    Karnataka businesses exist in **4 separate databases** with inconsistent names, missing PAN numbers,
    and mismatched addresses. BizPulse's entity resolution engine identifies these as the same business
    and assigns a single **UBID (Unified Business Identifier)**.
    """)

    # Show raw fragmented data
    st.subheader("Step 1 — Raw Records Across Government Databases")
    st.caption("Same businesses, 4 databases, zero consistency")

    tabs = st.tabs(list(FRAGMENTED_RECORDS.keys()))
    for tab, (source, records) in zip(tabs, FRAGMENTED_RECORDS.items()):
        with tab:
            df = pd.DataFrame(records)
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Step 2 — Run AI Entity Resolution Pipeline")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        The engine runs a **4-stage pipeline**:
        1. **Fuzzy Name Matching** — token-sort + token-set ratio (RapidFuzz)
        2. **PAN Cross-Reference** — validates Permanent Account Numbers across sources
        3. **Address Similarity** — normalized tokenized address comparison
        4. **UBID Assignment** — graph node creation in Neo4j (simulated)
        """)
    with col2:
        run_btn = st.button("Run Entity Resolution", type="primary", use_container_width=True)

    if "resolution_done" not in st.session_state:
        st.session_state.resolution_done = False
        st.session_state.resolved_entities = []
        st.session_state.resolution_logs = []

    if run_btn:
        st.session_state.resolution_done = False
        progress_bar = st.progress(0, text="Initializing pipeline...")
        log_container = st.empty()
        logs_so_far = []

        stages = [
            (0.1, "Connecting to GST Portal API..."),
            (0.2, "Connecting to Udyam Registry API..."),
            (0.3, "Connecting to Municipal Database API..."),
            (0.4, "Connecting to FSSAI Registry API..."),
            (0.55, "Running fuzzy name matching (RapidFuzz token-sort + token-set)..."),
            (0.70, "Cross-referencing PAN numbers across sources..."),
            (0.82, "Computing address similarity scores..."),
            (0.92, "Assigning UBIDs — writing to UBID graph (Neo4j)..."),
            (1.0, "Pipeline complete."),
        ]

        for pct, msg in stages:
            progress_bar.progress(pct, text=msg)
            logs_so_far.append(f"✓ {msg}")
            log_container.code("\n".join(logs_so_far), language=None)
            time.sleep(0.35)

        entities, logs = run_entity_resolution(
            FRAGMENTED_RECORDS, DEMO_UBID_ASSIGNMENTS
        )
        st.session_state.resolved_entities = entities
        st.session_state.resolution_logs = logs
        st.session_state.resolution_done = True
        progress_bar.empty()
        log_container.empty()
        st.success(f"Resolution complete — {len(entities)} unique entities identified across {sum(len(v) for v in FRAGMENTED_RECORDS.values())} raw records.")

    if st.session_state.resolution_done and st.session_state.resolved_entities:
        st.markdown("---")
        st.subheader("Step 3 — Resolved Entities with UBID Assignments")

        for entity in st.session_state.resolved_entities:
            with st.expander(
                f"{entity.ubid} — {entity.canonical_name}  |  Overall Confidence: {entity.overall_confidence:.1f}%",
                expanded=True,
            ):
                col_a, col_b = st.columns([1, 1])

                with col_a:
                    st.markdown("**Matched Records**")
                    for rec in entity.matched_records:
                        st.markdown(f"- `{rec.source}` → **{rec.raw_name}**" +
                                    (f" (PAN: {rec.pan})" if rec.pan else " (no PAN)"))

                with col_b:
                    st.markdown("**Resolution Pipeline Scores**")
                    for step in entity.steps:
                        icon = "✅" if step.passed else "⚠️"
                        bar_color = "normal" if step.passed else "off"
                        st.progress(
                            min(step.score / 100, 1.0),
                            text=f"{icon} {step.step_name}: {step.score:.1f}%",
                        )

                st.caption(f"Assigned UBID: **{entity.ubid}** — registered in UBID graph")

        st.markdown("---")
        st.subheader("Step 4 — Pairwise Fuzzy Name Score Matrix")
        st.caption("Shows how similar each raw name variant is to the others")

        all_names = []
        for entity in st.session_state.resolved_entities:
            for rec in entity.matched_records:
                all_names.append((rec.raw_name, entity.ubid))

        if all_names:
            names_only = [n for n, _ in all_names]
            matrix = [[fuzzy_name_match(a, b) for b in names_only] for a in names_only]
            df_matrix = pd.DataFrame(matrix, index=names_only, columns=names_only)

            import plotly.express as px
            fig = px.imshow(
                df_matrix,
                color_continuous_scale=["#d62728", "#F5A623", "#00D4B4"],
                zmin=0, zmax=100,
                text_auto=".0f",
                labels=dict(color="Similarity %"),
            )
            fig.update_layout(
                paper_bgcolor="#0F2040",
                font=dict(color="white", size=10),
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Engine Logs")
        with st.expander("View processing logs"):
            st.code("\n".join(st.session_state.resolution_logs), language=None)
