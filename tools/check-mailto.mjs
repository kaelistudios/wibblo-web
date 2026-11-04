#!/usr/bin/env node
// Revisa todos los enlaces mailto de los .html de este sitio (sin dependencias).
//
//   node tools/check-mailto.mjs
//
// Cada mailto debe:
//   - ir a la dirección permitida (ver ALLOWED),
//   - tener el asunto «[<Nombre>] » (con el espacio al final),
//   - tener el cuerpo "\n\n\n—\n<Nombre> web · <idioma>", con el idioma de la página
//     (el atributo lang más cercano antes del enlace),
//   - codificar los espacios como %20, nunca '+' (el '+' solo vale en la dirección).
// Además, ningún archivo puede seguir usando wearekaeli@gmail.com.
// Termina con código 1 si encuentra algún problema.
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Direcciones que este sitio puede usar → nombre visible de la app.
export const ALLOWED = {
  'soporte+wibblo@kaeliapps.com': 'Wibblo',
};
const OLD_ADDRESS = 'wearekaeli@gmail.com';
const SKIP_DIRS = new Set(['.git', 'node_modules']);

function decodeEntities(s) {
  return s
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);

/** Idioma del elemento abierto más cercano (con atributo lang) que contiene la posición. */
export function langAt(html, pos) {
  const stack = [];
  const re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][\w-]*)([^>]*)>/g;
  let m;
  while ((m = re.exec(html)) && m.index < pos) {
    if (!m[2]) continue;
    const tag = m[2].toLowerCase();
    if (m[1]) {
      const i = stack.map((e) => e.tag).lastIndexOf(tag);
      if (i >= 0) stack.length = i;
    } else if (!VOID.has(tag) && !m[3].trim().endsWith('/')) {
      const l = /(?:^|\s)lang\s*=\s*["']([a-zA-Z]{2})/.exec(m[3]);
      stack.push({ tag, lang: l ? l[1].toLowerCase() : null });
      if (tag === 'script' || tag === 'style') {
        const end = html.toLowerCase().indexOf(`</${tag}`, re.lastIndex);
        if (end >= 0 && end < pos) re.lastIndex = end;
      }
    }
  }
  for (let i = stack.length - 1; i >= 0; i--) if (stack[i].lang) return stack[i].lang;
  return null;
}

/** Devuelve la lista de problemas de un HTML (texto). */
export function checkHtml(html, allowed = ALLOWED) {
  const problems = [];
  if (html.includes(OLD_ADDRESS)) problems.push(`todavía aparece ${OLD_ADDRESS}`);
  const re = /href\s*=\s*(["'])(mailto:[^"']*)\1/gi;
  let m;
  let count = 0;
  while ((m = re.exec(html))) {
    count++;
    const href = decodeEntities(m[2]);
    const line = html.slice(0, m.index).split('\n').length;
    const where = `línea ${line}`;
    const lang = langAt(html, m.index);

    const q = href.indexOf('?');
    const to = decodeURIComponent(href.slice('mailto:'.length, q < 0 ? undefined : q));
    const query = q < 0 ? '' : href.slice(q + 1);
    const name = allowed[to];
    if (!name) {
      problems.push(`${where}: dirección no permitida «${to}»`);
      continue;
    }
    if (query.includes('+')) problems.push(`${where}: hay '+' en el asunto o el cuerpo (los espacios van como %20)`);
    const params = {};
    for (const part of query.split('&').filter(Boolean)) {
      const i = part.indexOf('=');
      const k = (i < 0 ? part : part.slice(0, i)).toLowerCase();
      try {
        params[k] = decodeURIComponent(i < 0 ? '' : part.slice(i + 1));
      } catch {
        problems.push(`${where}: «${k}» mal codificado`);
      }
    }
    if (params.subject !== `[${name}] `) {
      problems.push(`${where}: asunto ${JSON.stringify(params.subject)}, se esperaba ${JSON.stringify(`[${name}] `)}`);
    }
    if (!lang) {
      problems.push(`${where}: no se sabe el idioma de la página (falta lang)`);
    } else {
      const body = `\n\n\n—\n${name} web · ${lang}`;
      if (params.body !== body) {
        problems.push(`${where}: cuerpo ${JSON.stringify(params.body)}, se esperaba ${JSON.stringify(body)}`);
      }
    }
  }
  return { count, problems };
}

function htmlFiles(dir) {
  const out = [];
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(ent.name)) continue;
    const p = join(dir, ent.name);
    if (ent.isDirectory()) out.push(...htmlFiles(p));
    else if (ent.name.endsWith('.html')) out.push(p);
  }
  return out.sort();
}

if (resolve(process.argv[1] || '') === fileURLToPath(import.meta.url)) {
  const root = resolve(fileURLToPath(import.meta.url), '..', '..');
  let total = 0;
  let bad = 0;
  for (const file of htmlFiles(root)) {
    const { count, problems } = checkHtml(readFileSync(file, 'utf8'));
    total += count;
    const rel = relative(root, file);
    if (count) console.log(`${problems.length ? '✗' : '✓'} ${rel}: ${count} mailto`);
    for (const p of problems) {
      bad++;
      console.log(`  ${rel}: ${p}`);
    }
  }
  if (!total) {
    console.log('✗ no se encontró ningún mailto');
    bad++;
  }
  console.log(bad ? `\n${bad} problema(s).` : `\nTodo bien: ${total} mailto revisados.`);
  process.exitCode = bad ? 1 : 0;
}
