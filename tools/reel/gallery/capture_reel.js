// reel.html を1tickずつ進めて 30fps のJPGに書き出す。使い方: node capture_reel.js <秒> <出力dir>
// 実行は tools/reel (playwright の node_modules があるところ) から: node /path/capture_reel.js 7 /path/frames
const path = require('path');
const { chromium } = require(path.join('/Users/KCL/dinorenny-colortap/tools/reel/node_modules/playwright'));
const fs = require('fs'); const http = require('http');
(async () => {
  const secs = +(process.argv[2] || 7), out = process.argv[3] || 'frames'; fs.mkdirSync(out, { recursive:true });
  const root = __dirname;
  // 簡易静的サーバー(fetch('cards.json') が file:// だと動かないため)
  const mime = { '.html':'text/html', '.json':'application/json', '.jpg':'image/jpeg', '.png':'image/png' };
  const srv = http.createServer((req, res) => { const p = path.join(root, decodeURIComponent(req.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e){ res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); res.end(d); }); }).listen(0);
  const port = srv.address().port;
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport:{ width:1080, height:1920 }, deviceScaleFactor:1 });
  page.on('pageerror', e => console.log('pageerror', e.message));
  await page.goto(`http://127.0.0.1:${port}/reel.html`, { waitUntil:'networkidle' });
  await page.waitForFunction(() => window.REEL_READY === true, null, { timeout:60000 });
  let saved = 0;
  for (let f = 0; f < secs * 60; f++){
    await page.evaluate(() => { window.REEL.tick(); window.REEL.draw(); });
    if (f % 2 === 0){ const b64 = await page.evaluate(() => document.getElementById('cv').toDataURL('image/jpeg', .93)); fs.writeFileSync(`${out}/f_${String(saved).padStart(4,'0')}.jpg`, Buffer.from(b64.split(',')[1], 'base64')); saved++; }
  }
  console.log('saved', saved); await browser.close(); srv.close();
})();
