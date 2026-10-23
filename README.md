# wibblo.kaeliapps.com

Sitio de Wibblo, publicado con GitHub Pages desde este repo:

- `/` (`index.html`): página a la que lleva el QR de los PDF. En Android
  redirige a Google Play; en iPhone/iPad, al App Store
  (https://apps.apple.com/app/id6819557562); en computadora o sin JavaScript
  muestra los dos botones.
- `/descargar/` (`descargar/index.html`): la misma redirección a la tienda que la
  raíz (iPhone/iPad → App Store, Android → Google Play, computadora → las dos
  insignias). `/download/` es su alias en inglés y lleva ahí.
- `/privacidad/`: política de privacidad de Wibblo (la que se declara en
  Google Play Console y la que abre la app desde Ajustes).

**No cambiar** `/privacidad/`: es la dirección registrada en App Store Connect
y Google Play. Los términos de uso son el EULA estándar de Apple.

El patrón (DNS, repos, cómo agregar otra app) está documentado en el README de
`kaelistudios.github.io`.
