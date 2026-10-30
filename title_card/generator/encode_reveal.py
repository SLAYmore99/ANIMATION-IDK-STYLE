"""Fern-style 'encode' text reveal, orange/white CRT look.
Model measured from the Fern refs: each character cell walks through
empty -> 25% dither -> 50% -> 75% -> solid -> glyph, staggered per cell.
The head jumps BAND cells every STEP frames (on 2s), bands are 4 cells wide.
Out = the same walk reversed (glyph -> solid -> 75 -> 50 -> 25 -> empty).
Usage: python3 encode_reveal.py <card.json> <outdir>
"""
import json, sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 24
BAND, STEP, HOLD = 4, 2, 4             # cells per band, frames per jump, charge-up hold
WHITE = np.array([242, 238, 232.]); ORANGE = np.array([255, 122, 61.]); HALO_O = np.array([217, 119, 87.])
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])

def dither_tile(level, h, w, u=4):
    yy, xx = np.mgrid[0:h, 0:w]
    return (BAYER[(yy // u) % 4, (xx // u) % 4] < level * 16).astype(float)

class Line:
    def __init__(s, d):
        s.text = d['text']; s.x, s.y = d['x'], d['y']; s.col = d.get('color', 'white')
        s.P = d.get('pixel', 2); size = d.get('size', 11); track = d.get('track', 0)
        s.f_in = round(d['in'] * FPS); s.f_out = round(d['out'] * FPS); s.out_step = d.get('out_cells', 6)
        f = ImageFont.truetype(FONT, size)
        adv = round(f.getlength('M')) + track
        asc, desc = f.getmetrics()
        s.cw, s.ch = adv * s.P, (asc + desc) * s.P
        s.glyphs = []
        for c in s.text:                   # one bitmap per cell, art res -> nearest upscale
            g = Image.new('L', (adv, asc + desc), 0); dr = ImageDraw.Draw(g); dr.fontmode = '1'
            dr.text(((adv - f.getlength(c)) / 2, 0), c, font=f, fill=255)
            s.glyphs.append(np.asarray(g.resize((s.cw, s.ch), Image.NEAREST)) / 255.)
        s.tiles = {lv: dither_tile(lv, s.ch, s.cw) for lv in (0.25, 0.5, 0.75)}
        solid = np.ones((s.ch, s.cw)); solid[:, :1] = 0.82   # faint cell seam
        s.tiles[1.0] = solid
        s.width = s.cw * len(s.text)

    def state(s, i, f):
        """None=empty, float=dither/solid level, 'g'=glyph"""
        if f < s.f_in: return None
        if f >= s.f_out:
            k = f - s.f_out; head = s.out_step * (k // STEP + 1) - 1; e = head - i
            if e < 0: return 'g'
            return [1.0, 0.75, 0.5, 0.25][e // BAND] if e < 4 * BAND else None
        k = f - s.f_in
        head = BAND - 1 if k < HOLD else BAND - 1 + BAND * ((k - HOLD) // STEP + 1)
        d = head - i
        if d < 0: return None
        return [0.25, 0.5, 0.75, 1.0][d // BAND] if d < 4 * BAND else 'g'

    def draw(s, mask, f):
        for i, c in enumerate(s.text):
            st = s.state(i, f)
            if st is None: continue
            tile = s.glyphs[i] if st == 'g' else s.tiles[st]
            x0, y0 = s.x + i * s.cw, s.y
            mask[y0:y0 + s.ch, x0:x0 + s.cw] = np.maximum(mask[y0:y0 + s.ch, x0:x0 + s.cw], tile)

def blur(m, r):
    im = Image.fromarray((m * 255).astype('uint8'))
    if r < 10: return np.asarray(im.filter(ImageFilter.GaussianBlur(r))) / 255.
    sm = im.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(r / 4))
    return np.asarray(sm.resize((W, H), Image.BILINEAR)) / 255.

def glowify(m):
    return np.clip(m * 0.92 + blur(m, 2.5) * 0.55, 0, 1), blur(m, 22) * 0.45 + blur(m, 48) * 0.22

def main(card, out):
    C = json.load(open(card)); os.makedirs(out + '/pre', exist_ok=True); os.makedirs(out + '/alpha', exist_ok=True)
    lines = [Line(d) for d in C['lines']]; n = round(C['duration'] * FPS)
    photo = None
    if C.get('photo'):
        p = C['photo']; im = Image.open(p['path']).convert('L')
        im = im.resize((round(im.width * p['h'] / im.height), p['h']), Image.LANCZOS)
        photo = (np.asarray(im) / 255., p['x'], p['y'])
    rng = np.random.default_rng(7)
    yy, xx = np.mgrid[0:H, 0:W]; vig = 1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    bg = np.array([8, 5, 4.]) * vig[..., None]
    for f in range(n):
        mw, mo = np.zeros((H, W)), np.zeros((H, W))
        # rule line: draws left->right on 2s, retracts at out
        r = C.get('rule')
        if r:
            fi, fo = round(r['in'] * FPS), round(r['out'] * FPS); seg = r['w'] / 6
            if f >= fi:
                k = (min(f, fo) - fi) // STEP + 1; ww = min(r['w'], seg * k)
                if f >= fo: ww = max(0, r['w'] - seg * ((f - fo) // STEP + 1))
                mw[r['y']:r['y'] + 2, r['x']:r['x'] + int(ww)] = 1
        for L in lines: L.draw(mo if L.col == 'orange' else mw, f)
        cu = C.get('cursor')   # orange block cursor, blinks 12 frames on / 12 off
        if cu and round(cu['in'] * FPS) <= f < round(cu['out'] * FPS) and ((f - round(cu['in'] * FPS)) // 12) % 2 == 0:
            mo[cu['y']:cu['y'] + cu['h'], cu['x']:cu['x'] + cu['w']] = 1
        wc, wb = glowify(mw); oc, ob = glowify(mo)
        light = wc[..., None] * WHITE + wb[..., None] * WHITE * 0.30 + oc[..., None] * ORANGE + ob[..., None] * HALO_O * 0.55
        pre = bg + light
        if photo:
            ph, px, py = photo; h, w = ph.shape
            pre[py:py + h, px:px + w] = ph[..., None] * np.array([235, 228, 220.]) * 0.85 + 6
        pre += rng.normal(0, 2.2, pre.shape)
        Image.fromarray(np.clip(pre, 0, 255).astype('uint8')).save(f'{out}/pre/f_{f:04d}.png')
        a = np.clip(light.max(2) / 255, 0, 1)
        rgb = np.where(a[..., None] > 0.002, light / np.maximum(a[..., None], 1e-3), 0)
        Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype('uint8'), 'RGBA').save(f'{out}/alpha/f_{f:04d}.png')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
