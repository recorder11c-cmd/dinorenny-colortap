# ギャラリー降らせリール（IG用・7秒・1080×1920）

参考: WEGO×GRAPE BRAIN のリール（無地の地に切り抜きが降って積み上がり、白く抜けてロゴ）。構成だけ借りた。

手順（scratchpad が消えても作り直せる）
1. 作品カードの取得: `python3 fetch_cards.py <出力dir>`（api/gallery の approved・INTERVIEW以外を 320px 正方形で保存。cards.json も作る）
2. 書き出し: `node capture_reel.js 7 <frames dir>`（reel.html と同じフォルダで。playwright は ../node_modules を使う）
3. 結合: `ffmpeg -framerate 30 -i frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart out.mp4`

文言・色は reel.html の CFG。🔴 作家の作品を公式IGに出す前に作家の了承（10/2のルール）。
