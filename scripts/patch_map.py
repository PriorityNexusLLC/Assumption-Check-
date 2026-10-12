#!/usr/bin/env python3
"""One-off: replace the illustrative night sky in index.html with the real graph.

The old map placed entries on a spiral (positions meant nothing) and padded the
canvas with seventeen invented stars. This swaps it for a layout computed from
the registry's own links, with no invented data in it.

Run once; the result is committed. Kept in the repo so the change is auditable.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

NEW_SKY = r'''  // --- the map: every node and every line comes from the registry ---
  (function () {
    const canvas = document.getElementById("skyCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const C = {
      amber: "#ffd24a", blue: "#6bb0ef", green: "#4fe0ad",
      red: "#ef6f63", violet: "#b592f0", slate: "#8e9ab8"
    };

    // Nodes are entries. Colour is the claim's state; an entry with no
    // hypothesis yet is slate, not amber — "no testable form found" must not
    // look like "popular but untested".
    const nodes = entries.map(e => ({
      entry: e,
      colour: e.contested ? "violet" : (e.hypothesis ? e.hypothesis.star : "slate"),
      label: "Entry " + e.num + " — " + e.title.replace(/<[^>]+>/g, ""),
      x: 0, y: 0, vx: 0, vy: 0, deg: 0
    }));
    const byNum = {};
    nodes.forEach(n => { byNum[n.entry.num] = n; });

    // Two kinds of edge. A dependency is a hard tie; a shared field is a soft
    // one, and is only drawn when the field is specific — a field holding most
    // of the registry says nothing about any particular pair.
    const fieldCount = {};
    nodes.forEach(n => (n.entry.fields || []).forEach(f => {
      fieldCount[f] = (fieldCount[f] || 0) + 1;
    }));
    const edges = [];
    const seen = new Set();
    nodes.forEach(n => (n.entry.restsOn || []).forEach(num => {
      const t = byNum[num];
      if (!t) return;
      const key = [n.entry.num, num].sort().join("-") + ":dep";
      if (seen.has(key)) return;
      seen.add(key);
      edges.push({ a: n, b: t, kind: "dep" });
    }));
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const shared = (a.entry.fields || []).filter(
          f => (b.entry.fields || []).includes(f) && fieldCount[f] <= 3);
        if (!shared.length) continue;
        const key = [a.entry.num, b.entry.num].sort().join("-") + ":field";
        if (seen.has(key)) continue;
        seen.add(key);
        edges.push({ a, b, kind: "field", via: shared[0] });
      }
    }
    edges.forEach(e => { e.a.deg++; e.b.deg++; });

    // A fixed seed, so the same registry always draws the same sky. A map that
    // rearranged itself on every visit could not be referred to.
    let seed = 20261012;
    const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296;
    nodes.forEach((n, i) => {
      const a = i * 2.39996;
      n.x = 0.5 + Math.cos(a) * (0.08 + rnd() * 0.22);
      n.y = 0.5 + Math.sin(a) * (0.08 + rnd() * 0.22);
    });

    // Force layout: linked nodes pull together, every pair pushes apart.
    (function settle() {
      for (let step = 0; step < 420; step++) {
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i + 1; j < nodes.length; j++) {
            const a = nodes[i], b = nodes[j];
            let dx = b.x - a.x, dy = b.y - a.y;
            let d = Math.hypot(dx, dy) || 0.0001;
            const push = 0.00055 / (d * d);
            dx /= d; dy /= d;
            a.vx -= dx * push; a.vy -= dy * push;
            b.vx += dx * push; b.vy += dy * push;
          }
        }
        for (const e of edges) {
          const want = e.kind === "dep" ? 0.17 : 0.3;
          const k = e.kind === "dep" ? 0.014 : 0.005;
          let dx = e.b.x - e.a.x, dy = e.b.y - e.a.y;
          const d = Math.hypot(dx, dy) || 0.0001;
          const f = (d - want) * k;
          dx /= d; dy /= d;
          e.a.vx += dx * f; e.a.vy += dy * f;
          e.b.vx -= dx * f; e.b.vy -= dy * f;
        }
        for (const n of nodes) {
          n.vx += (0.5 - n.x) * 0.0016;
          n.vy += (0.5 - n.y) * 0.0016;
          n.x += n.vx; n.y += n.vy;
          n.vx *= 0.86; n.vy *= 0.86;
          n.x = Math.min(0.93, Math.max(0.07, n.x));
          n.y = Math.min(0.88, Math.max(0.12, n.y));
        }
      }
    })();

    const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const bg = Array.from({ length: 110 }, () => ({
      x: rnd(), y: rnd(), r: rnd() * 1.1 + 0.2, a: rnd() * 0.5 + 0.18, ph: rnd() * 6.283
    }));
    let W = 0, H = 0, raf = null, running = false, hover = null;

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = Math.max(1, W * dpr); canvas.height = Math.max(1, H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function magnitude(n) { return Math.min(10, 4 + 1.7 * n.deg); }
    function near(n) {
      if (!hover) return false;
      if (n === hover) return true;
      return edges.some(e => (e.a === hover && e.b === n) || (e.b === hover && e.a === n));
    }
    function drawSpike(x, y, len, col, a) {
      ctx.save(); ctx.translate(x, y); ctx.globalAlpha = a; ctx.lineWidth = 1;
      for (let k = 0; k < 2; k++) {
        ctx.rotate(k * Math.PI / 2);
        const lg = ctx.createLinearGradient(-len, 0, len, 0);
        lg.addColorStop(0, col + "00"); lg.addColorStop(0.5, col); lg.addColorStop(1, col + "00");
        ctx.strokeStyle = lg;
        ctx.beginPath(); ctx.moveTo(-len, 0); ctx.lineTo(len, 0); ctx.stroke();
      }
      ctx.restore();
    }
    function draw(t) {
      const g = ctx.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, "#070a16"); g.addColorStop(1, "#0e0b1a");
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "lighter";

      for (const s of bg) {
        const tw = reduce ? 0.8 : (0.45 + 0.55 * Math.sin(t * 0.0012 + s.ph));
        ctx.globalAlpha = s.a * tw * 0.6; ctx.fillStyle = "#aab4e0";
        ctx.beginPath(); ctx.arc(s.x * W, s.y * H, s.r, 0, 6.2832); ctx.fill();
      }

      for (const e of edges) {
        const lit = hover && (e.a === hover || e.b === hover);
        const dep = e.kind === "dep";
        ctx.globalAlpha = lit ? 0.85 : (hover ? 0.08 : (dep ? 0.4 : 0.14));
        ctx.strokeStyle = dep ? "#9fb0e8" : "#6d7aa8";
        ctx.lineWidth = dep ? 1.3 : 0.8;
        if (!dep) ctx.setLineDash([3, 4]);
        ctx.beginPath();
        ctx.moveTo(e.a.x * W, e.a.y * H);
        ctx.lineTo(e.b.x * W, e.b.y * H);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      nodes.forEach((n, i) => {
        const col = C[n.colour], mag = magnitude(n), coreR = 1 + mag * 0.35;
        const dim = hover && !near(n) ? 0.22 : 1;
        const tw = reduce ? 0.9 : (0.7 + 0.3 * Math.sin(t * (0.0011 + i * 0.00008) + i * 1.3));
        const x = n.x * W, y = n.y * H, halo = coreR * 7;
        const rg = ctx.createRadialGradient(x, y, 0, x, y, halo);
        rg.addColorStop(0, col); rg.addColorStop(0.18, col + "88"); rg.addColorStop(1, col + "00");
        ctx.globalAlpha = 0.5 * tw * dim; ctx.fillStyle = rg;
        ctx.beginPath(); ctx.arc(x, y, halo, 0, 6.2832); ctx.fill();
        if (mag >= 6) drawSpike(x, y, coreR * (5 + mag * 0.8) * tw, col, 0.4 * tw * dim);
        ctx.globalAlpha = 0.95 * dim;
        const cg = ctx.createRadialGradient(x, y, 0, x, y, coreR * 1.8);
        cg.addColorStop(0, "#ffffff"); cg.addColorStop(0.4, col); cg.addColorStop(1, col + "00");
        ctx.fillStyle = cg;
        ctx.beginPath(); ctx.arc(x, y, coreR * 1.8, 0, 6.2832); ctx.fill();
      });

      ctx.globalCompositeOperation = "source-over";
      ctx.font = '11px "IBM Plex Mono", monospace';
      for (const n of nodes) {
        const dim = hover && !near(n) ? 0.25 : 1;
        ctx.globalAlpha = 0.9 * dim; ctx.fillStyle = "#dfe4f5";
        const lw = ctx.measureText(n.label).width;
        const lx = n.x * W + 14 + lw > W - 8 ? n.x * W - 14 - lw : n.x * W + 14;
        ctx.fillText(n.label, lx, n.y * H + 3);
      }
      if (hover) {
        const links = edges.filter(e => e.a === hover || e.b === hover);
        const deps = links.filter(e => e.kind === "dep").length;
        const flds = links.filter(e => e.kind === "field");
        const bits = [];
        if (deps) bits.push(deps + (deps === 1 ? " dependency" : " dependencies"));
        if (flds.length) bits.push("shares " + [...new Set(flds.map(e => e.via))].join(", "));
        if (!bits.length) bits.push("no connections recorded yet");
        ctx.globalAlpha = 0.95; ctx.fillStyle = "#aab4e0";
        ctx.fillText(bits.join(" · "), 12, H - 12);
      }
      ctx.globalAlpha = 1;
    }
    function loop(t) { draw(t || 0); if (!reduce && running) raf = requestAnimationFrame(loop); }
    window.__sky = {
      start() {
        resize(); running = true;
        if (reduce) { draw(0); }
        else { if (raf) cancelAnimationFrame(raf); raf = requestAnimationFrame(loop); }
      },
      stop() { running = false; if (raf) cancelAnimationFrame(raf); }
    };
    window.addEventListener("resize", () => {
      if (vMap && !vMap.hidden) { resize(); draw(performance.now()); }
    });
    const hit = ev => {
      const r = canvas.getBoundingClientRect(), px = ev.clientX - r.left, py = ev.clientY - r.top;
      return nodes.find(n => Math.hypot(n.x * W - px, n.y * H - py) < 18);
    };
    canvas.addEventListener("mousemove", ev => {
      const n = hit(ev);
      canvas.style.cursor = n ? "pointer" : "default";
      if (n !== hover) { hover = n || null; if (reduce) draw(0); }
    });
    canvas.addEventListener("mouseleave", () => { hover = null; if (reduce) draw(0); });
    canvas.addEventListener("click", ev => { const n = hit(ev); if (n) go(n.entry.id); });
  })();
'''


def main():
    html = io.open(INDEX, encoding="utf-8").read()
    start = html.index("  // --- night sky (concept preview")
    end = html.index("  // --- boot ---")
    html = html[:start] + NEW_SKY + "\n" + html[end:]

    # the parser still read cross_links, which entries no longer carry
    html = html.replace(
        'const domains = str(meta.cross_links).split(/[·;]/).map(x => x.trim()).filter(Boolean);',
        'const domains = list(meta.also_in).map(x => String(x).trim()).filter(Boolean);', 1)
    html = html.replace('      cross: str(meta.cross_links),\n', '', 1)
    html = html.replace('      crossCount: domains.length,',
                        '      crossCount: domains.length,\n      fields: [str(meta.domain)].concat(domains).filter(Boolean),', 1)

    # the map page described itself as a concept; it is not one any more
    html = html.replace(
        '<p class="kicker">The night sky · real-build feature</p>',
        '<p class="kicker">The night sky</p>', 1)
    html = html.replace(
        '<span class="sky-note">Labeled stars are real entries — click one to open it · the rest are illustrative</span>',
        '<span class="sky-note">Every star is an entry — hover to see what it connects to, click to open it</span>', 1)
    old_note = html[html.index('  <div class="note">\n    <p class="k">Why it\'s a real-build feature</p>'):]
    old_note = old_note[:old_note.index("</div>") + 6]
    html = html.replace(old_note, '''  <div class="note">
    <p class="k">What you are looking at</p>
    <p>Every star is a registry entry and every line is a connection the registry records: a solid line is a dependency one entry declares on another, a dashed line is a field the two share. A field holding most of the registry is not drawn — it would join everything to everything and say nothing. Position is computed from those links, so claims that depend on each other sit together; the layout is seeded, so the same registry always draws the same sky. Nothing here is illustrative, and there is no filler: an empty region means nobody has filed a claim there yet.</p>
  </div>''', 1)
    html = html.replace('<footer><span class="mono">Map · concept · attached to the full build</span></footer>',
                        '<footer><span class="mono">Map · drawn from the registry</span></footer>', 1)
    html = html.replace(
        '<p class="lede">Every claim is a star. The more it connects — to its domains, and to the claims that rest on it — the brighter it burns. Color says what kind of star it is, so a bright one is never mistaken for a true one.</p>',
        '<p class="lede">Every claim is a star. The more it connects — to its fields, and to the claims that rest on it — the brighter it burns. Colour says what state the claim is in, so a bright one is never mistaken for a true one.</p>', 1)
    html = html.replace(
        '''<div class="vrow"><span class="skey" style="--c:#ffd24a"></span><span class="d"><b>Yellow</b> — popular hypothesis, never tested. Bright from attention, hollow underneath.</span></div>''',
        '''<div class="vrow"><span class="skey" style="--c:#8e9ab8"></span><span class="d"><b>Slate</b> — under investigation, with no testable form of the claim found yet. No verdict has been offered.</span></div>
    <div class="vrow"><span class="skey" style="--c:#ffd24a"></span><span class="d"><b>Yellow</b> — an open hypothesis: a test exists and has not been run.</span></div>''', 1)
    io.open(INDEX, "w", encoding="utf-8", newline="\n").write(html)
    print("index.html: map replaced, cross_links reference fixed, copy updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
