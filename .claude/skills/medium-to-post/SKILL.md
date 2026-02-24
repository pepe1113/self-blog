---
name: medium-to-post
description: "Converts a locally saved Medium HTML export into a blog post. Use this skill whenever the user wants to import, convert, or create a post from a file in medium_html/, or says 'build blog post', 'convert article', 'import all articles', or similar. Also triggers when given a Medium URL if local HTML files are available."
---

## Overview

Convert Medium-exported HTML files from `medium_html/` into properly formatted Markdown blog posts saved to `src/content/posts/{slug}/index.md`.

---

## Workflow

### Step 1 — Identify the Source File

All Medium HTML exports are in `medium_html/`. File naming convention:
```
{YYYY-MM-DD}_{encoded-title}-{id}.html
```

If the user specifies an article (by title, URL, or keyword), match it to the correct file with `ls medium_html/`. If the user says "all articles", process every file in the directory.

Already-imported posts have a folder in `src/content/posts/` — skip those unless the user asks to re-import.

---

### Step 2 — Parse the HTML

Run the bundled parser script:

```bash
python3 .claude/skills/medium-to-post/scripts/parse_html.py "medium_html/{filename}.html"
```

The script outputs sections delimited by `=== TITLE ===`, `=== PUBLISHED ===`, `=== DESCRIPTION ===`, `=== AUTHOR ===`, `=== IMAGES ===`, and `=== BODY ===`.

Read each section to get:
- **title** — exact article title
- **published** — ISO date (`YYYY-MM-DD`)
- **description** — subtitle/summary
- **author** — author name
- **images** — list of Medium CDN URLs, one per line
- **body** — article body already converted to Markdown

---

### Step 3 — Generate Tags

The HTML export does not include tags. Infer 2–5 tags from the title and body content:
- Lowercase, hyphens for multi-word (e.g. `front-end`, `javascript`)
- Prefer specific over generic

---

### Step 4 — Generate the Slug

Derive the slug from the title:
- Lowercase, replace spaces and special characters with hyphens
- Remove punctuation, collapse consecutive hyphens, strip leading/trailing hyphens

Example: `"來自 Behance 的 NFT 詐騙?!"` → `behance-nft-scam`

For non-Latin titles, transliterate or use meaningful English keywords from the content.

---

### Step 5 — Handle Images

1. Create `src/content/posts/{slug}/`
2. Try to download each image from the CDN URLs output by the parser:
   ```bash
   curl -sL "{url}" -o "src/content/posts/{slug}/image-{n}.{ext}"
   ```
   - Detect extension from URL (`.gif`, `.png`, `.jpg`); default to `.png`
   - After downloading, verify file size > 1KB — if smaller it's an error (Medium CDN may block downloads)
3. If download succeeds: replace CDN URL with local path `![alt](./image-1.png)`
   If download fails: keep the original CDN URL — browsers can still load it directly

**Note**: Medium's CDN (`cdn-images-1.medium.com`) often blocks non-browser requests regardless of headers. Keeping the original URL is an acceptable fallback — the image will still render in the published blog.

---

### Step 6 — Write the File

Write to `src/content/posts/{slug}/index.md`:

```markdown
---
title: "Article Title"
published: 2026-01-15
description: "Short summary."
tags: ['tag1', 'tag2']
author: "Author Name"
draft: false
---

[article body with local image paths]
```

If a folder with the same slug already exists, tell the user and ask whether to overwrite.

---

### Step 7 — Confirm

After saving, report:
- File path
- Title, date, tags
- Images: downloaded N / total M (note any failures)

When processing multiple files, show a summary table at the end.
