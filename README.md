# wibblo.kaeliapps.com

Sitio de Wibblo, publicado con GitHub Pages desde este repo (rama `main`).

- `/` (`index.html`, español), `/en/`, `/fr/` y `/pt/`: página principal de
  Wibblo. Tiene estas secciones: inicio con las insignias oficiales de las
  tiendas, las 12 actividades, fichas de ejemplo, cómo funciona, tutoriales,
  Gratis y Pro, preguntas frecuentes y pie.
  - En el teléfono, la tienda que corresponde va primero y resaltada.
  - La raíz lleva a `/en/`, `/fr/` o `/pt/` a quien tiene el teléfono en esos
    idiomas, salvo que haya elegido idioma en el menú (se recuerda en el
    navegador).
- `/descargar/` (`descargar/index.html`): redirección a la tienda (iPhone/iPad →
  App Store, Android → Google Play, computadora → las dos insignias).
  `/download/` es su alias en inglés y lleva ahí.
- `/privacidad/`: política de privacidad de Wibblo (la que se declara en
  Google Play Console y la que abre la app desde Ajustes).

**No cambiar** `/privacidad/`: es la dirección registrada en App Store Connect
y Google Play. Los términos de uso son el EULA estándar de Apple.

## Editar la página principal

Las 4 páginas se arman con un script, sin dependencias (Python 3.9 o más nuevo):

```bash
python3 fuente/build.py
```

- **Textos:** `fuente/textos/<idioma>.json`. Los nombres y las descripciones de
  las actividades son los mismos de la app (`.arb`).
- **Estilos y comportamiento:** `estilos.css` y `sitio.js` (se editan directo,
  sin volver a armar).
- **Imágenes:**
  - `img/generadores/` y `img/mascota/`: íconos y mascota, tomados de la app.
  - `img/ejemplos/<es|en>/`: fichas reales; fr y pt muestran las de inglés.
  - `badges/`: insignias oficiales de Apple y Google por idioma.
- **Letras:** `fonts/`, con Fredoka y Nunito (SIL OFL) servidas desde este sitio,
  sin Google Fonts.
- **Tutoriales:** capturas de la app en `tutoriales/capturas/<idioma>/`. Para
  agregar un video basta con poner el archivo y su título, sin volver a armar
  la página: ver `tutoriales/LEEME.md`.

Reglas de los textos: nunca presentar Wibblo como algo para el aula, la escuela
o los maestros, en ningún idioma; nunca usar "Memory" ni "Memorama" (el juego
se llama Parejas / Pairs Game / Paires / Pares); no escribir "próximamente";
y no poner precios, porque cambian por país y por tienda.

El patrón (DNS, repos, cómo agregar otra app) está documentado en el README de
`kaelistudios.github.io`.
