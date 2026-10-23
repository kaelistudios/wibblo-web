# Tutoriales de wibblo.kaeliapps.com

Cada tutorial (bingo, sopa de letras, crucigrama, matemáticas y código secreto)
tiene una guía paso a paso con capturas de la app (`capturas/<idioma>/`). Si
tiene video, el video se muestra arriba y la guía queda plegada debajo.

## Agregar un video (no hace falta volver a armar la página)

1. Copia el archivo en `tutoriales/videos/`, por ejemplo `bingo.mp4`. Usa MP4
   (H.264), vertical u horizontal, corto (menos de 1 minuto) y de menos de 20 MB.
2. Agrega su entrada en `tutoriales/videos.json`, con su título:

```json
{
  "bingo": {
    "archivo": "bingo.mp4",
    "titulo": { "es": "Cómo hacer un bingo", "en": "How to make a bingo" }
  }
}
```

- Las claves posibles son `bingo`, `wordsearch` (sopa de letras), `crossword`
  (crucigrama), `math` (matemáticas) y `secretcode` (código secreto).
- Un video distinto por idioma: `"archivo": { "es": "bingo-es.mp4", "en": "bingo-en.mp4" }`.
  Un idioma sin video usa el de español.
- El título que falte en un idioma usa el de español.
- Imagen de portada opcional: `"portada": "bingo.webp"` (en la misma carpeta).

3. Commit y push: el video aparece en los 4 idiomas.
