#!/usr/bin/env python3
"""Arma la página principal de wibblo.kaeliapps.com en los 4 idiomas.

    python3 fuente/build.py

Lee los textos de fuente/textos/<idioma>.json y escribe:
    index.html       (español, la raíz)
    en/index.html    fr/index.html    pt/index.html

No toca /privacidad/, /descargar/ ni /download/. Los videos de los tutoriales
no necesitan volver a correr esto: ver tutoriales/LEEME.md.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://wibblo.kaeliapps.com'
LANGS = ['es', 'en', 'fr', 'pt']
APP_STORE = 'https://apps.apple.com/app/id6819557562'
PLAY = 'https://play.google.com/store/apps/details?id=com.kaeli.wibblo'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
CONTACT = 'wearekaeli@gmail.com'

# Categorías y generadores en el mismo orden que el inicio de la app.
CATEGORIES = [
    ('games', ['bingo', 'pairs', 'domino']),
    ('activities', ['wordsearch', 'crossword', 'matching', 'flashcards', 'secretcode', 'answerpath']),
    ('math', ['math', 'colorsolve', 'sudoku']),
]
# Tutoriales: id → (ícono, prefijo de las capturas, cantidad de pasos).
TUTORIALS = [
    ('bingo', 'bingo', 'bingo', 4),
    ('wordsearch', 'wordsearch', 'sopa', 4),
    ('crossword', 'crossword', 'crucigrama', 3),
    ('math', 'math', 'matematicas', 3),
    ('secretcode', 'secretcode', 'codigo', 4),
]
# Fichas de ejemplo por idioma (fr y pt muestran las de inglés).
GALLERY_LANG = {'es': 'es', 'en': 'en', 'fr': 'en', 'pt': 'en'}
GALLERY = ['bingo', 'pairs', 'wordsearch', 'crossword', 'secretcode', 'math',
           'domino', 'matching', 'flashcards', 'answerpath', 'colorsolve', 'sudoku']


def e(s):
    return html.escape(s, quote=True)


def badges(t, base, lang, extra=''):
    return f'''<div class="stores{extra}">
        <a class="store appstore" href="{APP_STORE}"><span class="yours">{e(t['hero']['your_store'])}</span><img src="{base}badges/app-store-{lang}.svg" width="168" height="56" alt="{e(t['badges']['app_store_alt'])}"></a>
        <a class="store play" href="{PLAY}"><span class="yours">{e(t['hero']['your_store'])}</span><img src="{base}badges/google-play-{lang}.png" width="188" height="56" alt="{e(t['badges']['google_play_alt'])}"></a>
      </div>'''


def page(lang, t):
    base = '' if lang == 'es' else '../'
    url = f'{SITE}/' if lang == 'es' else f'{SITE}/{lang}/'
    privacy = f'{base}privacidad/' + ('' if lang == 'es' else '#en')
    nav = t['nav']
    alternates = '\n'.join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}/{"" if l == "es" else l + "/"}">' for l in LANGS)
    names = {l: json.load(open(os.path.join(ROOT, 'fuente', 'textos', l + '.json'), encoding='utf-8'))['meta']['language']
             for l in LANGS}
    menu = []
    for l in LANGS:
        href = (base or './') + ('' if l == 'es' else l + '/')
        current = ' aria-current="page"' if l == lang else ''
        menu.append(f'<a href="{href}" data-lang="{l}" lang="{l}"{current}>{e(names[l])}</a>')
    langs_menu = ''.join(menu)

    # Actividades
    cats = []
    for cat, ids in CATEGORIES:
        cards = ''.join(
            f'''<li class="gen">
            <img src="{base}img/generadores/{gid}.webp" width="72" height="72" alt="" loading="lazy">
            <h4>{e(t['generators']['items'][gid][0])}</h4>
            <p>{e(t['generators']['items'][gid][1])}</p>
          </li>''' for gid in ids)
        cats.append(f'''<div class="cat cat-{cat}">
        <h3>{e(t['generators']['categories'][cat])}</h3>
        <ul class="gens">{cards}</ul>
      </div>''')

    # Galería
    gl = GALLERY_LANG[lang]
    shots = ''.join(
        f'''<li><a class="sample" href="{base}img/ejemplos/{gl}/{gid}.webp" data-title="{e(t['generators']['items'][gid][0])}">
          <img src="{base}img/ejemplos/{gl}/{gid}-mini.webp" alt="{e(t['generators']['items'][gid][0])}" loading="lazy">
          <span>{e(t['generators']['items'][gid][0])}</span>
        </a></li>''' for gid in GALLERY)
    note = f'<p class="note">{e(t["gallery"]["note"])}</p>' if t['gallery']['note'] else ''

    # Cómo funciona
    how = ''.join(
        f'<li><span class="num">{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'
        for i, (a, b) in enumerate(t['how']['steps']))

    # Tutoriales
    tabs, panels = [], []
    for i, (tid, icon, prefix, count) in enumerate(TUTORIALS):
        tt = t['tutorials']['items'][tid]
        sel = 'true' if i == 0 else 'false'
        tabs.append(
            f'<button role="tab" id="tab-{tid}" aria-controls="tut-{tid}" aria-selected="{sel}" data-tab="{tid}">'
            f'<img src="{base}img/generadores/{icon}.webp" width="32" height="32" alt="">'
            f'<span>{e(t["generators"]["items"][icon][0])}</span></button>')
        steps = ''.join(
            f'''<li class="step">
              <img src="{base}tutoriales/capturas/{lang}/{prefix}-{n + 1}.webp" width="360" height="783" alt="{e(t['tutorials']['step'])} {n + 1}" loading="lazy">
              <p><b>{e(t['tutorials']['step'])} {n + 1}.</b> {e(text)}</p>
            </li>''' for n, text in enumerate(tt['steps'][:count]))
        panels.append(f'''<section class="tut" role="tabpanel" id="tut-{tid}" aria-labelledby="tab-{tid}" data-tutorial="{tid}">
          <h3>{e(tt['title'])}</h3>
          <div class="video-slot" hidden></div>
          <details class="guide" open>
            <summary>{e(t['tutorials']['show_steps'])}</summary>
            <ol class="steps">{steps}</ol>
          </details>
        </section>''')

    plans_free = ''.join(f'<li>{e(x)}</li>' for x in t['plans']['free']['items'])
    plans_pro = ''.join(f'<li>{e(x)}</li>' for x in t['plans']['pro']['items'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faq']['items'])

    strings = json.dumps({'video': t['tutorials']['video'], 'close': t['gallery']['close']}, ensure_ascii=False)

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['meta']['title'])}</title>
<meta name="description" content="{e(t['meta']['description'])}">
<link rel="canonical" href="{url}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<link rel="icon" href="{base}icon.png">
<meta name="theme-color" content="#2563EB">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wibblo">
<meta property="og:title" content="{e(t['meta']['title'])}">
<meta property="og:description" content="{e(t['meta']['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://kaeliapps.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{base}fonts/Fredoka-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}estilos.css">
<script>
  // Teléfono: resaltar la tienda que corresponde. Raíz en español: llevar a su idioma
  // a quien tiene el teléfono en inglés, francés o portugués (salvo que haya elegido idioma).
  (function () {{
    var h = document.documentElement, ua = navigator.userAgent || '';
    if (/Android/i.test(ua)) h.className += ' android';
    else if (/iPhone|iPad|iPod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) h.className += ' ios';
    {'' if lang != 'es' else """var chosen = null;
    try { chosen = localStorage.getItem('wibblo.lang'); } catch (e) {}
    if (!chosen && !location.hash) {
      var langs = navigator.languages || [navigator.language || ''];
      for (var i = 0; i < langs.length; i++) {
        var l = String(langs[i]).slice(0, 2).toLowerCase();
        if (l === 'es') break;
        if (l === 'en' || l === 'fr' || l === 'pt') { location.replace(l + '/'); return; }
      }
    }"""}
  }})();
</script>
<script src="{base}sitio.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Wibblo</a>
<header class="top">
  <a class="brand" href="{base or './'}{'' if lang == 'es' else lang + '/'}"><img src="{base}icon.png" width="40" height="40" alt=""><span>Wibblo</span></a>
  <nav class="menu" aria-label="Wibblo">
    <a href="#activities">{e(nav['generators'])}</a>
    <a href="#examples">{e(nav['examples'])}</a>
    <a href="#tutorials">{e(nav['tutorials'])}</a>
    <a href="#plans">{e(nav['plans'])}</a>
    <a href="#faq">{e(nav['faq'])}</a>
  </nav>
  <details class="langs">
    <summary aria-label="{e(nav['language'])}">{lang.upper()}</summary>
    <div>{langs_menu}</div>
  </details>
  <a class="get" href="#download">{e(nav['download'])}</a>
</header>

<main id="main">
  <section class="hero" id="download">
    <div class="hero-text">
      <h1>{e(t['hero']['title'])}</h1>
      <p class="lead">{e(t['hero']['text'])}</p>
      {badges(t, base, lang)}
    </div>
    <div class="hero-art" aria-hidden="false">
      <div class="blob"></div>
      <img class="mascot" src="{base}img/mascota/cheer.webp" width="420" height="420" alt="{e(t['hero']['mascot_alt'])}">
      <img class="float f1" src="{base}img/generadores/bingo.webp" width="72" height="72" alt="">
      <img class="float f2" src="{base}img/generadores/wordsearch.webp" width="64" height="64" alt="">
      <img class="float f3" src="{base}img/generadores/crossword.webp" width="60" height="60" alt="">
      <img class="float f4" src="{base}img/generadores/math.webp" width="68" height="68" alt="">
    </div>
  </section>

  <section class="band" id="activities">
    <h2>{e(t['generators']['title'])}</h2>
    <p class="intro">{e(t['generators']['intro'])}</p>
    <div class="cats">{''.join(cats)}</div>
  </section>

  <section class="band alt" id="examples">
    <h2>{e(t['gallery']['title'])}</h2>
    <p class="intro">{e(t['gallery']['intro'])}</p>
    {note}
    <ul class="gallery">{shots}</ul>
  </section>

  <section class="band" id="how">
    <h2>{e(t['how']['title'])}</h2>
    <ol class="how">{how}</ol>
  </section>

  <section class="band alt" id="tutorials">
    <h2>{e(t['tutorials']['title'])}</h2>
    <p class="intro">{e(t['tutorials']['intro'])}</p>
    <div class="tabs" role="tablist">{''.join(tabs)}</div>
    {''.join(panels)}
  </section>

  <section class="band" id="plans">
    <h2>{e(t['plans']['title'])}</h2>
    <p class="intro">{e(t['plans']['intro'])}</p>
    <div class="plans">
      <div class="plan"><h3>{e(t['plans']['free']['title'])}</h3><ul>{plans_free}</ul></div>
      <div class="plan pro"><h3><img src="{base}img/pro/crown.webp" width="32" height="32" alt="">{e(t['plans']['pro']['title'])}</h3><ul>{plans_pro}</ul></div>
    </div>
  </section>

  <section class="band alt" id="faq">
    <h2>{e(t['faq']['title'])}</h2>
    <div class="faq">{faq}</div>
  </section>

  <section class="cta">
    <img src="{base}img/mascota/celebrating.webp" width="200" height="200" alt="" loading="lazy">
    <div>
      <h2>{e(t['cta']['title'])}</h2>
      <p>{e(t['cta']['text'])}</p>
      {badges(t, base, lang)}
    </div>
  </section>
</main>

<footer class="foot">
  <nav>
    <a href="{privacy}">{e(t['footer']['privacy'])}</a>
    <a href="{EULA}">{e(t['footer']['terms'])}</a>
    <a href="mailto:{CONTACT}">{e(t['footer']['contact'])}</a>
    <a href="https://kaeliapps.com/">{e(t['footer']['kaeli'])}</a>
  </nav>
  <p>© Kaeli · Wibblo</p>
</footer>

<dialog class="lightbox" aria-label="{e(t['gallery']['title'])}">
  <button class="close" type="button" aria-label="{e(t['gallery']['close'])}">×</button>
  <img alt="">
  <p class="caption"></p>
</dialog>
<script id="strings" type="application/json">{strings}</script>
</body>
</html>
'''


def main():
    for lang in LANGS:
        t = json.load(open(os.path.join(ROOT, 'fuente', 'textos', f'{lang}.json'), encoding='utf-8'))
        out = os.path.join(ROOT, 'index.html' if lang == 'es' else os.path.join(lang, 'index.html'))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(page(lang, t))
        print('✓', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    main()
