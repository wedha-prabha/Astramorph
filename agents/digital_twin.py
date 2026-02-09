import numpy as np
import pandas as pd
from typing import Dict, Any
import logging

logger = logging.getLogger("DigitalTwinAgent")
logging.basicConfig(level=logging.INFO)


class DigitalTwinAgent:
    """
    Digital Twin Agent
    Simulates 1000 virtual COPD patients and drug response
    """

    def __init__(self, default_n_patients: int = 100, seed: int = 42):
        self.default_n_patients = default_n_patients
        self.seed = seed

    def run(
        self,
        drug: str,
        disease: str,
        n_patients: int | None = None
    ) -> Dict[str, Any]:

        n = n_patients or self.default_n_patients
        rng = np.random.default_rng(self.seed)

        logger.info(f"Simulating {n} virtual patients for {drug} in {disease}")

        # Disease-specific subtypes and parameters
        disease_lower = disease.lower()
        
        if "copd" in disease_lower:
            subtype_names = ["Eosinophilic COPD", "Neutrophilic COPD", "Mixed Inflammatory COPD"]
            subtype_probs = [0.3, 0.4, 0.3]
            baseline_inflam_mean = 60
            baseline_fev1_mean = 45
            base_inflam_reduction_range = (10, 30)
            base_fev1_gain_range = (3, 12)
            base_side_effect_rate = 0.08
        elif "asthma" in disease_lower:
            subtype_names = ["Allergic Asthma", "Non-Allergic Asthma", "Occupational Asthma"]
            subtype_probs = [0.5, 0.35, 0.15]
            baseline_inflam_mean = 55
            baseline_fev1_mean = 60
            base_inflam_reduction_range = (15, 35)
            base_fev1_gain_range = (5, 15)
            base_side_effect_rate = 0.05
        elif "diabetes" in disease_lower:
            subtype_names = ["Type 2 Diabetes", "Insulin Resistant", "Advanced Diabetes"]
            subtype_probs = [0.6, 0.25, 0.15]
            baseline_inflam_mean = 50
            baseline_fev1_mean = 75  # Not applicable but kept for compatibility
            base_inflam_reduction_range = (5, 20)
            base_fev1_gain_range = (0, 5)
            base_side_effect_rate = 0.06
        elif "heart" in disease_lower or "cardiovascular" in disease_lower:
            subtype_names = ["Coronary Artery Disease", "Heart Failure", "Arrhythmia"]
            subtype_probs = [0.4, 0.35, 0.25]
            baseline_inflam_mean = 45
            baseline_fev1_mean = 70
            base_inflam_reduction_range = (10, 25)
            base_fev1_gain_range = (2, 8)
            base_side_effect_rate = 0.07
        else:
            # Generic fallback
            subtype_names = [f"{disease} Type A", f"{disease} Type B", f"{disease} Type C"]
            subtype_probs = [0.33, 0.33, 0.34]
            baseline_inflam_mean = 55
            baseline_fev1_mean = 50
            base_inflam_reduction_range = (8, 25)
            base_fev1_gain_range = (2, 10)
            base_side_effect_rate = 0.08

        subtypes = rng.choice(
            subtype_names,
            size=n,
            p=subtype_probs
        )

        # Baseline patient parameters
        baseline_inflammation = rng.normal(baseline_inflam_mean, 10, n).clip(0, 100)
        baseline_fev1 = rng.normal(baseline_fev1_mean, 12, n).clip(20, 90)

        # Subtype-specific modifiers (disease-aware)
        inflam_modifier = {subtype: 1.0 + (i * 0.05) for i, subtype in enumerate(subtype_names)}
        side_effect_modifier = {subtype: 1.0 + (i * 0.1) for i, subtype in enumerate(subtype_names)}

        # Drug effect simulation
        base_inflam_reduction = rng.uniform(base_inflam_reduction_range[0], base_inflam_reduction_range[1], n)
        base_fev1_gain = rng.uniform(base_fev1_gain_range[0], base_fev1_gain_range[1], n)
        base_side_effect_rate = base_side_effect_rate

        inflam_reduction = []
        fev1_gain = []
        side_effect = []

        for i in range(n):
            st = subtypes[i]
            ir = base_inflam_reduction[i] * inflam_modifier[st]
            fg = base_fev1_gain[i] * inflam_modifier[st] * 0.9
            se = rng.random() < (base_side_effect_rate * side_effect_modifier[st])

            inflam_reduction.append(ir)
            fev1_gain.append(fg)
            side_effect.append(se)

        inflam_reduction = np.array(inflam_reduction)
        fev1_gain = np.array(fev1_gain)
        side_effect = np.array(side_effect)
        summary = {
            "drug": drug,
            "disease": disease,
            "n_patients": n,
            "avg_inflammation_reduction_pct": round(float(inflam_reduction.mean()), 2),
            "avg_fev1_change_pct": round(float(fev1_gain.mean()), 2),
            "side_effect_rate_pct": round(float(side_effect.mean() * 100), 2),
        }

        # -------------------------------
        # Patient table (return FIRST 200)
        # -------------------------------
        sample_n = min(200, n)

        df = pd.DataFrame({
            "Subtype": subtypes[:sample_n],
            "Baseline Inflammation": baseline_inflammation[:sample_n],
            "Baseline FEV1 (%)": baseline_fev1[:sample_n],
            "Inflammation Reduction (%)": inflam_reduction[:sample_n],
            "FEV1 Improvement (%)": fev1_gain[:sample_n],
            "Side Effect (0/1)": side_effect[:sample_n].astype(int)
        })

        return {
            "summary": summary,
            "patient_sample": df.to_dict(orient="records")
        }


if __name__ == "__main__":
    agent = DigitalTwinAgent()
    out = agent.run("Montelukast", "COPD")
    import json
    print(json.dumps(out["summary"], indent=2))
    print(pd.DataFrame(out["patient_sample"]).head(10)) 