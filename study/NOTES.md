# STUDY — field notes log

Running record of Aidan's feedback on the STUDY corner: what worked, what didn't,
and what should steer future field selection. Not built into the site — this is
the editorial memory behind `study.html`.

The content source of truth is the `GUIDES` list in
[`scripts/personal_corpus/build_study_guides.py`](../scripts/personal_corpus/build_study_guides.py).

---

## Selection guidance (steers the next batch)

_General principles Aidan has stated about what he wants more / less of._

- **Physics rated highest** — gravity-is-not-a-force was his favorite. Keep at least one
  hard-science field per batch.
- He wants a **quantum-gravity** follow-on: why general relativity and quantum mechanics
  contradict each other, and Claude's own reasoned opinion on the resolution. The field
  should take a *position* (the "argument" carries a genuine take), not survey the
  candidates neutrally.
- **Avoid ground he already owns.** The philology/Nietzsche field fell flat because he's
  read all of Nietzsche's primary work (incl. *Genealogy of Morality*). Before choosing a
  philosophy subject, check the read shelf — pick something genuinely *not yet crossed*,
  not a primer on an author he knows cold. The 20% philosophy slot should reach for the
  unfamiliar (a thinker/tradition off his shelf), not restate a favorite.

---

## Current fields — per-subject feedback

### 1. gravity-is-not-a-force — physics
- **Favorite of the batch.** Never thought of gravity this way.
- Salient line: "Spacetime tells matter how to move; matter tells spacetime how to curve."
- Wants to go **deeper** on the relativity↔quantum break. Quoted as the hook:
  > "Relativity describes spacetime as smooth and continuous; quantum theory describes a
  > world that is grainy, probabilistic, jittering at the smallest scales. … both theories
  > apply at once — and they flatly contradict each other … Einstein's curved spacetime is
  > almost certainly not the last word, but a breathtaking approximation of something deeper …
  > The shape of space, it seems, may itself be made of something — and we don't know what."
- **Request to Claude:** an AI is well-positioned to research/reason on *why* GR and QM don't
  agree — and to put forward its **own opinion** on the answer to this century-old problem.
  → Steer one of the next fields toward quantum gravity, with a genuine reasoned position in
    the "argument," not just a tour. (See selection guidance.)

### 2. how-good-got-two-meanings — philosophy/philology
- **Didn't like it** — knew it all already. Has read *all* of Nietzsche's primary work,
  including *On the Genealogy of Morality*. The field told him nothing new.

### 3. the-frontier-and-its-ghost — history
- Also interesting — landed as "the origins of our American spirit."

### 4. the-original-affluent-society — anthropology
- Very good. The point that landed hardest:
  > "Mobility punishes property — a thing you must carry on your back is a burden —
  > so they kept few possessions, and a person's standing was measured by what they
  > gave away, not what they held."

### 5. the-price-of-knowing — economics
- Interesting, but not groundbreaking — felt akin to Adam Smith's "invisible hand."
- What *did* land: the market being driven by **action, not the product/service** itself.
- Price reflects scarcity. And if there's no price yet, there's no existing market yet —
  no one knows the price or what people would pay, because they don't yet know they have
  *that* need. (The market only exists once the need is felt and priced.)

---

## Archive log

_Fields retired from the live index, with date and reason._

Mechanics: set `"archived": True` on the guide dict. The builder renders archived
fields to `study/archive/<slug>.html`, lists them in a navigable "Archive" section
on `study.html`, and leaves a redirect stub at the old `study/<slug>.html` path so
links already shared externally keep working.

| date | field | reason |
|------|-------|--------|
| 2026-06-06 | the-price-of-knowing | Batch 1 rotation. "Interesting, not groundbreaking." |
| 2026-06-06 | the-frontier-and-its-ghost | Batch 1 rotation. Liked it ("origins of the American spirit"). |
| 2026-06-06 | the-original-affluent-society | Batch 1 rotation. "Very good" — the give-away/property point. |
| 2026-06-06 | gravity-is-not-a-force | Batch 1 rotation. Favorite; succeeded by "What space is made of" (quantum gravity). |
| 2026-06-06 | how-good-got-two-meanings | Batch 1 rotation. Disliked — already knew it (read all of Nietzsche). |

## Batches

- **Batch 1** (fields 01–05, archived 2026-06-06): the-price-of-knowing, the-frontier-and-its-ghost,
  the-original-affluent-society, gravity-is-not-a-force, how-good-got-two-meanings.
- **Batch 2** (fields 06–10, live 2026-06-06): what-space-is-made-of (physics/quantum gravity —
  carries Claude's own reasoned position, per the gravity feedback), the-perennial-gale (Schumpeter,
  creative destruction — per the "markets are action" note), there-is-no-free-gift (Mauss, the gift —
  extends the affluent-society favorite), against-the-grain (James C. Scott — bridges Sahlins + Turner),
  empty-of-itself (Nāgārjuna — unfamiliar philosophy, NOT Nietzsche; rhymes with the quantum field).
