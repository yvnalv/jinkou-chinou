#!/usr/bin/env python3
"""
Databro Carousel Slide Renderer v2.
Recreates the exact authentic Databro Studio visual identity from reference slides:
- Minimalist flat dark matte background (#111213)
- Left-aligned clean layout with generous breathing room (NO heavy AI card-in-card boxes)
- Dual-tone title (Cyan + Lavender) on cover
- Clean scientific plots and coordinate axes (arrows, scatter/line, pill badges)
- Crisp teal header tables with white outlines and red dashed alert cells
- Clean code blocks without Mac window dots
- Authentic lime (#C1FF72) labels for sections & takeaway quotes
- True Databro outro slide with double-ring avatar and engagement bar
"""

import os
import base64
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"D:\yvnalv\Onedrive\03. Databro\Contents\Instagram\Feed\[261111] Frontier vs Open-Source LLM\slides"
ASSETS_DIR = r"d:\yvnalv\AI Skills\jinkou-chinou\domains\creative-media\databro-brand-motion\assets"
AVATAR_PATH = os.path.join(ASSETS_DIR, "brand-kit", "logos", "databro-avatar.jpg")

def get_base64_img(path: str) -> str:
    if not os.path.exists(path):
        return ""
    mime = "image/jpeg" if path.endswith((".jpg", ".jpeg")) else "image/png"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

avatar_b64 = get_base64_img(AVATAR_PATH)

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  width: 1080px;
  height: 1350px;
  background-color: #111213;
  color: #FFFFFF;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow: hidden;
  position: relative;
  -webkit-font-smoothing: antialiased;
}

/* Header persistent */
.header {
  position: absolute;
  top: 54px;
  left: 74px;
  right: 74px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 20;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-mini {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  border: 1.5px solid #FFFFFF;
  object-fit: cover;
}

.brand-texts {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 23px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.1;
  letter-spacing: -0.01em;
}

.brand-sub {
  font-size: 15px;
  font-weight: 400;
  color: #FFFFFF;
  opacity: 0.85;
}

.brand-handle {
  font-size: 20px;
  font-weight: 500;
  color: #FFFFFF;
  letter-spacing: -0.01em;
}

/* Stage container */
.stage {
  position: absolute;
  top: 150px;
  bottom: 50px;
  left: 74px;
  right: 74px;
  display: flex;
  flex-direction: column;
}

/* Typography styles matching Databro references */
.headline-lavender {
  font-size: 46px;
  font-weight: 800;
  color: #BB86FC;
  line-height: 1.25;
  letter-spacing: -0.02em;
  margin-bottom: 20px;
}

.subline-white {
  font-size: 23px;
  font-weight: 400;
  color: #E2E2E2;
  line-height: 1.48;
  margin-bottom: 32px;
}

.question-quote {
  font-size: 25px;
  font-weight: 700;
  color: #C1FF72;
  line-height: 1.4;
  margin-bottom: 30px;
}

/* Databro Authentic Grid Table */
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 10px 0 32px 0;
}

.data-table th {
  background: #00E5BE;
  color: #111213;
  font-size: 20px;
  font-weight: 800;
  padding: 18px 22px;
  text-align: center;
  border: 1.5px solid #00E5BE;
}

.data-table th:first-child {
  border-top-left-radius: 6px;
}
.data-table th:last-child {
  border-top-right-radius: 6px;
}

.data-table td {
  background: #111213;
  color: #FFFFFF;
  font-size: 20px;
  font-weight: 600;
  padding: 18px 22px;
  border: 1.5px solid #FFFFFF;
  text-align: center;
}

.data-table td.col-label {
  text-align: left;
  font-weight: 700;
  width: 28%;
}

.data-table td.alert-cell {
  border: 2px dashed #FF5757;
  color: #FF5757;
  font-weight: 700;
}

.data-table td.success-cell {
  color: #FFFFFF;
}

.check-icon {
  color: #00E5BE;
  margin-right: 6px;
}

.cross-icon {
  color: #FF5757;
  margin-right: 6px;
}
"""

def generate_slide_1():
    # Cover Slide: Big Dual-Tone Title (Cyan & Lavender) + Minimalist Scientific Line Plot
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.cover-title {{
  font-size: 64px;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 24px;
}}
.cover-title .cyan {{
  color: #00E5BE;
}}
.cover-title .purple {{
  color: #BB86FC;
}}
.chart-container {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
  position: relative;
}}
.pill-badge {{
  position: absolute;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 17px;
  font-weight: 700;
}}
.pill-cyan {{
  background: #00E5BE;
  color: #111213;
  right: 120px;
  top: 90px;
}}
.pill-gray {{
  background: #282828;
  color: #FFFFFF;
  left: 170px;
  bottom: 110px;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="cover-title">
      <span class="cyan">Frontier</span> vs <span class="purple">Open-Source</span>
    </h1>
    <p class="subline-white" style="font-size: 25px; max-width: 900px;">
      Kenapa model frontier mahal belum tentu jadi pilihan terbaik? Jawabannya ada di cara kita menghitung unit economics inferensi data.
    </p>

    <div class="chart-container">
      <!-- Minimalist Scientific Crossover Plot -->
      <svg width="780" height="520" viewBox="0 0 780 520">
        <!-- Axes -->
        <line x1="80" y1="440" x2="740" y2="440" stroke="#FFFFFF" stroke-width="2"/>
        <polyline points="730,434 740,440 730,446" fill="none" stroke="#FFFFFF" stroke-width="2"/>
        <text x="740" y="475" fill="#FFFFFF" font-size="17" font-weight="500" text-anchor="end">Volume token per hari -></text>

        <line x1="80" y1="440" x2="80" y2="50" stroke="#FFFFFF" stroke-width="2"/>
        <polyline points="74,60 80,50 86,60" fill="none" stroke="#FFFFFF" stroke-width="2"/>
        <text x="70" y="40" fill="#FFFFFF" font-size="17" font-weight="500" text-anchor="start" transform="rotate(-90 70,40)">Biaya operasional bulanan -></text>

        <!-- Shaded Background Area for Open-Source Benefit -->
        <polygon points="380,245 700,245 700,70 380,245" fill="rgba(0, 229, 190, 0.08)"/>

        <!-- Frontier API Linear Line (Coral Red) -->
        <line x1="80" y1="410" x2="700" y2="70" stroke="#FF5757" stroke-width="3.5"/>
        <text x="705" y="65" fill="#FF5757" font-size="18" font-weight="700">API Frontier (Linear)</text>

        <!-- Open-Source vLLM Line (Flat/Stepped Cyan) -->
        <line x1="80" y1="245" x2="700" y2="245" stroke="#00E5BE" stroke-width="3.5"/>
        <text x="705" y="250" fill="#00E5BE" font-size="18" font-weight="700">Self-Hosted vLLM (Flat)</text>

        <!-- Vertical Break-even Threshold (White dashed line) -->
        <line x1="380" y1="440" x2="380" y2="120" stroke="#FFFFFF" stroke-dasharray="6,6" stroke-width="2"/>
        <circle cx="380" cy="245" r="7" fill="#C1FF72"/>
        <text x="380" y="475" fill="#C1FF72" font-size="17" font-weight="700" text-anchor="middle">Titik Impas: 20M Token</text>
      </svg>

      <div class="pill-badge pill-gray">API Lebih Hemat</div>
      <div class="pill-badge pill-cyan">vLLM Hemat 65%</div>
    </div>
  </div>
</body>
</html>"""

def generate_slide_2():
    # Slide 2: "Pernah merhatiin ngga, bro?" with authentic Databro table & punchline
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.punchline {{
  font-size: 32px;
  font-weight: 800;
  color: #FFFFFF;
  margin-top: 24px;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Pernah merhatiin ngga, bro?</h1>
    <p class="subline-white">
      Pas awal bikin prototype, langganan API model frontier kerasa murah dan gampang banget. Tapi pas aplikasi rilis ke publik dan user mulai ramai, tagihan token membengkak di luar kendali.
    </p>

    <div class="question-quote">
      "Berarti kita wajib selalu deploy model open-source sendiri?"
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 34%;">Volume Traffic</th>
          <th style="width: 33%;">Frontier Cloud API</th>
          <th style="width: 33%;">Open-Source (vLLM)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="col-label">Traffic Rendah<br><span style="font-size: 15px; font-weight: 400; color: #AAA;">&lt; 1 Juta token/hari</span></td>
          <td class="success-cell"><span class="check-icon">&#10003;</span>Sangat Hemat</td>
          <td class="alert-cell"><span class="cross-icon">&#10005;</span>Rugi Biaya Server</td>
        </tr>
        <tr>
          <td class="col-label">Traffic Tinggi<br><span style="font-size: 15px; font-weight: 400; color: #AAA;">&gt; 20 Juta token/hari</span></td>
          <td class="alert-cell"><span class="cross-icon">&#10005;</span>Biaya Meledak</td>
          <td class="success-cell"><span class="check-icon">&#10003;</span>Hemat s/d 65%</td>
        </tr>
      </tbody>
    </table>

    <p class="subline-white" style="margin-bottom: 0;">
      Tentu ngga. Menjalankan GPU cluster untuk traffic sepi cuma buang-buang modal perusahaan yang belum tentu kembali.
    </p>

    <div class="punchline">
      Kita cuma melihat tim yang berhasil scale up.
    </div>
  </div>
</body>
</html>"""

def generate_slide_3():
    # Slide 3: "Apa itu Trade-off Arsitekturnya?" with clean minimal flow diagram + table
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.flow-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 12px 0 32px 0;
}}
.flow-card {{
  background: #111213;
  border: 1.5px solid #FFFFFF;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 220px;
  text-align: center;
}}
.flow-card.router {{
  border-color: #C1FF72;
  position: relative;
}}
.router-pill {{
  background: #C1FF72;
  color: #111213;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 2px 10px;
  border-radius: 10px;
  margin-bottom: 8px;
}}
.flow-title {{
  font-size: 19px;
  font-weight: 700;
  color: #FFFFFF;
}}
.flow-arrow {{
  font-size: 26px;
  color: #FFFFFF;
  font-weight: 700;
}}
.section-lime {{
  font-size: 23px;
  font-weight: 800;
  color: #C1FF72;
  margin-top: 16px;
  margin-bottom: 8px;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Apa itu Trade-off Arsitekturnya?</h1>
    <p class="subline-white">
      Setiap arsitektur mengorbankan hal berbeda. Nama lainnya: <strong style="color: #00E5BE;">CapEx vs OpEx Dilemma</strong>.
    </p>

    <!-- Clean Databro Flow Diagram -->
    <div class="flow-row">
      <div class="flow-card">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" style="margin-bottom: 6px;"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>
        <span class="flow-title">Aplikasi Kamu</span>
      </div>

      <span class="flow-arrow">&rarr;</span>

      <div class="flow-card router">
        <span class="router-pill">Gateway Router</span>
        <span class="flow-title">Model Router</span>
      </div>

      <span class="flow-arrow">&rarr;</span>

      <div style="display: flex; flex-direction: column; gap: 12px;">
        <div class="flow-card" style="border-color: #BB86FC; padding: 10px 18px; min-width: 200px;">
          <span style="color: #BB86FC; font-weight: 700; font-size: 16px;">Frontier API (Cloud)</span>
        </div>
        <div class="flow-card" style="border-color: #00E5BE; padding: 10px 18px; min-width: 200px;">
          <span style="color: #00E5BE; font-weight: 700; font-size: 16px;">vLLM Server (Lokal)</span>
        </div>
      </div>
    </div>

    <!-- Comparison Table -->
    <table class="data-table" style="margin-bottom: 16px;">
      <thead>
        <tr>
          <th style="width: 35%;">Parameter Kunci</th>
          <th style="width: 32%;">Frontier API</th>
          <th style="width: 33%;">Open-Source LLM</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="col-label">Kedaulatan Data</td>
          <td>Cloud pihak ketiga</td>
          <td style="color: #00E5BE;">100% Private di VPC</td>
        </tr>
        <tr>
          <td class="col-label">Fine-Tuning Bobot</td>
          <td>Terbatas via API</td>
          <td style="color: #BB86FC;">Bebas (LoRA / Quant)</td>
        </tr>
        <tr>
          <td class="col-label">Reasoning SOTA</td>
          <td style="color: #00E5BE;">Paling Canggih</td>
          <td>Mendekati di tugas fokus</td>
        </tr>
      </tbody>
    </table>

    <div class="section-lime">Kenapa ini krusial buat kamu?</div>
    <p class="subline-white" style="margin-bottom: 0;">
      Kalau kamu hardcode kode ke salah satu provider sejak awal, kamu bakal terjebak saat arsitektur butuh switch provider ketika sistem scale up.
    </p>
  </div>
</body>
</html>"""

def generate_slide_4():
    # Slide 4: "Buktinya pakai data benchmark" with side-by-side stats and Databro red alert box
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.stat-split {{
  display: flex;
  justify-content: space-between;
  margin: 16px 0 36px 0;
}}
.stat-col {{
  flex: 1;
  display: flex;
  flex-direction: column;
}}
.stat-col-title {{
  font-size: 22px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 8px;
}}
.big-number {{
  font-size: 60px;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 8px;
}}
.stat-sub {{
  font-size: 19px;
  color: #CCCCCC;
  line-height: 1.45;
  max-width: 400px;
}}
/* Databro Red Alert Box */
.databro-alert-box {{
  border: 2px solid #FF5757;
  border-radius: 14px;
  padding: 24px 28px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
}}
.alert-icon {{
  flex-shrink: 0;
  margin-top: 2px;
}}
.alert-text {{
  font-size: 21px;
  color: #FFFFFF;
  line-height: 1.48;
}}
.footnote {{
  font-size: 18px;
  color: #AAAAAA;
  line-height: 1.45;
}}
.footnote strong {{
  color: #C1FF72;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Buktinya pakai data benchmark</h1>
    <p class="subline-white">
      Performa model open-weights sekarang sudah bukan kaleng-kaleng lagi:
    </p>

    <div class="stat-split">
      <div class="stat-col">
        <span class="stat-col-title">LMSYS Chatbot Arena</span>
        <span class="big-number" style="color: #00E5BE;">Elo 1280+</span>
        <span class="stat-sub">Model Llama 3.3 70B & Qwen 2.5 menempel ketat frontier model generasi sebelumnya.</span>
      </div>

      <div class="stat-col">
        <span class="stat-col-title">Titik Impas Biaya</span>
        <span class="big-number" style="color: #FF5757;">20M Token</span>
        <span class="stat-sub">Volume harian di mana self-hosting vLLM di 4x L40S memotong biaya sampai 65%!</span>
      </div>
    </div>

    <!-- Databro Official Red Outline Callout Box -->
    <div class="databro-alert-box">
      <svg class="alert-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF5757" stroke-width="2.5">
        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
      <div class="alert-text">
        Model open-source yang di-deploy di GPU tanpa perhitungan traffic bakal <strong style="color: #FF5757;">boncos jutaan rupiah per bulan</strong>. Tapi kalau traffic kamu stabil di atas 20M token/hari, tetap bertahan di API frontier adalah pemborosan besar.
      </div>
    </div>

    <div class="footnote">
      <strong>Asal-usulnya:</strong> Angka kalkulasi diuji pada workload produksi komparasi token API proprietary vs cluster cloud instance 4x NVIDIA L40S 48GB VRAM via PagedAttention.
    </div>
  </div>
</body>
</html>"""

def generate_slide_5():
    # Slide 5: "Implementasi pakai Python" clean syntax card without Mac window dots + clean output
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.code-container {{
  background: #1A1D20;
  border-radius: 16px;
  border: 1px solid #2B3036;
  padding: 30px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 19px;
  line-height: 1.6;
  color: #E6EDF3;
  white-space: pre;
  margin-top: 10px;
  margin-bottom: 24px;
}}
.kw {{ color: #FF7B72; }}
.str {{ color: #A5D6FF; }}
.cmt {{ color: #8B949E; font-style: italic; }}
.var {{ color: #FFA657; }}
.output-label {{
  font-size: 22px;
  font-weight: 800;
  color: #C1FF72;
  margin-bottom: 12px;
}}
.output-card {{
  background: #15181B;
  border: 1.5px solid #2B3036;
  border-radius: 12px;
  padding: 20px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 19px;
  line-height: 1.6;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Implementasi pakai Python</h1>
    <p class="subline-white">
      Buktikan sendiri, code-nya simpel banget, bro!
    </p>

    <div class="code-container"><span class="kw">import</span> os
<span class="kw">from</span> openai <span class="kw">import</span> OpenAI

<span class="cmt"># 1. Flag kontrol environment</span>
use_local = os.getenv(<span class="str">"USE_LOCAL"</span>, <span class="str">"false"</span>) == <span class="str">"true"</span>

<span class="cmt"># 2. OpenAI SDK abstraction layer</span>
client = OpenAI(
    base_url=<span class="str">"http://localhost:8000/v1"</span> <span class="kw">if</span> use_local <span class="kw">else</span> <span class="str">"https://api.openai.com/v1"</span>,
    api_key=<span class="str">"token-vllm"</span> <span class="kw">if</span> use_local <span class="kw">else</span> os.getenv(<span class="str">"OPENAI_KEY"</span>)
)

model = <span class="str">"meta-llama/Llama-3.3-70B"</span> <span class="kw">if</span> use_local <span class="kw">else</span> <span class="str">"gpt-4o"</span></div>

    <div class="output-label">Output:</div>
    <div class="output-card">
      <div>Status Provider : <span style="color: #00E5BE; font-weight: 700;">vLLM Local Server (8000)</span></div>
      <div>Latency / Token : <span style="color: #00E5BE; font-weight: 700;">18.4 ms (AWQ Quantized)</span></div>
    </div>
  </div>
</body>
</html>"""

def generate_slide_6():
    # Slide 6: "Biar model kamu ngga ketipu" style checklist + Takeaway quote
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.check-item {{
  margin-bottom: 26px;
}}
.check-title {{
  font-size: 24px;
  font-weight: 800;
  color: #C1FF72;
  margin-bottom: 6px;
}}
.check-desc {{
  font-size: 21px;
  line-height: 1.48;
  color: #FFFFFF;
}}
.quote-container {{
  margin-top: 24px;
}}
.quote-tag {{
  font-size: 22px;
  font-weight: 800;
  color: #C1FF72;
  margin-bottom: 12px;
}}
.quote-body {{
  border-left: 2px solid #FFFFFF;
  padding-left: 24px;
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 23px;
  line-height: 1.5;
  color: #CED3DA;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Biar model kamu ngga boncos</h1>
    <p class="subline-white">
      3 hal yang perlu kamu cek sebelum mengunci arsitektur deployment:
    </p>

    <div class="check-item">
      <div class="check-title">#1: Mulai selalu dari Frontier API</div>
      <p class="check-desc">Validasi problem dan product-market fit dulu. Jangan buang waktu setup GPU cluster kalau idenya belum terbukti menghasilkan.</p>
    </div>

    <div class="check-item">
      <div class="check-title">#2: Hitung unit economics di 10M+ token</div>
      <p class="check-desc">Begitu biaya bulanan API menembus harga sewa 1 instance GPU cluster, segera siapkan pipeline vLLM terkuantisasi.</p>
    </div>

    <div class="check-item">
      <div class="check-title">#3: Cek regulasi privasi data pengguna</div>
      <p class="check-desc">Kalau kamu di industri Fintech atau Kesehatan, kedaulatan data di private VPC adalah syarat mati, bukan sekadar opsi.</p>
    </div>

    <div class="quote-container">
      <div class="quote-tag">Takeaway quote:</div>
      <div class="quote-body">
        "Frontier model membeli kecepatan iterasi dan reasoning tertinggi, sedangkan open-source model membeli kedaulatan data dan efisiensi biaya saat aplikasi kamu scale up."
      </div>
    </div>
  </div>
</body>
</html>"""

def generate_slide_7():
    # Slide 7: Official Databro Outro (Large dual-ring avatar, chevrons >>, and bottom engagement bar)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.outro-container {{
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  text-align: center;
}}
/* Large avatar with dual cyan/lavender ring border */
.avatar-ring-outer {{
  width: 250px;
  height: 250px;
  border-radius: 50%;
  border: 4px solid #00E5BE;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
  position: relative;
}}
.avatar-ring-inner {{
  width: 234px;
  height: 234px;
  border-radius: 50%;
  border: 4px solid #BB86FC;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F0ECE2;
}}
.avatar-large {{
  width: 100%;
  height: 100%;
  object-fit: cover;
}}
/* Double chevrons >> */
.chevron-tr {{
  position: absolute;
  top: 140px;
  right: 140px;
  font-size: 56px;
  font-weight: 900;
  color: #00E5BE;
  letter-spacing: -6px;
}}
.chevron-bl {{
  position: absolute;
  bottom: 280px;
  left: 140px;
  font-size: 56px;
  font-weight: 900;
  color: #BB86FC;
  letter-spacing: -6px;
}}
.outro-title {{
  font-size: 40px;
  font-weight: 800;
  line-height: 1.35;
  color: #FFFFFF;
  max-width: 780px;
  margin-bottom: 40px;
}}
/* Bottom Engagement Bar */
.engagement-bar {{
  position: absolute;
  bottom: 60px;
  left: 50px;
  right: 50px;
  background: #111213;
  border: 1.5px solid #FFFFFF;
  border-radius: 12px;
  padding: 16px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.bar-left {{
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #FFFFFF;
}}
.bar-icons {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.bar-right {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #FFFFFF;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar-mini">
      <div class="brand-texts">
        <span class="brand-name">Databro</span>
        <span class="brand-sub">Belajar Data Science</span>
      </div>
    </div>
    <span class="brand-handle">@databro.id</span>
  </div>

  <div class="stage">
    <div class="outro-container">
      <div class="chevron-tr">&gt;&gt;</div>
      <div class="chevron-bl">&gt;&gt;</div>

      <div class="avatar-ring-outer">
        <div class="avatar-ring-inner">
          <img src="{avatar_b64}" class="avatar-large">
        </div>
      </div>

      <h2 class="outro-title">
        Keputusan arsitektur AI ada di tangan kamu, bro.<br>
        Save dulu buat nanti!
      </h2>

      <!-- Bottom Engagement Bar identical to Databro reference -->
      <div class="engagement-bar">
        <div class="bar-left">
          <div class="bar-icons">
            <!-- Comment icon -->
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <!-- Heart icon -->
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            <!-- Share icon -->
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
          </div>
          <span>Like, comment & share, bro!</span>
        </div>

        <div class="bar-right">
          <span>Simpan biar ngga lupa!</span>
          <!-- Bookmark icon -->
          <svg width="22" height="22" viewBox="0 0 24 24" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    slides = [
        ("01.png", generate_slide_1()),
        ("02.png", generate_slide_2()),
        ("03.png", generate_slide_3()),
        ("04.png", generate_slide_4()),
        ("05.png", generate_slide_5()),
        ("06.png", generate_slide_6()),
        ("07.png", generate_slide_7()),
    ]

    print("Starting Playwright to render 7 Authentic Databro Carousel slides (1080x1350)...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)

        for filename, html_content in slides:
            temp_html_path = os.path.join(OUTPUT_DIR, f"temp_{filename}.html")
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            page.goto(f"file:///{temp_html_path.replace(os.sep, '/')}")
            page.wait_for_load_state("networkidle")
            
            output_png_path = os.path.join(OUTPUT_DIR, filename)
            page.screenshot(path=output_png_path, full_page=False)
            print(f"Rendered: {output_png_path}")

            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

        browser.close()
    print("All authentic Databro slides successfully rendered!")

if __name__ == "__main__":
    main()
