// ゲームを1フレームずつ進めて描画を書き出す(60fpsで進め、2枚に1枚を保存→30fps)。使い方: node capture.js <char> <秒> [ゲームURL]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const char = process.argv[2] || 'sue', secs = +(process.argv[3] || 11), base = process.argv[4] || 'https://charamarl.com/run.html';
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport:{ width:1100, height:720 }, deviceScaleFactor:2 });
  page.on('pageerror', e => console.log('pageerror', e.message));
  await page.goto(`${base}?char=${char}&internal=1`, { waitUntil:'networkidle' });
  await page.waitForFunction(() => window.DRRUN && document.fonts && document.fonts.status === 'loaded'); await page.waitForTimeout(500);
  await page.evaluate(() => {
    const D = window.DRRUN; D.start(); D.S.nextStar = 150;
    window.__bot = () => {
      const S = D.S, d = D.dino, G = 248, o = D.obstacles;
      if (S.fly > 0){ S.hold = d.y > 150; const b = o.find(x => x.type==='bird' && x.x > d.x - 40 && x.x - d.x < 180); if (b) S.hold = b.y > 150; return; }
      const near = o.find(x => x.x + x.w > d.x && x.x - d.x < 150); const st = D.star && D.star.x > d.x + 40 && D.star.x - d.x < 100;
      d.duck = false;
      if (near){ if (near.type === 'bird' && near.y <= G - 78){ if (d.onGround) d.duck = true; } else if (d.onGround) D.jump(); }
      else if (st && d.onGround) D.jump();
    };
  });
  let saved = 0;
  for (let f = 0; f < secs * 60; f++){
    const st = await page.evaluate(() => { window.__bot(); if (DRRUN.S.state === 'play') DRRUN.step(1); DRRUN.draw(); return DRRUN.S.state; });
    if (f % 2 === 0){ const b64 = await page.evaluate(() => document.getElementById('game').toDataURL('image/jpeg', .92)); fs.writeFileSync(`frames/g_${String(saved).padStart(4,'0')}.jpg`, Buffer.from(b64.split(',')[1], 'base64')); saved++; }
    if (st !== 'play'){ console.log('game over at frame', f); break; }
  }
  console.log('saved', saved); await browser.close();
})();
