# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev        # Start dev server
npm run build      # Build site + generate Pagefind search index (postbuild)
npm run preview    # Preview production build
npm run format     # Format with Prettier
```

No test suite is configured.

## Architecture

This is an **Astro 5** static blog using the [MultiTerm](https://github.com/StelClementine/multiterm-astro) theme — a terminal/code-editor aesthetic blog.

### Configuration

`src/site.config.ts` is the single source of truth for site settings: metadata, themes, navigation, Giscus comments, social links, and page size. Most customization starts here.

`astro.config.mjs` wires up the markdown pipeline (11 custom remark/rehype plugins), Expressive Code for syntax highlighting, MDX, and sitemap.

### Content

Blog posts live in `src/content/` as Markdown/MDX files. The content schema is defined in `src/content.config.ts`.

### Custom Markdown Plugins (`src/plugins/`)

Eleven custom plugins extend standard Markdown:
- `remark-github-card` — embed GitHub repo cards
- `remark-admonitions` — callout/admonition blocks
- `remark-character-dialogue` — character speech bubbles
- `remark-pixelated` (rehype) — pixel-art image rendering
- `remark-math` + `rehype-katex` — LaTeX math rendering
- Plus description extraction, reading time, gemoji, external link attributes, title figures

### Theming

Controlled via `site.config.ts > themes`. Currently in `single` mode with `one-dark-pro` and `one-light`. Theme colors can be overridden in `themes.overrides`. Additional [Shiki themes](https://shiki.style/themes) can be added to `themes.include`.

### Key Integrations

- **Giscus** — GitHub Discussions-based comments, configured in `site.config.ts > giscus`
- **Pagefind** — client-side search, indexed after `astro build` via postbuild script
- **Satori** — social card image generation at `src/pages/social-cards/[slug].png.ts`

### Pages & Routes

- `src/pages/` — file-based routing; API routes for RSS (`rss.xml.ts`), robots (`robots.txt.ts`), Giscus themes (`giscus/[theme].css.ts`), and social cards
- `src/layouts/` — shared page layouts
- `src/components/` — Astro components