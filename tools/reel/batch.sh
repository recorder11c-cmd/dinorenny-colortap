#!/bin/bash
# 使い方: ./batch.sh gmc ufoo ...   → ~/Downloads/CHARAMARL/03_画像/reel/run_reel_<char>_v1.mp4
cd "$(dirname "$0")"; OUT=~/Downloads/CHARAMARL/03_画像/reel; mkdir -p "$OUT"
for c in "$@"; do
  case $c in gmc|inkumo|mony|yurucrazy) FLIP=true;; *) FLIP=false;; esac
  case $c in blockma) PIX=true;; *) PIX=false;; esac
  case $c in sue) HERO=/Users/KCL/charamarl/run-art/sue_pixel.png; PIX=true;; *) HERO=/Users/KCL/charamarl/run-art/run_$c.png;; esac
  rm -rf frames out; mkdir -p frames out
  node capture.js $c 11 "https://charamarl.com/run.html" > "log_$c.txt" 2>&1 || { echo "capture failed $c"; continue; }
  printf '{"hero":"%s","flip":%s,"pixel":%s,"title1":"CHARAMARL","title2":"RUN","titleSize":94,"subtitle":"アクキーのキャラ10体で、かけっこ","url":"charamarl.com/run.html","endSub":"キャラは10体から選べる"}\n' "$HERO" "$FLIP" "$PIX" > cfg_$c.json
  PYTHONIOENCODING=utf-8 python3 -X utf8 compose.py cfg_$c.json >> "log_$c.txt" 2>&1 || { echo "compose failed $c"; continue; }
  ffmpeg -y -loglevel error -framerate 30 -i out/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$OUT/run_reel_${c}_v1.mp4" && cp sheet.png "sheet_$c.png" && echo "done $c"
done
echo ALL_DONE
