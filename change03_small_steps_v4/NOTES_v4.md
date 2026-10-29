# Change03 small steps → too late, v4 (2026-10-29)

Same as v3 (new head + boil, lighter glow, edge chromatic aberration, glitch-free hold). One change, from Rachit's note "the slow zoom out looks cheap":
- **The slow drift to the end is gone.** The zoom-out now rides on the original post-reveal motion: an extra centred zoom from **frame 201 (8.38 s)** to **frame 216 (9.01 s)** with his slide-up ease `cubic-bezier(0.215,0.61,0.355,1)`. It lands on the same framing the shoggoth had at 0:12 in v3 (89 %).
- **It stops dead at 0:09:** the plate's own leftover zoom between 216 and 229 is cancelled with poses measured frame to frame (`source/pose2.py`, `poses.json`). After that the frame is fixed and only the tentacles animate.
- Checked: no frame-diff spikes through the landing; motion decays smoothly into frame 216.

File: `change03_small_steps_v4/Change03_small_steps_v4_preview540.mp4`, `keyframes_v4_ending.jpg`.
