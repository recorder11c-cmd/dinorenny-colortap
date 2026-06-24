# COLOR TAP 統一フォーマット

新しいキャラクターの COLOR TAP を量産するための共通仕様です。
`template.html` をコピーして、先頭の `CONFIG` を書き換えるだけで完成します。

---

## 1. キャラごとに提供してもらう素材

| 項目 | 内容 | 備考 |
|------|------|------|
| **キーアートPNG** | 透過・正方形・**1080×1080px** 推奨 | SUEと同じ「顔アップ」スタイル。背景は透過 |
| **表示名** | 例: `PUTTI` / `MOSSUN` | 英字 |
| **背景色** | 例: `#4466ff` | 省略時は青 |
| **Shopify情報**（任意） | 商品URL ＋ 6色分の variant ID | 無ければ購入ボタンは商品トップへ |

> キーアートは「顔アップ・線がはっきり・彩度高め」が COLOR TAP 映えします。
> 既存の `art/sue.png` が参考サンプルです。

---

## 2. 新キャラの作り方（3ステップ）

```bash
# 1. テンプレートを複製
cp template.html putti.html

# 2. 素材を art/ に置く
#    art/putti.png

# 3. putti.html の CONFIG を編集
```

```js
const CONFIG = {
  character: "PUTTI",
  baseImage: "art/putti.png",
  bg: "#4466ff",
  baseHueOffset: -50,        // ← ベース色相補正（下記）
  palettes: [ ...6色（共通でOK） ],
  shop: { productUrl: "...", variants: { ... } }
};
```

---

## 3. baseHueOffset（色ズレ補正）の決め方

6色パレットは **赤ベース** を基準に作られています。
キャラの地色が赤以外だと色がズレるので、`baseHueOffset` で全体を回します。

| キャラの地色 | 目安オフセット |
|------------|--------------|
| 赤（SUE）   | `0`   |
| 黄（PUTTI） | `-50` |
| 青（MOSSUN）| `-210`（=+150）|

提供素材を見て最終調整します（自動検出も可能）。

---

## 4. デプロイ

`dinorenny-colortap.vercel.app/putti.html` のように、
このリポジトリに置けば各キャラのURLが自動で生える。

CHARAMARL 側の各キャラの「🎨 Color Tap」ボタンのリンク先を
そのURLに差し替えれば連携完了。
