# COLOR TAP 統一フォーマット（標準パイプライン）

新キャラの COLOR TAP を、SUE / プッチィ / モッスンと同じ品質で量産するための手順。
`template.html` をコピーして CONFIG を書き換え、画像は `tools/recolor_character.py` で生成する。

---

## デフォルトで入っている演出（テンプレート標準）

`template.html` から作れば、以下は自動で付く：

- **手描き風の揺らぎ（boil）** — 輪郭が微妙にコマ揺れ（SVG feTurbulence）
- **ぴょん（tap bounce）** — タップで上に跳ねる springy アニメ
- **カラーネーム flash** — タップごとに名前がぱっと出てフェードアウト（Hiragino bold / 黄影）
- **クリーム背景 `#F2EDE2`**、サイズ `min(94vmin,680px)`
- **TAP HERE**（初回のみ。タップで消える）
- **image方式は全色プリロード** → タップ即時切替（遅延なし）
- `prefers-reduced-motion` でアニメ自動オフ

---

## 1. キャラごとに用意するもの

| 項目 | 内容 |
|------|------|
| **元アート** | キャラの線画+塗り。`.ai` か透過/白背景 PNG。**顔アップ・はっきりした塗り**が映える |
| 表示名 | 例: `PUTTI` |
| 体の基準色 | 例: 黄=57° / 赤=0° / 青=211°（省略で自動検出も可） |
| Shopify情報 | 商品URL + 6色 variant ID（無ければ購入ボタンは自動で非表示） |

---

## 2. 画像生成（体だけ色変え＝5色POPを保証）

**重要な設計**：画像全体を回転させると青などで歯・羽・舌まで同化して暗くなる。
そこで **体（メインの色域）だけを各色へ回転し、歯/舌/口/羽/目/輪郭は元色のまま残す**。
これで全6色で「体＋元の鮮やかな別パーツ」の5色構成が常に維持される。

```bash
# .ai は先に高解像度PNGへ
qlmanage -t -s 1200 -o /tmp/ "/path/to/DR_アクキーxxx.ai"

# 6色バリアントを生成（透過版=COLOR TAP / 白背景版=ショップ）
python3 tools/recolor_character.py \
  --key xxx \
  --src /tmp/DR_アクキーxxx.ai.png \
  --base-hue 57 \                # 省略で自動検出
  --shop-dir /Users/KCL/charamarl/img/colors_nobg
```

出力:
- `art/colors/xxx_{red,yellow,green,cyan,blue,pink}.png`（透過・COLOR TAP用）
- `<shop-dir>/xxx_{...}.png`（白背景・CHARAMARLショップ用）

> 体の色域がうまく取れない時は `--win`（±度, 既定25）を調整。
> 特定パーツも一緒に変えたい/特定色だけ明るくしたい等は要相談（個別調整可）。

---

## 3. COLOR TAP ページを作る

```bash
cp template.html xxx.html
```

`xxx.html` の CONFIG を編集：

```js
const CONFIG = {
  character: "XXX",
  mode: "image",                 // 通常はこれ（事前生成PNGを切替）
  imageDir: "art/colors",
  imageKey: "xxx",
  baseImage: "art/colors/xxx_red.png",
  bg: "#F2EDE2",
  palettes: [ /* 既定のままでOK（key=red..pink） */ ],
  shop: { productUrl: "...", variants: { /* variant ID */ } },
};
```

### mode の使い分け
| mode | 用途 |
|------|------|
| `image` | **既定**。事前生成PNGを切替（最も正確・5色POP） |
| `char`  | 全身が黒系で本体が色を持たないキャラ（GMC等）。アクセントだけ hue-rotate |
| `bg`    | 背景の色を変える（全身真っ黒キャラ向け） |

---

## 4. デプロイ＆連携

- このリポジトリに置けば `dinorenny-colortap.vercel.app/xxx.html` が自動で生える
- CHARAMARL 側のそのキャラの「🎨 Color Tap」リンクを上記URLに設定
- 商品化が決まったら CONFIG.shop に Shopify情報を入れる（購入ボタンが自動表示）
