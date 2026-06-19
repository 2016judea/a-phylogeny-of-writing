---
name: primary-source-library
description: SCOPE/Build a full-text library of every book Aidan has read so Claude reasons on the primary sources themselves (actual passages), not academic summaries. Use when he wants analysis grounded in the books' real text — quotes, cross-book theme tracing, prose comparison.
---

# Primary-Source Library  ·  *scoped 2026-06-04, not yet built*

**Goal:** let Claude reason about Aidan's reading from the *actual text* of the
books — pulling real passages, comparing prose, tracing a theme across authors —
instead of leaning on critics' opinions. Source of the booklist: the
`reading_library` Notion DB / `data/personal_corpus/goodreads_reads.json` (310
dated reads, ~480 shelved).

## The hard constraint, stated up front

310 books ≈ **30–40M words ≈ ~45–55M tokens**. That will never fit in one context
window (today's max is ~1M). So "load every book into context" is **retrieval**,
not a single paste. The skill builds a local full-text corpus and pulls the
relevant passages on demand. Design for RAG from day one.

## Sourcing — split the list by copyright (this decides everything)

1. **Public domain (free, auto-fetchable).** A large slice of his canon —
   Melville, Dostoevsky, pre-1929 Joyce/Fitzgerald, Wilde, Austen, Poe, Whitman,
   the Romantic poets, Homer, Plato, Nietzsche, Thoreau, Wells, etc. Sources, in
   order of cleanliness: **Standard Ebooks** (best-formatted) → **Project
   Gutenberg** → **Internet Archive**. Probably ~40–50% of his list.
2. **In-copyright (NOT free; user must supply).** McCarthy, Bret Easton Ellis,
   DFW, Denis Johnson, Hemingway, Faulkner, most 20th–21st-c. fiction. These
   cannot be auto-fetched legally. Aidan supplies his **own legally-owned copies**
   (Kindle/Apple Books/Kobo EPUBs he purchased), used **privately for personal
   analysis only — never redistributed**. Kindle files are DRM'd; he'd export/
   convert his owned EPUBs himself. The skill must encode this guardrail and
   never scrape pirated full texts.

→ First build step is a **manifest**: for each of the 310, resolve `public_domain`
(with a Standard Ebooks / Gutenberg id) vs `needs_owned_copy`. That tells us how
much is free vs. blocked on Aidan.

## Architecture (phased)

**Phase 1 — Public-domain corpus (free, immediate, do this first).**
- `scripts/personal_corpus/fetch_primary_texts.py` — read the manifest, download
  the PD titles, strip Gutenberg/Standard-Ebooks boilerplate, store as
  `data/primary_texts/<slug>.txt` (gitignore this dir — it's large).
- Even just the PD half is enough to start grounded reasoning on the classics.

**Phase 2 — Owned-copy ingest.** A small `ingest_epub.py` that takes Aidan's
EPUB/TXT files (a drop folder), converts to plain text, stores alongside. Covers
the copyright titles he owns.

**Phase 3 — Retrieval layer (makes it usable).**
- **Exact-quote / keyword:** `ripgrep` over `data/primary_texts/` — instant, zero
  infra, great for "find every passage about X / where does McCarthy use 'sacrament'".
- **Semantic:** chunk (~1–2k tokens, overlap) → embed → local vector store
  (`sqlite-vec` or FAISS; embeddings via a small local model or an API). Lets the
  agent retrieve thematically-related passages across books without keywords.
- Index ties each chunk back to its `reading_library` row (title, author, read_year)
  so retrieval is filterable by when he read it.

**Phase 4 — Reasoning patterns the skill enables.**
- Theme tracing: "how does the idea of determinism move from Nietzsche →
  McCarthy → his own *a_higher_power*?" → retrieve passages from each, compare.
- Prose lineage: quantify how his writing's diction tracks McCarthy vs Ellis
  (he already has `2016judea/Prose-Similarities` — reuse that NLP approach).
- Grounded answers: every claim cites a real passage, not a critic.

## What to decide before building

1. **Scope of v1** — PD-only (free, ~150 books) vs wait for owned copies too?
   Recommend: build Phase 1 PD now; add owned copies as Aidan provides them.
2. **Retrieval** — ripgrep-only (zero setup, exact text) vs add embeddings
   (semantic, needs a vector store + embed budget). Recommend ripgrep first,
   embeddings when cross-book *semantic* search is the bottleneck.
3. **Storage/legal** — confirm `data/primary_texts/` stays local + gitignored;
   copyright texts are Aidan's own copies, private use only.

## Related

Booklist + dates: [[project-personal-corpus]], [[goodreads-fetch]]. Analysis that
would consume this: [[intellectual-history-analysis]] (today it reasons from
titles/authors; with this library it reasons from the text). Prior art in Aidan's
GitHub: `Prose-Similarities`, `literature-mutations`, `Novel_NLP_Analyzer`.

## References

**Uses:** [[goodreads-fetch]]
**See also:** [[study-guide]]
**Used by:** [[intellectual-history-analysis]]
