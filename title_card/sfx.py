"""Transition audio for the LIFE ON CLAUDE NINE title card: the bridge out of the nuclear flash.
0 s = frame 0 of the card (91 frames @ 23.976). Synthesised, numpy only.
  - aftermath: sub rumble + low pressure air, decaying from frame 0
  - a faint ear-ring (tinnitus) that dies away
  - soft filtered ticks on every encode step, panned with the head (title warm, subtitle finer)
  - a warm low chord blooms when the title resolves, holds, releases on the out
  - near-silent cursor ticks, reversed ticks + an air tail on the out, silence on the last frames
usage: python3 sfx.py <out.wav>   (48 kHz, 24-bit, stereo)
"""
import sys, subprocess, numpy as np

SR, FPS, NF = 48000, 24000 / 1001, 91
N = int(round(NF / FPS * SR))
t = np.arange(N) / SR
rng = np.random.default_rng(9)
L = np.zeros(N); R = np.zeros(N)


def fr(f):
    return f / FPS


def db(x):
    return 10 ** (x / 20)


def band(x, lo, hi):
    """FFT band-pass with soft edges"""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi < SR / 2:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def add(sig, start_s, pan=0.0, gain=1.0):
    i = int(start_s * SR)
    if i >= N:
        return
    sig = sig[:N - i] * gain
    a = (pan + 1) * np.pi / 4                   # constant-power pan
    L[i:i + len(sig)] += sig * np.cos(a)
    R[i:i + len(sig)] += sig * np.sin(a)


# 1. aftermath: sub rumble + pressure air, decaying from frame 0
brown = np.cumsum(rng.normal(0, 1, N)); brown -= np.convolve(brown, np.ones(4801) / 4801, 'same')
rum = band(brown, 0, 110); rum /= np.abs(rum).max()
rum = rum * np.exp(-t / 1.15) + np.sin(2 * np.pi * 34 * t) * 0.55 * np.exp(-t / 1.5)
air = band(rng.normal(0, 1, N), 180, 900); air /= np.abs(air).max()
air *= np.exp(-t / 0.45)
add(rum, 0, 0.0, db(-12))
add(air, 0, 0.15, db(-27))

# 2. ear-ring after the blast, dies away (slightly detuned L/R so it shimmers, not whistles)
ring_env = np.minimum(1, t / 0.06) * np.exp(-t / 1.05)
L += np.sin(2 * np.pi * 3950 * t) * ring_env * db(-38)
R += np.sin(2 * np.pi * 3972 * t) * ring_env * db(-38)


# 3. encode ticks
def tick(freq, dur=0.05, decay=0.016, click=0.003):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * tt) * np.exp(-tt / decay)
    c = band(rng.normal(0, 1, n), 1500, 7000) * np.exp(-tt / click)
    s = s + 0.35 * c / (np.abs(c).max() + 1e-9)
    return band(s, 200, 6500) / (np.abs(s).max() + 1e-9)


title_steps = [7] + list(range(10, 25, 2))          # charge-up, then every band jump / collapse
for k, f in enumerate(title_steps):
    p = -0.55 + 1.1 * k / (len(title_steps) - 1)
    add(tick(1350 + 25 * k), fr(f), p, db(-25 if f > 7 else -30))
sub_steps = list(range(20, 47, 2))
for k, f in enumerate(sub_steps):
    p = -0.35 + 0.7 * k / (len(sub_steps) - 1)
    add(tick(2600, decay=0.010), fr(f), p, db(-34))
for f in (46, 70):                                   # cursor blinks on
    add(tick(900, decay=0.006), fr(f), 0.3, db(-42))

# 4. resolve chord: warm low fifth blooming as the title lands (f16), released on the out (f76)
on, off = fr(16), fr(76)
env = np.clip((t - on) / 0.55, 0, 1) ** 2 * np.clip(1 - (t - off) / 0.45, 0, 1)
chord = np.zeros(N)
for fq, a in ((55, 1.0), (82.5, 0.55), (110, 0.6), (164.8, 0.28), (220, 0.18)):
    chord += a * (np.sin(2 * np.pi * fq * t) + 0.5 * np.sin(2 * np.pi * fq * 1.003 * t))
chord = band(chord, 0, 900) * env
chord /= np.abs(chord).max()
L += chord * db(-24) * 0.96; R += chord * db(-24)

# 5. out: reversed-order ticks, then an air tail that is silent by the end
out_steps = list(range(76, 86, 2))
for k, f in enumerate(out_steps):
    add(tick(1800 - 60 * k, decay=0.012), fr(f), -0.5 + 0.25 * k, db(-28))
tail = band(rng.normal(0, 1, N), 1800, 6000); tail /= np.abs(tail).max()
te = np.clip((t - fr(76)) / 0.15, 0, 1) * np.exp(-np.maximum(0, t - fr(80)) / 0.28)
add(tail * te, 0, 0.2, db(-33))

# master: gentle high cut, peak at -8 dBFS, last 4 frames fade to silence
mix = np.stack([band(L, 0, 12000), band(R, 0, 12000)], 1)
mix *= db(-8) / np.abs(mix).max()
fade = np.clip((fr(NF) - t) / fr(4), 0, 1)[:, None]
mix *= fade
out = sys.argv[1]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                '-c:a', 'pcm_s24le', out], input=mix.astype(np.float32).tobytes(), check=True)
print(out, f'{N / SR:.3f}s')
