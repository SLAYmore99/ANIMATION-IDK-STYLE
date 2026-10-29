"""Screen pass for "Life on Claude Nine, on a screen".
usage: python3 post.py <rawdir> <outdir> [frames]   -> outdir/fNNN.png (RGB on black) + outdir/alpha/fNNN.png (RGBA)
Two-layer glow + faint scanlines + hue-preserving tonemap (house recipe), very slight CRT curvature,
vertical motion blur from scroll speed, and the white-out on "war" (f156) as an overexposure of the screen.
"""
import sys, os, json, glob
import numpy as np, cv2

W, H = 1920, 1080
WAR, BLACK = 156, 166           # white-out starts on "war"; hard cut to black (same as v1)
WHITE_LEN = 7                   # frames to full white

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
SCAN = (1 - 0.10 * ((np.arange(H) % 3) == 2)).astype(np.float32)[:, None, None]

# slight barrel (CRT glass). k small: edges move ~6 px at the corners
nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (W / 2)
r2 = nx * nx + ny * ny
K = 0.012
MAPX = (W / 2 + nx * (1 + K * r2) * (W / 2)).astype(np.float32)
MAPY = (H / 2 + ny * (1 + K * r2) * (W / 2)).astype(np.float32)
# a touch of lens/CRT colour fringing toward the edges (red out, blue in), ~1.5 px at the corners
CA = 0.0016
MAPS = {c: ((W / 2 + (MAPX - W / 2) * s).astype(np.float32), (H / 2 + (MAPY - H / 2) * s).astype(np.float32))
        for c, s in ((2, 1 - CA), (1, 1.0), (0, 1 + CA))}       # BGR
# frame vignette: light from a screen in a dark room falls off toward the corners
VIG = (1 - 0.30 * np.clip(r2 / 0.75, 0, 1) ** 1.5).astype(np.float32)[..., None]


def glow(cv):
    core = cv2.GaussianBlur(cv, (0, 0), 1.6) * 0.7
    halo = cv2.GaussianBlur(cv, (0, 0), 9) * 0.45 + cv2.GaussianBlur(cv, (0, 0), 28) * 0.30
    out = (cv + core * 0.6 + halo) * SCAN
    m = out.max(axis=2, keepdims=True)
    return out / np.maximum(1.0, m / 255.0)


def vblur(cv, px):
    if px < 0.6:
        return cv
    n = int(round(px)) * 2 + 1
    k = np.zeros((n, 1), np.float32); k[:] = 1.0 / n
    return cv2.filter2D(cv, -1, k)


def ease_in(t):
    return t * t * t


def to_rgba(rgb):
    a = np.clip(rgb.max(axis=2) / 255.0, 0, 1)
    col = np.where(a[..., None] > 1e-4, rgb / np.maximum(a[..., None], 1e-4), 0)
    return np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)


def main():
    raw, out = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out, 'alpha'), exist_ok=True)
    meta = json.load(open(os.path.join(raw, 'meta.json')))
    files = sorted(glob.glob(os.path.join(raw, 'f*.png')))
    if len(sys.argv) > 3:
        want = {int(x) for x in sys.argv[3].split(',')}
        files = [f for f in files if int(os.path.basename(f)[1:4]) in want]
    for f in files:
        n = int(os.path.basename(f)[1:4])
        cv = cv2.imread(f).astype(np.float32)
        fm = meta['frames'][str(n)]
        prev = meta['frames'].get(str(n - 1))
        if prev:  # scroll speed in frame px -> light vertical smear, capped
            sp = abs(fm['scroll'] - prev['scroll']) * fm['zoom']
            cv = vblur(cv, min(7 * 2, sp * 0.12))
        if n >= BLACK:
            cv[:] = 0
        elif n >= WAR:
            t = min(1.0, (n - WAR + 1) / WHITE_LEN)
            # flash: the screen overexposes, brightest things blow out first, then everything goes white
            e = ease_in(t)
            cv = cv * (1 + 6 * e) + 255 * e * e
            cv = np.clip(cv, 0, 255)
        cv = glow(cv)
        cv = np.dstack([cv2.remap(np.ascontiguousarray(cv[..., c]), *MAPS[c], cv2.INTER_LINEAR, borderValue=0)
                        for c in range(3)])
        if n < WAR:
            cv = cv * VIG
        cv = np.clip(cv, 0, 255)
        cv2.imwrite(os.path.join(out, os.path.basename(f)), cv.astype(np.uint8))
        cv2.imwrite(os.path.join(out, 'alpha', os.path.basename(f)),
                    cv2.cvtColor(to_rgba(cv[..., ::-1]), cv2.COLOR_RGBA2BGRA))


if __name__ == '__main__':
    main()
