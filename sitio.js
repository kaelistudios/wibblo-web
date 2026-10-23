// wibblo.kaeliapps.com: pestañas de los tutoriales, videos (tutoriales/videos.json),
// galería en grande y recordar el idioma elegido. Sin JavaScript la página se ve completa.
(function () {
  var html = document.documentElement;
  html.classList.add('js');
  var lang = html.lang || 'es';
  var base = lang === 'es' ? '' : '../';
  var strings = {};
  try { strings = JSON.parse(document.getElementById('strings').textContent); } catch (e) {}

  // Idioma elegido a mano: la raíz ya no vuelve a cambiarlo.
  document.querySelectorAll('.langs a[data-lang]').forEach(function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('wibblo.lang', a.getAttribute('data-lang')); } catch (e) {}
    });
  });

  // Pestañas de los tutoriales.
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tabs [role="tab"]'));
  function show(id) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === id;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById('tut-' + t.getAttribute('data-tab')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { show(t.getAttribute('data-tab')); });
    t.addEventListener('keydown', function (ev) {
      var d = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      var next = tabs[(i + d + tabs.length) % tabs.length];
      next.focus(); show(next.getAttribute('data-tab'));
    });
  });
  if (tabs.length) show(tabs[0].getAttribute('data-tab'));

  // Videos: tutoriales/videos.json (ver tutoriales/LEEME.md). Si un tutorial tiene video,
  // se muestra arriba y la guía con capturas queda plegada debajo.
  fetch(base + 'tutoriales/videos.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (videos) {
      Object.keys(videos || {}).forEach(function (id) {
        var v = videos[id], panel = document.querySelector('.tut[data-tutorial="' + id + '"]');
        if (!v || !panel) return;
        var file = typeof v.archivo === 'string' ? v.archivo : (v.archivo || {})[lang] || (v.archivo || {}).es;
        if (!file) return;
        var title = (v.titulo || {})[lang] || (v.titulo || {}).es || '';
        var slot = panel.querySelector('.video-slot');
        var video = document.createElement('video');
        video.controls = true; video.preload = 'metadata'; video.playsInline = true;
        video.src = base + 'tutoriales/videos/' + file;
        if (v.portada) video.poster = base + 'tutoriales/videos/' + v.portada;
        if (title) video.setAttribute('aria-label', (strings.video || 'Video') + ': ' + title);
        slot.appendChild(video);
        if (title) { var p = document.createElement('p'); p.textContent = title; slot.appendChild(p); }
        slot.hidden = false;
        var guide = panel.querySelector('.guide');
        if (guide) guide.open = false;
      });
    })
    .catch(function () {});

  // Galería en grande.
  var box = document.querySelector('.lightbox');
  if (box && box.showModal) {
    var img = box.querySelector('img'), cap = box.querySelector('.caption');
    document.querySelectorAll('a.sample').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        img.src = a.getAttribute('href');
        img.alt = cap.textContent = a.getAttribute('data-title');
        box.showModal();
      });
    });
    box.querySelector('.close').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (ev) { if (ev.target === box) box.close(); });
  }
})();
