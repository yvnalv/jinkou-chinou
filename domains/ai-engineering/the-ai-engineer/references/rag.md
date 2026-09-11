# Retrieval-Augmented Generation (RAG)

How to build retrieval that finds the right evidence, generation that stays faithful to it, and evals for both.

## Contents

1. When to use RAG
2. Ingestion
3. Retrieval
4. Generation and citations
5. Permissions, freshness, and safety
6. Agentic retrieval
7. Evaluation
8. Common failures

---

## 1. When to use RAG

Use retrieval when answers depend on knowledge that is **private, large, or changing**: policies, product data, tickets, code, documentation. It keeps facts updatable and auditable without retraining.

Alternatives to consider first:

* **Whole document in context** for small, stable corpora that fit comfortably in the context window (with caching, this can be cheaper than a retrieval stack).
* **Structured lookup** (SQL, an API, a search engine the company already runs) when the data is tabular or already indexed; let the model call it as a tool.
* **Fine-tuning** is for form and behavior, not for facts that change (`references/fine-tuning.md`).

## 2. Ingestion

| Step | Guidance |
|---|---|
| Parsing | Extract text faithfully from PDFs, HTML, office files, and tables; keep headings, lists, and table structure. Bad parsing is the most common silent RAG failure; inspect samples |
| Cleaning | Remove boilerplate (navigation, footers), deduplicate near-identical documents, normalize whitespace and encoding |
| Chunking | Split on document structure (sections, paragraphs) before falling back to size limits. Start around a few hundred tokens with modest overlap, then tune with the retrieval eval |
| Contextual chunks | Prepend each chunk with its document title, section path, and a one- or two-sentence summary of where it sits in the document, so a chunk like "The limit is 30 days" still says *which* limit |
| Metadata | Source, URL, title, section, date, version, language, product, and **access-control labels**; used for filtering, citations, and freshness |
| Embeddings | Choose an embedding model with an eval on your queries (languages, domain terms, code); keep the model and dimensions recorded, because changing them means re-indexing |
| Updates | Incremental re-indexing on change, deletion propagation, and versioned indexes so you can roll back |

## 3. Retrieval

A strong default pipeline:

```text
query → (rewrite / expand) → hybrid search (keyword BM25 + vector) → fuse (reciprocal rank fusion)
      → metadata and permission filters → rerank top ~50–100 with a cross-encoder → keep top ~5–10 → generate
```

* **Hybrid search** consistently beats vector-only or keyword-only retrieval: vectors catch meaning, keywords catch exact terms (product codes, error messages, names).
* **Reranking** with a cross-encoder model is usually the largest single precision gain.
* **Query rewriting** helps multi-turn chats ("what about the other one?" → a self-contained query) and short or ambiguous queries; multiple sub-queries help compound questions.
* **Filters** (date, product, language, permissions) are applied at query time, not trusted to the model.
* Tune `k` and chunk size with the retrieval eval, not by feel.

## 4. Generation and citations

* Put retrieved chunks in a labelled documents section with IDs, titles, and dates; ask the model to answer **only** from them and to cite the document IDs it used.
* Instruct an explicit **"not found" behavior**: say the documents don't cover it, rather than falling back to general knowledge, unless the product allows that and labels it.
* Check citations programmatically where possible (cited IDs exist in the retrieved set; quoted text appears in the source).
* Show sources to users so they can verify.

## 5. Permissions, freshness, and safety

* **Enforce access control at retrieval**, using the end user's identity. A RAG system that can read everything leaks everything.
* Record document dates and prefer or require recent versions for time-sensitive topics; expire superseded content.
* **Retrieved content is untrusted input.** Documents, web pages, emails, and tickets can contain prompt-injection text. Never let retrieved text grant permissions or trigger tools without the controls in `references/security-and-safety.md`.
* Watch for vector-store weaknesses: poisoned documents inserted into the corpus, embedding inversion of sensitive text, and cross-tenant leakage in shared indexes.

## 6. Agentic retrieval

When retrieval is a tool the model calls (search, read document, follow link), the model decides what and when to retrieve:

* Better for multi-hop questions and exploration; slower, costlier, and harder to evaluate.
* Give the search tool good descriptions, filters as parameters, and compact result formats (title, snippet, ID), with a separate tool to read full documents.
* Cap the number of searches; log queries for error analysis.
* Evaluate the trajectory as well as the answer: were the right searches made, and did the model stop when it had enough?

## 7. Evaluation

Evaluate retrieval and generation **separately**, so you know which one to fix.

| Stage | Metric | How |
|---|---|---|
| Retrieval | Recall@k (were the needed chunks retrieved?) | Labelled query → relevant-chunk IDs; `retrieval_recall` grader in `scripts/eval_runner.py` |
| Retrieval | Precision, MRR, nDCG (are good chunks ranked high?) | Same labels; compute over the ranked list |
| Generation | Faithfulness / groundedness (is every claim supported by the retrieved context?) | LLM judge (`assets/llm_judge.template.py` with a faithfulness criterion), calibrated on human labels |
| Generation | Answer correctness and completeness | Reference answers with code checks or a judge |
| Generation | Citation accuracy | Cited IDs ⊆ retrieved IDs; quoted text found in source |
| End to end | "Not found" behavior | Cases whose answer is not in the corpus must produce an honest refusal |

Build the labelled set from real user questions (logs, support tickets), plus synthetic questions generated from documents and checked by a human. Include questions that need multiple chunks, exact-term queries, outdated-versus-current conflicts, and unanswerable questions.

## 8. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Right document exists but isn't retrieved | Parsing lost text, chunk lacks context, vocabulary mismatch | Fix parsing, contextual chunks, hybrid search, query rewriting |
| Retrieved but answer still wrong | Too many noisy chunks, conflicting versions, weak instruction | Rerank and trim, date filters, "answer only from documents" with citations |
| Confident answers to unanswerable questions | No "not found" instruction or eval cases | Add the behavior and cases |
| Users see documents they shouldn't | Permissions not enforced at retrieval | ACL filters with the user's identity |
| Quality drops over time | Stale index, new document types, drifting queries | Re-index on change, monitor retrieval metrics, add new failure cases to the eval |
