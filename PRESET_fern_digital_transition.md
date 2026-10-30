# Fern digital transition (preset)

**Name to call it:** "fern digital transition" (Rachit, 2026-10-30). When he says it, build exactly this: the Fern dither-block **encode reveal**, in and out. It is the effect on the LIFE ON CLAUDE NINE title card and he called it the most important thing to carry over. Colours and fonts change per animation; the mechanics below do not.

## What it looks like
A bar of 16 character cells sweeps left to right through the text. From the rear to the front it is **solid white | 75 % | 50 % checker | 25 % dots**, and the **real letters appear behind the solid band**. It never slides smoothly: it **jumps one 4-cell band every 2 frames**. Nothing glitches, nothing eases, nothing overshoots.

## Rules (measured on the title card clip, 2026-10-30; they confirm the 2026-10-24 model)
- **Per cell states:** empty -> 25 % -> 50 % -> 75 % -> solid -> glyph. Out is the same walk reversed: glyph -> solid -> 75 -> 50 -> 25 -> empty.
- **Band = 4 cells.** Bar = 4 bands = 16 cells (solid 4 + three dither bands of 4).
- **IN:** a **charge-up**: only the 25 % band (4 cells) sits for **3-4 frames** (title 3, subtitle 4). Then the head jumps **4 cells every 2 frames** (2 cells per frame). The head **clamps at the end of the line** (never overshoots); the rear then collapses in place, one band per 2 frames (solid + 75 + 50 -> solid + 75 -> solid -> letters). Title: starts f7, done f24 (17 frames = 0.71 s) for 19 cells.
- **OUT:** the head (solid) jumps **6 cells every 2 frames**, so it leaves faster than it arrived. Trailing bands 75 / 50 / 25 follow, then empty. Title: f78 -> f87 (10 frames).
- **Stagger between lines:** the second line starts **4 frames after the first line's head reaches the end of its line** (subtitle f20 vs title head clamped f16), so the lines overlap. On out, the second line starts **2 frames after** the first. The smaller line has smaller cells (title 72 px cells, subtitle 24 px) so its band is 288 px vs 96 px; the frame step stays 2.
- **Dither:** Bayer 4x4 ordered dither, **one dither pixel = 4x4 screen px**, levels 0.25 / 0.5 / 0.75. The **solid** band is flat white with a faint 1 px seam on the left of every cell (0.82) that gives away the per-character cells.
- **Colour:** the bar takes the colour of its text: white (about 250/249/246) for the title, Claude orange for machine lines (core about 255/125/70, halo #D97757). Never mix colours inside one bar.
- **Glow:** `core = m*0.92 + blur(m, 2.5)*0.55`; halo = `blur(m, 22)*0.45 + blur(m, 48)*0.22` (white halo x0.30, orange halo x0.55). Background of the preview mp4 is near-black with a vignette (RGB 8/5/4 x vignette) and sigma 2.2 grain; **the transparent .mov has no background**.
- **Sync rule (Fern):** the picture is still in the pause before a phrase; the reveal starts on the first syllable, 0-50 ms after the voice. Frames at 23.976 or 24 fps, stepped "on 2s".
- **Order on a card:** thin rule line draws first (if used), then the title, then the subtitle (overlapping as above), then a blinking orange block cursor (12 frames on / 12 off).

## Code
- Generator (Python, PIL + numpy): `C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\encode_reveal\generator\encode_reveal.py` with a card `.json` (sample `igor_card.json`). Constants `BAND=4, STEP=2, HOLD=4`, per-line `out_cells=6`, `pixel` = art-pixel size, `track`.
- AE version (untested in real AE): `...\encode_reveal\AE_template\Fern_encode_reveal_template.jsx` + `encode_reveal_sourcetext.txt`.
- Core state function (head position per frame; `i` = cell index):
```python
def state(i, f):                      # None=empty, float=dither/solid level, 'g'=glyph
    if f < f_in: return None
    if f >= f_out:                    # OUT
        k = f - f_out; head = out_cells*(k//STEP + 1) - 1; e = head - i
        if e < 0: return 'g'
        return [1.0, .75, .5, .25][e//BAND] if e < 4*BAND else None
    k = f - f_in                      # IN
    head = BAND-1 if k < HOLD else BAND-1 + BAND*((k-HOLD)//STEP + 1)
    d = head - i
    if d < 0: return None
    return [.25, .5, .75, 1.0][d//BAND] if d < 4*BAND else 'g'
```
- The reference clips: the title-card render `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\premiere\animations\AN4_title_LIFE_ON_CLAUDE_NINE.mov` (and AN1 for the name card), and the sample `...\encode_reveal\encode_reveal_igor_PREVIEW.mp4`.

## Don'ts
- No squares or blocky placeholder spawns; no smooth wipe; no easing on the head; no scale, blur or fade standing in for it. If something must appear in "digital" style, it uses this.

Related: Fern intro - pixel style (orange), Motion systems (named), Context - Title card animation (cloud session), Claude Nine intro - draft v1
