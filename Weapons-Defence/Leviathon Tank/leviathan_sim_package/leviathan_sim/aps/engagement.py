"""Hard-kill APS engagement timeline."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import LeviathanConfig


def simulate_aps(cfg: LeviathanConfig) -> Dict[str, Any]:
    aps = cfg.aps
    ranges_m = np.linspace(aps.engage_min_m, aps.engage_init_m, 10)

    timelines = []
    for r in ranges_m:
        t_flight = r / aps.atgm_approach_speed_m_s
        t_total = t_flight + aps.reaction_time_s + 1.0 / aps.track_update_hz
        pk = aps.single_shot_pk if r >= aps.engage_min_m else 0.0
        timelines.append(
            {
                "range_m": round(float(r), 0),
                "time_to_intercept_s": round(t_total, 3),
                "single_shot_pk": pk,
            }
        )

    # Two-shot salvo PK
    pk2 = 1 - (1 - aps.single_shot_pk) ** 2

    return {
        "radar_band": aps.radar_band,
        "detection_atgm_m": aps.detection_range_atgm_m,
        "detection_rpg_m": aps.detection_range_rpg_m,
        "engage_envelope_m": [aps.engage_min_m, aps.engage_init_m],
        "reaction_time_s": aps.reaction_time_s,
        "single_shot_pk": aps.single_shot_pk,
        "two_shot_pk": round(pk2, 3),
        "engagement_timeline": timelines,
        "notes": "Model assumes head-on ATGM at 200 m/s; no multi-target saturation.",
    }
