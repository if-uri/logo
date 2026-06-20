# ifuri — logo & brand package

A language-agnostic URI → handler adapter. The mark is a **conditional fork on a URI path**: a short
branch meeting a slash at a right angle (the `if` — the policy decision) flowing into a parallel `//`
(the URI). It encodes what the runtime does: *evaluate, then route*.

**Motto:** `name it run it`

## Folder structure

```
ifuri-logo/
├── README.md            this file
├── COLORS.md            colour system + tokens guide
├── color/               tokens.json · tokens.css · tokens.scss · tailwind.colors.js · palette.svg/png
├── svg/                 vector source (text outlined — no fonts needed)
│   ├── icon/            icon · icon-light · icon-mono · favicon · favicon-tiny
│   ├── mark/            bare mark (colour + mono)
│   ├── wordmark/        wordmark (light + dark)
│   └── lockup/          horizontal · tagline · stacked  (light / dark / mono)
├── png/                 raster, organised by size
│   ├── icon/16x16 … 1024x1024
│   ├── favicon/16x16 · 32x32 · 48x48 · apple-touch-icon-180 · icon-192 · icon-512
│   ├── mark/ · wordmark/ · lockup/ (by width: 400/800/1200/1600)
│   └── icon-light/ · icon-mono/
├── webp/                icon + key lockups (web-optimised)
├── pdf/                 vector for print (icon, mark, lockups)
└── ico/                 favicon.ico (16/32/48/64 multi-size)
```

## Which file do I use?

| Need | File |
|------|------|
| Website favicon | `ico/favicon.ico` + `png/favicon/*` + `svg/icon/ifuri-favicon.svg` |
| App / store icon | `png/icon/512x512` or `1024x1024`, `svg/icon/ifuri-icon.svg` |
| Tiny UI (≤16 px) | `svg/icon/ifuri-favicon-tiny.svg` (fork-only, stays legible) |
| Site header (light bg) | `svg/lockup/ifuri-lockup-horizontal.svg` |
| Site header (dark bg) | `svg/lockup/ifuri-lockup-horizontal-dark.svg` |
| With tagline | `svg/lockup/ifuri-lockup-tagline*.svg` |
| Centered / hero | `svg/lockup/ifuri-lockup-stacked*.svg` |
| Print | `pdf/*` |
| Single-colour / stamp | `*-mono.svg` |

## Colour
See `COLORS.md`. Tokens live in `color/`. TL;DR — primary `#4F46E5`,
accent `#10B981` (light) / `#34D399` (dark),
ink `#1E1B4B`.

## Type
Wordmark + motto are **Poppins** (Medium / Regular), outlined into the SVGs, so no font ships with
your site. For matching UI text, install Poppins or any geometric sans.

## Usage
- **Clear space:** ≥ the height of the mark's branch around the whole lockup.
- **Min size:** full mark to ~20 px; below that use `ifuri-favicon-tiny.svg`.
- **Don't:** recolour `if`/`uri` arbitrarily, rotate/skew the mark, add shadows/effects, or place the
  colour mark on a low-contrast background — use the `-dark` or `-mono` variants instead.

## Regenerate
`build2.py` builds every SVG, token file and the palette from the standardized tokens at the top of
the script. Change `MOTTO` or any ramp there and re-run, then re-export rasters.

## Site & deploy
- `make site` — `scripts/build_site.py` assembles the brand gallery into `_site/`
  (copies `svg/ png/ ico/ color/ pdf/ webp/`, generates `index.html` + `style.css`).
- `make deploy` — `scripts/deploy-plesk.sh` builds `_site/` then rsyncs it to **logo.ifuri.com**
  (Plesk). Override host/docroot via `IFURI_DEPLOY_HOST` / `IFURI_LOGO_DOCROOT`.

## Related projects

- Website: [ifuri.com](https://ifuri.com)
- Runtime: [tellmesh/urirun](https://github.com/tellmesh/urirun)
- Public docs: [if-uri/docs](https://github.com/if-uri/docs)
- Connector hub: [connect.ifuri.com](https://connect.ifuri.com)
- Installer: [get.ifuri.com](https://get.ifuri.com)
- Examples: [if-uri/examples](https://github.com/if-uri/examples)
- Current work summary:
  [work-summary-2026-06-20](https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md)

Repository notes: [TODO.md](TODO.md) · [CHANGELOG.md](CHANGELOG.md)


## License

Licensed under Apache-2.0.
