// Ajuste único del sitio de Wibblo.
// ANDROID_DISPONIBLE = false mientras Google no apruebe Wibblo en producción:
//   - la página principal muestra «Próximamente en Google Play» en lugar de la insignia de Google;
//   - /descargar/ en Android muestra ese mensaje y el enlace a la página principal (iPhone/iPad
//     siguen yendo al App Store).
// El día que Google apruebe producción: cambiar a true, commit y push. Vuelven la insignia y la
// redirección a Google Play.
var ANDROID_DISPONIBLE = false;
if (!ANDROID_DISPONIBLE) document.documentElement.className += ' android-soon';
