# Context: "Life on Claude Nine" blog + terminal beat (Claude Nine intro, change03 second half)

Drop this file in the repo root of the new session and read all of it first. You are **picking up an animation that already exists and making changes to it**. Rachit (video editor, Premiere Pro, Bengaluru) will tell you what to change. This note gives you everything the previous chats knew so you can start without re-asking the basics.

## 0. Read this first: what exists and what doesn't
- The animation is the **second half of `Change03_small_steps_to_title_v1.mp4`** (delivered 2026-10-24): the blog page comes back, three story lines light up, a pixel terminal runs `claude`, the page returns, the "flash of light" line lights up and the frame whites out. Rachit uploaded it as a **7.30 s excerpt: 1920x1080, 23.976 fps, 175 frames, with audio** (VO + music).
- **There is no source for this exact clip.** The folder `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change03_small_steps_to_title\` holds only the finished mp4. Treat the clip as the spec and **measure it frame by frame** (contact sheets, full-rate strips around every transition) before changing anything.
- **But the page itself has a source:** it is the same flat "Life on Claude Nine" blog page built for the blog beat (`change04_blog_beat`, HTML seek + Playwright, article engine). Start from `source_v4` / `source_v5` there (see section 6) and rebuild the page, highlighter and lens from it. The terminal and the white flash have no source; rebuild them.
- **Ask Rachit what he wants changed first**, then plan. If something is unclear, one short question.

## 1. Where this sits in the intro
- Project: a Fern-style YouTube intro about Igor Babuschkin's short story *Life on Claude Nine*. Practice work for Rachit's intro-training track (IDK INTROS), not a client job.
- Draft map: 89.6-101 s "blog back, three story lines light up on 'every single step', main-video terminal shot, story's own 'flash on the horizon' line whites out on 'war', data centre ('secret lab'), engineer with the pixel creature, his eyes on 'you', hard cut." This clip is the first part of that block (to the white-out). The secret-lab line was removed in change03, so the VO block shifted +17.92 s.
- VO (master v2, `C:\Users\rachi\Desktop\Work\INTROS\vo_final\VO timing v2.csv`, original timing before the draft re-time):
  - L27 77.080-78.011 "Every single step."
  - L28 78.411-81.572 "From one man's inbox to the brink of a nuclear war."
  - Take real timing from the clip's own audio (speech is loud through about 6.9 s, then it ends). No speech-to-text is available in the cloud container; get word onsets from the audio energy and fricatives and ask Rachit to confirm the key hits by ear.
- Delivered as its own clip, not baked into the full video. Rachit places it in Premiere.

## 2. What the current animation does (measured from the clip, seconds from clip start; frames at 23.976 fps)
Layout: the **page sits in the left half** of the frame (title at about x 410, y 85 in 1920x1080; body text column about 580 px wide, big margins, black everywhere else). The **terminal window sits right of centre**.

| Time | What happens |
|---|---|
| 0.00-0.50 | Flat blog page on black fades/pops in: title **"Life on Claude Nine"** (light grotesque, white), date **January 25, 2026** (mono, grey), body text dimmed grey. Subtle scan lines/phosphor on the page. |
| 0.50-2.40 | Hold, page dimmed except the title. Nothing moves. |
| ~2.50 | **Marker 1:** an orange highlighter bar lands on "That was the plan. Review and approve." (black text on orange fill). |
| ~3.00-3.50 | **Marker 2** on "He starts building tools that make Claude itself work better." (wraps onto a second line; the bar fills in sweeps) and **marker 3** on "Humans still control nuclear weapons". These are "the 3 steps" Rachit asked for orange markers on: each lights on a beat of "every single step". |
| ~3.75-4.00 | Hard cut to the **pixel terminal** (right side, thin light frame, three window dots, title `ivan@laptop: ~/email-automation`). |
| 4.00-4.90 | Terminal: `ivan@laptop ~/email-automation $ claude` is typed; the orange **Claude star** + "Claude Code" + `cwd: ~/email-automation` appear; then a prompt `> help me au...` types with an orange block cursor. |
| ~5.00 | Hard cut back to the page. The three markers have settled into **orange text** (no fill) with the rest dim. |
| 5.00-5.50 | A **new marker sweeps** left to right over "Then, on the horizon, a flash of light. Brighter than the sun." (the horizon line), after a short leading block. |
| 5.50-6.40 | Held on the lit horizon line. |
| ~6.45 | **White-out:** the frame flashes to near-white (page ghosting through) on "war". |
| 6.50-7.30 | Back to black; the clip ends on black. |

Rachit's earlier notes for this block (change03, 2026-10-24): the blog page is flat, with orange markers on the 3 steps; the pixel terminal shows `$ claude` with the Claude star from the first look test; the horizon line flashes white; then the draft-1 title card follows. Keep these unless he says otherwise.

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

## 4. Assets, fonts and where they live (his computer; ask him to attach what you need)
- Page and highlighter: blog beat sources (section 6). Heading = the **blog beat's Pairing A** was Inria Serif headings + Inter body, but this clip shows a **light grotesque heading** and Inter-like body, with the date in mono. Compare against `Blog_beat_v4.mp4` and match what the clip actually shows. Lime `#CEFC04` bars were used in the **article-style** blog beat v4; **this clip uses orange** markers (Claude orange) with black text. Don't mix them up.
- Terminal look: from `C:\Users\rachi\Desktop\Work\INTROS\assets\pixel_style\pixel_look_test_orange_v1.png` (the "first look test" with the Claude star) and the pixel Claude spark from `C:\Users\rachi\Desktop\Work\INTROS\STEPS ANIMATION REFERENCE\` (12 irregular rays, hub about 1/3 of the radius). Bitmap faces for the terminal: VT323 / Press Start 2P / IBM VGA style; Rachit supplied Neue Montreal and Instrument Serif as his "idk fonts" for headlines.
- Real text on the page is from the story's own lines (verbatim). Keep every line **verbatim from Igor Babuschkin's post**; never invent story text. Verify the post and date before showing it.
- Everything for this intro: `C:\Users\rachi\Desktop\Work\INTROS\`, per-change folders in `...\_claude_draft1\changeNN_<name>\`.

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
- Sister animations with source (copy their structure, don't mix their content): the **blog beat** (same page, same engine, closest relative) → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change04_blog_beat\source_v4\` (`index_v4.html`, `r4.py`, `sfx4.py`; also `source_v5\`) and the article engine `C:\Users\rachi\Desktop\Work\INTROS\ARTICLE ENGINE\` (`template.html`, `render.py`, `motion.py`, `lens.py`); L09 "first step" multiplication → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change05_first_step_multiply\source\` (`build.py`, `sfx.py`, `head_grid.npy`); "you're falling behind" → `C:\Users\rachi\Desktop\Work\INTROS\_claude_draft1\change07_falling_behind\` (`FALLING_BEHIND_v4_ALPHA.mov`, `source\build2.py`).
- Big files: the file-transfer tool alters .mov/.mp4 headers. Split into 24 MB parts, XOR each byte with `0x5A`, send, un-XOR and `cat` on the computer, and check the md5 against the original. (A plain split corrupted the ProRes header.)
- Environment: Python + numpy + OpenCV + Pillow, ffmpeg, Playwright/Chromium. The shell reaches only package registries and GitHub; fonts and assets must come from Rachit.

## 7. Open questions you should ask Rachit up front
- What exactly should change? (Page look, marker timing vs the VO, the terminal, the white-out, the length?)
- Is the VO being re-timed again? What length should it be to the frame?
- Should the page stay the same engine/look as the blog beat v4/v5, or the older style in this clip?
- Does he want an SFX layer (the old one used a HUD tick per marker, a click on the cut, and a hit on the white-out)?
- Is the terminal text (`help me au...`) final, or should it complete?

## 8. Shared notes (only if his Obsidian vault is connected to your session)
Vault: `C:\Users\rachi\Documents\OBSIDIAN AND CLAUDE\New folder\VAULT FOR CLAUDE MEMORY`. Read `IDK INTROS/Intro animations - parallel workflow.md`, `IDK INTROS/Intro animations - tracker.md`, `IDK INTROS/Fern intro - pixel style (orange).md`, `IDK INTROS/Claude Nine intro - draft v1.md`, `Style/Motion systems (named).md`. Update **only your own tracker row** (a small replace) and add a line to the Log in `IDK INTROS/IDK INTROS.md` after each delivery. If the vault is not connected, write up your decisions and delivered files at the end so Rachit can paste them in.

Related: Claude Nine intro - draft v1, Intro animations - parallel workflow, Intro animations - tracker, Fern intro - pixel style (orange)
