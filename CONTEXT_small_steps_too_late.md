# Context: "small steps → too late" animation (Claude Nine intro, change03)

Drop this file in the repo root of the new session and read all of it first. You are **picking up an animation that already exists and making changes to it**. Rachit (video editor, Premiere Pro, Bengaluru) will tell you what to change. This note gives you everything the previous chats knew so you can start without re-asking the basics.

## 0. Read this first: what exists and what doesn't
- The animation is **`Change03_small_steps_to_title_v1.mp4`**, delivered 2026-10-24 (the file Rachit uploads with this note is a 12.72 s excerpt of it: 1920x1080, 23.976 fps, 305 frames, with audio).
- **There is no source for it.** The folder `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change03_small_steps_to_title\` contains only that one mp4: no scripts, no frame PNGs, no layers. The chat that built it is gone. Treat the mp4 as the spec: **measure it frame by frame** (contact sheets, full-rate strips around every transition) before changing anything. Do not assume you can "just tweak a parameter".
- Expect to **rebuild** the parts that change. Everything that has to match (look, glow, motion) is described below, and two other animations built in the same style *do* have source you can borrow from (section 6).
- **Ask Rachit what he wants changed first**, then plan. If something is unclear, one short question.

## 1. Where this sits in the intro
- Project: a Fern-style YouTube intro about Igor Babuschkin's short story *Life on Claude Nine* ("Claude Nine intro"). Practice work for Rachit's intro-training track (IDK INTROS), not a client job.
- This animation is the **"small steps → too late" beat** (voiceover lines 23-25, production-map beat 15). In the full draft it runs 80 s → ~92.7 s; the same file continues to 104.6 s (title card), but this clip is the part up to and including the shoggoth hold.
- VO (master v2 file, `C:\Users\rachi\Desktop\Work\INTROS\vo_final\VO timing v2.csv`):
  - L23 67.916-70.032 "But what if it's a series of small steps?"
  - L24 70.332-71.978 "Where every step feels like winning"
  - L25 72.328-73.359 "until it's too late."
  - In the draft the VO was re-timed, and "it's too late" was moved so it **lands on the reveal frame** (the smiley → shoggoth change). Take the real timing from the clip Rachit gives you (its audio is in the file), not from these numbers. The clip's audio is loud 0-5.5 s (the three lines), mostly silent after, with a short hit around 7-8.5 s.
- The animation is **delivered as its own clip**, not baked into the full video. Rachit places it on his Premiere timeline.

## 2. What the current animation does (measured from the clip, times in the clip)
All times are seconds from the clip start; frames at 23.976 fps.

| Time | What happens |
|---|---|
| 0.00-0.50 | Black, a **white pixel character** (curly hair, round glasses, collar; the engineer asset) stands left of centre. Digital idle: tiny hard 1-art-pixel hop. |
| 0.50-1.25 | Five **rounded-pill "steps"** are drawn left to right (outlines, white), one per ~0.15 s. |
| 1.50-1.75 | A **small smiley** (white, dim → full) appears at the right end of the row. It is the goal. |
| 2.25-4.25 | **Coins/sparks drop in from the top edge** onto each pill in turn (small round pings, stepped). Each pill **fills solid white** as it is hit: step 1 ~2.3 s, 2 ~2.6, 3 ~3.0, 4 ~3.5, 5 ~3.9-4.2. Every step "feels like winning". One pill shows a tiny dark glitch pixel at ~3.75. |
| 4.25-4.60 | Everything held full white for a beat (tension, nothing moves except the idle). |
| ~4.70 | **Turn:** a glitch/scramble pass sweeps the row. Character, all five pills and a spray of particles go **red** (saturated red, not Claude orange). The pills become a twisted, skewed chain. The small smiley stays white. This is "until it's too late" arriving. |
| 4.75-5.75 | Red chain + red character held, jittering. |
| ~5.80-6.00 | The red row **exits right to left**, shrinking toward the character, while the small smiley **glitch-jumps to the centre**. |
| 6.00-6.50 | The smiley (now **orange pixel outline**, big art pixels) grows to fill the middle. |
| 6.50-7.50 | **Glitch transition 2D → 3D:** the pixel smiley tears (horizontal slice offsets, dropped rows) and resolves into a **dithered 3D orange smiley mask**. |
| 7.50-8.75 | **Staggered position jumps** (hard cuts) pull the mask left/up while a **shoggoth** (white dithered tentacled creature with eyes) appears behind it and fills the right. Reveal frame = "too late". |
| 8.75-12.72 | **Hold** on the shoggoth wearing the orange mask, slow drift, **rare** single-frame glitches only. It holds until the Terror Hit sound dies out (~5.4 s after the reveal, per the earlier notes), then it cuts away in the draft. |

Rachit's earlier notes for this beat (from the change round, 2026-10-24):
- The small-steps opening is kept. The red elements exit right to left.
- The smiley glitch-jumps to centre and grows, then a glitch transition from the 2D to the 3D smiley, then staggered position jumps into the shoggoth mask.
- The shoggoth glitches **rarely**; the hold lasts until the Terror Hit dies out.
- Later in the same file (not in the excerpt): blog page flat with orange markers on the 3 steps, pixel terminal `$ claude` with the Claude star, a horizon line that flashes white, then the title card. Not part of what you are changing unless Rachit says so.

## 3. Style lock (pixel / CRT world, same as every animation in this intro)
- **Transparent background in the final .mov.** Previews are shown on black. Light on black → alpha (recipe in section 6).
- **Colour means something:** white = humans and the world; **Claude orange** = Claude and what it does; here **red** is used for "it has turned" (the red scramble). Don't introduce other colours.
  - Orange: core `#FF7A3D` ≈ RGB(255,108,40), halo `#D97757` (terracotta). Pure `#D97757` alone goes muddy when it glows; use the saturated core.
  - White humans: about RGB(236,236,232).
- **Pixel art:** hard-edged, nearest-neighbour, one art pixel ≈ 4-6 screen px at 1920. Solid white fills with dark line details cut in, never outline drawings for characters. Sparse, centred layouts, one idea per frame, big empty margins.
- **Screen glow (Rachit wants it):** tight bloom (Gaussian σ≈1.6, ×0.7) + wide halo (σ≈9 ×0.6 plus σ≈28 ×0.42), then faint scanlines (every third row ×0.90), then a **hue-preserving tonemap** (`out /= max(1, maxchannel/255)`) so orange doesn't bleach to white.
- **No squares:** he rejected "squares as spawn effects". Things appear as their own shape: pixel dissolve (15/40/70/100 % coverage with a brightness flash), dither, scan-line encode.
- **Digital idle:** every icon hops 1 art pixel up and back every 9-10 frames, hard step, each out of phase. Nothing floats or breathes smoothly.
- **Two speeds:** layout/camera moves smooth at full frame rate; everything "digital" (typing, fills, pops, glitch) stepped at ~8-12 fps.
- **Cuts land on the peak of the speed curve** (one continuous move through the cut: outgoing accelerates, incoming starts at the same speed and decelerates).
- **Sync rule (Fern):** in the pause before a phrase the picture is still; the next beat starts on the first syllable (0-50 ms after the voice), never before it.
- **Premium means subtract:** remove any move that can be removed without loss.
- **Rachit's named moves:** *JUMP CUT* = outgoing 100→110 % scale over 10 frames ease-in, hard cut, incoming 90→100 % over 10 frames ease-out, about the frame centre. *slide up* = starts 50 px below, rises to place over 10 frames ease-out, opacity 0→100 % over the first 5 frames linear.
- **Fonts (when text is needed):** Rachit supplied **Neue Montreal** (Bold/Medium etc.) and **Instrument Serif** (his "idk fonts"). For pixel type, rasterise Neue Montreal Bold onto the art-pixel grid. Ask him for the files if you need them; they are not in this repo.

## 4. Assets and where they live (his computer; ask him to attach what you need)
- Character: `C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\engineer_asset_pack\` (40x54 grid, curly hair, round glasses, tee + chain; neutral and worried, 2 boil drawings). The L09 animation used `C:\Users\rachi\Desktop\Work\INTROS\STEPS ANIMATION REFERENCE\character icon .jpeg` (37x47 grid, 13.65 px cells).
- Smiley / shoggoth mask / 3D plates came from Veo/Nano Banana stills (prompt pack: `C:\Users\rachi\Desktop\Work\INTROS\3D_scene_prompt_pack.md`). The 3D shoggoth in the clip is a stylised dithered plate, not code-built.
- Everything for this intro: `C:\Users\rachi\Desktop\Work\INTROS\`, draft and per-change folders in `...\_claude_draft1\changeNN_<name>\` (this one is `change03_small_steps_to_title`).

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
- Sister animations with source (copy their structure, don't mix their content): L09 "first step" multiplication → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change05_first_step_multiply\source\` (`build.py`, `sfx.py`, `head_grid.npy`); "you're falling behind" → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change07_falling_behind\` (`FALLING_BEHIND_v4_ALPHA.mov`, `source\build2.py`).
- Big files: the file-transfer tool alters .mov/.mp4 headers. Split into 24 MB parts, XOR each byte with `0x5A`, send, un-XOR and `cat` on the computer, and check the md5 against the original. (A plain split corrupted the ProRes header.)
- Environment: Python + numpy + OpenCV + Pillow, ffmpeg, Playwright/Chromium. The shell reaches only package registries and GitHub; fonts and assets must come from Rachit.

## 7. Open questions you should ask Rachit up front
- What exactly should change? (Beats, timing to the VO, the red turn, the 2D→3D transition, the shoggoth reveal, the hold length?)
- Does it still need to sit in the same slot (length in frames), or is the VO being re-timed again?
- Rebuild in code, or keep the Veo/NB shoggoth plate and only rebuild the 2D part? Does he have the original plates and the character/smiley assets to attach?
- Does he want an SFX layer for the new version (the old one used the Terror Hit on the reveal and coin pings per step)?

## 8. Shared notes (only if his Obsidian vault is connected to your session)
Vault: `C:\Users\rachi\Documents\OBSIDIAN AND CLAUDE\New folder\VAULT FOR CLAUDE MEMORY`. Read `IDK INTROS/Intro animations - parallel workflow.md`, `IDK INTROS/Intro animations - tracker.md`, `IDK INTROS/Fern intro - pixel style (orange).md`, `IDK INTROS/Claude Nine intro - draft v1.md`, `Style/Motion systems (named).md`. Update **only your own tracker row** (a small replace) and add a line to the Log in `IDK INTROS/IDK INTROS.md` after each delivery. If the vault is not connected, write up your decisions and delivered files at the end so Rachit can paste them in.

Related: Claude Nine intro - draft v1, Intro animations - parallel workflow, Intro animations - tracker, Fern intro - pixel style (orange)
