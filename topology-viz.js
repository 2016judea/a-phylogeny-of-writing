// ============================================================
    // THEMES — clustered from the Notion writing_library corpus
    // ============================================================
    const THEMES = [
      { id: 'reaching', label: 'reaching / ad astra',  color: '#A87B5C', light: '#D2B097', accent: '#7C5536' },
      { id: 'mind',     label: 'mind & machine',       color: '#5B7A9E', light: '#9DB6CE', accent: '#3F5773' },
      { id: 'inner',    label: 'inner weather',        color: '#6B8B6B', light: '#A8C0A4', accent: '#4A6649' },
      { id: 'time',     label: 'inheritance & time',   color: '#9C6A8A', light: '#C49AB1', accent: '#6E4A60' },
      { id: 'place',    label: 'place & encounter',    color: '#B8924E', light: '#D9B884', accent: '#856830' },
      { id: 'examined', label: 'the examined day',     color: '#7E6FA0', light: '#B2A5C8', accent: '#574B73' },
    ];

    // ============================================================
    // CORPUS — pruned to the strongest signal: poetry, Substack essays,
    // landmark journals. Loose notes mostly removed to let the canopy breathe.
    // ============================================================
    const CORPUS = [
      // reaching
      { id: 's6', title: "May '23", theme: 'reaching', source: 'substack', date: "2023-05-20", weight: 4 },
      { id: 's26', title: "February ‘25", theme: 'reaching', source: 'substack', date: "2025-02-15", weight: 4 },
      { id: 's30', title: "June '25", theme: 'reaching', source: 'substack', date: "2025-06-13", weight: 4 },
      { id: 's31', title: "August '25", theme: 'reaching', source: 'substack', date: "2025-08-25", weight: 4 },
      { id: 's50', title: "Publishing a newspaper.", theme: 'reaching', source: 'substack', date: "2026-05-20", weight: 4 },
      { id: 'p1', title: "Ad Astra", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p3', title: "Ambition", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p6', title: "Hang High the Roof Beams", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p10', title: "Move Cross Country", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p13', title: "Portal", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p18', title: "The Merchant Ship", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p20', title: "Tumbling Astronauts", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      { id: 'p21', title: "Your Morning Halo", theme: 'reaching', source: 'poetry', date: "", weight: 3 },
      // mind
      { id: 's10', title: "September '23", theme: 'mind', source: 'substack', date: "2023-09-27", weight: 4 },
      { id: 's12', title: "November '23", theme: 'mind', source: 'substack', date: "2023-11-25", weight: 4 },
      { id: 's22', title: "December '24", theme: 'mind', source: 'substack', date: "2024-12-08", weight: 4 },
      { id: 's24', title: "Titans and Transformers", theme: 'mind', source: 'substack', date: "2025-01-22", weight: 4 },
      { id: 's25', title: "DeepSeek", theme: 'mind', source: 'substack', date: "2025-01-28", weight: 4 },
      { id: 's32', title: "September '25", theme: 'mind', source: 'substack', date: "2025-09-01", weight: 4 },
      { id: 's35', title: "The AI Bubble", theme: 'mind', source: 'substack', date: "2025-11-28", weight: 4 },
      { id: 's44', title: "APR 26", theme: 'mind', source: 'substack', date: "2026-04-15", weight: 4 },
      { id: 's47', title: "Working w/Claude Code", theme: 'mind', source: 'substack', date: "2026-05-03", weight: 4 },
      { id: 's49', title: "Thought Experiment", theme: 'mind', source: 'substack', date: "2026-05-18", weight: 4 },
      // inner
      { id: 's11', title: "October '23", theme: 'inner', source: 'substack', date: "2023-10-24", weight: 4 },
      { id: 's14', title: "January '24", theme: 'inner', source: 'substack', date: "2024-01-24", weight: 4 },
      { id: 's18', title: "May '24", theme: 'inner', source: 'substack', date: "2024-05-21", weight: 4 },
      { id: 's19', title: "August '24", theme: 'inner', source: 'substack', date: "2024-08-21", weight: 4 },
      { id: 's20', title: "October '24", theme: 'inner', source: 'substack', date: "2024-10-22", weight: 4 },
      { id: 's21', title: "November '24", theme: 'inner', source: 'substack', date: "2024-11-23", weight: 4 },
      { id: 's23', title: "January '25", theme: 'inner', source: 'substack', date: "2025-01-18", weight: 4 },
      { id: 's37', title: "DEC 25 — PT2", theme: 'inner', source: 'substack', date: "2025-12-27", weight: 4 },
      { id: 's41', title: "FEB 26", theme: 'inner', source: 'substack', date: "2026-02-17", weight: 4 },
      { id: 's45', title: "Physical Media Journal", theme: 'inner', source: 'substack', date: "2026-04-18", weight: 4 },
      { id: 's46', title: "Soulful", theme: 'inner', source: 'substack', date: "2026-04-25", weight: 4 },
      { id: 's51', title: "Appreciative.", theme: 'inner', source: 'substack', date: "2026-05-22", weight: 4 },
      { id: 's53', title: "Something Greek", theme: 'inner', source: 'substack', date: "2026-05-31", weight: 4 },
      { id: 'p2', title: "After Dark", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      { id: 'p5', title: "For Tiera", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      { id: 'p7', title: "Let's Get Sentimental Babe", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      { id: 'p9', title: "Maple Leaves", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      { id: 'p14', title: "Purple Pettled Peonies", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      { id: 'p15', title: "Rainbow Trout", theme: 'inner', source: 'poetry', date: "", weight: 3 },
      // time
      { id: 's13', title: "December '23", theme: 'time', source: 'substack', date: "2023-12-17", weight: 4 },
      { id: 's16', title: "March '24", theme: 'time', source: 'substack', date: "2024-03-20", weight: 4 },
      { id: 's33', title: "SEPT 25 — PT2", theme: 'time', source: 'substack', date: "2025-09-25", weight: 4 },
      { id: 's36', title: "DEC 25", theme: 'time', source: 'substack', date: "2025-12-10", weight: 4 },
      { id: 's40', title: "Primitive Anthropology", theme: 'time', source: 'substack', date: "2026-02-01", weight: 4 },
      { id: 's42', title: "MAR 26", theme: 'time', source: 'substack', date: "2026-03-04", weight: 4 },
      { id: 's43', title: "MAR 26 PT2", theme: 'time', source: 'substack', date: "2026-03-24", weight: 4 },
      { id: 'p17', title: "The Flood", theme: 'time', source: 'poetry', date: "", weight: 3 },
      { id: 'p19', title: "These Stones", theme: 'time', source: 'poetry', date: "", weight: 3 },
      // place
      { id: 's27', title: "South Africa", theme: 'place', source: 'substack', date: "2025-03-01", weight: 4 },
      { id: 's38', title: "Italia", theme: 'place', source: 'substack', date: "2026-01-03", weight: 4 },
      { id: 's39', title: "NYC", theme: 'place', source: 'substack', date: "2026-01-23", weight: 4 },
      { id: 'p4', title: "Big Sky", theme: 'place', source: 'poetry', date: "", weight: 3 },
      { id: 'p11', title: "One Mountain, Four Angels", theme: 'place', source: 'poetry', date: "", weight: 3 },
      { id: 'p12', title: "Parallel Rails", theme: 'place', source: 'poetry', date: "", weight: 3 },
      { id: 'p16', title: "The Fair", theme: 'place', source: 'poetry', date: "", weight: 3 },
      // examined
      { id: 's1', title: "January: Part 1 '23", theme: 'examined', source: 'substack', date: "2023-01-08", weight: 4 },
      { id: 's2', title: "January: Part 2 '23", theme: 'examined', source: 'substack', date: "2023-01-24", weight: 4 },
      { id: 's3', title: "February '23", theme: 'examined', source: 'substack', date: "2023-02-24", weight: 4 },
      { id: 's4', title: "March '23", theme: 'examined', source: 'substack', date: "2023-03-19", weight: 4 },
      { id: 's5', title: "April '23", theme: 'examined', source: 'substack', date: "2023-04-15", weight: 4 },
      { id: 's7', title: "June '23", theme: 'examined', source: 'substack', date: "2023-06-18", weight: 4 },
      { id: 's8', title: "July '23", theme: 'examined', source: 'substack', date: "2023-07-15", weight: 4 },
      { id: 's9', title: "August '23", theme: 'examined', source: 'substack', date: "2023-08-23", weight: 4 },
      { id: 's15', title: "February '24", theme: 'examined', source: 'substack', date: "2024-02-22", weight: 4 },
      { id: 's17', title: "April '24", theme: 'examined', source: 'substack', date: "2024-04-25", weight: 4 },
      { id: 's28', title: "April '25", theme: 'examined', source: 'substack', date: "2025-04-18", weight: 4 },
      { id: 's29', title: "Monopolistic Behavior in Modern Business", theme: 'examined', source: 'substack', date: "2025-05-30", weight: 4 },
      { id: 's34', title: "OCT 25", theme: 'examined', source: 'substack', date: "2025-10-28", weight: 4 },
      { id: 's48', title: "The Stoddard Temple is a threat to many things.", theme: 'examined', source: 'substack', date: "2026-05-06", weight: 4 },
      { id: 's52', title: "Opinions on the stock market", theme: 'examined', source: 'substack', date: "2026-05-28", weight: 4 },
      { id: 'p8', title: "Like An American", theme: 'examined', source: 'poetry', date: "", weight: 3 },
    ];

    // ============================================================
    // CROSS-THEME LINKS — convergent ideas across clusters
    // (filtered to only include surviving nodes)
    // ============================================================
    const CROSS_LINKS = [
      ['s10', 's14'], ['s28', 's30'], ['s24', 's52'], ['s24', 's30'], ['s17', 's19'], ['s16', 's53'], ['s4', 's16'], ['s31', 's47'], ['s29', 's32'], ['s26', 's29'], ['s25', 's28'], ['s23', 's27'], ['s22', 's23'], ['s20', 'p1'], ['s2', 's39'], ['s2', 's22'], ['s18', 's43'], ['s14', 's47'], ['s13', 's17'], ['s11', 'p8'], ['s10', 's11'], ['p1', 'p8'], ['s9', 's37'], ['s9', 's31'],
    ];

    // ============================================================
    // SETUP
    // ============================================================
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const tip = document.getElementById('tip');
    const tipTitle = document.getElementById('tip-title');
    const tipMeta = document.getElementById('tip-meta');

    let W, H, dpr;
    let positions = {};
    let hovered = null;
    let activeTheme = null;
    let focusedTheme = null;
    let animFrame;
    let t = 0;
    let isNarrow = false;
    let dark = matchMedia('(prefers-color-scheme: dark)').matches;
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => { dark = e.matches; });

    let MARGIN_X = 90;
    let MARGIN_Y_TOP = 50;
    let MARGIN_Y_BOTTOM = 60;
    let HIT_LEAF = 144;
    let HIT_THEME = 400;

    // Stats
    const totalEntries = CORPUS.length;
    const sourceTotals = CORPUS.reduce((acc, n) => { acc[n.source] = (acc[n.source]||0)+1; return acc; }, {});
    document.getElementById('stats').innerHTML =
      '<span class="stat-num">' + totalEntries + '</span> entries · ' +
      '<span class="stat-num">' + THEMES.length + '</span> themes · ' +
      '<span class="stat-num">' + Object.keys(sourceTotals).length + '</span> forms';

    // Legend
    const legendEl = document.getElementById('legend');
    THEMES.forEach(th => {
      const item = document.createElement('div');
      item.className = 'legend-item';
      item.dataset.theme = th.id;
      const count = CORPUS.filter(n => n.theme === th.id).length;
      item.innerHTML = '<div class="legend-dot" style="background:' + th.color + '"></div>' +
        th.label + ' <span style="opacity:0.6;margin-left:2px">·' + count + '</span>';
      item.onclick = () => {
        activeTheme = activeTheme === th.id ? null : th.id;
        document.querySelectorAll('.legend-item').forEach(el => {
          el.classList.toggle('dim', activeTheme && el.dataset.theme !== activeTheme);
        });
      };
      legendEl.appendChild(item);
    });

    function themeColor(themeId, alpha) {
      if (alpha === undefined) alpha = 1;
      const th = THEMES.find(x => x.id === themeId);
      if (!th) return 'rgba(120,120,120,' + alpha + ')';
      const hex = dark ? th.light : th.color;
      const r = parseInt(hex.slice(1,3), 16);
      const g = parseInt(hex.slice(3,5), 16);
      const b = parseInt(hex.slice(5,7), 16);
      return 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
    }

    function themeAccent(themeId) {
      const th = THEMES.find(x => x.id === themeId);
      return dark ? th.light : th.accent;
    }

    function resize() {
      dpr = window.devicePixelRatio || 1;
      const wrap = canvas.parentElement;
      W = wrap.offsetWidth;
      H = wrap.offsetHeight;
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);

      // Responsive margins: tight on phones so the topology can fill the canvas
      isNarrow = W < 540;
      if (isNarrow) {
        MARGIN_X = 32;
        MARGIN_Y_TOP = 28;
        MARGIN_Y_BOTTOM = 28;
        // Larger touch targets — finger tips are not mouse pointers
        HIT_LEAF = 484;   // (22px)^2
        HIT_THEME = 784;  // (28px)^2
      } else {
        MARGIN_X = 90;
        MARGIN_Y_TOP = 50;
        MARGIN_Y_BOTTOM = 60;
        HIT_LEAF = 144;
        HIT_THEME = 400;
      }

      initPositions();
    }

    // Deterministic-ish jitter from id (so re-renders are stable)
    function hashFloat(seed) {
      let h = 2166136261;
      for (let i = 0; i < seed.length; i++) {
        h ^= seed.charCodeAt(i);
        h = Math.imul(h, 16777619);
      }
      return ((h >>> 0) % 10000) / 10000;
    }

    function initPositions() {
      positions = {};
      const cx = W / 2;
      const cy = H / 2;
      const maxR = Math.min(
        (W - 2 * MARGIN_X) / 2,
        (H - MARGIN_Y_TOP - MARGIN_Y_BOTTOM) / 2
      );

      // ── OVERVIEW MODE: aidan at center, themes orbit at ~50% radius ──
      if (!focusedTheme) {
        positions['__root'] = { x: cx, y: cy, isRoot: true };

        const N = THEMES.length;
        const startAngle = -Math.PI / 2;
        const baseR = maxR * 0.5;

        THEMES.forEach((th, i) => {
          const angle = startAngle + (i / N) * Math.PI * 2;
          positions['__' + th.id] = {
            x: cx + Math.cos(angle) * baseR,
            y: cy + Math.sin(angle) * baseR,
            isTheme: true,
            themeId: th.id,
            angle: angle,
            baseR: baseR
          };
        });

        placeLeaves();
        return;
      }

      // ── FOCUS MODE: a single theme becomes the center ──
      // The focused theme sits at center. The other themes drift to the edges
      // as faint satellites — context but not competition.
      const focused = THEMES.find(t => t.id === focusedTheme);
      const others = THEMES.filter(t => t.id !== focusedTheme);

      // Hide root in focus mode (the focused theme replaces it conceptually)
      positions['__root'] = { x: cx, y: cy, isRoot: true, hidden: true };

      // Focused theme at center
      positions['__' + focused.id] = {
        x: cx, y: cy,
        isTheme: true,
        themeId: focused.id,
        angle: 0,
        baseR: 0,
        isFocus: true
      };

      // Other themes pushed to the perimeter
      const satelliteR = maxR * 0.92;
      const startAngle = -Math.PI / 2;
      others.forEach((th, i) => {
        const angle = startAngle + (i / others.length) * Math.PI * 2;
        positions['__' + th.id] = {
          x: cx + Math.cos(angle) * satelliteR,
          y: cy + Math.sin(angle) * satelliteR,
          isTheme: true,
          themeId: th.id,
          angle: angle,
          baseR: satelliteR,
          isSatellite: true
        };
      });

      placeLeaves();
    }

    // Place leaves around their theme nodes with organic variance.
    // Stable across renders (deterministic from id) but irregularly spaced
    // so it doesn't read as a perfect spoke pattern.
    function placeLeaves() {
      const byTheme = {};
      CORPUS.forEach(n => {
        if (!byTheme[n.theme]) byTheme[n.theme] = [];
        byTheme[n.theme].push(n);
      });

      // Distance scale — tighter on narrow screens
      const ds = isNarrow ? 0.62 : 1.0;

      Object.keys(byTheme).forEach(themeId => {
        const tp = positions['__' + themeId];
        const leaves = byTheme[themeId];

        let wedge, baseAngle, minDist, distRange;

        if (tp.isFocus) {
          wedge = Math.PI;
          baseAngle = 0;
          minDist = 90 * ds;
          distRange = 130 * ds;
        } else if (tp.isSatellite) {
          wedge = 0.6;
          baseAngle = tp.angle;
          minDist = 35 * ds;
          distRange = 30 * ds;
        } else {
          wedge = 0.5;
          baseAngle = tp.angle;
          minDist = 70 * ds;
          distRange = 60 * ds;
        }

        leaves.forEach((n, i) => {
          const u = leaves.length === 1 ? 0.5 : i / (leaves.length - 1);
          const angularJitter = (hashFloat(n.id + '_aj') - 0.5) * (wedge * 0.4);
          const radialJitter = hashFloat(n.id + '_rj');

          const leafAngle = baseAngle + (u - 0.5) * 2 * wedge + angularJitter;

          const isOutlier = hashFloat(n.id + '_o') > 0.78;
          const outlierBoost = isOutlier ? (25 + hashFloat(n.id + '_ob') * 25) * ds : 0;

          const dist = minDist + n.weight * 8 * ds + radialJitter * distRange + outlierBoost;

          positions[n.id] = {
            x: tp.x + Math.cos(leafAngle) * dist,
            y: tp.y + Math.sin(leafAngle) * dist,
            phase: hashFloat(n.id + '_p') * Math.PI * 2,
            speed: 0.7 + hashFloat(n.id + '_s') * 0.5,
            // Smaller drift amplitude on narrow screens — less room for motion
            amp: (isNarrow ? 2.5 : 4) + hashFloat(n.id + '_a') * (isNarrow ? 2.5 : 4),
            satellite: tp.isSatellite,
            node: n
          };
        });
      });
    }

    // No force simulation. Layout computes once and freezes.
    // What follows is purely decorative drift applied at draw time —
    // tiny per-node oscillation around the fixed position.

    function curvedPath(ax, ay, bx, by, curveAmount) {
      if (curveAmount === undefined) curveAmount = 0.3;
      const mx = (ax + bx) / 2;
      const my = (ay + by) / 2;
      const dx = bx - ax;
      const dy = by - ay;
      const len = Math.sqrt(dx*dx + dy*dy) + 0.001;
      const ox = -dy/len * curveAmount * len * 0.15;
      const oy = dx/len * curveAmount * len * 0.15;
      return { cpx: mx + ox, cpy: my + oy };
    }

    function isFaded(themeId) {
      return activeTheme && themeId !== activeTheme;
    }

    // Decorative drift — slow, gentle, returns the visible (rendered) position
    // for any node. Theme nodes breathe radially outward; leaves drift in 2D.
    function rendered(id) {
      const p = positions[id];
      if (!p) return null;
      if (p.isRoot) {
        return { x: p.x, y: p.y };
      }
      if (p.isTheme) {
        // Theme nodes breathe — slowly expand and contract along their outward axis
        // so the whole canopy feels like it's inhaling
        const breath = Math.sin(t * 0.5 + p.angle * 1.5) * 5;
        return {
          x: p.x + Math.cos(p.angle) * breath,
          y: p.y + Math.sin(p.angle) * breath
        };
      }
      // Leaves: Lissajous-like drift, each at its own phase/speed/amplitude
      const ox = Math.cos(t * p.speed + p.phase) * p.amp;
      const oy = Math.sin(t * p.speed * 0.7 + p.phase) * p.amp;
      return { x: p.x + ox, y: p.y + oy };
    }

    // Tempo: noticeable but unhurried. Full leaf orbit ~10–14 seconds.
    const TIME_STEP = 0.005;

    function draw() {
      ctx.clearRect(0, 0, W, H);
      t += TIME_STEP;

      // 1. Cross-theme links
      CROSS_LINKS.forEach(pair => {
        const aId = pair[0], bId = pair[1];
        const a = rendered(aId);
        const b = rendered(bId);
        if (!a || !b) return;
        const aNode = positions[aId].node;
        const bNode = positions[bId].node;
        const faded = isFaded(aNode.theme) && isFaded(bNode.theme);

        const cp = curvedPath(a.x, a.y, b.x, b.y, 0.6);

        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.quadraticCurveTo(cp.cpx, cp.cpy, b.x, b.y);
        ctx.strokeStyle = dark
          ? 'rgba(220,220,210,' + (faded ? 0.04 : 0.13) + ')'
          : 'rgba(80,70,55,' + (faded ? 0.04 : 0.13) + ')';
        ctx.lineWidth = 0.6;
        ctx.setLineDash([2.5, 4]);
        ctx.stroke();
        ctx.setLineDash([]);
      });

      // 2. Root → theme branches (only in overview mode)
      if (!focusedTheme) {
        THEMES.forEach(th => {
          const r = rendered('__root');
          const p = rendered('__' + th.id);
          const faded = isFaded(th.id);

          const cp = curvedPath(r.x, r.y, p.x, p.y, 0.4);
          ctx.beginPath();
          ctx.moveTo(r.x, r.y);
          ctx.quadraticCurveTo(cp.cpx, cp.cpy, p.x, p.y);
          ctx.strokeStyle = themeColor(th.id, faded ? 0.2 : 0.7);
          ctx.lineWidth = 2.2;
          ctx.lineCap = 'round';
          ctx.stroke();
        });
      }

      // 3. Theme → leaf branches
      CORPUS.forEach(n => {
        const tp = rendered('__' + n.theme);
        const np = rendered(n.id);
        const faded = isFaded(n.theme);
        const isSatellite = positions[n.id].satellite;
        // Satellite leaves get much fainter branches — they're context, not focus
        const branchAlpha = faded ? 0.05 : (isSatellite ? 0.18 : 0.4);

        const cp = curvedPath(tp.x, tp.y, np.x, np.y, 0.3);
        ctx.beginPath();
        ctx.moveTo(tp.x, tp.y);
        ctx.quadraticCurveTo(cp.cpx, cp.cpy, np.x, np.y);
        ctx.strokeStyle = themeColor(n.theme, branchAlpha);
        ctx.lineWidth = 0.8;
        ctx.stroke();
      });

      // 4. Theme nodes
      THEMES.forEach((th, idx) => {
        const themePos = positions['__' + th.id];
        const p = rendered('__' + th.id);
        const isHov = hovered === '__' + th.id;
        const isFocus = themePos.isFocus;
        const isSatellite = themePos.isSatellite;
        // Heartbeat: focused theme pulses bigger, satellites smaller
        const pulseAmt = isFocus ? 0.09 : (isSatellite ? 0.04 : 0.07);
        const pulse = 1 + pulseAmt * Math.sin(t * 0.8 + idx * 1.2);
        const faded = isFaded(th.id);
        const baseR = isFocus ? 18 : (isSatellite ? 9 : 12);
        const r = (isHov ? baseR + 2 : baseR) * pulse;

        ctx.beginPath();
        ctx.arc(p.x, p.y, r + 6, 0, Math.PI * 2);
        ctx.fillStyle = themeColor(th.id, faded ? 0.04 : 0.12);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
        ctx.fillStyle = themeColor(th.id, faded ? 0.3 : 1);
        ctx.fill();

        ctx.fillStyle = dark ? 'rgba(20,18,15,0.85)' : 'rgba(255,253,248,0.95)';
        ctx.font = "500 10px 'Geist Mono', monospace";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(th.id.slice(0,1).toUpperCase(), p.x, p.y + 0.5);

        if (!faded) {
          // Focused theme: label below the central node, larger, italic
          if (isFocus) {
            ctx.fillStyle = dark ? 'rgba(232,226,212,0.95)' : 'rgba(28,24,20,0.95)';
            ctx.font = isNarrow
              ? "italic 500 14px 'EB Garamond', serif"
              : "italic 500 16px 'EB Garamond', serif";
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            ctx.fillText(th.label, p.x, p.y + r + 8);
          } else if (!isNarrow) {
            // Satellite or overview theme: label projects radially outward
            // (Skipped on narrow screens — the legend at top serves as key)
            ctx.fillStyle = isSatellite
              ? (dark ? 'rgba(220,215,205,0.45)' : 'rgba(60,55,45,0.45)')
              : (dark ? 'rgba(220,215,205,0.7)' : 'rgba(60,55,45,0.7)');
            ctx.font = "400 11px 'Geist Mono', monospace";
            const angle = themePos.angle;
            const labelDist = r + 16;
            const lx = p.x + Math.cos(angle) * labelDist;
            const ly = p.y + Math.sin(angle) * labelDist;
            if (Math.cos(angle) > 0.3) {
              ctx.textAlign = 'left';
            } else if (Math.cos(angle) < -0.3) {
              ctx.textAlign = 'right';
            } else {
              ctx.textAlign = 'center';
            }
            ctx.textBaseline = 'middle';
            ctx.fillText(th.label, lx, ly);
          }
        }
      });

      // 5. Leaf nodes
      CORPUS.forEach(n => {
        const p = rendered(n.id);
        const isHov = hovered === n.id;
        const faded = isFaded(n.theme);
        const isSatellite = positions[n.id].satellite;

        const sizeMap = { poetry: 5, substack: 5.5, journal: 4, notes: 3.5, short_story: 5, novel: 5, project: 4 };
        const baseSize = sizeMap[n.source] || 4;
        // Satellite leaves render smaller — context, not focus
        const sizeMul = isSatellite ? 0.65 : 1;
        const r = (isHov ? baseSize + 3 : baseSize) * sizeMul;

        ctx.beginPath();
        if (n.source === 'poetry') {
          ctx.moveTo(p.x, p.y - r);
          ctx.lineTo(p.x + r, p.y);
          ctx.lineTo(p.x, p.y + r);
          ctx.lineTo(p.x - r, p.y);
          ctx.closePath();
        } else if (n.source === 'notes') {
          ctx.rect(p.x - r * 0.8, p.y - r * 0.8, r * 1.6, r * 1.6);
        } else {
          ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
        }

        // Satellite leaves are visibly muted
        const fillAlpha = faded ? 0.15 : (isSatellite ? 0.4 : (isHov ? 1 : 0.85));
        const strokeAlpha = faded ? 0.08 : (isSatellite ? 0.25 : 0.5);
        ctx.fillStyle = themeColor(n.theme, fillAlpha);
        ctx.fill();
        ctx.strokeStyle = themeColor(n.theme, strokeAlpha);
        ctx.lineWidth = 0.6;
        ctx.stroke();

        if (isHov && !faded) {
          ctx.fillStyle = dark ? 'rgba(240,235,225,0.95)' : 'rgba(30,25,20,0.92)';
          ctx.font = isNarrow
            ? "italic 400 12px 'EB Garamond', serif"
            : "italic 400 14px 'EB Garamond', serif";
          ctx.textBaseline = 'top';

          const textWidth = ctx.measureText(n.title).width;
          const halfText = textWidth / 2;
          let labelX = p.x;
          let align = 'center';
          if (labelX + halfText > W - 6) {
            labelX = W - 6;
            align = 'right';
          } else if (labelX - halfText < 6) {
            labelX = 6;
            align = 'left';
          }
          ctx.textAlign = align;
          ctx.fillText(n.title, labelX, p.y + r + 4);
        }
      });

      // 6. Root (overview mode only)
      if (!focusedTheme) {
        const rp = rendered('__root');
        ctx.beginPath();
        ctx.arc(rp.x, rp.y, 26, 0, Math.PI * 2);
        ctx.strokeStyle = dark ? 'rgba(230,225,215,0.25)' : 'rgba(60,50,40,0.22)';
        ctx.lineWidth = 0.8;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(rp.x, rp.y, 19, 0, Math.PI * 2);
        ctx.fillStyle = dark ? '#e8e2d4' : '#1c1814';
        ctx.fill();

        ctx.fillStyle = dark ? '#1c1814' : '#f5f0e6';
        ctx.font = "italic 400 13px 'EB Garamond', serif";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('aidan', rp.x, rp.y + 0.5);
      }

      animFrame = requestAnimationFrame(draw);
    }

    // ── TOOLTIP POSITIONING ───────────────────────────────────
    // Keeps tooltip fully inside canvas bounds, flipping as needed.
    function positionTooltip(nodeX, nodeY) {
      const tipW = isNarrow ? 204 : 264;
      const tipH = 68;
      const pad = 10;
      const offset = 14;

      // Horizontal: prefer right of node, flip left if overflow
      let tx = nodeX + offset;
      if (tx + tipW + pad > W) tx = nodeX - offset - tipW;
      tx = Math.max(pad, Math.min(W - tipW - pad, tx));

      // Vertical: centre on node, clamp to canvas
      let ty = nodeY - tipH / 2;
      ty = Math.max(pad, Math.min(H - tipH - pad, ty));

      tip.style.left = tx + 'px';
      tip.style.top = ty + 'px';
    }

    // ── HIT TESTING ───────────────────────────────────────────
    function handlePoint(mx, my) {
      let found = null;
      let foundData = null;
      let foundX = 0, foundY = 0;

      for (const n of CORPUS) {
        const p = rendered(n.id);
        const dx = p.x - mx, dy = p.y - my;
        if (dx*dx + dy*dy < HIT_LEAF) {
          found = n.id;
          foundData = { kind: 'leaf', node: n };
          foundX = p.x; foundY = p.y;
          break;
        }
      }

      if (!found) {
        for (const th of THEMES) {
          const p = rendered('__' + th.id);
          const dx = p.x - mx, dy = p.y - my;
          if (dx*dx + dy*dy < HIT_THEME) {
            found = '__' + th.id;
            foundData = { kind: 'theme', theme: th };
            foundX = p.x; foundY = p.y;
            break;
          }
        }
      }

      hovered = found;

      if (foundData) {
        if (foundData.kind === 'leaf') {
          const n = foundData.node;
          tipTitle.textContent = n.title;
          const dateStr = n.date ? new Date(n.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }) : '';
          tipMeta.innerHTML =
            '<span class="tooltip-source" style="background:' + themeColor(n.theme, 0.2) + ';color:' + themeAccent(n.theme) + '">' + n.source + '</span>' +
            dateStr;
        } else {
          const th = foundData.theme;
          const count = CORPUS.filter(n => n.theme === th.id).length;
          tipTitle.textContent = th.label;
          tipMeta.innerHTML = '<span style="color:' + themeAccent(th.id) + '">theme cluster</span> · ' + count + ' entries';
        }

        positionTooltip(foundX, foundY);
        tip.classList.add('visible');
        canvas.style.cursor = 'pointer';
      } else {
        tip.classList.remove('visible');
        canvas.style.cursor = 'default';
      }
    }

    // ── MOUSE EVENTS ──────────────────────────────────────────
    canvas.addEventListener('mousemove', e => {
      const rect = canvas.getBoundingClientRect();
      handlePoint(e.clientX - rect.left, e.clientY - rect.top);
    });

    canvas.addEventListener('mouseleave', () => {
      hovered = null;
      tip.classList.remove('visible');
    });

    // ── TOUCH EVENTS ──────────────────────────────────────────
    canvas.addEventListener('touchstart', e => {
      if (e.touches.length === 0) return;
      const rect = canvas.getBoundingClientRect();
      const touch = e.touches[0];
      handlePoint(touch.clientX - rect.left, touch.clientY - rect.top);
    }, { passive: true });

    document.addEventListener('touchstart', e => {
      if (!canvas.contains(e.target)) {
        hovered = null;
        tip.classList.remove('visible');
      }
    }, { passive: true });

    // ── CLICK — theme focus toggle ─────────────────────────────
    canvas.addEventListener('click', e => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      for (const th of THEMES) {
        const p = rendered('__' + th.id);
        const dx = p.x - mx, dy = p.y - my;
        if (dx*dx + dy*dy < HIT_THEME) {
          focusedTheme === th.id ? setFocus(null) : setFocus(th.id);
          return;
        }
      }
    });

    function setFocus(themeId) {
      focusedTheme = themeId;
      const btn = document.getElementById('recenter-btn');
      btn.classList.toggle('visible', !!themeId);
      initPositions();
    }

    document.getElementById('recenter-btn').addEventListener('click', () => setFocus(null));

    window.addEventListener('keydown', e => {
      if (e.key === 'Escape' && focusedTheme) setFocus(null);
    });

    window.addEventListener('resize', () => {
      cancelAnimationFrame(animFrame);
      resize();
      draw();
    });

    resize();
    draw();
