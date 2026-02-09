import streamlit as st
import pandas as pd
from orchestrator import Orchestrator
from utils.logger import logger

# Helper function to draw simple lung visualization
def draw_lung_visualization(inflammation_before, inflammation_after, fev1_before, fev1_after):
    """Create a visual representation of lung health before and after treatment"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### 🫁 BEFORE")
        st.markdown(f"""
        **Inflammation:** {inflammation_before:.0f}%
        
        **FEV1:** {fev1_before:.1f}%
        """)
        # Before state - more red
        health_before = max(0, 100 - inflammation_before)
        st.progress(health_before / 100, text=f"Lung Health: {health_before:.0f}%")
    
    with col2:
        st.markdown("")
        st.markdown("")
        st.markdown("### ➡️")
        st.markdown("*Drug Treatment*")
    
    with col3:
        st.markdown("### 🫁 AFTER")
        st.markdown(f"""
        **Inflammation:** {inflammation_after:.0f}%
        
        **FEV1:** {fev1_after:.1f}%
        """)
        # After state - more green
        health_after = max(0, 100 - inflammation_after)
        st.progress(health_after / 100, text=f"Lung Health: {health_after:.0f}%")
    
    # Show improvements
    st.markdown("---")
    inflammation_reduction = inflammation_before - inflammation_after
    fev1_improvement = fev1_after - fev1_before
    
    improvement_col1, improvement_col2 = st.columns(2)
    with improvement_col1:
        st.metric("Inflammation Reduction", f"{inflammation_reduction:.1f}%", delta=f"-{inflammation_reduction:.1f}%", delta_color="inverse")
    with improvement_col2:
        st.metric("FEV1 Improvement", f"+{fev1_improvement:.1f}%", delta=f"+{fev1_improvement:.1f}%")
st.set_page_config(page_title="AstraMorph: Drug Repurposing", layout="wide")
st.title("💊 AstraMorph: AI-Powered Drug Repurposing")
st.markdown(
    "Unlock new therapeutic potentials by analyzing existing drugs "
    "against new diseases using **mechanism analysis**, **literature review**, "
    "and **digital-twin simulations**."
)
st.sidebar.header("Input Parameters")
drug_name = st.sidebar.text_input("Drug Name", "Montelukast")
disease_name = st.sidebar.text_input("Disease Name", "COPD")
run_btn = st.sidebar.button("Run Repurposing Analysis")
st.sidebar.markdown(
    """
---
**How to use:**
1. Enter a **drug name** and a **disease name**.
2. Click **Run Repurposing Analysis**.
3. The app uses a built-in Gemini API key from the backend code (or mock mode if not set).
"""
)
if run_btn:
    with st.spinner("Running AstraMorph workflow..."):
        try:
            orchestrator = Orchestrator()
            results = orchestrator.run_repurposing_workflow(drug_name, disease_name)
            st.success("Analysis complete ✅")
        except Exception as e:
            logger.error("Error in workflow: %s", e, exc_info=True)
            st.error(f"An error occurred during the analysis: {e}")
            st.stop()

    mech = results["mechanism"]
    lit = results["literature"]
    simulated_data = results["simulation"]
    score = results["score"]

    # Tabs for clearer UX
    tab1, tab2, tab3, tab4 = st.tabs(
        ["1️⃣ BioMechanism", "2️⃣ Literature", "3️⃣ Digital Twin", "4️⃣ Score"]
    )

    # ---------- Tab 1: Mechanism ----------
    with tab1:
        st.subheader("🔬 Drug Mechanism in the Human Body")
        
        # Mechanism Summary in a nice box
        summary = mech.get("summary", "No summary available.")
        st.info(f"**Mechanism:** {summary}", icon="💡")
        
        st.markdown("### 🧬 How It Works (Mechanistic Steps)")
        steps = mech.get("steps", [])
        if steps:
            for i, step in enumerate(steps, start=1):
                col1, col2 = st.columns([1, 20])
                with col1:
                    st.markdown(f"**{i}**")
                with col2:
                    st.markdown(step)
        else:
            st.info("No mechanistic steps available from the agent output.")

        st.markdown("### 🎯 Molecular Targets")
        targets = mech.get("targets", [])
        if targets:
            for target in targets:
                st.success(f"• {target}", icon="✅")
        else:
            st.info("No targets identified.")
        
        # Confidence Score with visual indicator
        confidence = mech.get("confidence", 0)
        st.markdown(f"### Confidence Level")
        st.progress(confidence / 100, text=f"{confidence}/100")

    # ---------- Tab 2: Literature ----------
    with tab2:
        st.subheader("📚 Evidence from Literature")
        
        # Evidence Strength Score
        support_score = lit.get("support_score", 0)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### Supporting Evidence")
        with col2:
            st.metric("Evidence Strength", f"{support_score}/100")
        
        evidence = lit.get("evidence", [])
        if evidence:
            for idx, e in enumerate(evidence, 1):
                with st.container():
                    st.markdown(f"""
                    **📖 Study {idx}**  
                    {e}
                    """)
                    st.divider()
        else:
            st.info("No evidence items returned by the literature agent.")

        st.markdown("### ⚠️ Evidence Gaps & Research Needs")
        gaps = lit.get("gaps", [])
        if gaps:
            for idx, g in enumerate(gaps, 1):
                st.warning(f"**Gap {idx}:** {g}", icon="🔍")
        else:
            st.info("No explicit gaps identified by the literature agent.")

    # ---------- Tab 3: Digital Twin ----------
    with tab3:
        st.subheader("🫁 Digital Twin Simulation (Virtual Patients)")
        summary = simulated_data.get("summary", {})
        
        # Key metrics
        st.markdown("### 📊 Simulation Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Virtual Patients", f"{summary.get('n_patients', 0)}")
        with col2:
            st.metric("Avg Inflammation↓", f"{summary.get('avg_inflammation_reduction_pct', 0.0):.1f}%")
        with col3:
            st.metric("Avg FEV1 Gain", f"{summary.get('avg_fev1_change_pct', 0.0):.1f}%")
        with col4:
            st.metric("Side Effect Rate", f"{summary.get('side_effect_rate_pct', 0.0):.1f}%")
        
        # Before/After Lung Visualization
        st.markdown("---")
        st.markdown("### 🫁 Average Patient: Before & After Treatment")
        
        patients_sample = simulated_data.get("patient_sample", [])
        if patients_sample:
            df_patients = pd.DataFrame(patients_sample)
            
            # Calculate average baseline and post-treatment values
            avg_inflammation_before = df_patients["Baseline Inflammation"].mean()
            avg_inflammation_after = avg_inflammation_before - (summary.get('avg_inflammation_reduction_pct', 0.0))
            avg_fev1_before = df_patients["Baseline FEV1 (%)"].mean()
            avg_fev1_after = avg_fev1_before + (summary.get('avg_fev1_change_pct', 0.0))
            
            # Display lung visualization
            draw_lung_visualization(
                avg_inflammation_before, 
                max(0, avg_inflammation_after),
                avg_fev1_before,
                avg_fev1_after
            )
        
        # Display all 100 virtual patients
        st.markdown("---")
        st.markdown("### 📋 All Virtual Patients Data (100 Patients)")
        
        if patients_sample:
            df_patients = pd.DataFrame(patients_sample)
            
            # Display with better formatting
            st.dataframe(
                df_patients,
                use_container_width=True,
                height=400,
                column_config={
                    "Subtype": st.column_config.TextColumn("Disease Subtype", width="medium"),
                    "Baseline Inflammation": st.column_config.NumberColumn("Baseline Inflammation (%)", format="%.1f"),
                    "Baseline FEV1 (%)": st.column_config.NumberColumn("Baseline FEV1 (%)", format="%.1f"),
                    "Post-Treatment Inflammation": st.column_config.NumberColumn("Post-Treatment Inflammation (%)", format="%.1f"),
                    "Post-Treatment FEV1 (%)": st.column_config.NumberColumn("Post-Treatment FEV1 (%)", format="%.1f"),
                    "Experienced Side Effect": st.column_config.CheckboxColumn("Side Effect?"),
                }
            )
            
            # Download option
            csv = df_patients.to_csv(index=False)
            st.download_button(
                label="📥 Download Patient Data (CSV)",
                data=csv,
                file_name=f"virtual_patients_{drug_name}_{disease_name}.csv",
                mime="text/csv"
            )
            
            # Summary statistics
            st.markdown("---")
            st.markdown("### 📈 Patient Data Statistics")
            st.dataframe(df_patients.describe(), use_container_width=True)
        else:
            st.info("No patient sample table was returned by the digital twin agent.")

    # ---------- Tab 4: Score ----------
    with tab4:
        st.subheader("⭐ Final Repurposing Score & Verdict")

        overall = score.get("overall_repurposing_score", 0.0)
        
        # Main verdict with color coding
        verdict = score.get("verdict", "N/A")
        if overall >= 70:
            st.success(f"✅ **VERDICT: {verdict}**", icon="🎯")
        elif overall >= 50:
            st.warning(f"⚠️ **VERDICT: {verdict}**", icon="📊")
        else:
            st.error(f"❌ **VERDICT: {verdict}**", icon="🚫")

        st.markdown(f"### 📊 Overall Repurposing Score")
        st.progress(overall / 100, text=f"{overall:.1f}%")
        
        st.markdown("### 📈 Component Scores")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Efficacy Score",
                f"{score.get('efficacy_score', 0.0):.0f}/100",
                help="How effective the drug is likely to be"
            )
            st.metric(
                "Mechanism Confidence",
                f"{score.get('mechanism_confidence', 0.0):.0f}/100",
                help="How well-established is the mechanism"
            )
        with col2:
            st.metric(
                "Safety Score",
                f"{score.get('safety_score', 0.0):.0f}/100",
                help="Safety profile assessment"
            )
            st.metric(
                "Literature Support",
                f"{score.get('literature_support_score', 0.0):.0f}/100",
                help="Supporting evidence from literature"
            )

else:
    st.info("Enter a drug & disease on the left, then click **Run Repurposing Analysis**.")