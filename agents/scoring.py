# agents/scoring.py
from typing import Dict, Any

def compute_score(
    mech: Dict[str, Any],
    lit: Dict[str, Any],
    sim: Dict[str, Any]
) -> Dict[str, Any]:
    mech_conf = float(mech.get("confidence", 50))
    lit_score = float(lit.get("support_score", 50))
    sim_sum = sim.get("summary", {})
    eff = float(sim_sum.get("avg_inflammation_reduction_pct", 10.0))
    se_rate = float(sim_sum.get("side_effect_rate_pct", 10.0))

    efficacy_score = max(0.0, min(100.0, eff * 1.5))          # more reduction = more efficacy
    safety_score = max(0.0, min(100.0, (100 - se_rate)))      # fewer side effects = safer

    # weighted sum
    final_score = (
        0.4 * efficacy_score +
        0.25 * safety_score +
        0.2 * lit_score +
        0.15 * mech_conf
    )
    final_score = round(final_score, 1)

    verdict = "Positive" if final_score >= 65 else "Negative"

    return {
        "efficacy_score": round(efficacy_score, 1),
        "safety_score": round(safety_score, 1),
        "literature_support_score": round(lit_score, 1),
        "mechanism_confidence": round(mech_conf, 1),
        "overall_repurposing_score": final_score,
        "verdict": verdict
    }
