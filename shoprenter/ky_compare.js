// Sandbox ↔ GitHub-demó összevetés a böngészőben: mindkét oldalt azonos szélességű iframe-be tölti, és elemenként összeveti a számított stílusokat.
window.kyCmp = async function (srPath, demoPath, width, opts) {
  opts = opts || {};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const mk = () => { const f = document.createElement('iframe'); f.style.cssText = 'position:absolute;left:-40000px;top:0;border:0;height:1200px;width:' + width + 'px'; document.body.appendChild(f); return f; };
  const a = mk(), b = mk();
  const html = await (await fetch('https://stratoswebdesign.github.io/kontyos/' + demoPath + '?t=' + Date.now())).text();
  const base = 'https://stratoswebdesign.github.io/kontyos/' + demoPath.replace(/[^/]*$/, '');
  await new Promise(r => { a.onload = r; a.srcdoc = html.replace('<head>', '<head><base href="' + base + '">'); });
  await new Promise(r => { b.onload = r; b.src = srPath; });
  await sleep(1500);
  // friss kontyos.css a sandbox-iframe-ben
  const bd = b.contentDocument, l = bd.querySelector('link[href*="kontyos.css"]');
  if (l) await new Promise(r => { const n = bd.createElement('link'); n.rel = 'stylesheet'; n.href = l.href.split('?')[0] + '?x=' + Date.now(); n.onload = r; n.onerror = r; l.after(n); l.remove(); });
  await sleep(800);
  [a, b].forEach(f => { const d = f.contentDocument; d.querySelectorAll('.demo-bar').forEach(e => e.remove()); });
  const P = ['display', 'position', 'float', 'fontSize', 'fontFamily', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing', 'textTransform', 'marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'color', 'backgroundColor', 'backgroundImage', 'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderRadius', 'boxShadow', 'flexDirection', 'flexWrap', 'justifyContent', 'alignItems', 'gap', 'gridTemplateColumns', 'opacity', 'transform', 'textDecorationLine', 'listStyleType', 'verticalAlign', 'boxSizing', 'overflow', 'zIndex', 'objectFit', 'whiteSpace', 'cursor', 'visibility'];
  if (opts.skip) opts.skip.forEach(k => { const i = P.indexOf(k); if (i > -1) P.splice(i, 1); });
  const sig = (doc, root) => [...root.querySelectorAll('*')].filter(e => !/^(SCRIPT|STYLE|svg|path|g|circle|rect|line|polyline|polygon|use|defs|symbol|ellipse|text|tspan|clipPath|mask|linearGradient|stop)$/i.test(e.tagName)).map(e => { const c = doc.defaultView.getComputedStyle(e); return { t: e.tagName + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 3).join('.') : ''), p: P.map(k => c[k]), w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height) }; });
  const rootsA = [a.contentDocument.querySelector('.site-head'), a.contentDocument.querySelector('body > main'), a.contentDocument.querySelector('footer')];
  const rootsB = [b.contentDocument.querySelector('.ky-head .site-head'), b.contentDocument.querySelector('.ky > main'), b.contentDocument.querySelector('.ky-foot footer')];
  const out = [];
  ['head', 'main', 'foot'].forEach((nm, i) => {
    if (!rootsA[i] || !rootsB[i]) { out.push(nm + ': MISSING ' + !!rootsA[i] + '/' + !!rootsB[i]); return; }
    const A = sig(a.contentDocument, rootsA[i]), B = sig(b.contentDocument, rootsB[i]);
    if (A.length !== B.length) out.push(nm + ': count ' + A.length + ' vs ' + B.length);
    const seen = new Set(); let n = 0;
    for (let j = 0; j < Math.min(A.length, B.length) && n < (opts.max || 25); j++) {
      if (A[j].t.split('.')[0] !== B[j].t.split('.')[0]) { out.push(nm + ' STRUCT@' + j + ' ' + A[j].t + ' | ' + B[j].t); break; }
      const nv = v => String(v).replace(/\?v=[0-9a-f]+/g, '');
      const d = P.map((k, q) => nv(A[j].p[q]) !== nv(B[j].p[q]) ? k + ':' + A[j].p[q] + '→' + B[j].p[q] : null).filter(Boolean);
      const dw = Math.abs(A[j].w - B[j].w) > 2 ? 'w' + A[j].w + '→' + B[j].w : '', dh = Math.abs(A[j].h - B[j].h) > 2 ? 'h' + A[j].h + '→' + B[j].h : '';
      if (d.length || (opts.size && (dw || dh))) { const key = A[j].t + d.join(); if (seen.has(key)) continue; seen.add(key); out.push(nm + '#' + j + ' ' + A[j].t.slice(0, 50) + ' :: ' + d.join(' ; ').slice(0, 260) + (opts.size ? ' ' + dw + ' ' + dh : '')); n++; }
    }
  });
  // keret: dokumentum-magasság, fejléc/logó/lábléc helye (a .ky-n kívüli Shoprenter-sávok kiszűrésére)
  const R = (doc, sel) => { const e = doc.querySelector(sel); if (!e) return 'none'; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top + doc.defaultView.scrollY), Math.round(r.width), Math.round(r.height)].join(','); };
  const da = a.contentDocument, db = b.contentDocument;
  const fr = [['doc', 'html', 'html'], ['head', '.site-head', '.ky-head .site-head'], ['logo', '.site-head .logo', '.ky-head .site-head .logo'], ['main', 'body > main', '.ky > main'], ['foot', 'footer', '.ky-foot footer']];
  const ha = da.documentElement.scrollHeight, hb = db.documentElement.scrollHeight;
  if (Math.abs(ha - hb) > 2) out.unshift('DOC height ' + ha + '→' + hb);
  fr.slice(1).forEach(([n, sa, sb]) => { const x = R(da, sa), y = R(db, sb); if (x !== y) out.unshift('RECT ' + n + ' ' + x + '→' + y); });
  // a lábléc alatt / fejléc fölött maradó idegen sáv
  const fb = db.querySelector('.ky-foot footer'); if (fb) { const gap = hb - (fb.getBoundingClientRect().bottom + db.defaultView.scrollY); if (gap > 1) out.unshift('BELOW-FOOTER gap ' + Math.round(gap)); }
  window.kyLast = { a, b };
  a.remove(); b.remove();
  return out;
};
'kyCmp ready';
