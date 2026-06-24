#!/usr/bin/env python3
"""
CHARAMARL / COLOR TAP キャラクター画像 標準処理パイプライン
================================================================
1キャラの元アート（.ai を qlmanage 変換した PNG、または透過/白背景 PNG）から
6色バリアントを生成する。設計方針:

  - 高解像度(760px)・1回処理で劣化させない
  - 「体（メインの色域）だけ」を目標色へ回転 → 歯/舌/口/羽など他パーツは元色キープ
    （= どの色でも5色POPを維持。全体回転だと青等で同化して暗くなるのを回避）
  - 黒(輪郭)・白(目/歯)は保護。外周のみ透過（内側の白は残す）

出力:
  art/colors/<key>_<color>.png        … 透過版（COLOR TAP用）
  <shop_dir>/<key>_<color>.png        … 白背景版（CHARAMARL ショップ用, 任意）

使い方:
  python3 tools/recolor_character.py \
      --key putti --src /tmp/DR_アクキーputti.ai.png \
      [--base-hue 57] [--shop-dir /Users/KCL/charamarl/img/colors_nobg]

  --base-hue 省略時は自動検出。
  .ai は先に:  qlmanage -t -s 1200 -o /tmp/ "<file>.ai"
"""
import argparse, math, os
from collections import deque
import numpy as np
from PIL import Image

SIZE = 760
WHITE_THR = 238

# 6色の目標（体の色相）。歯/舌/口/羽は触らないので、ここは体だけに効く。
TARGETS = [
    ("red",    2,   1.15, 1.20),
    ("yellow", 50,  1.20, 1.05),
    ("green",  120, 1.30, 1.02),
    ("cyan",   175, 1.30, 1.10),
    ("blue",   225, 1.20, 1.18),
    ("pink",   305, 1.30, 1.06),
]


def build_base(src):
    """高解像度で読み込み、外周だけ透過のalphaを作る（内側の白=目/歯は保持）。"""
    im = Image.open(src).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    a = np.array(im)
    h, w = a.shape[:2]
    alpha = np.full((h, w), 255, np.uint8)
    vis = np.zeros((h, w), bool)
    q = deque()

    def seed(y, x):
        r, g, b = a[y, x]
        if r > WHITE_THR and g > WHITE_THR and b > WHITE_THR and not vis[y, x]:
            vis[y, x] = True
            q.append((y, x))

    for x in range(w):
        seed(0, x); seed(h - 1, x)
    for y in range(h):
        seed(y, 0); seed(y, w - 1)
    while q:
        y, x = q.popleft()
        alpha[y, x] = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not vis[ny, nx]:
                r, g, b = a[ny, nx]
                if r > WHITE_THR and g > WHITE_THR and b > WHITE_THR:
                    vis[ny, nx] = True
                    q.append((ny, nx))
    return np.array(im), alpha


def detect_base_hue(rgb):
    """有彩色の主要色相をベクトル平均で検出（体の色を推定）。"""
    hsv = np.array(Image.fromarray(rgb).convert("HSV")).astype(float)
    H, S, V = hsv[:,:,0]*360/255, hsv[:,:,1]/255, hsv[:,:,2]/255
    m = (S > 0.4) & (V > 0.3)
    hs = H[m]
    if hs.size == 0:
        return 0.0
    ang = np.radians(hs)
    return math.degrees(math.atan2(np.sin(ang).mean(), np.cos(ang).mean())) % 360


def recolor_body(rgb, alpha, base_hue, target_hue, sat_mul, val_mul, win=25):
    """体の色域(base_hue±win)だけを target_hue へ。他パーツ・黒・白は不変。"""
    hsv = np.array(Image.fromarray(rgb).convert("HSV")).astype(np.int16)
    H, S, V = hsv[:,:,0].copy(), hsv[:,:,1].copy(), hsv[:,:,2].copy()
    deg = H.astype(float) * 360 / 255
    d = np.abs(deg - base_hue); d = np.minimum(d, 360 - d)
    body = (d < win) & (S > 60) & (V > 55)
    off = int((target_hue - base_hue) / 360 * 255)
    H2 = (H + off) % 256
    S2 = np.clip(S * sat_mul, 0, 255)
    V2 = np.clip(V * val_mul, 0, 255)
    H = np.where(body, H2, H); S = np.where(body, S2, S); V = np.where(body, V2, V)
    out = Image.fromarray(np.dstack([H, S, V]).astype("uint8"), "HSV").convert("RGB")
    return np.dstack([np.array(out), alpha]).astype("uint8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="キャラのキー名 (例: putti)")
    ap.add_argument("--src", required=True, help="元PNG(.ai変換済み 等)")
    ap.add_argument("--base-hue", type=float, default=None, help="体の基準色相。省略で自動検出")
    ap.add_argument("--win", type=float, default=25, help="体の色域の幅(±度)")
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), "..", "art", "colors"))
    ap.add_argument("--shop-dir", default=None, help="白背景版の出力先(任意)")
    args = ap.parse_args()

    rgb, alpha = build_base(args.src)
    base = args.base_hue if args.base_hue is not None else detect_base_hue(rgb)
    print(f"[{args.key}] base hue = {base:.1f}{'  (auto)' if args.base_hue is None else ''}")

    os.makedirs(args.out_dir, exist_ok=True)
    if args.shop_dir:
        os.makedirs(args.shop_dir, exist_ok=True)

    for name, t, sm, vm in TARGETS:
        rgba = recolor_body(rgb, alpha, base, t, sm, vm, win=args.win)
        im = Image.fromarray(rgba, "RGBA")
        im.save(os.path.join(args.out_dir, f"{args.key}_{name}.png"))
        if args.shop_dir:
            wb = Image.new("RGBA", im.size, (255, 255, 255, 255))
            wb.paste(im, mask=im)
            wb.convert("RGB").save(os.path.join(args.shop_dir, f"{args.key}_{name}.png"))
        print(f"  -> {args.key}_{name}.png")
    print("done")


if __name__ == "__main__":
    main()
