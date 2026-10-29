# Change03 small steps → too late, v2 (2026-10-29)

Paste into the vault: Projects / IDK INTROS tracker row for change03.

## What changed (v1 → v2), same 305 frames, 23.976 fps, beats untouched
- **Character replaced** with Rachit's new head (traced from his image onto a 37x47 art-pixel grid, 4.5 px cells, same centre and baseline as the old bust).
  - Same stepped entry (frames 2-10: +56 / +20 / +4 px, then in place).
  - **Hair boil** like the old character: two drawings, swap every 6 frames from frame 7 (only hair curl strokes step 1 art pixel; face never moves). Frozen while the red chain exits (142-158), as before.
  - Red turn copies the old glitch exactly: per-band horizontal slice offsets measured from the old character each frame (9 px bands), same pink→red colours (114-115), red `#FA4943`, dim dither on 140-141, fade on 159-161, scramble particles kept.
- **Screen glow on everything**: bloom σ1.6 ×0.2 + halo σ9 ×0.4 + σ28 ×0.25, scanlines every 3rd row ×0.90, hue-preserving tonemap. (The full house glow ×0.7/0.6/0.42 filled in the 1-pixel face lines and fogged the shoggoth dither, so it was rejected.)
- **After the reveal**: the 4 glitch bursts removed (226-228, 243-245, 271-273, 288-290 replaced by the neighbouring clean plate frames). Nothing before frame 226 changed except head + glow.
- **Zoom continues** from frame 228 (where the old zoom-out stopped) at the measured rate (~0.26 %/frame), easing to **87 % at frame 305**, about the frame centre. The plate's cut edges fade in as they come on screen.
- Black floor cleaned (h264 noise removed) so the alpha is clean.

## Files
- `change03_small_steps_v2/Change03_small_steps_v2_preview540.mp4`: preview with the original VO
- `keyframes_v2.jpg`, `head_closeup_v2.png`
- `source/`: build.py (comp), glow.py (glow + alpha), head.py / grid.py (head grid + boil)
- HD (1080p MP4 + ProRes 4444 alpha) after approval.
