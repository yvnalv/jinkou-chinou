# Databro Voice, Tone, and Fact-Checking Standards

This guide outlines the editorial style, Indonesian language conventions, and rigorous research rules for all Databro Studio content (@databroid / @databro.id).

**Contents:** 1. Persona and voice · 2. Storytelling voice (hook, story arc, sentence rhythm, AI-ish patterns, honesty, worked example) · 3. Full Spectrum audience · 4. Editorial constraints · 5. Zero em-dash rule · 6. Fact-checking

---

## 1. Databro Persona and Voice

- **Core Identity**: The friendly, technically sharp senior peer who breaks down complex AI and data topics into clear, intuitive insights over coffee.
- **Tagline**: *Belajar Data Science*
- **Audience**: Full Spectrum (orang awam dengan nol latar belakang teknis, pemula/mahasiswa IT, hingga data scientist dan engineer senior).
- **Signature Tone**: Casual Bahasa Indonesia ("bro" tone) yang elegan tapi santai, numbers-led, dan berbasis data nyata (genuine).

### Language Rules & Vocabulary
- **Strict Pronoun Guardrails (Non-Negotiable)**:
  - **Banned Pronouns**: Strictly NEVER use `"Lu"`, `"Lo"`, `"Loe"`, or `"Gue"`. They sound overly informal and conflict with Databro's respected educational identity.
  - **Required Second-Person Address**:
    - **`"Kamu"` (Default)**: Warm, friendly, approachable tech mentor speaking directly to a learner (*"laptop kamu"*, *"model ML kamu"*, *"supaya kamu gak bingung"*).
    - **`"Anda"` (Formal / Enterprise)**: Use when discussing enterprise SLAs, enterprise architecture, or formal business scenarios.
    - **`"Kalian"` / `"Teman-teman"` (Plural)**: When addressing the wider audience or community (*"buat kalian yang mau belajar"*).
  - **First-Person Address**:
    - **`"Kita"` (Default)**: Inclusive and collaborative for walkthroughs and explainers (*"Yuk kita coba setup"*, *"Sekarang kita cek di terminal"*).
    - **`"Saya"` / `"Databro"`**: For official announcements or brand sign-offs.
  - **The "Bro" Salutation**:
    - The word **`"Bro"`** is preserved as an energetic brand greeting and closing punctuation (*"Bro, tahu nggak sih..."*, *"Belajar bareng Databro!"*, *"Simpelnya gini, bro."*).
    - **Never confuse `"Bro"` with the pronoun `"Lo"`**: Always pair with `"kamu"` (e.g. *"Bro, model ML kamu..."*, NEVER *"Bro, model ML lo..."*).
- **Relatable Everyday Hooks**: Open with scenarios every human or practitioner recognizes:
  - *"Pernah merhatiin ngga, bro... kenapa restoran paling enak sering ada di gang sempit?"*
  - *"Bro, pernah ngga model machine learning kamu akurasinya tinggi pas latihan, tapi pas di-deploy langsung jeblok?"*
  - *"Banyak yang ngira data science itu cuma soal coding machine learning..."*
- **Technical English Terms**: Keep standard data and AI terminology in English rather than awkward translations:
  - Use `feature engineering` (not "rekayasa fitur")
  - Use `data leakage` (not "kebocoran data")
  - Use `overfitting` (not "kelebihan pengepasan")
  - Use `embeddings`, `vector search`, `loss function`, `benchmark`

---

## 2. Storytelling Voice (All Content)

Every Databro piece (reels script, carousel, caption, article) is a **story**: a hook that opens a question in the first 2 to 3 seconds, then a flowing narrative that answers it. It should sound like a friend explaining over coffee, never like an AI reading a list of facts.

### 2.1 The hook (first 2 to 3 seconds)
- The **first sentence is the hook: at most 9 words** (about 2 to 3 seconds when spoken). It is also the first line of the post caption and matches the cover.
- It opens a question, a surprise, or a relatable moment, and the payoff later in the story answers it.
- Good: *"Ngobrol sama AI pakai bahasa Indonesia ternyata lebih boros, bro."*, *"AI Engineer ternyata jarang ngelatih model sendiri."*, *"Restoran paling enak kok sering di gang sempit?"*
- Weak: a definition (*"Token adalah satuan terkecil dalam..."*), a greeting with no tension (*"Halo semuanya, kali ini kita bahas..."*), or a long setup sentence.

### 2.2 The story arc
| Beat | Reels (45 to 75 s) | What happens |
|---|---|---|
| Hook | 0 to 3 s | One short line that opens the question. |
| Setup | 3 to 12 s | The everyday moment where the topic shows up ("Waktu kamu ngetik pesan ke ChatGPT..."). |
| Discovery | 12 to 50 s | How it really works, told as cause and effect. Facts and numbers appear as things that *happen* ("waktu kita coba di tokenizer GPT-4o, kata ini kepotong jadi dua"). |
| Payoff | 50 to 60 s | The moment that answers the hook. |
| Takeaway + CTA | last 8 to 12 s | One practical thing to do, then the save/follow line. |

Carousels use the same arc across slides: cover = hook, the middle slides = setup and discovery, the takeaway slide = payoff.

### 2.3 Sentence rhythm (spoken Indonesian)
- Write **flowing spoken sentences of about 10 to 22 words** that carry cause and consequence with connectors: *karena, jadi, makanya, ternyata, padahal, terus, waktu, sampai, supaya*.
- Allow **at most one short punch sentence (5 words or fewer) per beat**, used for emphasis ("Cara motongnya juga unik."). Never stack short sentences.
- Numbers and comparisons are told inside a sentence, not dictated with colons ("ML Engineering: data, model, produk." reads like a slide, not speech).
- Keep it casual and real: *nggak, gimana, kepotong, ngetik*, "kamu/kita", technical terms in English and explained the first time.
- Read every line out loud. If it sounds like a list being read, rewrite it.

### 2.4 AI-ish patterns to avoid
`scripts/format_content_idea.py` flags many of these as `styleWarnings`.
- **Stacked short sentences**: *"Model tidak membaca kata. Model membaca token. Token itu angka."*
- **Colon reveals and dictated lists**: *"Jawabannya: token."*, *"Paling atas: application development, prompt, konteks, dan interface."*
- **Mechanical enumeration** in voiceover: *"Pertama, ... Kedua, ... Ketiga, ..."* (on-screen numbering is fine; the voice tells it as a flow).
- **Stock phrases**: *"Di era digital ini"*, *"Mari kita bahas"*, *"Tahukah kamu"*, *"Semoga bermanfaat"*, *"game changer"*, *"revolusioner"*, *"rahasia"*.
- **"Not X but Y" reveals**: *"Bukan cuma X, tapi juga Y"*, *"Tidak hanya X, tetapi Y"*.
- **Repeated crutches**: *"Simpelnya gini"* or *"Nah,"* opening several beats (once per script is fine).
- **Definition as the first line** and **summaries that repeat the script** (*"Jadi intinya, X adalah..."* restating every point).

### 2.5 Honesty inside stories
- First-person anecdotes ("Kemarin saya...") must be true. Otherwise use a "kamu" scenario or a clearly hypothetical one ("Bayangin kamu lagi...").
- Measured numbers name their source in the sentence or on screen ("di tokenizer GPT-4o", "menurut LinkedIn Grad Guide 2025"). Illustrative numbers are marked as illustrations.

### 2.6 Worked example: stiff vs story
From the "Apa itu AI Engineering?" reel, scene 3 (same facts, same length).

**Stiff (AI-ish):**
> Bedanya sama ML Engineering? Urutan kerjanya. ML Engineering: data, model, baru produk. AI Engineering kebalik: produk dulu, baru investasi di data dan model kalau produknya terbukti.

**Story:**
> Dulu, kalau mau bikin fitur AI, kamu harus ngumpulin data dan ngelatih model berbulan-bulan sebelum ada produk yang bisa dicoba. Sekarang urutannya kebalik, karena modelnya sudah jadi, jadi kamu bisa bikin produknya duluan dan baru investasi di data dan model setelah produknya terbukti dipakai orang.

---

## 3. The Full Spectrum Audience Rule (Simultaneous Read)

Every single Databro post or script is read by both a newcomer and a senior engineer simultaneously:
1. **Never Intimidating to Non-Technical Readers**:
   - Avoid unexplained jargon or mathematical acronyms dropped without context.
   - Use plain language definitions the first time an advanced concept appears.
   - Ground abstract concepts in relatable everyday friction (e.g. Berkson's fallacy explained via restaurant food vs location).
2. **Substantive & Credible for Senior Engineers**:
   - The underlying explanation must be 100% technically correct.
   - No misleading, hand-waving simplifications that fall apart under scrutiny.
   - Cite real architectural mechanisms, exact benchmarks, and actual parameter constraints.
3. **The "Bro" Tone as the Unifying Bridge**:
   - The casual "bro" tone and relatable hooks make technical accuracy approachable without sacrificing depth.

---

## 4. Editorial Constraints & Principles

### The 5 Project Principles
1. **Simplicity First**: Semua konten harus mudah dipahami bahkan oleh orang yang baru mengenal data science.
2. **Data-Driven**: Semua insight yang dibagikan harus berbasis data atau eksperimen nyata.
3. **Practical Use Case**: Fokus pada contoh nyata penggunaan data science di kehidupan sehari-hari dan industri.
4. **Educational Value**: Setiap konten harus memberikan nilai pembelajaran konkret.
5. **Visual Clarity**: Visualisasi data harus jelas, elegan, dan tidak membingungkan.

### Editorial Guardrails
- **Strict Ban on Tragedy/Negative News**: Dilarang keras memakai berita duka, bencana, kecelakaan, atau isu emosional negatif sebagai hook konten.
- **Positive or Neutral Viral Hooks**: Hook harus terasa natural, bernada positif atau netral, dan terhubung secara organik ke edukasi data science atau AI.
- **Indonesia Contextualization**: Kaitkan tren global ke konteks Indonesia (adopsi AI lokal, survei data gaji, industri fintech/e-commerce nasional, evolusi peran Data Analyst menjadi AI Orchestrator).
- **Warning: Jangan generate visual/desain image tanpa konfirmasi atau permintaan eksplisit dari user.**

---

## 5. Absolute Ban on Em-Dashes (The Zero Em-Dash Rule)

- **Strict Constraint**: Never use em-dashes (`—`) or en-dashes (`–`) anywhere in titles, slides, captions, or research notes.
- **Why**: Databro's clean typographic system strictly uses colons (`:`), hyphens (`-`), clean parentheses, or simple sentence breaks.
- **Examples**:
  - WRONG: `Agentic AI — Masa Depan Otomasi`
  - CORRECT: `Agentic AI: Masa Depan Otomasi`
  - WRONG: `Model ini cepat — bahkan di CPU biasa`
  - CORRECT: `Model ini cepat, bahkan di CPU biasa.`

---

## 6. Strict Fact-Checking & Anti-Hallucination Policy

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
