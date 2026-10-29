# Change03 small steps → too late, v3 (2026-10-29)

Same as v2 (new head + hair boil, glitch-free reveal hold, zoom-out to 87 %), with two changes from Rachit's feedback "too much glow":
- **Glow cut to about a third of v2.** No tight bloom now (it was filling the 1-pixel face lines), only a soft halo: σ9 ×0.12 + σ28 ×0.06, scanlines every 3rd row ×0.90, hue-preserving tonemap. It now sits close to the clip's own softness: no fog over the shoggoth dither.
- **Slight chromatic aberration toward the edges:** red pushed outward and blue pulled inward. It grows with r² from 0 px in the centre to 4 px at the corners, so the centre stays sharp. Applied after the glow (`source/ca.py`).

Files: `change03_small_steps_v3/Change03_small_steps_v3_preview540.mp4`, `keyframes_v3.jpg` (last tile = 2x crop: edge fringe + head), `source/`.
