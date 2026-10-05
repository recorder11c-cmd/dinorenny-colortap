# CHARA MODE(★1個目でON: COMBO/FEVER/紙吹雪/虹、★2個目で二段ジャンプ)を run.html 系に当てる。使い方: python3 chara_mode_patch.py <file> [owner]
import sys
p=sys.argv[1]; has_owner=len(sys.argv)>2 and sys.argv[2]=='owner'
s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(p,s.count(a),a[:80]); s=s.replace(a,b)
assert 'CHARA MODE' not in s, 'already patched'
rep("  .ttl span{color:var(--accent);}",
"""  .ttl span{color:var(--accent);}
  .bgfx{position:fixed;inset:0;z-index:0;pointer-events:none;background:linear-gradient(120deg,#FF3EA5,#FFE000,#00D4FF,#7FE000,#FF7A00,#FF3EA5);background-size:400% 400%;animation:bgcycle 5s linear infinite;opacity:0;mix-blend-mode:multiply;transition:opacity .6s;}
  body.dopaon .bgfx{opacity:.5;}
  @keyframes bgcycle{0%{background-position:0% 0%}100%{background-position:100% 100%}}
  .wrap{position:relative;z-index:1;}
  body.fever .chip{animation:feverchip .4s ease-in-out infinite;background:linear-gradient(135deg,#FFE27A,#FF3EA5);}
  @keyframes feverchip{0%,100%{transform:scale(1)}50%{transform:scale(1.08) rotate(-2deg)}}""")
rep('<body>\n<div class="wrap">','<body>\n<div class="bgfx"></div>\n<div class="wrap">')
rep("<span>ライバルをかわすと +10</span>","<span>ライバルをかわすと +10</span>\n    <span>★1個目で CHARA MODE（かわすと全部COMBO・5コンボでFEVER 点2倍）、2個目で 二段ジャンプ 解放</span>")
rep("  const DODGE_BONUS = 10;      // ライバルをかわしたときのボーナス点",
"""  const DODGE_BONUS = 10;      // ライバルをかわしたときのボーナス点
  // CHARA MODE: ★1個目でON(COMBO/FEVER/紙吹雪/虹)、2個目で二段ジャンプ解放
  const DOPA = { on:false, dj:false, burgers:0, combo:0, fever:false, flash:0, zoom:0, pop:0 };
  const RB = ['#FF3EA5','#FFE000','#00D4FF','#7FE000','#FF7A00','#fff','#B266FF'];
  const hue = (o=0) => `hsl(${(S.t*7 + o) % 360},100%,60%)`;
  function setFever(on){ DOPA.fever = on; document.body.classList.toggle('fever', on); }
  function setDopa(on){ DOPA.on = on; document.body.classList.toggle('dopaon', on); }""")
rep("    S.state = 'play'; S.t = 0; S.speed = 6;", "    DOPA.burgers = 0; DOPA.combo = 0; DOPA.dj = false; DOPA.flash = 0; DOPA.zoom = 0; setFever(false); setDopa(false); dino.dj = false;\n    S.state = 'play'; S.t = 0; S.speed = 6;")
if has_owner:
    rep("    S.state = 'over'; S.shake = 14; if (!isOwner) S.goldPreview = 240;", "    S.state = 'over'; S.shake = DOPA.on ? 30 : 14; if (DOPA.on){ DOPA.flash = 22; burst(dino.x + dino.size*.5, dino.y - dino.size*.5, 120, RB); } setFever(false); if (!isOwner) S.goldPreview = 240;")
    rep("      dino.vy = (dino.duck ? -15 : -16.5) * T.jump; dino.onGround = false; dino.duck = false; dino.dj = false;\n      beep(520, .14, 'square', .05, 260);\n      burst(dino.x + dino.size*.6, GROUND, 8, ['#fff', '#FFD400']);\n    } else if (ownerMode && !dino.dj){",
        "      dino.vy = (dino.duck ? -15 : -16.5) * T.jump; dino.onGround = false; dino.duck = false; dino.dj = false;\n      beep(520, .14, 'square', .05, 260);\n      if (DOPA.on){ burst(dino.x + dino.size*.6, GROUND, 26, RB); S.shake = Math.max(S.shake, 4); } else burst(dino.x + dino.size*.6, GROUND, 8, ['#fff', '#FFD400']);\n    } else if ((ownerMode || DOPA.dj) && !dino.dj){")
    rep("if (dino.y >= GROUND){ if(!dino.onGround){ dino.squash = 1; burst(dino.x + dino.size*.4, GROUND, 6, ['#fff','#1B1B1F']); } dino.y = GROUND; dino.vy = 0; dino.onGround = true; dino.dj = false; }",
        "if (dino.y >= GROUND){ if(!dino.onGround){ dino.squash = 1; if (DOPA.on){ burst(dino.x + dino.size*.4, GROUND, 30, RB); S.shake = Math.max(S.shake, 7); } else burst(dino.x + dino.size*.4, GROUND, 6, ['#fff','#1B1B1F']); } dino.y = GROUND; dino.vy = 0; dino.onGround = true; dino.dj = false; }")
    rep("if (hit(db, ob)){ S.fly = 0; S.grace = T.grace; S.shake = 8; endGoldFly();", "if (hit(db, ob)){ S.fly = 0; S.grace = T.grace; S.shake = DOPA.on ? 14 : 8; DOPA.combo = 0; setFever(false); endGoldFly();")
    rep("        flashes.push({ text: ownerMode ? `GOLD ★ FLY ${flySec}s!` : `FLY ${flySec}s!`, life:80 }); burst(dino.x + dino.size*.5, dino.y - dino.size*.5, 40, ['#FFE000','#fff','#FF3EA5','#00D4FF']);",
"""        DOPA.burgers++;
        if (DOPA.burgers === 1){ setDopa(true); DOPA.flash = 14; DOPA.zoom = 16; S.shake = Math.max(S.shake, 12); flashes.push({ text:'⚡ CHARA MODE ON!! ⚡', life:100, big:true }); burst(W*.5, H*.5, 160, RB); [0,80,160,240,320,400].forEach((d,i) => setTimeout(() => beep(500 + i*120, .1, 'square', .07), d)); }
        else if (DOPA.burgers === 2){ DOPA.dj = true; DOPA.flash = 12; DOPA.zoom = 14; flashes.push({ text:'二段ジャンプ 解放!!', life:90, big:true }); burst(W*.5, H*.5, 120, RB); }
        else { DOPA.flash = 10; DOPA.zoom = 10; }
        flashes.push({ text: ownerMode ? `GOLD ★ FLY ${flySec}s!` : `FLY ${flySec}s!`, life:80, big:DOPA.on }); burst(dino.x + dino.size*.5, dino.y - dino.size*.5, DOPA.on ? 120 : 40, DOPA.on ? RB : ['#FFE000','#fff','#FF3EA5','#00D4FF']);""")
    rep("    if (isOwner || S.fly > 0){ ctx.shadowColor = S.fly > 0 ? 'rgba(255,255,255,.95)' : 'rgba(255,200,0,.95)'; ctx.shadowBlur = 22; }",
        "    if (isOwner || S.fly > 0 || DOPA.fever){ ctx.shadowColor = DOPA.fever ? hue() : S.fly > 0 ? 'rgba(255,255,255,.95)' : 'rgba(255,200,0,.95)'; ctx.shadowBlur = DOPA.fever ? 30 : 22; }")
    rep("      if (isOwner || S.fly > 0){ ctx.shadowBlur = 0; ctx.drawImage(sprite.canvas, -s*.5, -s*.96, s, s); }", "      if (isOwner || S.fly > 0 || DOPA.fever){ ctx.shadowBlur = 0; ctx.drawImage(sprite.canvas, -s*.5, -s*.96, s, s); }")
    rep("window.DRRUN = { S, dino, step, draw, start, jump, CHAR,", "window.DRRUN = { S, dino, step, draw, start, jump, CHAR, DOPA,")
else:
    rep("    S.state = 'over'; S.shake = 14;", "    S.state = 'over'; S.shake = DOPA.on ? 30 : 14; if (DOPA.on){ DOPA.flash = 22; burst(dino.x + dino.size*.5, dino.y - dino.size*.5, 120, RB); } setFever(false);")
    rep("""    if (dino.onGround){
      dino.vy = (dino.duck ? -15 : -16.5) * T.jump; dino.onGround = false; dino.duck = false;
      beep(520, .14, 'square', .05, 260);
      burst(dino.x + dino.size*.6, GROUND, 8, ['#fff', '#FFD400']);
    }""",
"""    if (dino.onGround){
      dino.vy = (dino.duck ? -15 : -16.5) * T.jump; dino.onGround = false; dino.duck = false; dino.dj = false;
      beep(520, .14, 'square', .05, 260);
      if (DOPA.on){ burst(dino.x + dino.size*.6, GROUND, 26, RB); S.shake = Math.max(S.shake, 4); } else burst(dino.x + dino.size*.6, GROUND, 8, ['#fff', '#FFD400']);
    } else if (DOPA.dj && !dino.dj){   // 二段ジャンプ(★2個目で解放)
      dino.dj = true; dino.vy = -13.5 * T.jump;
      beep(700, .12, 'square', .05, 320);
      burst(dino.x + dino.size*.5, dino.y - dino.size*.35, 16, RB);
      flashes.push({ text:'二段ジャンプ！', life:30, small:true });
    }""")
    rep("if (dino.y >= GROUND){ if(!dino.onGround){ dino.squash = 1; burst(dino.x + dino.size*.4, GROUND, 6, ['#fff','#1B1B1F']); } dino.y = GROUND; dino.vy = 0; dino.onGround = true; }",
        "if (dino.y >= GROUND){ if(!dino.onGround){ dino.squash = 1; if (DOPA.on){ burst(dino.x + dino.size*.4, GROUND, 30, RB); S.shake = Math.max(S.shake, 7); } else burst(dino.x + dino.size*.4, GROUND, 6, ['#fff','#1B1B1F']); } dino.y = GROUND; dino.vy = 0; dino.onGround = true; dino.dj = false; }")
    rep("if (hit(db, ob)){ S.fly = 0; S.grace = T.grace; S.shake = 8;", "if (hit(db, ob)){ S.fly = 0; S.grace = T.grace; S.shake = DOPA.on ? 14 : 8; DOPA.combo = 0; setFever(false);")
    rep("        flashes.push({ text:`FLY ${flySec}s!`, life:80 }); burst(dino.x + dino.size*.5, dino.y - dino.size*.5, 40, ['#FFE000','#fff','#FF3EA5','#00D4FF']);",
"""        DOPA.burgers++;
        if (DOPA.burgers === 1){ setDopa(true); DOPA.flash = 14; DOPA.zoom = 16; S.shake = Math.max(S.shake, 12); flashes.push({ text:'⚡ CHARA MODE ON!! ⚡', life:100, big:true }); burst(W*.5, H*.5, 160, RB); [0,80,160,240,320,400].forEach((d,i) => setTimeout(() => beep(500 + i*120, .1, 'square', .07), d)); }
        else if (DOPA.burgers === 2){ DOPA.dj = true; DOPA.flash = 12; DOPA.zoom = 14; flashes.push({ text:'二段ジャンプ 解放!!', life:90, big:true }); burst(W*.5, H*.5, 120, RB); }
        else { DOPA.flash = 10; DOPA.zoom = 10; }
        flashes.push({ text:`FLY ${flySec}s!`, life:80, big:DOPA.on }); burst(dino.x + dino.size*.5, dino.y - dino.size*.5, DOPA.on ? 120 : 40, DOPA.on ? RB : ['#FFE000','#fff','#FF3EA5','#00D4FF']);""")
    rep("    if (isOwner || S.fly > 0){ ctx.shadowColor = S.fly > 0 ? 'rgba(255,255,255,.95)' : 'rgba(255,200,0,.95)'; ctx.shadowBlur = 22; }",
        "    if (isOwner || S.fly > 0 || DOPA.fever){ ctx.shadowColor = DOPA.fever ? hue() : S.fly > 0 ? 'rgba(255,255,255,.95)' : 'rgba(255,200,0,.95)'; ctx.shadowBlur = DOPA.fever ? 30 : 22; }")
    rep("      if (isOwner || S.fly > 0){ ctx.shadowBlur = 0; ctx.drawImage(sprite.canvas, -s*.5, -s*.96, s, s); }", "      if (isOwner || S.fly > 0 || DOPA.fever){ ctx.shadowBlur = 0; ctx.drawImage(sprite.canvas, -s*.5, -s*.96, s, s); }")
    rep("window.DRRUN = { S, dino, step, draw, start, jump, get obstacles()", "window.DRRUN = { S, dino, step, draw, start, jump, DOPA, get obstacles()")
# 共通
rep("      if (o.type !== 'bird' || o.passed) return;", "      if (o.passed || (!DOPA.on && o.type !== 'bird')) return;")
rep("      if (passed){ o.passed = true; S.dist += DODGE_BONUS / 1; S.dodges = (S.dodges || 0) + 1; flashes.push({ text:'かわした！ +' + DODGE_BONUS, life:35, small:true }); beep(740, .08, 'triangle', .04); }",
"""      if (passed && !DOPA.on){ o.passed = true; S.dist += DODGE_BONUS / 1; S.dodges = (S.dodges || 0) + 1; flashes.push({ text:'かわした！ +' + DODGE_BONUS, life:35, small:true }); beep(740, .08, 'triangle', .04); }
      else if (passed){ o.passed = true; DOPA.combo++; const bonus = DODGE_BONUS * Math.min(DOPA.combo, 10); S.dist += bonus; S.dodges = (S.dodges || 0) + 1;
        flashes.push({ text:`+${bonus}`, life:28, small:true }); DOPA.pop = 14; S.shake = Math.max(S.shake, 4);
        burst(dino.x + dino.size*.5, dino.y - dino.size*.5, 24, RB);
        beep(440 + Math.min(DOPA.combo, 12)*70, .08, 'square', .05); setTimeout(() => beep(660 + Math.min(DOPA.combo, 12)*70, .1, 'square', .05), 70);
        if (DOPA.combo === 5){ setFever(true); DOPA.flash = 10; DOPA.zoom = 12; flashes.push({ text:'FEVER!! 点2倍', life:60, big:true }); burst(W*.5, H*.5, 120, RB); [0,90,180,270,360].forEach((d,i) => setTimeout(() => beep(600 + i*140, .12, 'square', .07), d)); }
      }""")
rep("      burst(W*.5, 90, 40, ['#FF3EA5','#00D4FF','#FFE000','#7FE000','#FF7A00','#fff']);", "      if (DOPA.on){ DOPA.zoom = 10; DOPA.flash = 6; S.shake = Math.max(S.shake, 6); burst(W*.5, 90, 90, RB); } else burst(W*.5, 90, 40, ['#FF3EA5','#00D4FF','#FFE000','#7FE000','#FF7A00','#fff']);")
rep("    S.dist += S.speed * dt * .03 * (S.fly > 0 ? FLY_MULT : 1);", "    S.dist += S.speed * dt * .03 * (S.fly > 0 ? FLY_MULT : 1) * (DOPA.fever ? 2 : 1);")
rep("    particles.forEach(p => { p.x += p.vx*dt; p.y += p.vy*dt; p.vy += .25*dt; p.life -= dt; });",
"""    if (S.state === 'play' && DOPA.on){
      particles.push({ x:dino.x + dino.size*.25, y:dino.y - dino.size*.5 + (Math.random()-.5)*50, vx:-DIR*(3+Math.random()*3), vy:(Math.random()-.5)*1.5, life:26, c:hue(Math.random()*120), r:3+Math.random()*4 });
      if (DOPA.fever){ for (let i=0;i<2;i++) particles.push({ x:Math.random()*W, y:-10, vx:(Math.random()-.5)*2, vy:2+Math.random()*3, life:110, c:RB[Math.floor(Math.random()*RB.length)], r:3+Math.random()*4 }); }
    }
    if (DOPA.flash > 0) DOPA.flash -= dt; if (DOPA.zoom > 0) DOPA.zoom -= dt; if (DOPA.pop > 0) DOPA.pop -= dt;
    particles.forEach(p => { p.x += p.vx*dt; p.y += p.vy*dt; p.vy += (p.life > 100 ? .02 : .25)*dt; p.life -= dt; });""")
rep("    if (S.shake > 0) ctx.translate((Math.random()-.5)*S.shake, (Math.random()-.5)*S.shake);\n",
    "    if (S.shake > 0) ctx.translate((Math.random()-.5)*S.shake, (Math.random()-.5)*S.shake);\n    if (DOPA.zoom > 0){ const z = 1 + DOPA.zoom * .003; ctx.translate(W*.5, H*.5); ctx.scale(z, z); ctx.translate(-W*.5, -H*.5); }\n")
rep("    // 太陽\n",
"""    if (DOPA.fever){ ctx.save(); ctx.globalAlpha = .45; for (let i = 0; i < 7; i++){ ctx.fillStyle = hue(i*51); ctx.fillRect(-20, -20 + i*(GROUND+20)/7, W+40, (GROUND+20)/7 + 2); } ctx.restore(); }
    if (DOPA.on && S.state === 'play' && S.speed > 7.5){ ctx.save(); ctx.globalAlpha = Math.min(.6, (S.speed-7)*.12); ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; for (let i = 0; i < 14; i++){ const y = (i*53 + S.t*3) % GROUND, x = (i*131 + S.t*S.speed*5) % (W+200) - 100; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 60 + S.speed*8, y); ctx.stroke(); } ctx.restore(); }
    // 太陽
""")
rep("      const a = Math.min(1, f.life/25), sc = f.small ? 1 : 1 + (1 - Math.min(1, (70 - f.life)/10))*.6;",
    "      const a = Math.min(1, f.life/25), sc = (f.small || f.big) ? 1 : 1 + (1 - Math.min(1, (70 - f.life)/10))*.6;")
rep("ctx.translate(f.small ? dino.x + dino.size*.5 : W*.5, f.small ? dino.y - dino.size - 10 : 92);", "ctx.translate(f.small ? dino.x + dino.size*.5 : W*.5, f.small ? dino.y - dino.size - 10 : (f.big ? 58 : 92));")
rep("ctx.font = f.small ? '900 16px \"M PLUS Rounded 1c\", sans-serif' : '900 34px \"M PLUS Rounded 1c\", sans-serif';", "ctx.font = f.small ? '900 16px \"M PLUS Rounded 1c\", sans-serif' : (f.big ? '900 24px \"M PLUS Rounded 1c\", sans-serif' : '900 34px \"M PLUS Rounded 1c\", sans-serif');")
rep("      ctx.fillStyle = '#FFE000'; ctx.fillText(f.text, 0, 0);\n      ctx.restore();\n    });",
"""      ctx.fillStyle = f.big ? hue(f.life*9) : '#FFE000'; ctx.fillText(f.text, 0, 0);
      ctx.restore();
    });
    if (DOPA.on && S.state === 'play' && DOPA.combo >= 2){ ctx.save(); ctx.font = '900 22px "M PLUS Rounded 1c", sans-serif'; ctx.textAlign = 'left'; ctx.textBaseline = 'top'; ctx.lineWidth = 6; ctx.strokeStyle = '#1B1B1F'; const t = `${DOPA.fever ? 'FEVER ' : ''}COMBO ×${DOPA.combo}`; const ps = 1 + Math.max(0, DOPA.pop)/14*.5; ctx.translate(14, 12); ctx.scale(ps, ps); ctx.strokeText(t, 0, 0); ctx.fillStyle = hue(); ctx.fillText(t, 0, 0); ctx.restore(); }
    if (DOPA.flash > 0){ ctx.save(); ctx.globalAlpha = Math.min(.45, DOPA.flash/26); ctx.fillStyle = '#fff'; ctx.fillRect(-40, -40, W+80, H+80); ctx.restore(); }""")
rep("    ctx.save(); ctx.translate(cx, cy); ctx.rotate(f*.08); ctx.scale(1, 1 - Math.abs(f)*.08);", "    ctx.save(); ctx.translate(cx, cy); ctx.rotate(DOPA.on ? o.flap*1.3 : f*.08); ctx.scale(1, 1 - Math.abs(f)*.08);")
open(p,'w',encoding='utf-8').write(s); print('patched',p)
