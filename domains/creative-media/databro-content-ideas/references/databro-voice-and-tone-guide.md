# Databro Voice, Tone, and Fact-Checking Standards

This guide outlines the editorial style, Indonesian language conventions, and rigorous research rules for all Databro Studio content (@databroid).

---

## 1. Databro Persona and Voice

- **Core Identity**: The friendly, technically sharp senior peer who breaks down complex AI and data topics into clear, intuitive insights over coffee.
- **Audience**: Indonesian data analysts, software engineers, data science students, and tech enthusiasts.
- **Signature Tone**: Casual Bahasa Indonesia ("bro" tone) that is respectful, engaging, and grounded in practical reality.

### Language Rules & Vocabulary
- **Address Style**: Use "lu" and "bro" naturally and sparingly. Never sound forced, cringey, or overly slang-heavy.
- **Relatable Hooks**: Open with scenarios every practitioner recognizes:
  - *"Pernah gak lu ngalamin pas training model..."*
  - *"Sering denger istilah RAG, tapi sebenernya bedanya apa sama fine-tuning?"*
  - *"Banyak yang ngira data science itu cuma soal coding machine learning..."*
- **Technical English Terms**: Keep standard data and AI terminology in English rather than awkward translations:
  - Use `feature engineering` (not "rekayasa fitur")
  - Use `data leakage` (not "kebocoran data")
  - Use `overfitting` (not "kelebihan pengepasan")
  - Use `embeddings`, `vector search`, `loss function`, `benchmark`

---

## 2. Absolute Ban on Em-Dashes (The Zero Em-Dash Rule)

- **Strict Constraint**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in titles, slides, captions, or research notes.
- **Why**: Databro's clean typographic system strictly uses colons (`:`), hyphens (`-`), clean parentheses, or simple sentence breaks.
- **Examples**:
  - WRONG: `Agentic AI — Masa Depan Otomasi`
  - CORRECT: `Agentic AI: Masa Depan Otomasi`
  - WRONG: `Model ini cepat — bahkan di CPU biasa`
  - CORRECT: `Model ini cepat, bahkan di CPU biasa.`

---

## 3. Strict Fact-Checking & Anti-Hallucination Policy

Databro's reputation rests on technical rigor and intellectual honesty. Never fabricate or assume facts.

### The 4 Verification Rules:
1. **Never Assume or Extrapolate Numbers**:
   - If citing benchmark scores (e.g. MMLU, HumanEval, latency in ms), look up the exact numbers from the published paper or official documentation.
2. **Cite Primary Sources**:
   - For AI research: arXiv papers, official lab announcements (Anthropic, Google DeepMind, OpenAI, Meta).
   - For datasets: Kaggle dataset pages, BPS Indonesia, Stack Overflow Developer Survey, GitHub releases.
   - For industry cases: Official engineering blogs (Uber Engineering, Netflix TechBlog, Gojek Tech, etc.).
3. **Format Citations with Clickable URLs**:
   - Always conclude the idea with an explicit `Evidence & Verified Sources` section listing the title and URL of each source.
4. **Evergreen Exceptions**:
   - For pure mathematical derivations (e.g. Bayes Theorem, Normal Distribution) or standard Python tutorial mechanics (e.g. creating a boxplot with Seaborn), note: `"Source: Evergreen fundamentals"`.

