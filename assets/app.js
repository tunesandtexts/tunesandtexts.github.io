/* Tunes and Texts — static site. All data is read from site-data/*.json (built by build/build_site_data.py
   from the release CSVs). Routing is on plain hash names (#text-DE-00295, #tune-4457a, #hymnal-tlh …). */
(function () {
  'use strict';

  var REPO = 'tunesandtexts/tunesandtexts.github.io';
  var SITE = 'https://tunesandtexts.github.io/';
  var EMAIL = 'jhutchns@gmail.com';
  var DATA = 'site-data/';

  var LANGS = { de: 'German', da: 'Danish', no: 'Norwegian', nn: 'Nynorsk', sv: 'Swedish', en: 'English',
    fi: 'Finnish', cs: 'Czech', sk: 'Slovak', pl: 'Polish', es: 'Spanish' };
  var LORDER = ['de', 'da', 'no', 'nn', 'sv', 'en', 'fi', 'cs', 'sk', 'pl', 'es'];
  var BADGE = { p: 'probable', c: 'check', x: 'rejected' };
  var REL = {
    own: 'Melody in Zahn\'s register', supp: 'Melody in Zahn\'s supplement', also: 'Also sung to (Zahn register)',
    struct: 'Melody of the original (from Zahn\'s register)', structalso: 'Also sung to, via the original (Zahn)',
    sung: 'Sung to (named in a hymnal or source)', printed: 'Printed with this tune in a hymnal',
    variant: 'Variant chosen by its opening notes'
  };
  var RELGROUP = { own: 0, supp: 0, struct: 0, also: 1, structalso: 1, sung: 2, printed: 2, variant: 2 };
  var GROUPNAME = ['The original\'s melodies', 'Also sung to', 'Sung to in hymnals and sources'];

  var S = {
    texts: {}, tlist: [], tunes: {}, tlistTunes: [], links: [], ev: [], byText: {}, byTune: {}, kids: {},
    appear: [], apByText: {}, apByHym: {}, hymnals: [], hymBySlug: {}, hymByCode: {}, people: [], pBySlug: {},
    pByText: {}, tunenames: {}, meta: {}, details: {}, scholar: false, state: {}
  };

  // ------------------------------------------------------------------ helpers
  function $(sel, el) { return (el || document).querySelector(sel); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function stripDates(s) {
    return String(s || '').replace(/\s*\(?\b(?:d\.|b\.|fl\.|c\.|ca\.)?\s*1[2-9]\d\d(?:\s*[-–]\s*\d{2,4})?\)?\.?/g, '').replace(/,\s*(?=,|;|$)/g, '').replace(/\s{2,}/g, ' ').trim();
  }
  function fmt(n) { return Number(n).toLocaleString('en-US'); }
  function norm(s) {
    s = String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    s = s.replace(/ß/g, 'ss').replace(/æ/g, 'ae').replace(/ø/g, 'o').replace(/œ/g, 'oe').replace(/ł/g, 'l').replace(/đ/g, 'd');
    s = s.replace(/[^a-z0-9]+/g, ' ').trim();
    s = s.replace(/th/g, 't').replace(/y/g, 'i').replace(/([a-z])\1+/g, '$1');
    return s;
  }
  function natcmp(a, b) { return String(a).localeCompare(String(b), 'en', { numeric: true, sensitivity: 'base' }); }
  function slugify(s) {
    return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase();
  }
  function badge(b) { return b && BADGE[b] ? ' <span class="badge ' + b + '">' + BADGE[b] + '</span>' : ''; }
  function langChip(l) { return '<span class="lang ' + esc(l) + '" title="' + esc(LANGS[l] || l) + '">' + esc(l) + '</span>'; }
  function T(id) { return S.texts[id]; }
  function flags(t) { return t ? t[7] : []; }
  function hasFlag(t, f) { return flags(t).indexOf(f) >= 0; }
  function flagVal(t, prefix) {
    var fl = flags(t);
    for (var i = 0; i < fl.length; i++) if (typeof fl[i] === 'string' && fl[i].indexOf(prefix) === 0) return fl[i].slice(prefix.length);
    return '';
  }
  function extLinks(t) {
    var fl = flags(t);
    for (var i = 0; i < fl.length; i++) if (fl[i] && fl[i].links) return fl[i].links;
    return [];
  }
  function textLink(id, cls) {
    var t = T(id);
    if (!t) return '<span class="id">' + esc(id) + '</span>';
    return '<a class="' + (cls || '') + '" href="#text-' + esc(id) + '">' + esc(t[2] || id) + '</a>';
  }
  function tuneLabel(no) {
    var u = S.tunes[no];
    return u ? (u[5] || '') : '';
  }
  function tuneLink(no) { return '<a href="#tune-' + esc(no) + '">Zahn ' + esc(no) + '</a>'; }
  function view(html) {
    var m = $('#main');
    m.innerHTML = '<div class="view">' + html + '</div>';
    return m.firstChild;
  }
  function setTitle(s) { document.title = s ? s + ' · Tunes and Texts' : 'Tunes and Texts'; }

  // ------------------------------------------------------------------ data loading
  function getJSON(name) {
    return fetch(DATA + name).then(function (r) {
      if (!r.ok) throw new Error(name + ': ' + r.status);
      return r.json();
    });
  }

  function load() {
    var names = ['texts.json', 'tunes.json', 'links.json', 'evidence.json', 'appear.json', 'hymnals.json',
      'people.json', 'tunenames.json', 'meta.json'];
    var done = 0;
    return Promise.all(names.map(function (n) {
      return getJSON(n).then(function (d) {
        done++;
        var el = $('#loading-detail');
        if (el) el.textContent = done + ' of ' + names.length + ' files';
        return d;
      });
    })).then(function (r) {
      var texts = r[0], tunes = r[1], links = r[2];
      S.ev = r[3]; S.appear = r[4]; S.hymnals = r[5]; S.people = r[6]; S.tunenames = r[7]; S.meta = r[8];
      texts.forEach(function (t) {
        S.texts[t[0]] = t;
        t.n = norm(t[2]);
        t.na = norm(t[3]);
      });
      S.tlist = texts;
      texts.forEach(function (t) {
        if (t[5]) (S.kids[t[5]] = S.kids[t[5]] || []).push(t[0]);
      });
      tunes.forEach(function (u) { S.tunes[u[0]] = u; u.n = norm(u[5]); });
      S.tlistTunes = tunes;
      S.links = links;
      links.forEach(function (l) {
        (S.byText[l[0]] = S.byText[l[0]] || []).push(l);
        (S.byTune[l[1]] = S.byTune[l[1]] || []).push(l);
      });
      S.appear.forEach(function (a) {
        (S.apByText[a[0]] = S.apByText[a[0]] || []).push(a);
        (S.apByHym[a[1]] = S.apByHym[a[1]] || []).push(a);
      });
      S.hymnals.forEach(function (h) { S.hymBySlug[h.slug] = h; S.hymByCode[h.code] = h; });
      S.people.forEach(function (p) {
        S.pBySlug[p.slug] = p;
        p.n = norm(p.name + ' ' + (p.variants || []).join(' '));
        p.t.forEach(function (id) { (S.pByText[id] = S.pByText[id] || []).push(p); });
      });
      var m = S.meta;
      $('#foot-meta').textContent = 'Release ' + m.release + ' · built ' + m.built + ' from ' + m.base + '.';
    });
  }

  function bucket(key) {
    var m = /^([A-Z]{2})-(\d+)/.exec(key);
    if (m) return m[1] + Math.floor(parseInt(m[2], 10) / 250);
    m = /^(\d+)/.exec(key);
    return m ? 'Z' + Math.floor(parseInt(m[1], 10) / 250) : 'misc';
  }
  function details(key) {
    var b = bucket(key);
    if (!S.details[b]) S.details[b] = getJSON('details/' + b + '.json').catch(function () { return {}; });
    return S.details[b].then(function (d) { return d[key] || []; });
  }
  function renderDetails(key, el) {
    if (!el) return;
    el.innerHTML = '<p class="muted">Loading the source record…</p>';
    details(key).then(function (secs) {
      if (!secs.length) { el.innerHTML = '<p class="muted">No source record.</p>'; return; }
      el.innerHTML = secs.map(function (s) {
        return '<div><h3>' + esc(s[0]) + '</h3><div class="kv">' + s[1].map(function (f) {
          var v = f[2] ? '<a href="' + esc(f[2]) + '" rel="noopener">' + esc(f[1] || f[2]) + '</a>' : esc(f[1]);
          return '<div class="k">' + esc(f[0]) + '</div><div>' + v + '</div>';
        }).join('') + '</div></div>';
      }).join('');
    });
  }

  // ------------------------------------------------------------------ family tree
  function rootOf(id) {
    var seen = {}, cur = id;
    while (T(cur) && T(cur)[5] && !seen[cur]) { seen[cur] = 1; cur = T(cur)[5]; }
    return cur;
  }
  // Tunes of a text split into the original's melodies and other melodies.
  // orig: own / supplement / melody of the original, for this text and for its root original. other: every other linked tune.
  function tuneSplit(id) {
    var live = function (x) { return (S.byText[x] || []).filter(function (l) { return l[3] !== 'x'; }); };
    var orig = {}, other = {}, root = rootOf(id);
    var fam = live(id).concat(root !== id ? live(root) : []), alsoOnly = false;
    fam.forEach(function (l) { if (RELGROUP[l[2]] === 0) orig[l[1]] = 1; });
    // An original with no melody of its own in Zahn, only "also sung to" tunes, was sung to existing tunes: those count as borrowed.
    if (!Object.keys(orig).length) fam.forEach(function (l) { if (l[2] === 'also' || l[2] === 'structalso') { orig[l[1]] = 1; alsoOnly = true; } });
    live(id).forEach(function (l) { if (!orig[l[1]]) other[l[1]] = 1; });
    var all = live(id).map(function (l) { return l[1]; });
    var mine = Object.keys(orig).filter(function (n) { return all.indexOf(n) >= 0; });
    return { orig: Object.keys(orig), other: Object.keys(other), all: all, known: Object.keys(orig).length > 0,
      own: alsoOnly ? [] : mine.filter(function (n) { return tuneKind(id, n) === 1; }), borrowed: alsoOnly ? mine : mine.filter(function (n) { return tuneKind(id, n) === 0; }) };
  }
  // 1 = the tune first appeared with the original (Zahn prints it under that text), 0 = the original borrowed it, null = not known
  function tuneKind(id, no) {
    var root = rootOf(id), r = null;
    [root, id].forEach(function (x) { (S.byText[x] || []).forEach(function (l) { if (l[1] === no && RELGROUP[l[2]] === 0 && l[5] !== '' && l[5] != null && r === null) r = l[5]; }); });
    return r;
  }
  function tuneYearOk(no, f) {
    var y = parseInt((S.tunes[no] || [])[9], 10);
    if (!f.tfrom && !f.tto) return true;
    if (isNaN(y)) return false;
    return (!f.tfrom || y >= +f.tfrom) && (!f.tto || y <= +f.tto);
  }
  function kidsOf(id) {
    var k = (S.kids[id] || []).filter(function (c) { return S.scholar || !hasFlag(T(c), 'nd'); });
    return k.sort(function (a, b) {
      var A = T(a), B = T(b);
      return (LORDER.indexOf(A[1]) - LORDER.indexOf(B[1])) || natcmp(A[2], B[2]);
    });
  }
  function containsId(id, target, depth) {
    if (id === target) return true;
    if (depth > 8) return false;
    var k = S.kids[id] || [];
    for (var i = 0; i < k.length; i++) if (containsId(k[i], target, depth + 1)) return true;
    return false;
  }
  function nodeHtml(id, here, depth) {
    var t = T(id);
    var extra = [];
    if (flagVal(t, 'dup:')) extra.push('<span class="badge n">duplicate of ' + esc(flagVal(t, 'dup:')) + '</span>');
    if (hasFlag(t, 'title')) extra.push('<span class="badge n">title only</span>');
    if (hasFlag(t, 'nd')) extra.push('<span class="badge n">not a first line</span>');
    var h = '<li><div class="node' + (id === here ? ' here' : '') + '">' + langChip(t[1]) +
      '<span class="t">' + (id === here ? esc(t[2]) : textLink(id)) + badge(t[6]) + ' ' + extra.join(' ') + '</span>' +
      '<span class="a">' + esc(stripDates(t[3])) + (t[3] ? ' · ' : '') + '<span class="id">' + esc(id) + '</span></span>' +
      (t[5] && t[9] ? '<span class="a evidence">' + esc(t[9]) + '</span>' : '') + '</div>';
    if (depth < 8) {
      var kids = kidsOf(id);
      if (kids.length) {
        var groups = {};
        kids.forEach(function (k) { var l = T(k)[1]; (groups[l] = groups[l] || []).push(k); });
        h += '<ul>';
        LORDER.forEach(function (l) {
          var g = groups[l];
          if (!g) return;
          var inner = g.map(function (k) { return nodeHtml(k, here, depth + 1); }).join('');
          if (g.length > 6) {
            var open = g.some(function (k) { return containsId(k, here, 0); });
            h += '<li><details' + (open ? ' open' : '') + '><summary>' + esc(LANGS[l] || l) + ': ' + g.length +
              ' texts</summary><ul>' + inner + '</ul></details></li>';
          } else h += inner;
        });
        h += '</ul>';
      }
    }
    return h + '</li>';
  }

  function kindNote(l) {
    if (RELGROUP[l[2]] !== 0) return '';
    var k = tuneKind(l[0], l[1]), u = S.tunes[l[1]] || [];
    if (k === 1) return ' · <b>own tune</b>';
    if (k === 0) return ' · <b>borrowed</b>: first printed with “' + esc((u[5] || '').replace(/[,;.]?\s*$/, '')) + '”';
    return '';
  }
  // ------------------------------------------------------------------ tunes of a text
  function tuneRows(ls, opts) {
    opts = opts || {};
    var groups = [[], [], []];
    ls.forEach(function (l) {
      if (l[3] === 'x' && !S.scholar) return;
      groups[RELGROUP[l[2]] || 0].push(l);
    });
    var html = '';
    groups.forEach(function (g, gi) {
      if (!g.length) return;
      var seen = {};
      g = g.filter(function (l) { var k = l[1] + l[2]; if (seen[k]) return false; seen[k] = 1; return true; });
      g.sort(function (a, b) { return natcmp(a[1], b[1]); });
      html += '<h3>' + GROUPNAME[gi] + ' <span class="count">' + g.length + '</span></h3><ul class="rows">' +
        g.map(function (l) {
          var u = S.tunes[l[1]] || [];
          return '<li><span class="lang tune">' + esc(u[1] || '') + '</span><div class="main">' + tuneLink(l[1]) +
            ' <span class="first">' + esc(u[5] || '') + '</span>' + badge(l[3]) + '</div>' +
            '<div class="sub">' + esc([u[7], u[9]].filter(Boolean).join(', ')) + ' · ' + esc(REL[l[2]] || l[2]) + kindNote(l) + '</div>' +
            (S.ev[l[4]] ? '<div class="sub evidence">' + esc(S.ev[l[4]]) + '</div>' : '') + '</li>';
        }).join('') + '</ul>';
    });
    return html;
  }

  // ------------------------------------------------------------------ views
  var FILTER_LANGS = [['de', 'German'], ['en', 'English'], ['da', 'Danish'], ['no', 'Norwegian'], ['nn', 'Nynorsk'], ['sv', 'Swedish'], ['fi', 'Finnish'], ['cs', 'Czech'], ['sk', 'Slovak'], ['pl', 'Polish'], ['es', 'Spanish']];
  var PDLABEL = { pd: 'Public domain', pd70: 'Likely public domain (life + 70)', cr: 'Probably in copyright', '': 'Copyright not known' };
  function blankFilters() { return { langs: [], origin: '', hymnal: '', author: '', meter: '', tune: '', link: '', from: '', to: '', pd: '', tfrom: '', tto: '', fam: '' }; }
  function filtersOn(f) { return f.langs.length || f.origin || f.hymnal || f.author || f.meter || f.tune || f.link || f.from || f.to || f.pd || f.tfrom || f.tto || f.fam; }

  function viewHome() {
    setTitle('');
    var m = S.meta, L = m.langs || {};
    var f = S.state.f = S.state.f || blankFilters();
    var hs = S.hymnals.slice().sort(function (a, b) { return natcmp(a.name, b.name); });
    var v = view(
      '<div class="home-grid"><div class="section">' +
      '<h1>Which tune goes with this text, where does it come from, and is there already a translation?</h1>' +
      '<p class="lede">Search a first line in German, Danish, Norwegian, Swedish, English, Finnish, Czech or Slovak, an author or translator, a Zahn number or a text ID (EN-05224, de 295).</p>' +
      '<form class="searchbox" role="search" id="sform"><label for="q" class="skip">Search</label>' +
      '<input type="search" id="q" autocomplete="off" spellcheck="false" placeholder="e.g. Nun danket alle Gott, Winkworth, 5142, Af Dybsens Nød"></form>' +
      '<p class="search-hint">Old spellings match modern ones (Thür and Tür, seyn and sein). Diacritics are ignored.</p>' +
      '<details class="adv" id="adv"' + (filtersOn(f) ? ' open' : '') + '><summary>Advanced search</summary><div class="adv-grid">' +
      '<div><span style="font-size:var(--t-sm);font-weight:500">Language of the text</span><div class="langs">' + FILTER_LANGS.map(function (l) {
        return '<label><input type="checkbox" name="fl" value="' + l[0] + '"' + (f.langs.indexOf(l[0]) >= 0 ? ' checked' : '') + '> ' + l[1] + '</label>'; }).join('') + '</div></div>' +
      '<label for="f-origin">Language of the original<select id="f-origin"><option value="">Any</option>' + [['de', 'German'], ['la', 'Latin (via German)'], ['da', 'Danish'], ['no', 'Norwegian'], ['sv', 'Swedish'], ['en', 'English (no other original)'], ['cs', 'Czech'], ['fi', 'Finnish'], ['none', 'Original not identified']].map(function (o) {
        return '<option value="' + o[0] + '"' + (f.origin === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-hymnal">In hymnal<select id="f-hymnal"><option value="">Any</option>' + hs.map(function (h) {
        return '<option value="' + esc(h.code) + '"' + (f.hymnal === h.code ? ' selected' : '') + '>' + esc(h.name) + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-author">Author or translator<input type="text" id="f-author" value="' + esc(f.author) + '" placeholder="e.g. Gerhardt"></label>' +
      '<label for="f-meter">Meter<input type="text" id="f-meter" value="' + esc(f.meter) + '" placeholder="e.g. 8.7.8.7"></label>' +
      '<label for="f-tune">Tune<select id="f-tune">' + [['', 'Any'], ['yes', 'Has a Zahn tune'], ['orig', 'Original\'s melody (own or borrowed)'], ['own', 'Own tune'], ['borrowed', 'Only borrowed tunes'], ['other', 'Another melody'], ['unk', 'Tune, original unknown'], ['no', 'No tune recorded']].map(function (o) {
        return '<option value="' + o[0] + '"' + (f.tune === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-fam">Place in the family tree<select id="f-fam">' + [['', 'Any'], ['orig', 'Originals only (top of the tree)'], ['origk', 'Originals that have translations'], ['tr', 'Translations only']].map(function (o) {
        return '<option value="' + o[0] + '"' + (f.fam === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-link">Link to the original<select id="f-link">' + [['', 'Any'], ['sure', 'From the source (no label)'], ['p', 'Probable'], ['c', 'Check'], ['none', 'No original linked']].map(function (o) {
        return '<option value="' + o[0] + '"' + (f.link === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-pd">Copyright status<select id="f-pd">' + [['', 'Any (show everything)'], ['pd', 'Public domain'], ['pd+', 'Public domain or likely (life + 70)'], ['cr', 'Probably in copyright'], ['unk', 'Not known']].map(function (o) {
        return '<option value="' + o[0] + '"' + (f.pd === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<label for="f-tfrom">Tune year from<input type="text" id="f-tfrom" inputmode="numeric" value="' + esc(f.tfrom) + '" placeholder="1524"></label>' +
      '<label for="f-tto">Tune year to<input type="text" id="f-tto" inputmode="numeric" value="' + esc(f.tto) + '" placeholder="1700"></label>' +
      '<label for="f-from">Text year from<input type="text" id="f-from" inputmode="numeric" value="' + esc(f.from) + '" placeholder="1520"></label>' +
      '<label for="f-to">Text year to<input type="text" id="f-to" inputmode="numeric" value="' + esc(f.to) + '" placeholder="1800"></label>' +
      '</div><div class="adv-actions"><button type="button" class="btn primary" id="f-apply">Apply filters</button><button type="button" class="btn" id="f-clear">Clear filters</button>' +
      '<span class="muted" style="font-size:var(--t-sm)">Filters work with or without words in the search box, and all filters must match (AND). “Own tune” means Zahn prints the tune under the original hymn (it first appeared with it); “only borrowed” means the original had no tune of its own: every melody it was sung to was first printed with another text; “another melody” is a tune the original does not have. Tune years narrow to those tunes. “Originals” are the hymns at the top of a family tree, whatever their tune; a text with no original linked counts as an original. The year is the date the source gives for the text (Zahn\'s earliest tune year for German texts). Copyright status is guidance from print dates and death dates, not legal advice: see <a href="#about">About</a>.</span></div></details>' +
      '<div id="results"></div></div>' +
      '<aside class="browse card"><div><h3>Browse tunes</h3><ul><li><a href="#tunes-az">By first line, A–Z</a></li>' +
      '<li><a href="#tunes-zahn">By Zahn number</a></li><li><a href="#tunes-meter">By meter</a></li></ul></div>' +
      '<div><h3>Browse texts</h3><ul><li><a href="#people">Authors and translators</a></li><li><a href="#hymnals">Hymnals</a> (Pontoppidan 1740, Landstad, TLH, ELH …)</li></ul></div>' +
      '<div><h3>Tools</h3><ul><li><a href="#melody">Melody search</a>: play a few notes, find the Zahn tunes that open that way</li>' +
      '<li><a href="#compare">Compare two hymnals</a>: shared hymns and tunes</li></ul></div>' +
      '<div><h3>In the index</h3><div class="stats">' +
      '<div><b>' + fmt(m.tunes) + '</b>Zahn tunes</div><div><b>' + fmt(L.de || 0) + '</b>German texts</div>' +
      '<div><b>' + fmt(L.en || 0) + '</b>English texts</div><div><b>' + fmt((L.da || 0) + (L.no || 0) + (L.nn || 0) + (L.sv || 0)) + '</b>Scandinavian texts</div>' +
      '<div><b>' + fmt((L.fi || 0) + (L.cs || 0) + (L.sk || 0) + (L.pl || 0) + (L.es || 0)) + '</b>Finnish, Czech, Slovak …</div><div><b>' + fmt(m.links) + '</b>text–tune links</div>' +
      '</div></div></aside></div>');
    var q = $('#q', v);
    q.value = S.state.q || '';
    var timer;
    function go() { S.state.q = q.value; S.state.lim = 60; runSearch(q.value); }
    q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(go, 150); });
    $('#sform', v).addEventListener('submit', function (e) { e.preventDefault(); go(); });
    function readFilters() {
      f.langs = Array.prototype.slice.call(v.querySelectorAll('input[name="fl"]:checked')).map(function (x) { return x.value; });
      f.origin = $('#f-origin', v).value; f.hymnal = $('#f-hymnal', v).value; f.author = $('#f-author', v).value.trim();
      f.meter = $('#f-meter', v).value.trim(); f.tune = $('#f-tune', v).value; f.link = $('#f-link', v).value; f.fam = $('#f-fam', v).value;
      f.from = $('#f-from', v).value.trim(); f.to = $('#f-to', v).value.trim(); f.pd = $('#f-pd', v).value; f.tfrom = $('#f-tfrom', v).value.trim(); f.tto = $('#f-tto', v).value.trim();
    }
    $('#f-apply', v).addEventListener('click', function () { readFilters(); go(); });
    v.querySelectorAll('#adv select, #adv input[type="checkbox"]').forEach(function (el) { el.addEventListener('change', function () { readFilters(); go(); }); });
    v.querySelectorAll('#adv input[type="text"]').forEach(function (el) { el.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); readFilters(); go(); } }); });
    $('#f-clear', v).addEventListener('click', function () { S.state.f = blankFilters(); viewHome(); });
    if (q.value || filtersOn(f)) runSearch(q.value); else showExamples();
    if (window.matchMedia('(min-width: 700px)').matches) q.focus();
  }

  function showExamples() {
    var ex = ['DE-04097', 'DE-00295', 'NO-0001', 'DA-0402', 'FI-0001'].filter(T);
    $('#results').innerHTML = '<div class="section"><h3>Try one</h3><ul class="rows">' + ex.map(textRow).join('') + '</ul></div>';
  }

  function textRow(id) {
    var t = T(id);
    return '<li>' + langChip(t[1]) + '<div class="main"><span class="first">' + textLink(id) + '</span>' + badge(t[6]) +
      (flagVal(t, 'dup:') ? ' <span class="badge n">duplicate</span>' : '') + '</div>' +
      '<div class="sub">' + esc(stripDates(t[3])) + (t[3] ? ' · ' : '') + '<span class="id">' + esc(id) + '</span>' +
      (t[5] && T(t[5]) ? ' · from ' + esc(LANGS[T(t[5])[1]] || '') + ' “' + esc(T(t[5])[2]) + '”' : '') + '</div></li>';
  }
  function tuneRow(no) {
    var u = S.tunes[no];
    return '<li><span class="lang tune">' + esc(u[1]) + '</span><div class="main">' + tuneLink(no) + ' <span class="first">' + esc(u[5]) + '</span></div>' +
      '<div class="sub">' + esc([u[7], u[9], u[4]].filter(Boolean).join(' · ')) + '</div></li>';
  }

  // "en-05224", "EN 5224", "de295" -> a text ID that exists
  function idFromQuery(raw) {
    var m = /^\s*([a-z]{2})[\s\-_.]*0*(\d{1,5})\s*$/i.exec(raw);
    if (!m) return '';
    var pre = m[1].toUpperCase(), n = m[2];
    for (var w = 4; w <= 5; w++) {
      var id = pre + '-' + (new Array(Math.max(0, w - n.length) + 1).join('0')) + n;
      if (T(id)) return id;
    }
    return '';
  }
  function originLang(t) {
    var r = T(rootOf(t[0]));
    if (!t[5]) return '';
    if (r && r[1] === 'de' && /latin|lat\./i.test(r[3] + ' ' + (r[9] || ''))) return 'la';
    return r ? r[1] : '';
  }
  function matchFilters(t, f) {
    if (f.langs.length && f.langs.indexOf(t[1]) < 0) return false;
    if (f.origin) {
      var o = originLang(t);
      if (f.origin === 'none') { if (t[5] || t[1] === 'de') return false; }
      else if (f.origin === 'en') { if (t[1] !== 'en' || t[5]) return false; }
      else if (f.origin === 'de') { if (!(t[5] && (o === 'de' || o === 'la'))) return false; }
      else if (o !== f.origin) return false;
    }
    if (f.hymnal && !(S.apByText[t[0]] || []).some(function (a) { return a[1] === f.hymnal; })) return false;
    if (f.author) {
      var na = norm(f.author), ps = S.pByText[t[0]] || [];
      if (t.na.indexOf(na) < 0 && !ps.some(function (p) { return p.n.indexOf(na) >= 0; })) return false;
    }
    if (f.meter && String(t[4] || '').replace(/[^0-9A-Za-z]+/g, '.').indexOf(f.meter.replace(/[^0-9A-Za-z]+/g, '.')) !== 0) return false;
    if (f.tune || f.tfrom || f.tto) {
      var sp = tuneSplit(t[0]);
      if (f.tune === 'unk' && sp.known) return false;
      var pool = f.tune === 'own' ? sp.own : f.tune === 'borrowed' ? (sp.own.length ? [] : sp.borrowed) : f.tune === 'orig' ? sp.orig.filter(function (n) { return sp.all.indexOf(n) >= 0; }) : f.tune === 'other' ? (sp.known ? sp.other : []) : sp.all;
      if (f.tune === 'no') { if (sp.all.length) return false; }
      else if (!pool.some(function (n) { return tuneYearOk(n, f); })) return false;
    }
    if (f.fam) {
      if (f.fam === 'tr' && !t[5]) return false;
      if ((f.fam === 'orig' || f.fam === 'origk') && t[5]) return false;
      if (f.fam === 'origk' && !(S.kids[t[0]] || []).length) return false;
    }
    if (f.link) {
      if (f.link === 'none') { if (t[5]) return false; }
      else if (f.link === 'sure') { if (!t[5] || t[6]) return false; }
      else if (t[6] !== f.link) return false;
    }
    if (f.pd) {
      var pc = t[10] || '';
      if (f.pd === 'pd' && pc !== 'pd') return false;
      if (f.pd === 'pd+' && pc !== 'pd' && pc !== 'pd70') return false;
      if (f.pd === 'cr' && pc !== 'cr') return false;
      if (f.pd === 'unk' && pc) return false;
    }
    if (f.from || f.to) {
      var y = parseInt(t[8], 10);
      if (!y) return false;
      if (f.from && y < parseInt(f.from, 10)) return false;
      if (f.to && y > parseInt(f.to, 10)) return false;
    }
    return true;
  }

  function search(q, f) {
    var nq = norm(q), raw = q.trim();
    var out = { texts: [], tunes: [], people: [] };
    var fon = f && filtersOn(f);
    if (!nq && !fon) return out;
    var idq = idFromQuery(raw);
    if (idq && (!fon || matchFilters(T(idq), f))) out.texts.push([0, idq]);
    if (!fon) {
      if (S.tunes[raw.toLowerCase()]) out.tunes.push([0, raw.toLowerCase()]);
      if (/^\d+$/.test(raw)) S.tlistTunes.forEach(function (u) { if (u[0] !== raw && u[0].replace(/[a-z]+$/, '') === raw) out.tunes.push([1, u[0]]); });
    }
    var toks = nq ? nq.split(' ') : [];
    function score(n) {
      if (!nq) return 5;
      if (!n) return -1;
      if (n === nq) return 1;
      if (n.indexOf(nq) === 0) return 2;
      var words = ' ' + n;
      for (var i = 0; i < toks.length; i++) if (words.indexOf(' ' + toks[i]) < 0) return n.indexOf(nq) >= 0 ? 4 : -1;
      return 3;
    }
    if (!idq || fon) S.tlist.forEach(function (t) {
      if (hasFlag(t, 'nd') && !S.scholar) return;
      if (t[0] === idq) return;
      if (fon && !matchFilters(t, f)) return;
      var s = score(t.n);
      if (s < 0) { s = score(t.na); if (s >= 0) s += 4; }
      if (s >= 0) out.texts.push([s + (flagVal(t, 'dup:') ? 0.5 : 0), t[0]]);
    });
    if (nq && !fon && !/^\d+$/.test(raw) && !idq) S.tlistTunes.forEach(function (u) { var s = score(u.n); if (s >= 0 && s < 4) out.tunes.push([s + 1, u[0]]); });
    if (nq && !fon && !/^\d+$/.test(raw) && !idq) Object.keys(S.tunenames).forEach(function (no) {
      if (!S.tunes[no]) return;
      var best = -1;
      S.tunenames[no].forEach(function (nm) { var s = score(norm(nm[0])); if (s >= 0 && s < 4 && (best < 0 || s < best)) best = s; });
      if (best >= 0 && !out.tunes.some(function (x) { return x[1] === no; })) out.tunes.push([best + 1, no]);
    });
    if (nq && !fon && !idq) S.people.forEach(function (p) { var s = score(p.n); if (s >= 0) out.people.push([s, p.slug, p.t.length + p.m.length]); });
    out.texts.sort(function (a, b) { return a[0] - b[0] || T(a[1])[2].length - T(b[1])[2].length || natcmp(a[1], b[1]); });
    out.tunes.sort(function (a, b) { return a[0] - b[0] || natcmp(a[1], b[1]); });
    out.people.sort(function (a, b) { return a[0] - b[0] || b[2] - a[2]; });
    return out;
  }

  function runSearch(q) {
    var box = $('#results');
    if (!box) return;
    var f = S.state.f || blankFilters();
    if (!q.trim() && !filtersOn(f)) { showExamples(); return; }
    var r = search(q, f);
    S.state.last = r;
    var lim = S.state.lim || 60;
    var h = '';
    if (r.people.length) {
      h += '<div class="section"><h3>Authors, translators, composers <span class="count">' + r.people.length + '</span></h3><p>' +
        r.people.slice(0, 12).map(function (p) { var P = S.pBySlug[p[1]]; return '<a href="#person-' + P.slug + '">' + esc(P.name) + '</a> <span class="muted">(' + p[2] + ')</span>'; }).join(' · ') + '</p></div>';
    }
    h += '<div class="section"><h3>Texts <span class="count">' + fmt(r.texts.length) + (filtersOn(f) ? ' (filtered)' : '') + '</span></h3>';
    if (r.texts.length) h += '<ul class="rows">' + r.texts.slice(0, lim).map(function (x) { return textRow(x[1]); }).join('') + '</ul>';
    else h += '<p class="muted">No text matches' + (q.trim() ? ' “' + esc(q) + '”' : '') + (filtersOn(f) ? ' with these filters' : '') + '. Try fewer words or fewer filters.</p>';
    h += '<div class="result-tools">' + (r.texts.length > lim ? '<button class="btn" id="more">Show ' + Math.min(200, r.texts.length - lim) + ' more</button>' : '') +
      (r.texts.length ? '<button class="btn" id="xlsx">Export ' + fmt(r.texts.length) + ' texts to Excel</button>' : '') +
      '<button class="btn" id="totop">↑ Back to top</button><span class="muted" id="xlsx-note" style="font-size:var(--t-sm)"></span></div></div>';
    if (r.tunes.length) h += '<div class="section"><h3>Tunes <span class="count">' + fmt(r.tunes.length) + '</span></h3><ul class="rows">' +
      r.tunes.slice(0, 30).map(function (x) { return tuneRow(x[1]); }).join('') + '</ul>' +
      (r.tunes.length > 30 ? '<p class="muted">First 30 shown. Narrow the search, or <a href="#tunes-az">browse the tunes</a>.</p>' : '') + '</div>';
    box.innerHTML = h;
    var mb = $('#more');
    if (mb) mb.addEventListener('click', function () { S.state.lim = lim + 200; runSearch(q); });
    $('#totop').addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); var qq = $('#q'); if (qq) qq.focus({ preventScroll: true }); });
    var xb = $('#xlsx');
    if (xb) xb.addEventListener('click', function () { exportXlsx(r.texts.map(function (x) { return x[1]; }), q); });
  }

  function exportRows(ids) {
    return ids.map(function (id) {
      var t = T(id), o = t[5] ? T(rootOf(id)) : null, par = t[5] ? T(t[5]) : null;
      var tunes = (S.byText[id] || []).filter(function (l) { return l[3] !== 'x'; }).map(function (l) { return l[1]; });
      var seen = {}; tunes = tunes.filter(function (x) { if (seen[x]) return false; seen[x] = 1; return true; });
      return {
        'ID': id, 'Language': LANGS[t[1]] || t[1], 'First line': t[2],
        'Author / translator': (S.pByText[id] || []).map(function (p) { return p.name; }).join('; ') || stripDates(t[3]),
        'Credit as printed': t[3], 'Meter': t[4], 'Year': t[8], 'Copyright status (guidance)': PDLABEL[t[10] || ''], 'Copyright basis': t[11] || '',
        'Translated from (ID)': t[5] || '', 'Translated from (first line)': par ? par[2] : '',
        'Link to original': t[5] ? (BADGE[t[6]] || 'from the source') : '',
        'Original (root) ID': o ? o[0] : '', 'Original (root) first line': o ? o[2] : '', 'Original language': o ? (LANGS[o[1]] || o[1]) : '',
        'Zahn tunes': tunes.join(' '),
        'Original\'s melodies': (function () { var sp = tuneSplit(id); return sp.orig.filter(function (n) { return sp.all.indexOf(n) >= 0; }).join(' '); })(),
        'Own tune': (function () { return tuneSplit(id).own.join(' '); })(),
        'Borrowed tunes': (function () { return tuneSplit(id).borrowed.join(' '); })(),
        'Place in family': T(id)[5] ? 'translation' : 'original',
        'Other melodies': (function () { var sp = tuneSplit(id); return sp.known ? sp.other.join(' ') : ''; })(), 'Hymnals': (S.apByText[id] || []).map(function (a) { return a[1] + ' ' + a[2]; }).join('; '),
        'Page': SITE + '#text-' + id
      };
    });
  }
  function exportXlsx(ids, q) {
    var note = $('#xlsx-note');
    function write() {
      try {
        var ws = window.XLSX.utils.json_to_sheet(exportRows(ids));
        ws['!cols'] = [10, 10, 48, 28, 28, 14, 6, 12, 40, 14, 12, 40, 12, 18, 30, 40].map(function (w) { return { wch: w }; });
        var wb = window.XLSX.utils.book_new();
        window.XLSX.utils.book_append_sheet(wb, ws, 'Search results');
        var meta = window.XLSX.utils.aoa_to_sheet([['Tunes and Texts: Lutheran Hymns in German, Scandinavian and English'], ['Search', q || ''], ['Filters', JSON.stringify(S.state.f)],
          ['Exported', new Date().toISOString().slice(0, 10)], ['Release', S.meta.release + ', ' + S.meta.base], ['License', 'CC0 for the project\'s own work; first lines and credits remain subject to their sources\' terms']]);
        window.XLSX.utils.book_append_sheet(wb, meta, 'About');
        window.XLSX.writeFile(wb, 'Tunes_and_Texts_search_' + new Date().toISOString().slice(0, 10) + '.xlsx');
        if (note) note.textContent = /github\.io$|localhost/.test(location.hostname) ? 'Downloaded.' : 'Saved — if nothing downloaded, this preview blocks downloads; the live site allows them.';
      } catch (e) { if (note) note.textContent = 'Export failed: ' + e.message; }
    }
    if (window.XLSX) return write();
    if (note) note.textContent = 'Preparing the file…';
    var sc = document.createElement('script');
    sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
    sc.onload = write;
    sc.onerror = function () { if (note) note.textContent = 'The Excel library could not be loaded.'; };
    document.head.appendChild(sc);
  }

  function viewText(id) {
    var t = T(id);
    if (!t) return viewMissing('No text with the ID ' + id + '.');
    setTitle(t[2]);
    S.current = { kind: 'text', id: id, label: t[2] };
    var root = rootOf(id), parent = t[5];
    var notes = [];
    var dup = flagVal(t, 'dup:');
    if (dup) notes.push('<div class="notice">This row is a duplicate, kept for the record. Use ' + textLink(dup) + ' <span class="id">' + esc(dup) + '</span>.</div>');
    var same = flagVal(t, 'same:');
    if (same && T(same)) notes.push('<div class="notice amber">Same text as ' + textLink(same) + ' <span class="id">' + esc(same) + '</span> (another spelling or printing).</div>');
    if (hasFlag(t, 'nd')) notes.push('<div class="notice">Kept for the record: this row is not a hymn first line (an import artefact or heading).</div>');
    if (hasFlag(t, 'title')) notes.push('<div class="notice amber">A title, not a first line.</div>');
    if (hasFlag(t, 'notr')) notes.push('<div class="notice amber">Not a translation of a German text.</div>');
    if (t[6] && parent) notes.push('<div class="notice amber">The link to the original is <b>' + BADGE[t[6]] + '</b>.' +
      (t[9] ? ' <span class="scholar-only">Basis: ' + esc(t[9]) + '</span>' : ' Turn on scholar view to see the evidence.') + '</div>');
    var people = S.pByText[id] || [];
    var auth = people.length ? people.map(function (p) { return '<a href="#person-' + p.slug + '">' + esc(p.name) + '</a>'; }).join('; ') +
      (t[3] ? ' <span class="scholar-only">(as printed: ' + esc(t[3]) + ')</span>' : '')
      : esc(stripDates(t[3]));
    var ext = extLinks(t).map(function (l) { return '<a href="' + esc(l[1]) + '" rel="noopener">' + esc(l[0]) + '</a>'; }).join('');

    // tunes: this text's own links, else the nearest original's
    var ls = S.byText[id] || [], via = '';
    if (!ls.length) {
      var cur = parent, guard = 0;
      while (cur && T(cur) && guard++ < 8) {
        if ((S.byText[cur] || []).length) { ls = S.byText[cur]; via = cur; break; }
        cur = T(cur)[5];
      }
    }
    var tunesHtml = ls.length ? (via ? '<p class="muted">No tune is recorded for this text itself. These are the tunes of its original, ' + textLink(via) + ' <span class="id">' + esc(via) + '</span>.</p>' : '') + tuneRows(ls)
      : '<p class="muted">No tune is recorded for this text' + (t[1] !== 'de' && !parent ? ' (its original is not identified)' : '') + '.</p>';

    var ap = (S.apByText[id] || []).slice().sort(function (a, b) { return natcmp(a[1], b[1]) || natcmp(a[2], b[2]); });
    var apHtml = ap.length ? '<ul class="plain">' + ap.map(function (a) {
      var h = S.hymByCode[a[1]];
      return '<li><a href="#hymnal-' + h.slug + '">' + esc(h.name) + '</a> ' + (a[7] ? '<a class="mono" href="' + esc(a[7]) + '" rel="noopener">' + esc(a[2]) + ' (scan)</a>' : '<span class="mono">' + esc(a[2]) + '</span>') +
        (a[3] && norm(a[3]) !== t.n ? ' <span class="muted">“' + esc(a[3]) + '”</span>' : '') +
        (a[4] ? ' · printed with ' + a[4].split(' ').map(tuneLink).join(', ') + badge(a[6]) : '') + '</li>';
    }).join('') + '</ul>' : '<p class="muted">Not in any of the indexed hymnals.</p>';
    var treeSize = countTree(root, 0);

    view('<div class="crumbs"><a href="#home">Search</a><span>›</span><span>' + esc(LANGS[t[1]] || t[1]) + ' text</span><span class="id">' + esc(id) + '</span></div>' +
      '<div class="record-head">' + '<div>' + langChip(t[1]) + ' <span class="muted">' + esc(LANGS[t[1]] || '') + '</span></div>' +
      '<h1>' + esc(t[2]) + '</h1><div class="meta">' + (auth ? '<span><b>' + (t[1] === 'de' || !parent ? 'Author' : 'Translator / credit') + ':</b> ' + auth + '</span>' : '') +
      (t[4] ? '<span><b>Meter:</b> <a href="#meter-' + t[4].replace(/[^0-9A-Za-z]+/g, '-') + '">' + esc(t[4]) + '</a></span>' : '') +
      (t[8] ? '<span><b>Year:</b> ' + esc(t[8]) + '</span>' : '') + '<span class="pd pd-' + (t[10] || 'unk') + '" title="' + esc(t[11] || 'No print date or death date known') + '">' + PDLABEL[t[10] || ''] + '</span>' + '<span class="id">' + esc(id) + '</span></div>' +
      (ext ? '<div class="extlinks">' + ext + '</div>' : '') + notes.join('') + '</div>' +
      '<div class="two"><div class="section"><h2>Family of translations <span class="count">' + treeSize + ' text' + (treeSize === 1 ? '' : 's') + '</span></h2>' +
      (treeSize === 1 ? '<p class="muted">No translation or original of this text is recorded yet.</p>' : '') +
      '<ul class="tree">' + nodeHtml(root, id, 0) + '</ul></div>' +
      '<div class="section"><h2>Tunes</h2>' + tunesHtml + '<h2>In hymnals</h2>' + apHtml + '</div></div>' +
      '<div class="section scholar-only"><h2>Source record</h2><div class="record-src" id="rec"></div></div>');
    if (S.scholar) renderDetails(id, $('#rec'));
  }
  function countTree(id, d) {
    if (d > 8) return 1;
    return 1 + kidsOf(id).reduce(function (s, k) { return s + countTree(k, d + 1); }, 0);
  }

  // incipit → ABC (pitches only, as whole notes, under Zahn's key signature)
  var KEYS = { '0': 'C', '1#': 'G', '2#': 'D', '3#': 'A', '4#': 'E', '5#': 'B', '6#': 'F#', '7#': 'C#',
    '1b': 'F', '2b': 'Bb', '3b': 'Eb', '4b': 'Ab', '5b': 'Db', '6b': 'Gb', '7b': 'Cb' };
  function keyAlts(ks) {
    var m = /^(\d)([#b])/.exec(ks || ''), alt = {};
    if (!m) return alt;
    var order = m[2] === '#' ? 'FCGDAEB' : 'BEADGCF';
    for (var i = 0; i < +m[1]; i++) alt[order[i]] = m[2] === '#' ? 1 : -1;
    return alt;
  }
  function toAbc(notes, ks) {
    var m = /^(\d[#b]|0)/.exec(ks || '');
    var key = m ? KEYS[m[1]] : 'C';
    var ka = keyAlts(ks), state = {}, out = [];
    (notes || '').split(/\s+/).forEach(function (n) {
      var p = /^([A-G])(#{1,2}|b{1,2})?(\d)$/.exec(n);
      if (!p) return;
      var L = p[1], a = p[2] ? (p[2][0] === '#' ? p[2].length : -p[2].length) : 0, o = +p[3];
      var sk = L + o, cur = sk in state ? state[sk] : (ka[L] || 0), mark = '';
      if (a !== cur) { mark = a === 0 ? '=' : a > 0 ? new Array(a + 1).join('^') : new Array(-a + 1).join('_'); state[sk] = a; }
      var s = o >= 5 ? L.toLowerCase() + new Array(o - 4).join("'") : L + new Array(5 - o).join(',');
      out.push(mark + s);
    });
    return 'X:1\nM:none\nL:1/1\nK:' + key + ' clef=treble\n' + out.join(' ') + ' |]\n';
  }
  function drawIncipit(el, notes, ks, small) {
    if (!el || !window.ABCJS) return;
    try {
      window.ABCJS.renderAbc(el, toAbc(notes, ks), { responsive: 'resize', staffwidth: small ? 520 : 760, scale: small ? 0.8 : 1,
        paddingtop: 0, paddingbottom: 0, paddingleft: 0, paddingright: 0, add_classes: true });
    } catch (e) { el.textContent = notes; }
  }

  function viewTune(no) {
    var u = S.tunes[no];
    if (!u) return viewMissing('No Zahn tune numbered ' + no + '.');
    setTitle('Zahn ' + no + ' · ' + u[5]);
    S.current = { kind: 'tune', id: no, label: 'Zahn ' + no + ' ' + u[5] };
    var ls = (S.byTune[no] || []).filter(function (l) { return S.scholar || l[3] !== 'x'; });
    var byGroup = [[], [], []], seen = {};
    ls.forEach(function (l) {
      var k = l[0] + '|' + RELGROUP[l[2]];
      if (seen[k]) return; seen[k] = 1;
      byGroup[RELGROUP[l[2]] || 0].push(l);
    });
    var textsHtml = byGroup.map(function (g, gi) {
      if (!g.length) return '';
      g.sort(function (a, b) { var A = T(a[0]), B = T(b[0]); return (LORDER.indexOf(A[1]) - LORDER.indexOf(B[1])) || natcmp(A[2], B[2]); });
      var lim = 80;
      return '<h3>' + ['Texts with this as their own melody', 'Texts also sung to it', 'Sung to it in hymnals and sources'][gi] + ' <span class="count">' + g.length + '</span></h3>' +
        '<ul class="rows">' + g.slice(0, lim).map(function (l) {
          var t = T(l[0]);
          return '<li>' + langChip(t[1]) + '<div class="main"><span class="first">' + textLink(l[0]) + '</span>' + badge(l[3]) + '</div>' +
            '<div class="sub">' + esc(t[3] || '') + (t[3] ? ' · ' : '') + '<span class="id">' + esc(l[0]) + '</span> · ' + esc(REL[l[2]] || '') + '</div>' +
            (S.ev[l[4]] ? '<div class="sub evidence">' + esc(S.ev[l[4]]) + '</div>' : '') + '</li>';
        }).join('') + '</ul>' + (g.length > lim ? '<p class="muted">' + (g.length - lim) + ' more not shown.</p>' : '');
    }).join('');
    var names = S.tunenames[no] || [];
    var listen = names.map(function (n) {
      var url = 'https://hymnary.org/search?qu=' + encodeURIComponent('tuneTitle:"' + n[0] + '" in:tunes');
      return '<a href="' + esc(url) + '" rel="noopener">' + esc(n[0]) + ' on hymnary.org</a>' + (n[1] ? ' <span class="badge c">check</span>' : '');
    });
    var same = (u[15] || '').split(/[\s,;]+/).filter(function (x) { return S.tunes[x]; });
    var fact = function (k, v) { return v ? '<div><span class="k">' + k + '</span><span>' + v + '</span></div>' : ''; };
    var de = (S.byTune[no] || []).filter(function (l) { return (l[2] === 'own' || l[2] === 'supp') && T(l[0]) && T(l[0])[1] === 'de'; });
    view('<div class="crumbs"><a href="#tunes-zahn">Tunes</a><span>›</span><span>Zahn vol. ' + esc(u[1]) + '</span></div>' +
      '<div class="record-head"><div><span class="lang tune">Zahn</span> <span class="muted">Tune ' + esc(no) + '</span></div>' +
      '<h1>' + esc(u[5] || 'Zahn ' + no) + '</h1><div class="meta"><span><b>Zahn</b> ' + esc(no) + '</span>' +
      '<span><b>Vol.</b> ' + esc(u[1]) + ', p. ' + esc(u[2]) + '</span>' + (u[4] ? '<span><b>Syllables:</b> ' + esc(u[4]) + '</span>' : '') + '</div>' +
      '<div class="extlinks">' + (u[16] ? '<a href="' + esc(u[16]) + '" rel="noopener">Scan: Zahn ' + esc(u[1]) + ', p. ' + esc(u[2]) + ' (archive.org)</a>' : '') + '</div></div>' +
      '<div class="two"><div class="section">' +
      (u[12] ? '<div class="incipit"><div id="inc"></div><p class="incipit-cap">Opening notes as read from Zahn (pitches only' + (u[10] ? ', key signature ' + esc(u[10]) : '') + '). Reading confidence: ' + esc(u[13] || 'not given') + '. Check the scan for the rhythm.</p></div>' : '<p class="muted">No opening notes recorded.</p>') +
      '<div class="card facts">' + fact('Text in Zahn', esc(u[5]) + (de.length ? ' · ' + de.slice(0, 2).map(function (l) { return textLink(l[0]); }).join(', ') : '')) +
      fact('Text author', esc(u[6])) + fact('Composer / attribution', esc(u[7])) + fact('First source', esc(u[8])) + fact('Year', esc(u[9])) +
      fact('Meter type', esc(u[3])) + fact('Time', esc(u[11])) + fact('Same melody as', same.map(tuneLink).join(', ')) +
      fact('Duplicate of', esc(u[17] ? 'master row ' + u[17] : '')) + '</div>' +
      '<div class="section"><h2>Listen / scores</h2>' + (listen.length ? '<p class="muted">Settings of this tune or text on hymnary.org. A setting may follow a different variant than Zahn ' + esc(no) + '.</p><ul class="plain">' +
        listen.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>' : '<p class="muted">No hymnary.org tune is matched to this Zahn number yet. The scan above shows the full melody.</p>') + '</div>' +
      '</div><div class="section"><h2>Texts sung to this tune <span class="count">' + ls.length + ' links</span></h2>' + (textsHtml || '<p class="muted">No text is linked to this tune.</p>') + '</div></div>' +
      '<div class="section scholar-only"><h2>Source record</h2><div class="record-src" id="rec"></div></div>');
    if (u[12]) drawIncipit($('#inc'), u[12], u[10]);
    if (S.scholar) renderDetails(no, $('#rec'));
  }

  // browse tunes
  function pager(total, page, size, base) {
    var pages = Math.ceil(total / size);
    if (pages <= 1) return '';
    var h = '<div class="pager">';
    for (var i = 0; i < pages; i++) {
      h += i === page ? '<b>' + (i + 1) + '</b>' : '<a href="#' + base + '-p' + (i + 1) + '">' + (i + 1) + '</a>';
    }
    return h + '</div>';
  }
  function tunesTabs(on) {
    return '<div class="tabs">' + [['tunes-az', 'First line A–Z'], ['tunes-zahn', 'Zahn number'], ['tunes-meter', 'Meter']].map(function (x) {
      return '<a href="#' + x[0] + '"' + (x[0] === on ? ' class="on"' : '') + '>' + x[1] + '</a>';
    }).join('') + '</div>';
  }
  function viewTunesAZ(letter, page) {
    setTitle('Tunes A–Z');
    letter = (letter || 'a').toLowerCase();
    var letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
    var list = S.tlistTunes.filter(function (u) { return (u.n[0] || '#') === letter; })
      .sort(function (a, b) { return a.n.localeCompare(b.n) || natcmp(a[0], b[0]); });
    var size = 300, p = page || 0;
    view('<h1>Tunes</h1>' + tunesTabs('tunes-az') + '<p class="lede">Zahn\'s tunes by the first line of the text they carry in Zahn.</p>' +
      '<div class="letters">' + letters.map(function (l) { return '<a href="#tunes-az-' + l + '"' + (l === letter ? ' class="on"' : '') + '>' + l.toUpperCase() + '</a>'; }).join('') + '</div>' +
      '<div class="section"><h2>' + letter.toUpperCase() + ' <span class="count">' + fmt(list.length) + ' tunes</span></h2>' + pager(list.length, p, size, 'tunes-az-' + letter) +
      '<ul class="rows">' + list.slice(p * size, p * size + size).map(function (u) { return tuneRow(u[0]); }).join('') + '</ul>' + pager(list.length, p, size, 'tunes-az-' + letter) + '</div>');
  }
  function viewTunesZahn(page) {
    setTitle('Tunes by Zahn number');
    var list = S.tlistTunes.slice().sort(function (a, b) { return natcmp(a[0], b[0]); });
    var size = 250, p = page || 0, pages = Math.ceil(list.length / size);
    var opts = '';
    for (var i = 0; i < pages; i++) opts += '<option value="' + (i + 1) + '"' + (i === p ? ' selected' : '') + '>' + list[i * size][0] + ' – ' + list[Math.min(list.length, i * size + size) - 1][0] + '</option>';
    var v = view('<h1>Tunes</h1>' + tunesTabs('tunes-zahn') + '<p class="lede">All ' + fmt(list.length) + ' melodies in Zahn, Die Melodien der deutschen evangelischen Kirchenlieder (1889–1893), in Zahn\'s order: by meter type, then by date.</p>' +
      '<label class="pager" for="range">Numbers <select id="range">' + opts + '</select></label>' +
      '<ul class="rows">' + list.slice(p * size, p * size + size).map(function (u) { return tuneRow(u[0]); }).join('') + '</ul>' + pager(list.length, p, size, 'tunes-zahn'));
    $('#range', v).addEventListener('change', function () { location.hash = 'tunes-zahn-p' + this.value; });
  }
  function meterKey(s) { return String(s || '').replace(/\(.*?\)/g, '').replace(/\s+/g, '').replace(/[^0-9A-Za-z.]+$/, ''); }
  function viewTunesMeter(key) {
    setTitle('Tunes by meter');
    var groups = {};
    S.tlistTunes.forEach(function (u) { var k = meterKey(u[4]); if (k) (groups[k] = groups[k] || []).push(u); });
    var keys = Object.keys(groups).sort(function (a, b) { return groups[b].length - groups[a].length || natcmp(a, b); });
    if (key) {
      var mk = key.replace(/-/g, '.'), g = groups[mk] || [];
      var texts = S.tlist.filter(function (t) { return t[4] && t[4].replace(/[^0-9A-Za-z]+/g, '.') === mk && !hasFlag(t, 'nd'); });
      setTitle('Meter ' + mk);
      view('<h1>Meter ' + esc(mk) + '</h1>' + tunesTabs('tunes-meter') +
        '<div class="two"><div class="section"><h2>Tunes <span class="count">' + g.length + '</span></h2>' +
        (g.length ? '<ul class="rows">' + g.sort(function (a, b) { return natcmp(a[0], b[0]); }).map(function (u) { return tuneRow(u[0]); }).join('') + '</ul>' : '<p class="muted">No Zahn tune has this exact syllable pattern.</p>') +
        '</div><div class="section"><h2>Texts in this meter <span class="count">' + texts.length + '</span></h2>' +
        (texts.length ? '<ul class="rows">' + texts.slice(0, 400).map(function (t) { return textRow(t[0]); }).join('') + '</ul>' : '<p class="muted">No text has this meter recorded.</p>') +
        '</div></div>');
      return;
    }
    view('<h1>Tunes</h1>' + tunesTabs('tunes-meter') + '<p class="lede">Syllables per line, as Zahn gives them (8.7.8.7 = four lines of 8, 7, 8 and 7 syllables). Most common first.</p>' +
      '<ul class="plain cols">' + keys.map(function (k) { return '<li><a href="#meter-' + k.replace(/\./g, '-') + '" class="mono">' + esc(k) + '</a> <span class="muted">' + groups[k].length + '</span></li>'; }).join('') + '</ul>');
  }

  // people
  function viewPeople(letter) {
    setTitle('Authors and translators');
    letter = (letter || 'a').toLowerCase();
    var list = S.people.filter(function (p) { return p.letter === letter; }).sort(function (a, b) { return natcmp(norm(a.sort), norm(b.sort)); });
    view('<h1>Authors, translators and composers</h1><p class="lede">By surname. Spellings of one name (J. Rist, Rist, Johann Rist) are listed together; a person\'s page shows every form the sources print. A surname alone stays separate when several people share it.</p>' +
      '<div class="letters">' + 'abcdefghijklmnopqrstuvwxyz'.split('').map(function (l) { return '<a href="#people-' + l + '"' + (l === letter ? ' class="on"' : '') + '>' + l.toUpperCase() + '</a>'; }).join('') + '</div>' +
      '<ul class="plain cols">' + list.map(function (p) {
        return '<li><a href="#person-' + p.slug + '">' + esc(p.sort) + '</a> <span class="muted">' + [p.t.length ? p.t.length + ' text' + (p.t.length > 1 ? 's' : '') : '', p.m.length ? p.m.length + ' tune' + (p.m.length > 1 ? 's' : '') : ''].filter(Boolean).join(', ') + '</span></li>';
      }).join('') + '</ul>');
  }
  function viewPerson(slug) {
    var p = S.pBySlug[slug];
    if (!p) return viewMissing('No such name in the index.');
    setTitle(p.name);
    S.current = { kind: 'person', id: slug, label: p.name };
    var texts = p.t.filter(T).sort(function (a, b) { var A = T(a), B = T(b); return (LORDER.indexOf(A[1]) - LORDER.indexOf(B[1])) || natcmp(A[2], B[2]); });
    var tunes = p.m.slice().sort(natcmp);
    view('<div class="crumbs"><a href="#people-' + p.letter + '">Authors</a><span>›</span></div><h1>' + esc(p.name) + '</h1>' +
      (p.variants && p.variants.length ? '<p class="variants">Also printed as: ' + p.variants.map(esc).join(' · ') + '</p>' : '') +
      '<div class="two"><div class="section"><h2>Texts <span class="count">' + texts.length + '</span></h2>' +
      (texts.length ? '<ul class="rows">' + texts.map(textRow).join('') + '</ul>' : '<p class="muted">None.</p>') + '</div>' +
      '<div class="section"><h2>Tunes (as composer or source) <span class="count">' + tunes.length + '</span></h2>' +
      (tunes.length ? '<ul class="rows">' + tunes.map(tuneRow).join('') + '</ul>' : '<p class="muted">None.</p>') + '</div></div>');
  }

  // hymnals
  function viewHymnals() {
    setTitle('Hymnals');
    var groups = {};
    S.hymnals.forEach(function (h) { var k = h.kind === 'reference' ? 'ref' : h.kind === 'collection' ? 'col' : h.lang; (groups[k] = groups[k] || []).push(h); });
    var order = [['en', 'English hymnals'], ['col', 'English translation collections'], ['da', 'Danish'], ['no', 'Norwegian'], ['sv', 'Swedish'], ['fi', 'Finnish'], ['cs', 'Czech'], ['sk', 'Slovak'], ['ref', 'Reference works']];
    view('<h1>Hymnals</h1><p class="lede">The hymnals and collections whose numbers are in the index, oldest first in each group.</p>' +
      '<div class="hymnal-groups">' + order.filter(function (o) { return groups[o[0]]; }).map(function (o) {
        return '<div class="section"><h2>' + o[1] + '</h2><ul class="rows">' + groups[o[0]].sort(function (a, b) { return natcmp(a.year || '9999', b.year || '9999') || natcmp(a.name, b.name); }).map(function (h) {
          return '<li><span class="lang">' + esc(h.lang) + '</span><div class="main"><a href="#hymnal-' + h.slug + '">' + esc(h.name) + '</a></div><div class="sub">' +
            (h.pub ? esc(h.pub.replace(/\s*\[hymnary[^\]]*\]/, '')) + ' · ' : '') + fmt(h.n) + ' entries</div></li>';
        }).join('') + '</ul></div>';
      }).join('') + '</div>');
  }
  function firstTunes(id) {
    var ls = (S.byText[id] || []).filter(function (l) { return l[3] !== 'x'; });
    ls.sort(function (a, b) { return (RELGROUP[a[2]] - RELGROUP[b[2]]) || natcmp(a[1], b[1]); });
    var seen = {}, out = [];
    ls.forEach(function (l) { if (!seen[l[1]] && out.length < 3) { seen[l[1]] = 1; out.push(l[1]); } });
    return out;
  }
  function viewHymnal(slug) {
    var h = S.hymBySlug[slug];
    if (!h) return viewMissing('No such hymnal in the index.');
    setTitle(h.name);
    S.current = { kind: 'hymnal', id: slug, label: h.name };
    var rows = (S.apByHym[h.code] || []).slice().sort(function (a, b) { return natcmp(a[2], b[2]) || natcmp(a[3], b[3]); });
    view('<div class="crumbs"><a href="#hymnals">Hymnals</a><span>›</span><span class="mono">' + esc(h.code) + '</span></div><h1>' + esc(h.name) + '</h1>' +
      (h.pub ? '<p class="muted">' + esc(h.pub) + '</p>' : '') + '<p class="lede">' + fmt(rows.length) + ' entries in the index. Code in the data: <span class="mono">' + esc(h.code) + '</span>. ' +
      '<a href="#compare-' + h.slug + '">Compare with another hymnal</a>.</p>' +
      '<div class="tablewrap"><table><thead><tr><th class="num">No.</th><th>First line (as printed)</th><th>Text in the index</th><th>Tunes</th></tr></thead><tbody>' +
      rows.map(function (a) {
        var t = T(a[0]);
        return '<tr><td class="num mono">' + (a[7] ? '<a href="' + esc(a[7]) + '" rel="noopener">' + esc(a[2]) + '</a>' : esc(a[2])) + '</td><td><span class="first">' + esc(a[3] || t[2]) + '</span></td><td>' + langChip(t[1]) + ' ' + textLink(a[0]) + ' <span class="id">' + esc(a[0]) + '</span></td><td>' +
          (a[4] ? a[4].split(' ').map(tuneLink).join(', ') + ' <span class="muted">printed</span>' + badge(a[6]) : firstTunes(a[0]).map(tuneLink).join(', ')) +
          (a[5] ? '<div class="muted">' + esc(a[5]) + '</div>' : '') + '</td></tr>';
      }).join('') + '</tbody></table></div>');
  }

  // compare
  function hymnalSets(code) {
    var roots = {}, printed = {}, linked = {};
    (S.apByHym[code] || []).forEach(function (a) {
      var r = rootOf(a[0]);
      (roots[r] = roots[r] || []).push(a);
      (a[4] || '').split(' ').forEach(function (no) { if (no) printed[no] = 1; });
      // melodies linked: the original's own melodies and what the text itself is sung to (not every variant)
      (S.byText[r] || []).forEach(function (l) { if (l[3] !== 'x' && (l[2] === 'own' || l[2] === 'supp')) linked[l[1]] = 1; });
      (S.byText[a[0]] || []).forEach(function (l) { if (l[3] !== 'x' && RELGROUP[l[2]] === 2) linked[l[1]] = 1; });
    });
    return { roots: roots, printed: printed, linked: linked, hasPrinted: Object.keys(printed).length > 0 };
  }
  function viewCompare(pre) {
    setTitle('Compare two hymnals');
    var hs = S.hymnals.slice().sort(function (a, b) { return natcmp(a.name, b.name); });
    var A = S.state.cmpA || (pre && S.hymBySlug[pre] ? pre : 'tlh'), B = S.state.cmpB || (A === 'elh' ? 'tlh' : 'elh');
    if (!S.hymBySlug[A]) A = hs[0].slug;
    if (!S.hymBySlug[B]) B = hs[1].slug;
    function sel(id, val) {
      return '<select id="' + id + '">' + hs.map(function (h) { return '<option value="' + h.slug + '"' + (h.slug === val ? ' selected' : '') + '>' + esc(h.name) + (h.name !== h.code ? ' (' + esc(h.code) + ')' : '') + '</option>'; }).join('') + '</select>';
    }
    var v = view('<h1>Compare two hymnals</h1><p class="lede">Hymns count as shared when both books carry the same text or a translation of the same original (the same family). Tunes count as shared when both books link a text to the same Zahn melody.</p>' +
      '<div class="compare-pick"><label for="ca">First hymnal' + sel('ca', A) + '</label><label for="cb">Second hymnal' + sel('cb', B) + '</label></div><div id="cmp"></div>');
    function run() {
      S.state.cmpA = $('#ca').value; S.state.cmpB = $('#cb').value;
      var ha = S.hymBySlug[S.state.cmpA], hb = S.hymBySlug[S.state.cmpB];
      var a = hymnalSets(ha.code), b = hymnalSets(hb.code);
      var shared = Object.keys(a.roots).filter(function (r) { return b.roots[r]; });
      shared.sort(function (x, y) { return natcmp((a.roots[x][0] || [])[2], (a.roots[y][0] || [])[2]); });
      var usePrinted = a.hasPrinted && b.hasPrinted;
      var ta = usePrinted ? a.printed : a.linked, tb = usePrinted ? b.printed : b.linked;
      var st = Object.keys(ta).filter(function (t) { return tb[t]; }).sort(natcmp);
      var tuneWord = usePrinted ? 'Zahn tunes printed in both' : 'Zahn melodies linked in both';
      var ca = Object.keys(a.roots).length, cb = Object.keys(b.roots).length;
      function cell(list) {
        return list.map(function (e) { return '<span class="mono">' + esc(e[2]) + '</span> ' + textLink(e[0]); }).join('<br>');
      }
      $('#cmp').innerHTML = '<div class="summary-tiles"><div><b>' + fmt(shared.length) + '</b>hymn families in both</div><div><b>' + fmt(ca - shared.length) + '</b>only in ' + esc(ha.code) + '</div>' +
        '<div><b>' + fmt(cb - shared.length) + '</b>only in ' + esc(hb.code) + '</div><div><b>' + fmt(st.length) + '</b>' + tuneWord + '</div></div>' +
        '<div class="section"><h2>Shared hymns <span class="count">' + shared.length + '</span></h2>' + (shared.length ? '<div class="tablewrap"><table><thead><tr><th>Original (family)</th><th>' + esc(ha.name) + '</th><th>' + esc(hb.name) + '</th></tr></thead><tbody>' +
        shared.map(function (r) {
          var t = T(r);
          return '<tr><td>' + langChip(t[1]) + ' ' + textLink(r) + '</td><td>' + cell(a.roots[r]) + '</td><td>' + cell(b.roots[r]) + '</td></tr>';
        }).join('') + '</tbody></table></div>' : '<p class="muted">No hymn is shared.</p>') + '</div>' +
        '<div class="section"><h2>Shared tunes <span class="count">' + st.length + '</span></h2><p class="muted">' +
        (usePrinted ? 'Tunes identified in the music of both books (the Zahn variant printed with the hymn).' :
          'At least one book has no printed tunes in the index, so this compares the melodies linked to its hymns: the original\'s own melodies, and tunes named for the text in hymnals and sources.') + '</p>' + (st.length ? '<ul class="plain cols">' + st.map(function (no) { return '<li>' + tuneLink(no) + ' <span class="muted">' + esc(tuneLabel(no)) + '</span></li>'; }).join('') + '</ul>' : '<p class="muted">No Zahn tune is shared.</p>') + '</div>';
    }
    $('#ca', v).addEventListener('change', run);
    $('#cb', v).addEventListener('change', run);
    run();
  }

  // melody search
  var NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];
  var BASE = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
  function midiOf(n) { var p = /^([A-G])(#{1,2}|b{1,2})?(\d)$/.exec(n); if (!p) return null; return BASE[p[1]] + (p[2] ? (p[2][0] === '#' ? p[2].length : -p[2].length) : 0) + (+p[3] + 1) * 12; }
  function nameOf(m) { return NAMES[m % 12] + (Math.floor(m / 12) - 1); }
  function parseNotes(s) {
    var out = [], prev = 67;
    String(s).replace(/,/g, ' ').split(/\s+/).forEach(function (tok) {
      var p = /^([A-Ga-g])(#{1,2}|b{1,2}|is|es|s)?(\d)?$/.exec(tok.trim());
      if (!p) return;
      var L = p[1].toUpperCase(), acc = p[2] || '', a = acc === 'is' ? 1 : (acc === 'es' || acc === 's') ? -1 : acc ? (acc[0] === '#' ? acc.length : -acc.length) : 0;
      var pc = (BASE[L] + a + 12) % 12, m;
      if (p[3]) m = BASE[L] + a + (+p[3] + 1) * 12;
      else { m = prev - ((prev - pc) % 12 + 12) % 12; if (prev - m > 6) m += 12; }
      out.push(m); prev = m;
    });
    return out;
  }
  var tuneInts = null;
  function intsFor() {
    if (tuneInts) return tuneInts;
    tuneInts = S.tlistTunes.map(function (u) {
      var iv = u[14] ? u[14].split(/\s+/).map(Number).filter(function (x) { return !isNaN(x); }) : [];
      if (!iv.length && u[12]) { var ms = u[12].split(/\s+/).map(midiOf); for (var i = 1; i < ms.length; i++) if (ms[i] != null && ms[i - 1] != null) iv.push(ms[i] - ms[i - 1]); }
      return [u[0], iv];
    });
    return tuneInts;
  }
  function melodyMatch(q, mode, where) {
    var qi = [];
    for (var i = 1; i < q.length; i++) qi.push(q[i] - q[i - 1]);
    if (!qi.length) return [];
    var sgn = function (x) { return x > 0 ? 1 : x < 0 ? -1 : 0; };
    var eq = mode === 'contour' ? function (a, b) { return sgn(a) === sgn(b); } : function (a, b) { return a === b; };
    var res = [];
    intsFor().forEach(function (t) {
      var iv = t[1], maxStart = where === 'any' ? iv.length - qi.length : 0;
      for (var s = 0; s <= maxStart; s++) {
        var ok = s + qi.length <= iv.length;
        for (var j = 0; ok && j < qi.length; j++) if (!eq(iv[s + j], qi[j])) ok = false;
        if (ok) { res.push([t[0], s]); break; }
      }
    });
    return res.sort(function (a, b) { return a[1] - b[1] || natcmp(a[0], b[0]); });
  }
  function viewMelody() {
    setTitle('Melody search');
    var st = S.state.mel = S.state.mel || { notes: [67, 67, 69, 71, 67], mode: 'exact', where: 'start' };
    var keys = '';
    var whites = [], blacks = [];
    for (var m = 60; m <= 84; m++) { var nm = NAMES[m % 12]; if (nm.length === 1) whites.push(m); else blacks.push(m); }
    var w = 100 / whites.length;
    whites.forEach(function (m, i) { keys += '<button type="button" class="w" data-m="' + m + '" style="left:' + (i * w) + '%;width:' + w + '%" aria-label="' + nameOf(m) + '">' + (m % 12 === 0 ? nameOf(m) : '') + '</button>'; });
    blacks.forEach(function (m) {
      var i = whites.indexOf(m - 1);
      keys += '<button type="button" class="b" data-m="' + m + '" style="left:' + ((i + 1) * w - w * 0.3) + '%;width:' + (w * 0.6) + '%" aria-label="' + nameOf(m) + '"></button>';
    });
    var v = view('<h1>Melody search</h1><p class="lede">Play or type the first few notes of a melody. The search compares the steps between the notes, so any key works. Four or five notes usually narrow it to a handful of Zahn tunes.</p>' +
      '<div class="keys" id="keys">' + keys + '</div>' +
      '<div class="melody-controls"><label for="mnotes" class="skip">Notes</label><input type="text" id="mnotes" spellcheck="false" placeholder="Type notes: G G A B G, or G4 G4 A4 B4 G4, or German names: g a h c">' +
      '<button type="button" class="btn" id="mundo">Undo</button><button type="button" class="btn" id="mclear">Clear</button></div>' +
      '<div class="opts"><label><input type="radio" name="mmode" value="exact" id="mm1"> Exact steps</label><label><input type="radio" name="mmode" value="contour" id="mm2"> Up/down only</label>' +
      '<label><input type="radio" name="mwhere" value="start" id="mw1"> At the start</label><label><input type="radio" name="mwhere" value="any" id="mw2"> Anywhere in the opening</label></div>' +
      '<div class="incipit"><div id="mstaff"></div><p class="incipit-cap" id="mcap"></p></div><div id="mres"></div>');
    var input = $('#mnotes', v);
    function sync(fromInput) {
      if (!fromInput) input.value = st.notes.map(nameOf).join(' ');
      $('#mm1').checked = st.mode === 'exact'; $('#mm2').checked = st.mode === 'contour';
      $('#mw1').checked = st.where === 'start'; $('#mw2').checked = st.where === 'any';
      var names = st.notes.map(nameOf).join(' ');
      if (st.notes.length) drawIncipit($('#mstaff'), names, '0', true); else $('#mstaff').innerHTML = '';
      $('#mcap').textContent = st.notes.length ? st.notes.length + ' notes: ' + names : 'No notes yet.';
      var r = st.notes.length >= 3 ? melodyMatch(st.notes, st.mode, st.where) : [];
      var box = $('#mres');
      if (st.notes.length < 3) { box.innerHTML = '<p class="muted">Enter at least three notes.</p>'; return; }
      var lim = 40;
      box.innerHTML = '<div class="section"><h2>Matching tunes <span class="count">' + fmt(r.length) + '</span></h2>' +
        (r.length ? '<ul class="rows">' + r.slice(0, lim).map(function (x, i) {
          var u = S.tunes[x[0]];
          return '<li><span class="lang tune">' + esc(u[1]) + '</span><div class="main">' + tuneLink(x[0]) + ' <span class="first">' + esc(u[5]) + '</span>' +
            (x[1] ? ' <span class="badge n">from note ' + (x[1] + 1) + '</span>' : '') + '</div><div class="sub">' + esc([u[7], u[9], u[4]].filter(Boolean).join(' · ')) + '</div>' +
            '<div class="sub mini" id="mi' + i + '"></div></li>';
        }).join('') + '</ul>' + (r.length > lim ? '<p class="muted">First ' + lim + ' shown. Add a note to narrow the search.</p>' : '')
          : '<p class="muted">No Zahn tune opens with these steps. Try “Up/down only”, or “Anywhere in the opening”.</p>') + '</div>';
      r.slice(0, lim).forEach(function (x, i) { var u = S.tunes[x[0]]; if (u[12]) drawIncipit($('#mi' + i), u[12], u[10], true); });
    }
    $('#keys', v).addEventListener('click', function (e) {
      var b = e.target.closest('button[data-m]');
      if (!b) return;
      st.notes.push(+b.getAttribute('data-m'));
      if (st.notes.length > 16) st.notes.shift();
      b.classList.add('hit'); setTimeout(function () { b.classList.remove('hit'); }, 150);
      sync();
    });
    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { st.notes = parseNotes(input.value).slice(0, 16); sync(true); }, 250); });
    $('#mundo', v).addEventListener('click', function () { st.notes.pop(); sync(); });
    $('#mclear', v).addEventListener('click', function () { st.notes = []; sync(); });
    [['mm1', 'mode', 'exact'], ['mm2', 'mode', 'contour'], ['mw1', 'where', 'start'], ['mw2', 'where', 'any']].forEach(function (x) {
      $('#' + x[0], v).addEventListener('change', function () { st[x[1]] = x[2]; sync(); });
    });
    sync();
  }

  // static pages
  function viewAbout() {
    setTitle('About');
    var m = S.meta, L = m.langs || {};
    view('<div class="prose"><h1>About Tunes and Texts</h1>' +
      '<p><b>Tunes and Texts: Lutheran Hymns in German, Scandinavian and English</b> is a linked index of Lutheran hymn tunes and texts. It answers one question: which tune goes with this text, where does the text come from, and is there already a translation?</p>' +
      '<p class="notice amber">This is <b>release 0.9, provisional and under review</b>. The sources it draws on are being invited to look it over and send corrections or objections. Release 1.0, with a DOI, will follow the review.</p>' +
      '<h2>What is in it</h2><ul>' +
      '<li><b>' + fmt(m.tunes) + ' tunes</b>: every melody in Johannes Zahn, <i>Die Melodien der deutschen evangelischen Kirchenlieder</i> (6 vols., 1889–1893), with its source, meter and opening notes, and a link to the scan.</li>' +
      '<li><b>' + fmt(L.de || 0) + ' German texts</b>: Zahn\'s text register, and texts added by this project from Julian, hymnary.org, Carver\'s Hymnoglypt and the Kirchen-Gesangbuch of 1862.</li>' +
      '<li><b>' + fmt(L.en || 0) + ' English texts</b>, most linked to the German (or Latin) text they translate.</li>' +
      '<li><b>' + fmt((L.da || 0) + (L.no || 0) + (L.nn || 0) + (L.sv || 0)) + ' Danish, Norwegian and Swedish texts</b>, including the whole of Pontoppidan\'s <i>Den nye Psalme-Bog</i> (1740) checked against Breitendich\'s melody book (1764).</li>' +
      '<li><b>' + fmt((L.fi || 0) + (L.cs || 0) + (L.sk || 0) + (L.pl || 0) + (L.es || 0)) + ' Finnish, Czech, Slovak, Polish and Spanish texts.</b></li></ul>' +
      '<p><b>No hymn texts are included</b>: only first lines, authors and translators, and sources, as in Julian\'s <i>Dictionary of Hymnology</i> and on hymnary.org.</p>' +
      '<h2>How sure is each link?</h2><ul><li><b>No label</b>: taken from the source itself (Zahn\'s register, the printed hymnal, the translator\'s own note), or checked against it.</li>' +
      '<li><span class="badge p">probable</span> one source, or a reading that is very likely but not certain. Shown on purpose, with its evidence.</li>' +
      '<li><span class="badge c">check</span> needs a look.</li><li><span class="badge x">rejected</span> a link once made and later disproved. Kept, with the reason, in scholar view only.</li></ul>' +
      '<p>Turn on <b>Scholar view</b> (top right) to see on every line the source, evidence tags (PR printed page; SC/JV Julian\'s scanned text; KN compiler\'s judgement) and the reasoning, and the full source record of each text and tune.</p>' +
      '<h2>Copyright status</h2><p>Each text carries a copyright label, worked out from dates; it is guidance, not legal advice. <b>Public domain</b>: printed in a book before 1931 (public domain in the United States), marked Public Domain on hymnary.org, or every credited author and translator died by 1930. <b>Likely public domain (life + 70)</b>: every credited person died 1931–1955 and no printing before 1931 was found; public domain where the term is life + 70 years, but check before using it in the United States. <b>Probably in copyright</b>: hymnary.org gives a copyright notice, or a credited person died in 1956 or later or is living. <b>Not known</b>: no print date or death date to go on. A revised wording can be in copyright even when the older version is free. Death dates come from the authority list (German National Library, GND). Melodies from Zahn (1889–1893) are all public domain; harmonizations in modern hymnals may not be.</p>' +
      '<h2>Method</h2><p>Data were extracted, read and matched with Claude (an AI model by Anthropic): OCR of registers and melody books, reading of opening notes on scanned pages, matching first lines across languages. Every value records its source; uncertain values are labelled; the compiler reviewed the open questions and decided them. Quality control: seeded random samples in 16 batches (QC #2), an automated check of every row and a 500-row random sample (QC #3: serious-error rate at most about 1 % at 95 % confidence), and a full read of the last additions.</p>' +
      '<h2>Credit and license</h2><p>Compiled by John Hutchins. <b>CC0 1.0</b> for this project\'s own contributions: IDs, links, decisions, corrections and readings. Values drawn from the listed sources remain subject to those sources\' terms; see <a href="#sources">Sources</a>. Please credit the sources you use.</p>' +
      '<h2>How to cite</h2><p>Hutchins, John (comp.). <i>Tunes and Texts: Lutheran Hymns in German, Scandinavian and English</i>, release 0.9 (provisional, 2026-11-20). https://tunesandtexts.github.io/</p>' +
      '<h2>Data</h2><p>Every table is free to download: <a href="#data">CSV files and one Excel workbook</a>.</p>' +
      '<h2>Corrections</h2><p>Use <b>Suggest a correction</b> at the foot of any page: open a GitHub issue, or write to <span class="mono">' + EMAIL + '</span>.</p></div>');
  }
  function viewSources() {
    setTitle('Sources');
    var v = view('<div class="prose" id="src"><h1>Sources</h1><p class="muted">Loading…</p></div>');
    fetch(DATA + 'sources.html').then(function (r) { return r.text(); }).then(function (h) {
      $('#src', v).innerHTML = '<h1>Sources</h1><p class="lede">Every source, what was taken from it, its terms and the credit line.</p>' + h;
    }).catch(function () { $('#src', v).innerHTML = '<h1>Sources</h1><p>See SOURCES.md in the repository.</p>'; });
  }
  function viewData() {
    setTitle('Download the data');
    var v = view('<div class="prose" id="dl"><h1>Download the data</h1><p class="muted">Loading…</p></div>');
    getJSON('files.json').then(function (files) {
      var groups = {};
      files.forEach(function (f) { var g = f.path.split('/').slice(0, -1).join('/') || 'docs'; (groups[g] = groups[g] || []).push(f); });
      $('#dl', v).innerHTML = '<h1>Download the data</h1><p>All files are UTF-8 CSV, CC0 for the project\'s own work (see <a href="#sources">Sources</a> for the terms of the values drawn from sources). Columns are explained in <a href="DATA_DICTIONARY.md">DATA_DICTIONARY.md</a>.</p>' +
        (/github\.io$|localhost|127\.0\.0\.1/.test(location.hostname) ? '' : '<p class="notice amber">This is the private preview: the files below download from the GitHub site once it is live, not from here.</p>') +
        '<p><a class="btn primary" href="downloads/Tunes_and_Texts_0.9_provisional.xlsx">Excel workbook, all tables (.xlsx)</a></p>' +
        Object.keys(groups).sort().map(function (g) {
          return '<h2 class="mono" style="font-size:1rem">' + esc(g) + '</h2><div class="tablewrap"><table><thead><tr><th>File</th><th class="num">Rows</th><th class="num">Size</th></tr></thead><tbody>' +
            groups[g].map(function (f) { return '<tr><td><a href="' + esc(f.path) + '">' + esc(f.path.split('/').pop()) + '</a></td><td class="num">' + (f.rows != null ? fmt(f.rows) : '') + '</td><td class="num">' + Math.max(1, Math.round(f.bytes / 1024)) + ' KB</td></tr>'; }).join('') +
            '</tbody></table></div>';
        }).join('');
    });
  }
  function viewMissing(msg) {
    setTitle('Not found');
    view('<h1>Not found</h1><p>' + esc(msg) + ' <a href="#home">Back to search</a>.</p>');
  }

  // ------------------------------------------------------------------ corrections
  function correctionBar() {
    var c = S.current;
    var label = c ? (c.kind === 'tune' ? 'tune ' : c.kind === 'text' ? 'text ' : c.kind === 'hymnal' ? 'hymnal ' : '') + c.id : 'this page';
    $('#correct-slot').innerHTML = '<div class="correct-bar"><span>Something wrong on this page? Sources and readers are invited to say so.</span>' +
      '<button type="button" class="btn primary" id="correct">Suggest a correction to ' + esc(label) + '</button></div>';
    $('#correct').addEventListener('click', openCorrection);
  }
  function openCorrection() {
    var c = S.current || { kind: 'page', id: location.hash.slice(1) || 'home', label: document.title };
    var page = SITE + (location.hash || '');
    var title = 'Correction: ' + c.id + (c.label && c.label !== c.id ? ' – ' + c.label : '');
    var body = 'Page: ' + page + '\nRecord: ' + c.id + '\n\nWhat is wrong:\n\nWhat it should be:\n\nSource (book, page, link):\n';
    var issue = 'https://github.com/' + REPO + '/issues/new?template=correction.yml&title=' + encodeURIComponent(title) +
      '&record=' + encodeURIComponent(c.id) + '&page=' + encodeURIComponent(page);
    var mail = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('[Tunes and Texts] ' + title) + '&body=' + encodeURIComponent(body);
    $('#dlg-body').innerHTML = '<p>About <b>' + esc(c.label || c.id) + '</b> <span class="id">' + esc(c.id) + '</span>. Say what is wrong, what it should be, and the source.</p>' +
      '<div class="choice"><b>With a GitHub account</b><a class="btn primary" href="' + esc(issue) + '" rel="noopener">Open a GitHub issue</a><span class="muted">Public, so others can see it has been reported.</span></div>' +
      '<div class="choice"><b>By email</b><a class="btn" href="' + esc(mail) + '">Write an email</a><span class="copyrow"><span class="mono">' + EMAIL + '</span><button type="button" class="btn small" id="copymail">Copy address</button></span>' +
      '<span class="muted">Mention the record ID ' + esc(c.id) + '.</span></div>';
    $('#dlg').hidden = false;
    $('#copymail').addEventListener('click', function () {
      var b = this;
      try { navigator.clipboard.writeText(EMAIL).then(function () { b.textContent = 'Copied'; }, function () { b.textContent = 'Copy failed'; }); } catch (e) { b.textContent = 'Copy failed'; }
    });
    $('#dlg-close').focus();
  }

  // ------------------------------------------------------------------ router
  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, ''));
    var m, nav = 'home';
    S.current = null;
    if (!h || h === 'home') viewHome();
    else if ((m = /^text-(.+)$/.exec(h))) viewText(m[1]);
    else if ((m = /^tune-(.+)$/.exec(h))) { viewTune(m[1]); nav = 'tunes'; }
    else if ((m = /^tunes-az(?:-([a-z]))?(?:-p(\d+))?$/.exec(h))) { viewTunesAZ(m[1], m[2] ? m[2] - 1 : 0); nav = 'tunes'; }
    else if ((m = /^tunes-zahn(?:-p(\d+))?$/.exec(h))) { viewTunesZahn(m[1] ? m[1] - 1 : 0); nav = 'tunes'; }
    else if (h === 'tunes-meter') { viewTunesMeter(); nav = 'tunes'; }
    else if ((m = /^meter-(.+)$/.exec(h))) { viewTunesMeter(m[1]); nav = 'tunes'; }
    else if ((m = /^people(?:-([a-z]))?$/.exec(h))) { viewPeople(m[1]); nav = 'people'; }
    else if ((m = /^person-(.+)$/.exec(h))) { viewPerson(m[1]); nav = 'people'; }
    else if (h === 'hymnals') { viewHymnals(); nav = 'hymnals'; }
    else if ((m = /^hymnal-(.+)$/.exec(h))) { viewHymnal(m[1]); nav = 'hymnals'; }
    else if ((m = /^compare(?:-(.+))?$/.exec(h))) { if (m[1]) S.state.cmpA = m[1]; viewCompare(m[1]); nav = 'compare'; }
    else if (h === 'melody') { viewMelody(); nav = 'melody'; }
    else if (h === 'about') { viewAbout(); nav = 'about'; }
    else if (h === 'sources') { viewSources(); nav = 'about'; }
    else if (h === 'data') { viewData(); nav = 'about'; }
    else viewMissing('This address does not match a page.');
    document.querySelectorAll('.nav a').forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-nav') === nav); });
    correctionBar();
    window.scrollTo(0, 0);
  }

  function initScholar() {
    var box = $('#scholar');
    try { S.scholar = localStorage.getItem('tt-scholar') === '1'; } catch (e) { S.scholar = false; }
    box.checked = S.scholar;
    document.body.classList.toggle('scholar', S.scholar);
    box.addEventListener('change', function () {
      S.scholar = box.checked;
      document.body.classList.toggle('scholar', S.scholar);
      try { localStorage.setItem('tt-scholar', S.scholar ? '1' : '0'); } catch (e) { /* storage unavailable */ }
      route();
    });
  }

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') $('#dlg').hidden = true; });
  $('#dlg-close').addEventListener('click', function () { $('#dlg').hidden = true; });
  $('#dlg').addEventListener('click', function (e) { if (e.target.id === 'dlg') $('#dlg').hidden = true; });
  initScholar();
  load().then(function () {
    window.addEventListener('hashchange', route);
    route();
  }).catch(function (e) {
    $('#main').innerHTML = '<div class="loading"><p>The index could not be loaded.</p><p class="muted">' + esc(e.message) + '</p></div>';
  });

  window.TT = { S: S, search: search, toAbc: toAbc, melodyMatch: melodyMatch, parseNotes: parseNotes };
})();
