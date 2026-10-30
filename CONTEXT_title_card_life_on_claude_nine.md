# Context: LIFE ON CLAUDE NINE title card (Claude Nine intro), with the "fern digital transition"

Drop this file in the repo root of the new session and read all of it first. You are **picking up an animation that already exists and making changes to it**. Rachit (video editor, Premiere Pro, Bengaluru) will tell you what to change. This note gives you everything the previous chats knew so you can start without re-asking the basics. **The most important thing is the digital transition (the encode reveal in and out). Keep it exactly (section 3b); it is a named preset, "fern digital transition".**

## 0. Read this first: what exists and what doesn't
- The animation is the **title card "LIFE ON CLAUDE NINE" + "> a short story by igor babuschkin"**, the last beat of the Claude Nine intro. Rachit uploaded it as `life_on_claude_nine.mp4`: **3.80 s, 1920x1080, 23.976 fps, 91 frames, silent** (no audio at all), on black.
- It was built with the **encode-reveal generator** (Python, PIL + numpy) in an earlier chat. The generator and its Igor name-card sample **do exist** on Rachit's computer (`C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\encode_reveal\generator\encode_reveal.py` + `igor_card.json`; ask him to attach them). The **card file for this title card was not kept** (the earlier cloud workspace is gone). An earlier render of the same card exists as `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\premiere\animations\AN4_title_LIFE_ON_CLAUDE_NINE.mov` (108 frames @ 24 fps, PNG codec with alpha). Treat the uploaded mp4 as the spec and **measure it frame by frame** before changing anything.
- Expect to re-create the card JSON from section 2 and re-render with the generator; change only what Rachit asks.
- **Ask Rachit what he wants changed first**, then plan. If something is unclear, one short question.

## 1. Where this sits in the intro
- Project: a Fern-style YouTube intro about Igor Babuschkin's short story *Life on Claude Nine*. Practice work (IDK INTROS), not a client job.
- Draft map: 101-105.6 s "title card LIFE ON CLAUDE NINE (encode reveal) + 'a short story by igor babuschkin'", after the hard cut on the engineer's eyes. The horizon line flashes white just before (see the blog + terminal beat).
- Silent clip: in the draft the title lands on a music/SFX moment, not on the VO. SFX, if needed, are a separate layer (none exists for this clip).
- Delivered as its own clip, not baked into the full video.

## 2. What the current animation does (measured from the clip; frames at 23.976 fps, clip frame numbers)
Two lines centred in the frame: the **title** (white, chunky bitmap caps, 19 cells, cell width 72 px = 8 art pixels x 9 px, cap height 72 px, spanning x 274-1646, rows y 467-538) and the **subtitle** below it (orange, lowercase terminal text, 8x8-style cell 24 px wide = art pixel 3 px, spanning x 554-1371, rows y 618-663). Background is black with a very faint warm vignette (about RGB 4,2,0 at centre) in the preview mp4; the final .mov must be transparent.

| Frames | What happens |
|---|---|
| 0-6 | Black. |
| 7-9 | **Charge-up:** a single 4-cell band of 25 % dither sits at the left end of the title (x 274-560). |
| 10-15 | **Bar sweeps right:** the head jumps one band (288 px = 4 cells) every 2 frames (f10 -> 849, f12 -> 1137, f14 -> 1425); the bar grows to 4 bands (solid / 75 / 50 / 25) by f14. Letters appear behind the solid band from f16 ("LIFE" first). |
| 16-24 | **Head clamps at the end of the line** (f16, x 1641). The rear collapses in place, one band per 2 frames; f24 title fully resolved. |
| 20-24 | Subtitle charge-up: orange 25 % band (4 cells = 96 px) at its left end, f20-23. |
| 24-44 | **Subtitle sweeps right** in orange, same mechanics (head +96 px per 2 frames: 742, 839, 933, 1029, 1125, 1221, 1317, clamp 1367 at f38), then collapses; fully resolved by about f44. |
| 45-77 | **Hold** (2.2 s). Nothing moves. |
| 78-87 | **Title out:** the same walk reversed (letters -> solid -> 75 -> 50 -> 25 -> empty), head jumps **6 cells (432 px) per 2 frames**: rear edge f82 418, f84 851, f86 1284, gone f88. |
| 80-90 | **Subtitle out,** starts 2 frames after the title: rear edge f84 598, f86 744, f88 888, gone by f90. |
| 90 | Black. |

No glitches, no scale, no blur anywhere. Only the encode bar moves.

## 3. Style lock (pixel / CRT world, same as every animation in this intro)
- **Transparent background in the final .mov.** Previews are shown on black. Light on black → alpha (recipe in section 6).
- **Colour means something:** white = humans and the world; **Claude orange** = Claude and what it does; here **red** is used for "it has turned" (the red scramble). Don't introduce other colours.
  - Orange: core `#FF7A3D` ≈ RGB(255,108,40), halo `#D97757` (terracotta). Pure `#D97757` alone goes muddy when it glows; use the saturated core.
  - White humans: about RGB(236,236,232).
- **Pixel art:** hard-edged, nearest-neighbour, one art pixel ≈ 4-6 screen px at 1920. Solid white fills with dark line details cut in, never outline drawings for characters. Sparse, centred layouts, one idea per frame, big empty margins.
- **Screen glow (Rachit wants it):** tight bloom (Gaussian σ≈1.6, ×0.7) + wide halo (σ≈9 ×0.6 plus σ≈28 ×0.42), then faint scanlines (every third row ×0.90), then a **hue-preserving tonemap** (`out /= max(1, maxchannel/255)`) so orange doesn't bleach to white.
- **THE signature effect here is the "fern digital transition" (section 3b). It must survive every change.**
- **No squares:** he rejected "squares as spawn effects". Things appear as their own shape: pixel dissolve (15/40/70/100 % coverage with a brightness flash), dither, scan-line encode.
- **Digital idle:** every icon hops 1 art pixel up and back every 9-10 frames, hard step, each out of phase. Nothing floats or breathes smoothly.
- **Two speeds:** layout/camera moves smooth at full frame rate; everything "digital" (typing, fills, pops, glitch) stepped at ~8-12 fps.
- **Cuts land on the peak of the speed curve** (one continuous move through the cut: outgoing accelerates, incoming starts at the same speed and decelerates).
- **Sync rule (Fern):** in the pause before a phrase the picture is still; the next beat starts on the first syllable (0-50 ms after the voice), never before it.
- **Premium means subtract:** remove any move that can be removed without loss.
- **Rachit's named moves:** *JUMP CUT* = outgoing 100→110 % scale over 10 frames ease-in, hard cut, incoming 90→100 % over 10 frames ease-out, about the frame centre. *slide up* = starts 50 px below, rises to place over 10 frames ease-out, opacity 0→100 % over the first 5 frames linear.
- **Fonts (when text is needed):** Rachit supplied **Neue Montreal** (Bold/Medium etc.) and **Instrument Serif** (his "idk fonts"). For pixel type, rasterise Neue Montreal Bold onto the art-pixel grid. Ask him for the files if you need them; they are not in this repo.

## 3b. THE PRESET: "fern digital transition"
Rachit's name for this effect; when he says it, build exactly this (it is also saved in his memory and vault).

**Name to call it:** "fern digital transition" (Rachit, 2026-10-30). When he says it, build exactly this: the Fern dither-block **encode reveal**, in and out. It is the effect on the LIFE ON CLAUDE NINE title card and he called it the most important thing to carry over. Colours and fonts change per animation; the mechanics below do not.

#### What it looks like
A bar of 16 character cells sweeps left to right through the text. From the rear to the front it is **solid white | 75 % | 50 % checker | 25 % dots**, and the **real letters appear behind the solid band**. It never slides smoothly: it **jumps one 4-cell band every 2 frames**. Nothing glitches, nothing eases, nothing overshoots.

#### Rules (measured on the title card clip, 2026-10-30; they confirm the 2026-10-24 model)
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

#### Code
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

#### Don'ts
- No squares or blocky placeholder spawns; no smooth wipe; no easing on the head; no scale, blur or fade standing in for it. If something must appear in "digital" style, it uses this.

## 4. Assets and where they live (his computer; ask him to attach what you need)
- Generator + sample: `C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\encode_reveal\` (`generator\encode_reveal.py`, `generator\igor_card.json`, `AE_template\`, `encode_reveal_igor_PREVIEW.mp4`, `encode_reveal_igor_TEXT_ALPHA.mov`, `encode_reveal_ref_vs_ours.png`).
- Earlier renders of this card and the name card: `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\premiere\animations\` (AN1 name, AN2 cursor, AN3 loading bars, AN4 title).
- Fonts: the generator's default is DejaVu Sans Mono Bold rendered at a small size and nearest-upscaled (which gives the chunky look). The clip's title is probably that; compare against AN4 and the clip before you change it. Rachit's "idk fonts" (Neue Montreal, Instrument Serif) are for headlines in other animations, not for this card, unless he says so.
- Everything for this intro: `C:\Users\rachi\Desktop\Work\INTROS\`, per-change folders in `...\_claude_draft1\changeNN_<name>\`.

## 4b. Open questions you should ask Rachit up front
- What exactly should change (timing, size, wording, colours, hold length, a sound)?
- Exact length in frames this slot needs, and where the first frame lands in his timeline.
- Does he want the subtitle wording or a cursor changed? (The earlier Igor card had a blinking orange block cursor; this clip shows none.)
- Does he want an SFX layer (a click per band step, a hit on the solid band, a tail on the out)?
- Does the "fern digital transition" also go onto other text in the intro (it's a preset; he may ask you to apply it elsewhere)?

## 5. Process Rachit expects (house rules)
1. Study the current clip frame by frame before designing. Say what you learned.
2. **Show key frames first** (labelled with frame number / VO word). Then a **low-quality preview** (≈540p mp4 with the VO). Only then the final render. Manage tokens: small crops and half-res previews while iterating.
3. The final **.mov = ProRes 4444 with alpha** (transparent), same fps and exact length as the section in his current version. Preview mp4 with VO on black. SFX, if asked, as a **separate layer**: one full-length 48 kHz .wav (0 s = frame 0) + stems, never baked in.
4. Each new version is a new `vN` file in a new `changeNN_<name>\` folder; never overwrite another chat's files. Always give **full Windows paths** (e.g. `C:\Users\rachi\Desktop\Work\INTROS\...`), never shortened ones.
5. **No After Effects Dynamic Link**; plain clips/layers only. Premiere handoffs: separate layers, each one continuous.
6. Check before sending: first and last frame, frames either side of every cut, midpoints of every move, alpha (corner pixel transparent), `ffprobe` length and fps. He notices a stray frame.
7. If he says the animation looks "choppy" or "glitches at the end", look at the **last 12 frames and every fade** first. Lessons from "you're falling behind": per-cell random dissolves on a fade-out read as noise; use a clean brightness ease-out; don't leave a blinking cursor or off-grid slips in the ending.
8. He works fast and directly. Show, don't describe at length. Don't tell him you can't see/hear something; measure it. There is no speech-to-text in the cloud container: get word timings from the audio energy + fricative spectrogram (`f`, `s`, `b` onsets), say that you did, and ask him to confirm key hits by ear.

## 6. Reusable code recipes (battle-tested in the sister animations)
- Glow, scanlines, tonemap, alpha (from `build.py` in the L09 and falling-behind renders):
```python
core = cv2.GaussianBlur(cv, (0,0), 1.6) * 0.7
halo = cv2.GaussianBlur(cv, (0,0), 9) * 0.6 + cv2.GaussianBlur(cv, (0,0), 28) * 0.42
out  = (cv + core + halo) * SCAN            # SCAN = 1 - 0.10*(row % 3 == 2)
m = out.max(axis=2, keepdims=True); out = out / np.maximum(1.0, m/255.0)   # hue-preserving
def to_rgba(rgb):                            # light on black -> straight alpha (exact over black)
    a = np.clip(rgb.max(axis=2)/255.0, 0, 1)
    col = np.where(a[...,None] > 1e-4, rgb/np.maximum(a[...,None],1e-4), 0)
    return np.dstack([np.clip(col,0,255), a*255]).astype(np.uint8)
```
- Encode: `ffmpeg -framerate 24000/1001 -i f%03d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -vendor apl0 out.mov` (name frames `f%03d`, not `f%02d`).
- Pixel dissolve in: coverage 15 → 40 → 70 → 100 % over ~8 frames via a fixed random order per shape, brightness 0.3 → 1.0 plus a soft flash.
- Sister animations with source (copy their structure, don't mix their content): the **encode-reveal generator** (this animation's engine, see 3b) → `C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\encode_reveal\generator\encode_reveal.py` (ask Rachit to attach it; it is also in this repo if he committed it); L09 "first step" multiplication → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change05_first_step_multiply\source\` (`build.py`, `sfx.py`, `head_grid.npy`); "you're falling behind" → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change07_falling_behind\` (`FALLING_BEHIND_v4_ALPHA.mov`, `source\build2.py`).
- Big files: the file-transfer tool alters .mov/.mp4 headers. Split into 24 MB parts, XOR each byte with `0x5A`, send, un-XOR and `cat` on the computer, and check the md5 against the original. (A plain split corrupted the ProRes header.)
- Environment: Python + numpy + OpenCV + Pillow, ffmpeg, Playwright/Chromium. The shell reaches only package registries and GitHub; fonts and assets must come from Rachit.

## 8. Shared notes (only if his Obsidian vault is connected to your session)
Vault: `C:\Users\rachi\Documents\OBSIDIAN AND CLAUDE\New folder\VAULT FOR CLAUDE MEMORY`. Read `IDK INTROS/Intro animations - parallel workflow.md`, `IDK INTROS/Intro animations - tracker.md`, `IDK INTROS/Fern intro - pixel style (orange).md`, `IDK INTROS/Claude Nine intro - draft v1.md`, `Style/Motion systems (named).md`. Update **only your own tracker row** (a small replace) and add a line to the Log in `IDK INTROS/IDK INTROS.md` after each delivery. If the vault is not connected, write up your decisions and delivered files at the end so Rachit can paste them in.

Related: Claude Nine intro - draft v1, Intro animations - parallel workflow, Intro animations - tracker, Fern intro - pixel style (orange)
