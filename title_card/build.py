"""LIFE ON CLAUDE NINE title card, v2 design.
Fern digital transition (encode reveal) exactly as the preset: BAND=4 cells, head jumps on 2s,
charge-up hold, clamp at line end, out at 6 cells / 2 frames, lines staggered.
New: Neue Montreal (stand-in Inter until the files arrive) rasterised onto an art-pixel grid,
proportional cells, LED-style pixel gaps, smaller orange subtitle, blinking cursor, screen pass.
usage: python3 build.py <outdir> [frames]   -> outdir/fNNN.png (on black) + outdir/alpha/fNNN.png
"""
import sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, N = 1920, 1080, 91
BAND, STEP = 4, 2
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = os.path.join(HERE, 'fonts', 'Inter-700.ttf')     # -> NeueMontreal-Bold
FONT_MED = os.path.join(HERE, 'fonts', 'Inter-500.ttf')      # -> NeueMontreal-Medium
WHITE = np.array([242, 238, 232.])
ORANGE = np.array([255, 122, 61.])
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])


def dither(level, h, w, u=4):
    yy, xx = np.mgrid[0:h, 0:w]
    return (BAYER[(yy // u) % 4, (xx // u) % 4] < level * 16).astype(np.float32)


def pixel_grid(h, w, P, gap):
    """art-pixel screen texture: each P x P pixel with a faint darker seam on its right/bottom edge"""
    g = np.ones((h, w), np.float32)
    if P >= 4:
        g[:, P - 1::P] = gap
        g[P - 1::P, :] = gap
    return g


class Line:
    def __init__(s, text, font, cap_px, P, track, cy, f_in, f_out, hold, color, out_cells=6):
        s.text, s.P, s.f_in, s.f_out, s.hold, s.col, s.out_cells = text, P, f_in, f_out, hold, color, out_cells
        # rasterise at art resolution: pick the size whose cap height is cap_px art pixels
        size = 4
        while True:
            f = ImageFont.truetype(font, size)
            b = f.getbbox('H')
            if b[3] - b[1] >= cap_px:
                break
            size += 1
        asc, desc = f.getmetrics()
        top = b[1] - 1
        rows = (b[3] - b[1]) + desc + 2           # cap height + descenders
        s.cells = []                              # (x_art, w_art, bitmap_art)
        x = 0
        for c in text:
            adv = max(1, round(f.getlength(c))) + track
            g = Image.new('L', (adv, rows), 0)
            d = ImageDraw.Draw(g)
            d.text((round(track / 2), -top), c, font=f, fill=255)
            # grey-level raster thresholded a little low: keeps the strokes full on the coarse grid
            s.cells.append((x, adv, (np.asarray(g) > 100).astype(np.float32)))
            x += adv
        s.wa, s.ha = x, rows
        s.w, s.h = x * P, rows * P
        s.x0 = (W - s.w) // 2 // 4 * 4
        s.y0 = (cy - (cap_px * P) // 2) // 4 * 4
        s.grid = pixel_grid(s.h, s.w, P, 0.68)

    def state(s, i, f):
        if f < s.f_in:
            return None
        if f >= s.f_out:
            k = f - s.f_out; head = s.out_cells * (k // STEP + 1) - 1; e = head - i
            if e < 0:
                return 'g'
            return [1.0, 0.75, 0.5, 0.25][e // BAND] if e < 4 * BAND else None
        k = f - s.f_in
        head = BAND - 1 if k < s.hold else BAND - 1 + BAND * ((k - s.hold) // STEP + 1)
        d = head - i          # past the last cell the head is simply not drawn (clamp), the rear keeps collapsing
        if d < 0:
            return None
        return [0.25, 0.5, 0.75, 1.0][d // BAND] if d < 4 * BAND else 'g'

    def draw(s, mask, f):
        for i, (xa, wa, bm) in enumerate(s.cells):
            st = s.state(i, f)
            if st is None:
                continue
            x0, y0, w = s.x0 + xa * s.P, s.y0, wa * s.P
            if st == 'g':
                tile = np.kron(bm, np.ones((s.P, s.P), np.float32)) * s.grid[:, xa * s.P:xa * s.P + w]
            elif st == 1.0:
                tile = np.ones((s.h, w), np.float32); tile[:, :max(1, s.P // 3)] = 0.82   # cell seam
            else:
                tile = dither(st, s.h, w)
            reg = mask[y0:y0 + s.h, x0:x0 + w]
            np.maximum(reg, tile, out=reg)


# ---- the card -----------------------------------------------------------------------------
TITLE = Line('LIFE ON CLAUDE NINE', FONT_BOLD, cap_px=15, P=5, track=1, cy=500,
             f_in=7, f_out=76, hold=3, color='white')
SUB = Line('> a short story by igor babuschkin', FONT_MED, cap_px=8, P=2, track=0, cy=596,
           f_in=20, f_out=78, hold=4, color='orange', out_cells=10)   # 34 small cells: bigger out step so it clears by f86, no fade
CURSOR = dict(on=46, off=76, blink=12)            # orange block after the subtitle, 12 on / 12 off

# ---- screen pass (same family as the article: subtle glow, faint scanlines, slight curve) ----
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
SCAN = (1 - 0.10 * ((np.arange(H) % 3) == 2)).astype(np.float32)[:, None, None]
nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (W / 2)
r2 = nx * nx + ny * ny
K, CA = 0.012, 0.0016
MAPX = (W / 2 + nx * (1 + K * r2) * (W / 2)).astype(np.float32)
MAPY = (H / 2 + ny * (1 + K * r2) * (W / 2)).astype(np.float32)
MAPS = {c: ((W / 2 + (MAPX - W / 2) * s).astype(np.float32), (H / 2 + (MAPY - H / 2) * s).astype(np.float32))
        for c, s in ((2, 1 - CA), (1, 1.0), (0, 1 + CA))}


def light(mw, mo):
    def glow(m, halo_k):
        core = m * 0.95 + cv2.GaussianBlur(m, (0, 0), 1.4) * 0.30
        halo = cv2.GaussianBlur(m, (0, 0), 7) * 0.40 + cv2.GaussianBlur(m, (0, 0), 20) * 0.22
        return core, halo * halo_k
    wc, wh = glow(mw, 0.45)
    oc, oh = glow(mo, 0.75)
    rgb = (wc[..., None] * WHITE + wh[..., None] * WHITE + oc[..., None] * ORANGE
           + oh[..., None] * np.array([217, 119, 87.]))
    rgb = rgb * SCAN
    m = rgb.max(axis=2, keepdims=True)
    rgb = rgb / np.maximum(1.0, m / 255.0)
    rgb = np.dstack([cv2.remap(np.ascontiguousarray(rgb[..., c]), *MAPS[c], cv2.INTER_LINEAR, borderValue=0)
                     for c in range(3)])
    return np.clip(rgb, 0, 255)


def to_rgba(rgb):
    a = np.clip(rgb.max(axis=2) / 255.0, 0, 1)
    col = np.where(a[..., None] > 1e-4, rgb / np.maximum(a[..., None], 1e-4), 0)
    return np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)


def frame(f):
    mw = np.zeros((H, W), np.float32); mo = np.zeros((H, W), np.float32)
    TITLE.draw(mw, f)
    SUB.draw(mo, f)
    if CURSOR['on'] <= f < CURSOR['off'] and ((f - CURSOR['on']) // CURSOR['blink']) % 2 == 0:
        P = SUB.P; cx = SUB.x0 + SUB.w + 3 * P; ch = 8 * P
        mo[SUB.y0 + P:SUB.y0 + P + ch, cx:cx + 4 * P] = 1.0
    return light(mw, mo)


def main():
    out = sys.argv[1]
    os.makedirs(os.path.join(out, 'alpha'), exist_ok=True)
    fs = range(N) if len(sys.argv) < 3 else [int(x) for x in sys.argv[2].split(',')]
    for f in fs:
        rgb = frame(f)
        cv2.imwrite(os.path.join(out, f'f{f:03d}.png'), rgb[..., ::-1].astype(np.uint8))
        cv2.imwrite(os.path.join(out, 'alpha', f'f{f:03d}.png'), cv2.cvtColor(to_rgba(rgb), cv2.COLOR_RGBA2BGRA))


if __name__ == '__main__':
    main()
