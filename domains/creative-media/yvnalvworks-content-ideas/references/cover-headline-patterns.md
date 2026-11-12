# yvnalvworks Cover Headline Patterns

The copy rules for carousel slide 1, taken from the two published yvnalvworks covers. Every carousel idea delivers a `coverHeadline` that follows these rules, so `/yvnalvworks-brand-motion` can render it straight onto the standard cover without rewriting.

## 1. Published references

| Cover headline (as broken on the slide) | Pattern | Lime highlight |
|---|---|---|
| 3 AI Updates / Every Builder / **Should Know** / in April 2026 | Numbered listicle with time anchor | The promise |
| What AI Engineers / Should Know / About **Microsoft / Agent Framework** | Audience question | The subject |

## 2. Formulas

| Use for | Formula | Example |
|---|---|---|
| Single tool, framework, paper, or release | `What [Audience] Should Know About [[Subject]]` | What CV Engineers / Should Know / About [[TensorRT 11]] |
| Monthly roundup or news digest | `[N] [Topic] Every [Audience] [[Should Know]] in [Month Year]` | 5 Edge AI Shifts / Every Builder / [[Should Know]] / in May 2026 |
| Curated resources (papers, repos, case studies) | `[N] [Things] [Audience] [[Should Read]]` | 7 Eval Papers / AI Engineers / [[Should Read]] |
| Failure mode or fix | `Why [[Subject]] Fails in Production` | Why Your / [[Edge Model]] / Fails in / Production |

The "Should Know" and "Should Read" audience promise is the house voice. Use the failure formula only when the content really is a diagnosis.

A bonus can go in the copy: "... Should Read (With Links)", "... With Code". The slide never gets a separate pill or badge.

## 3. Rules

1. **Title Case**, no trailing punctuation, no emoji, no em-dashes or en-dashes.
2. **6 to 10 words**, broken by hand into **3 to 4 lines** of about 2 to 3 words. Each line is at most **18 characters** including spaces (the cover headline is 96px; longer lines overflow). The limit is a ceiling, not a guarantee: wide letters (W, M, K, w) overflow sooner. "Should Know About" (17 characters) does **not** fit on one line; always break it as `Should Know` / `About [[Subject]]`, exactly like the published reference.
3. **Exactly one highlight phrase**, marked `[[...]]`: either the promise (`Should Know`, `Should Read`) or the subject (the tool or concept name). Never highlight a filler word, and never two phrases.
4. Put the highlighted phrase on its own line(s) where possible. `\n` marks a line break and may sit inside `[[...]]` when the subject spans two lines.
5. Name a **specific audience** (AI Engineers, CV Engineers, Builders, ML Teams), not "everyone" or "you guys".
6. Add a **time anchor** (`in April 2026`) to anything news-driven, so the post ages honestly.
7. Keep it 100% Technical English. Exact product names keep their official casing.

## 4. JSON form

```json
"coverHeadline": "What AI Engineers\nShould Know\nAbout [[Microsoft\nAgent Framework]]"
```

`scripts/format_content_idea.py` checks the line count, line length, and the single highlight.

## 5. Relation to the hook

The cover headline is a promise. The `hookStatement` (the counter-intuitive bold claim) is kept, but it opens the post caption and the reel's first spoken line. It is no longer printed on the cover.
