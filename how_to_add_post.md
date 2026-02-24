1. 直接複製（最簡單）

Obsidian 的 .md 檔案幾乎可以直接用，只需在開頭加上 frontmatter：

---

title: 文章標題
published: 2026-02-24
description: 文章簡介
tags: ['frontend', 'design']

---

這裡是內文...

把完成的筆記複製到 src/content/posts/ 就能發布。

2. 用 Obsidian Vault 直接指向 content 資料夾

在 Obsidian 設定中，把 vault 位置設定為 src/content/posts/，或用 symlink：

ln -s /path/to/obsidian/vault/blog src/content/posts

這樣在 Obsidian 寫完就直接同步，省去複製步驟。

3. 注意相容性問題

┌────────────────────┬─────────────────────────────────┐
│ Obsidian 語法 │ Astro 支援狀況 │
├────────────────────┼─────────────────────────────────┤
│ [[wikilinks]] │ ❌ 需轉換 │
├────────────────────┼─────────────────────────────────┤
│ ![[image.png]] │ ❌ 需改成標準 ![](image.png) │
├────────────────────┼─────────────────────────────────┤
│ #tag 行內 tag │ ❌ 改用 frontmatter tags │
├────────────────────┼─────────────────────────────────┤
│ callouts > [!NOTE] │ ✅ 你的 remark-admonitions 支援 │
├────────────────────┼─────────────────────────────────┤
│ LaTeX $$...$$ │ ✅ 你有 remark-math │
└────────────────────┴─────────────────────────────────┘

4. 圖片管理

將圖片放在 src/content/posts/ 同層或 public/images/，Obsidian 附件資料夾也可以 symlink 過去。

---

最推薦的方式：用 symlink 讓 Obsidian vault 直接對應 src/content/posts/，搭配一個 Obsidian 模板來自動生成
frontmatter，寫完後 git commit 即發布。
