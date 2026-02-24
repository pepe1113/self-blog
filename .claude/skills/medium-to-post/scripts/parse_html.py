#!/usr/bin/env python3
"""
Parse a Medium-exported HTML file and print structured content:
- Metadata (title, date, description, author)
- Article body as Markdown
- All image URLs

Usage:
    python3 parse_html.py <path/to/article.html>
"""

import sys
import re
from html.parser import HTMLParser
from datetime import datetime


def strip_tags(html):
    """Remove all HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', html)


def parse_medium_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Metadata ---
    title_m = re.search(r'<h1[^>]*class="p-name"[^>]*>(.*?)</h1>', content, re.S)
    title = strip_tags(title_m.group(1)).strip() if title_m else ''

    subtitle_m = re.search(r'<section[^>]*data-field="subtitle"[^>]*>(.*?)</section>', content, re.S)
    description = strip_tags(subtitle_m.group(1)).strip() if subtitle_m else ''

    time_m = re.search(r'<time[^>]*datetime="([^"]+)"', content)
    published = ''
    if time_m:
        try:
            published = datetime.fromisoformat(time_m.group(1).replace('Z', '+00:00')).strftime('%Y-%m-%d')
        except Exception:
            published = time_m.group(1)[:10]

    author_m = re.search(r'class="p-author h-card"[^>]*>(.*?)</a>', content)
    author = strip_tags(author_m.group(1)).strip() if author_m else ''

    # --- Body ---
    body_m = re.search(r'<section[^>]*data-field="body"[^>]*>(.*?)</section>\s*</section>', content, re.S)
    body_html = body_m.group(1) if body_m else content

    # Convert to Markdown
    md = html_to_markdown(body_html)

    # --- Images ---
    images = re.findall(r'src="(https://cdn-images-1\.medium\.com/[^"]+)"', content)
    # deduplicate preserving order
    seen = set()
    unique_images = []
    for img in images:
        if img not in seen:
            seen.add(img)
            unique_images.append(img)

    print("=== TITLE ===")
    print(title)
    print("\n=== PUBLISHED ===")
    print(published)
    print("\n=== DESCRIPTION ===")
    print(description)
    print("\n=== AUTHOR ===")
    print(author)
    print("\n=== IMAGES ===")
    for img in unique_images:
        print(img)
    print("\n=== BODY ===")
    print(md)


def html_to_markdown(html):
    """Convert Medium HTML body to Markdown."""
    # Headings
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f'\n## {strip_tags(m.group(1)).strip()}\n', html, flags=re.S)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', lambda m: f'\n### {strip_tags(m.group(1)).strip()}\n', html, flags=re.S)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: f'\n# {strip_tags(m.group(1)).strip()}\n', html, flags=re.S)

    # Blockquotes
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: f'\n> {strip_tags(m.group(1)).strip()}\n', html, flags=re.S)

    # Code blocks
    def code_block(m):
        lang_m = re.search(r'data-code-block-lang="([^"]+)"', m.group(0))
        lang = lang_m.group(1) if lang_m else ''
        code = strip_tags(m.group(1)).strip()
        # unescape common HTML entities
        code = code.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('<br />', '\n').replace('<br/>', '\n').replace('<br>', '\n')
        return f'\n```{lang}\n{code}\n```\n'
    html = re.sub(r'<pre[^>]*>(.*?)</pre>', code_block, html, flags=re.S)

    # Inline code
    html = re.sub(r'<code[^>]*>(.*?)</code>', lambda m: f'`{strip_tags(m.group(1))}`', html, flags=re.S)

    # Bold / italic
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', lambda m: f'**{strip_tags(m.group(1))}**', html, flags=re.S)
    html = re.sub(r'<em[^>]*>(.*?)</em>', lambda m: f'*{strip_tags(m.group(1))}*', html, flags=re.S)

    # Links
    html = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f'[{strip_tags(m.group(2))}]({m.group(1)})', html, flags=re.S)

    # Images with optional captions
    def image_tag(m):
        src = re.search(r'src="([^"]+)"', m.group(0))
        cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', m.group(0), re.S)
        alt = strip_tags(cap.group(1)).strip() if cap else ''
        url = src.group(1) if src else ''
        return f'\n![{alt}]({url})\n'
    html = re.sub(r'<figure[^>]*>.*?</figure>', image_tag, html, flags=re.S)

    # Lists
    html = re.sub(r'<ul[^>]*>(.*?)</ul>', lambda m: m.group(1), html, flags=re.S)
    html = re.sub(r'<ol[^>]*>(.*?)</ol>', lambda m: m.group(1), html, flags=re.S)
    html = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f'- {strip_tags(m.group(1)).strip()}\n', html, flags=re.S)

    # Paragraphs
    html = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: f'\n{strip_tags(m.group(1)).strip()}\n', html, flags=re.S)

    # <br>
    html = re.sub(r'<br\s*/?>', '\n', html)

    # HR
    html = re.sub(r'<hr[^>]*/?>',  '\n---\n', html)

    # Strip remaining tags
    html = re.sub(r'<[^>]+>', '', html)

    # Unescape HTML entities
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')

    # Collapse 3+ blank lines into 2
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_html.py <file.html>")
        sys.exit(1)
    parse_medium_html(sys.argv[1])
