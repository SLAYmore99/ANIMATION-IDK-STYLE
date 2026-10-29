# CLAUDE.md: Rachit's animation style (handoff from the Twitter-feed session, 2026-10-29)

> **Working on the "small steps → too late" animation (change03)?** Read [`CONTEXT_small_steps_too_late.md`](CONTEXT_small_steps_too_late.md) first. It has the measured breakdown of the existing clip, its pixel/CRT recipes and the questions to ask Rachit. Where it is more specific than this file (pixel world, glow, transfers), it wins for that animation.

Paste this file at the root of a new repo. Claude Code reads it automatically. It holds everything learned while building the Twitter/X feed animation for the "Claude Nine" YouTube intro: the look, the glow, the fonts, the motion taste, the exact numbers measured from his references, what he approved and rejected, and the technical recipes that worked. Use it for every animation.

---

## 1. Who and how to work

- **Rachit**: video editor and motion designer (Bengaluru). Edits in **Premiere Pro**. Builds intros in the style of the YouTube channel **idk** (and Fern, Kurzgesagt, Vox).
- He works fast and directly. **Show, don't describe.** Order of work for any animation:
  1. Study every reference frame by frame (contact sheets, dense strips around each move, measure the motion). Tell him what you learned in a few lines.
  2. **Key frames** (stills at every beat, labelled with frame number and what happens) or a short plan of the shot sequence if he asks for one.
  3. **Low-quality preview** (540p MP4 with VO/SFX).
  4. **HD render** only after he says go (see delivery, section 8).
- Check your own output frame by frame before sending (section 7). He notices one stray frame.
- Make the call yourself and state it in one line; ask one short question only when something is truly ambiguous. When he names a reference, measure it; don't approximate.
- After every change, keep a short written log of what changed and why (he keeps an Obsidian vault; write notes he can paste).

## 2. The look: minimal, idk-style

What he wants, learned from repeated feedback:

- **Pure black void.** One thing to read at a time. Big black margins. Nothing on screen that isn't being read.
- **Minimal UI.** He rejected a detailed phone (titanium bezel, glass reflection, rim light, 3D tilt, status bar, tabs) as "chaotic and cheap". The phone is at most a **hairline outline** (0.6 pt at 16% white) and the island. Header = the X mark only.
- **Flat camera. No tilt, no perspective.** Never let the UI slide left/right: he rejected "centring whatever you're showing" because it made the UI shift sideways. **Fix the horizontal position and the zoom for the whole piece; only the content scrolls.**
- **Centred in frame.** The screen/post sits in the middle of the frame with equal margins (idk frames). Centre the screen, not individual elements.
- **One post in focus.** Focused element 100% white. Everything else **blurred but visible**: about 32% opacity + 3.2 pt gaussian blur (from his "Blur and Scroll Through" reference). Inside the focused post: key text full white, the rest dims to ~35%, links like "Show more" to ~10%.
- **Text first.** On a text post, the media under it recedes (~22%) while the words are read; it comes up only when the camera moves to it.
- **No cheap transitions.** No instant-start swipes, no snapping, no overlapping logos over content. Everything eases.
- **Premium = subtract.** If a move can be removed without loss, remove it.

## 3. Colour, glow, fonts

### Colour (what carries meaning)
| Use | Value |
|---|---|
| Background | `#000000` (his video background is near-black). Final files are transparent. |
| Main text | `#E7E9EA` (X dark text) |
| Secondary text | `#71767B` |
| Lines/separators | `#2F3336` |
| X blue (verified, links) | `#1D9BF0` (kept as in the real app so far) |
| **Highlighter** | **`#CCFF00`** (rgb 204,255,0). His final choice. Before that: white (rejected as cheap), then `#EEFF3A`. |
| Claude orange | `#D97757` (terracotta, about rgb 218/119/86). From the intro's style lock: orange = Claude and anything Claude does. Use only where Claude is meant. |

### Glow (keep it subtle)
- **Key text being read:** `text-shadow: 0 0 6px rgba(255,255,255,0.35)` only on the lit words, only while the rest of the post is dimmed.
- **Highlighter bar:** `box-shadow: 0 0 14px rgba(204,255,0,0.28)`. Black letters on the bar have no glow.
- **Claude orange elements:** `box-shadow: 0 0 10px rgba(217,119,87,0.55)`.
- From the intro's style lock (for the pixel/CRT world of the other animations in the same intro): a **two-layer screen glow** on everything: a tight bloom (~2 px) so edges hit full white, plus a soft wide halo (15-45 px) that fades out. It should feel like light from a screen in a dark room, and it must look identical when the transparent file sits over his black.
- **Exact pixel-world glow (battle-tested, from the context file):** bloom Gaussian σ≈1.6 ×0.7, halo σ≈9 ×0.6 + σ≈28 ×0.42, faint scanlines (every third row ×0.90), then a **hue-preserving tonemap** (`out /= max(1, maxchannel/255)`) so orange doesn't bleach to white. Light on black → straight alpha via `a = max(rgb)/255`, `col = rgb/a`. In the pixel world, use orange core **`#FF7A3D`** (≈255,108,40) with halo `#D97757`; plain `#D97757` alone goes muddy when it glows. White humans ≈ rgb(236,236,232). Red is used for "it has turned".

### Fonts
- **His "idk fonts" (supplied by him; ask for the files, they're not in the repo):** **Neue Montreal** (Bold/Medium, etc.) and **Instrument Serif**. For pixel type, rasterise Neue Montreal Bold onto the art-pixel grid.
- **UI text:** X uses **Chirp** (not free). He hasn't supplied it, so **Inter** is the stand-in (regular 15 px body / 20 px line in phone points, bold names). Ask for Chirp if the UI must be exact.
- **Emoji:** Noto Color Emoji.
- Intro style lock, for the pixel/CRT animations: bitmap/terminal faces: condensed terminal caps for labels, lowercase terminal for typed text, chunky game caps for titles. Typing uses a block cursor and is stepped (4-5 characters per step).
- Render text with real layout (canvas `measureText` wrapping, not guessed widths), so highlights and camera targets hit exact words.

## 4. Motion: his named systems and measured references

### Named moves (build exactly this when he names them)
- **slide up:** starts **50 px below** final position, rises into place over **10 frames**, ease `cubic-bezier(0.215, 0.61, 0.355, 1)`. **Opacity 0 → 100% over the first 5 frames, linear**, then holds. He uses this as the **in-animation of a section** (it's also how idk brings a tweet in: measured on ref04 at 1.55 s, the tweet hard-cuts in and rises ~60 px over ~10 frames while brightening).
- **JUMP CUT:** outgoing 100 → 110% scale over 10 frames, ease-in `cubic-bezier(0.55,0.055,0.675,0.19)` (accelerating); hard cut; incoming 90 → 100% over 10 frames, ease-out `cubic-bezier(0.215,0.61,0.355,1)`. Scale about the frame centre. Motion blur stays inside each shot; never blend across the cut.
- AE terms he uses: "out" = Easy Ease Out on the first key (starts slow, fastest at the end); "in" = Easy Ease In on the last key (fastest at the start, slowest at the end). "10 keyframes" = 10 frames.

### The scroll (the move he cared most about)
His reference "Blur and Scroll Through" (Envato Twitter template, light mode) at 7.29-8.9 s, measured by phase correlation, cumulative px per frame at 270p:
```
0, 1, 5, 14, 28, 50, 83, 131, 197, 281, 373, 461, 532, 592, 644, 692, 732, 768, 800,
828, 853, 876, 897, 916, 933, 949, 963, 976, 988, 999, 1009, 1018, 1026, 1033, 1040,
1046, 1051, 1056, 1061, 1065, 1068, 1070
```
- Asymmetric: **9-frame speed-up**, peak (~92 px/f at 270p), then a **long soft settle** (each frame ~10% slower). Travel ~4 screen heights. Out-of-focus cards blurred even when still. No zoom; only the feed moves.
- He first asked for exactly this, then said it felt **"hyper"**. Final approved curve = **45% that measured curve + 55% `cubic-bezier(0.45, 0, 0.2, 1)`**, resampled to the scroll's length (quick scrolls 24-28 frames, a "little longer" scroll 30). Peak speed is then 2.78x the average instead of 3.53x. Keep motion blur light (vertical only, proportional to speed, capped ~7 pt).
- What he rejected: a fast-start "catch" curve (one-frame jumps read as a "cheap swipe"); symmetric short eases that felt like a swipe; heavy motion smear.
- Between hero posts, scroll **through blurred filler posts** (1 filler for a quick scroll, 2 for a longer one) so it feels like really scrolling a feed.
- Focus hand-over during a scroll: the leaving post recedes (fade + blur) over the first ~35% of the move; the arriving post sharpens between 30% and 72%.

### Highlighter (idk's "how to focus on tweets" style, ref04 + ref05)
- ref05 (idk): a blur cut into a big crop, ~0.3 s still, then a marker sweeps left to right over ~0.55 s (fast start, slow finish).
- Built version (approved):
  - Marker is **shorter than the line box** (line height − 2.5 pt, starting 1.5 pt down), radius 2.5, colour `#CCFF00`.
  - Sweeps **line by line** in reading order, 12 frames total (`cubic-bezier(0.33, 0.6, 0.3, 1)`).
  - A soft **6-pt leading edge** while sweeping that **shrinks to nothing over the last 12%** (no snap when it completes).
  - Letters turn black **only behind the solid part** (a black copy of the text clipped to the bar, never the base text recoloured).
  - **Start the sweep only when the post has fully settled and is sharp** (at 80% of the scroll). Sweeping over still-moving or still-blurring text was the "glitch" he saw.
  - **Hold it** after the sweep so it registers: ~14 frames (0.6 s) minimum; never start the next move the frame the sweep ends.
  - Highlight only the phrase he names (e.g. only "CLAUDE + YouTube = $$$$", not the line under it).
- Earlier "lit vs dim" from ref04 still applies: key words stay white, the rest of the post dims.

### Other rules from the intro's brief and his notes
- **Sync:** in the pause before a phrase the picture is still; the next beat starts on the first syllable (0-50 ms after the voice). Nothing anticipates the word.
- **No linear motion** except opacity ramps and constant drifts. Entrances fast-in, soft landing; exits ~70% of the entrance time.
- **Two speeds** (pixel world): layout/camera moves smooth at full frame rate; "digital" things (typing, encodes, pops) stepped at ~8-12 fps.
- **Digital idle** (pixel world): every icon hops 1 art pixel up and back every 9-10 frames, hard step, each out of phase. Nothing sits dead still, nothing floats smoothly.
- **No plain squares** for spawn effects; elements appear in their own shape (pixel dissolve, dither, scan-line encode). Fern-style text encode: each character cell walks empty → 25% dither → 50% checker → 75% → solid → the letter, 4 cells per band, stepped every 2-3 frames.
- **Pacing:** tightly paced, slowly ramping up (holds get a little shorter as it goes), **never rushed**. He set hard length caps (10 s, then 12 s, then 6 s); fit the cut to the cap by trimming holds and video windows, not by speeding up scrolls.

## 5. Content rules for social-post animations
- Real posts exactly as posted: real handle, text, counts, date. Pull them yourself (section 6).
- Video posts: play the clip window he names; the poster frame must be the **first frame of the exact segment that plays** (otherwise the start jumps). The duration chip **counts down the real remaining time** while it plays (a static timestamp was flagged).
- Trim spoken clips to his exact words (speech-to-text for word timings, cut the pauses, verify the cut by transcribing it again).

## 6. Technical recipes (what worked)

**Stack:** Remotion (React) for everything UI/feed-based. Posts are data (`posts.json`), shot timings are data (`beats.json`), so swapping a post or retiming is a one-line change.
- Remotion's own Chrome download may be blocked in a cloud container. Point it at a local Chromium: `Config.setBrowserExecutable("/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")` (path for Claude Code cloud).
- **Crisp zoom:** scale the UI with CSS `zoom` (laid out at full resolution), not `transform: scale` (rasterises at 1x and looks soft). Note `left/top` of a zoomed element are in zoomed units.
- **Independent tracks**, not one global keyframe list: scroll, camera, and each post's fade/blur/dim/marker/media animate separately, so a highlight can start while the scroll tail settles.
- One shared `beats.json` read by both the timeline and the SFX script, so sound never drifts from picture.
- Transparent version: a context flag that drops every black background (scene, phone screen, post cards), so the file sits over any footage.

**Fetching X posts** (needs the environment's network set to full internet or these hosts allowed: x.com, api.x.com, twitter.com, pbs.twimg.com, video.twimg.com, abs.twimg.com, api.fxtwitter.com):
- `https://api.fxtwitter.com/status/<id>`: text, author, avatar, counts, date, direct photo/video URLs. Use the `/status/<id>` form (the `/<user>/status/<id>` form returned "Not found").
- Avatars: replace `_normal` with `_400x400` in `avatar_url`.
- Long videos: pull only the segment with ffmpeg. ffmpeg needs the proxy set explicitly in a cloud container: `export http_proxy=$HTTPS_PROXY` and `-ca_file /root/.ccr/ca-bundle.crt`.
- X search pages need a login; find posts by web search instead.

**Speech-to-text for word timings** (works when the environment has full internet; otherwise use audio energy + fricative onsets and ask him to confirm by ear): `pip install faster-whisper`, model `small.en`, `word_timestamps=True`. Feed it a numpy array (its own audio loader failed with the installed `av` version). Whisper spells "Claude Code" as "cloud code"; it may also invent words at the very end of a clip.

**SFX (when no library is available):** synthesise. Whooshes = band-passed pink/white noise whose level and brightness follow the scroll's speed curve (peaks on the fastest frame, fades through the settle); soft 2.35 kHz ticks on each highlight start; a gentle low tap on the section's in-animation. Keep it subtle: whoosh peaks about −24 dBFS, ticks −26, under a VO around −14. Deliver as its own 48 kHz 24-bit stereo .wav stem.

## 7. Checks before sending anything
- **Frame-diff scan** (mean absolute difference between consecutive frames): flag isolated spikes that aren't planned cuts. Smooth moves show ramps; glitches show single-frame spikes.
- **Measure moves you're emulating** with phase correlation and compare the curve to the reference numbers.
- **Highlight check:** count highlighter-coloured pixels per frame. A clean sweep rises smoothly, then holds perfectly flat (0% wobble). Wobble or dips = the bar is sweeping over moving/blurring text.
- **Framing check:** draw a centre crosshair on every hero frame; confirm the screen sits centred and nothing drifts sideways (measure horizontal shift; low correlation peaks ≤0.06 in blurred frames are noise).
- Audio: `volumedetect` per section (VO vs SFX vs clip audio). Quiet clip audio gets normalised (`loudnorm=I=-16:TP=-1.5`).
- Final files: ffprobe size, fps, frame count; alpha corners = 0.

## 8. Delivery
- **Spec:** 1920x1080, **23.976 fps** (his clips), length to the frame of his cut.
- **Preview:** 540p MP4 with VO + SFX (`--scale=0.5`).
- **HD:** 1080p H.264 MP4 (CRF ~14) with VO + SFX, plus **ProRes 4444 with alpha** (`--codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png --muted`), plus the **SFX stem .wav** separately. When he asks for "just the MP4 and SFX", send only those.
- Re-encode source clips at full resolution for HD (previews can use 960-wide copies).
- **Big files** (ProRes is ~30 MB per second): too big for GitHub (100 MB/file), and his file-transfer tool alters .mov/.mp4 headers. **Default (from the change03 chat, where a plain split corrupted the ProRes header):** split into 24 MB parts, XOR every byte with `0x5A`, send; he un-XORs and joins on the computer, then checks the md5 against the original. In the Twitter session, plain 95 MB binary parts sent through the Claude app (+ a Windows `.bat` running `copy /b ...` then `certutil -hashfile ... MD5`) rejoined to the right md5 here. Always give him the md5 and a join script, whichever method. (A split zip failed to verify; don't use it.)
- No After Effects Dynamic Link. Premiere: animation on a video track, SFX stem on its own audio track.
- Always give full file paths and keep every version (new file per version, git tags for cuts he may come back to).

## 9. His references for this style (what each one taught)
| Reference | Lesson |
|---|---|
| idk "MOST IMPORTANT: how to focus on the tweets" (ref04) | Real tweets on pure black; ~0.8-1.2 s per post; blur-punch into a post; key words white, rest dims; quote tweets stack; slide-up entry (~60 px over ~10 f). |
| idk "clean highlight" (ref05) | Marker sweep left to right ~0.55 s, fast start, slow finish; depth-of-field crop. |
| "Blur and Scroll Through" (Envato, light) | The scroll curve above; blurred neighbours; heavy blur at speed (he later wanted it calmer). |
| "UI incorporated with phone screen" (light) | Phone never shown whole; camera close; tabs ease sideways. |
| "Dark mode UI interaction in phone" | Dark X feed with inline autoplaying videos; dim second phone behind for depth. |
| Figma "X Social Media Post Mockup" (dark + light, iPhone with Dynamic Island) | Base for the X post UI: header X mark, name + verified + handle + date, body, media card, action row. |

## 10. The intro this belongs to (context)
- YouTube intro about Igor Babuschkin's short story "Life on Claude Nine", built in parallel chats, one animation per chat, each delivered as a separate clip he edits into his timeline.
- VO line for the Twitter section: "Every time you open Twitter, you see someone winning." (it leads into "And there's this constant anxiety...").
- The other animations live in a **pixel/CRT world** (white = humans/world, Claude orange = Claude, two-layer glow, bitmap type, stepped digital motion). The Twitter section stayed **crisp real UI** on black so it reads as the real app; pixel touches only at the edges, if at all.
- Final state of the Twitter section (v10, 6 s cut): opens on a 3D eye video (slide-up in) → scroll → "CLAUDE + YouTube = $$$$" highlighted → scroll → a motion-design video → a slightly longer scroll → "Software is dead, long live software!" highlighted with the GitHub repo card below, held to the end. Highlights `#CCFF00`, fixed centred camera, calm scrolls, subtle synthesised SFX.
