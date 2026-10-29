// Renders raw frames of "Life on Claude Nine, on a screen" (change03 second half, v3: article only, gap for B-roll).
// usage: node render.js <outdir> [frames: "all" | "0,40,72" ]
// Timeline is in frames at 23.976 fps, synced to the VO onsets measured from the v1 clip:
// Every f60, single f68, step f77 | From f93 (B-roll gap f94-122), inbox ~f112, to the ~f120, brink ~f123, nuclear ~f137, war f156.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const N = 175;
const T = {
  fadeIn: [0, 10],        // brightness ease-out
  jumpOut: [50, 60],      // JUMP CUT: outgoing 100 -> 110 %, ease-in; hard cut at 60 ("Every")
  jumpIn: [60, 70],       // incoming 90 -> 100 %, ease-out
  m1: [68, 80],           // marker "email automation system" on "single", held to the B-roll cut
  gap: [94, 123],         // empty: Rachit's Claude terminal B-roll goes here ("From one man's inbox")
  scroll: [110, 136],     // scroll to the horizon line; it started under the B-roll, so f123 cuts in
                          // just past peak speed and the tail settles (cut on the speed curve)
  m2: [136, 148],         // marker "a flash of light." once the scroll has settled (on "nuclear")
  black: 166,             // hard cut to black (white-out itself is done in post.py from f156)
};
const Z_WIDE = 1.22, Z_CLOSE = 2.1;   // wide: the monitor nearly fills frame; close: a big depth-of-field crop

// --- curves -----------------------------------------------------------------
function bezier(x1, y1, x2, y2) {
  return t => {
    if (t <= 0) return 0; if (t >= 1) return 1;
    let lo = 0, hi = 1, u = t;
    for (let i = 0; i < 40; i++) {
      u = (lo + hi) / 2;
      const x = 3 * x1 * u * (1 - u) ** 2 + 3 * x2 * u * u * (1 - u) + u ** 3;
      if (x < t) lo = u; else hi = u;
    }
    return 3 * y1 * u * (1 - u) ** 2 + 3 * y2 * u * u * (1 - u) + u ** 3;
  };
}
const easeOut = bezier(0.215, 0.61, 0.355, 1), easeIn = bezier(0.55, 0.055, 0.675, 0.19);
const sweep = bezier(0.33, 0.6, 0.3, 1), calm = bezier(0.45, 0, 0.2, 1);
// approved scroll: 45 % measured "Blur and Scroll Through" curve + 55 % cubic-bezier(0.45,0,0.2,1)
const REF = [0,1,5,14,28,50,83,131,197,281,373,461,532,592,644,692,732,768,800,828,853,876,897,916,
  933,949,963,976,988,999,1009,1018,1026,1033,1040,1046,1051,1056,1061,1065,1068,1070].map(v => v / 1070);
function scrollCurve(t) {
  const x = t * (REF.length - 1), i = Math.min(REF.length - 2, Math.floor(x));
  const ref = REF[i] + (REF[i + 1] - REF[i]) * (x - i);
  return 0.45 * ref + 0.55 * calm(t);
}
const clamp = v => Math.max(0, Math.min(1, v));
const prog = (f, [a, b]) => clamp((f - a) / (b - a));
const ramp = (x, a, b) => clamp((x - a) / (b - a));

function state(f, G) {
  const s = { focus: {}, lit: {}, restDim: {}, m1: 0, m2: 0, mo1: 1, mo2: 1 };
  s.bright = (f >= T.black || (f >= T.gap[0] && f < T.gap[1])) ? 0 : easeOut(prog(f, T.fadeIn));
  s.cy = 405;
  if (f < T.jumpIn[0]) {                       // wide: the monitor, title in focus, slow constant push
    const k = f >= T.jumpOut[0] ? 1 + 0.10 * easeIn((f - T.jumpOut[0] + 1) / 10) : 1;
    const drift = 1 + 0.035 * (Math.min(f, T.jumpOut[0]) / T.jumpOut[0]);
    s.zoom = Z_WIDE * drift * k; s.scroll = 0; s.cx = 720; s.cy = 330;
    s.dim = 0.12; s.blur = 1.1;
    s.focus[1] = 1; s.focus[2] = 0.5;            // title, date
    return s;
  }
  const partB = f >= T.gap[0];
  const k = 0.9 + 0.1 * easeOut(prog(f, T.jumpIn));
  // slow constant drift-in on each close shot (nothing sits dead still)
  const drift = partB ? 1 + 0.02 * prog(f, [T.scroll[1], T.black]) : 1 + 0.02 * prog(f, [T.jumpIn[1], T.gap[0]]);
  s.zoom = Z_CLOSE * k * drift;
  s.cx = partB ? G.cx2 : G.cx1;               // fixed per shot: the crop is centred on the marked phrase
  const sp = scrollCurve(prog(f, T.scroll));
  s.scroll = (G.y1 - 405) + sp * (G.y2 - G.y1);
  s.dim = 0.16; s.blur = 2.2;
  const leave = 1 - ramp(prog(f, T.scroll), 0, 0.35), arrive = ramp(prog(f, T.scroll), 0.30, 0.72);
  s.focus[G.k1] = leave; s.focus[G.k2] = arrive;
  const p1 = prog(f, T.m1), p2 = prog(f, T.m2);
  s.m1 = sweep(p1); s.mo1 = leave; s.m2 = sweep(p2);
  s.lit.hl1 = ramp(p1, 0, 0.5) * leave; s.restDim[G.k1] = 1;
  s.lit.hl2 = ramp(p2, 0, 0.5);          s.restDim[G.k2] = 1;
  return s;
}

(async () => {
  const out = process.argv[2] || 'raw';
  const which = (process.argv[3] || 'all') === 'all' ? [...Array(N).keys()] : process.argv[3].split(',').map(Number);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const pg = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + path.resolve(__dirname, 'page.html'));
  await pg.evaluate(html => { document.getElementById('content').innerHTML = html; },
    fs.readFileSync(path.join(__dirname, 'content.html'), 'utf8'));
  await pg.evaluate(() => document.fonts.ready);
  const G = await pg.evaluate(() => init());
  const meta = { frames: {} };
  for (const f of which) {
    const s = state(f, G);
    await pg.evaluate(s => frame(s), s);
    await pg.screenshot({ path: path.join(out, `f${String(f).padStart(3, '0')}.png`) });
    // where the highlighted phrase sits on screen (for the white-out origin in post.py)
    meta.frames[f] = { scrollSpeed: 0, zoom: s.zoom, scroll: s.scroll };
  }
  // phrase-2 centre in frame px once settled
  const r = G.hl2;
  meta.flashOrigin = { x: 960 + ((r[0].x + r[r.length - 1].x + r[r.length - 1].w) / 2 - 720) * Z_CLOSE, y: 540 };
  fs.writeFileSync(path.join(out, 'meta.json'), JSON.stringify(meta));
  await browser.close();
})();
