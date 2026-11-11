#!/usr/bin/env python3
"""
Databro Carousel Slide Renderer.
Renders 1080x1350 (4:5) Instagram Feed Carousel slides using Playwright.
Adheres strictly to Databro Studio brand tokens, left-aligned layout,
clean vector SVG icons, zero em-dashes, and conversational Indonesian wording.
"""

import os
import base64
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"D:\yvnalv\Onedrive\03. Databro\Contents\Instagram\Feed\[261111] Frontier vs Open-Source LLM\slides"
ASSETS_DIR = r"d:\yvnalv\AI Skills\jinkou-chinou\domains\creative-media\databro-brand-motion\assets"
AVATAR_PATH = os.path.join(ASSETS_DIR, "brand-kit", "logos", "databro-avatar.jpg")
LOGO_LANDSCAPE_PATH = os.path.join(ASSETS_DIR, "brand-kit", "logos", "DATABRO-01-rev-yvnalv-(White)-Landscape.png")

def get_base64_img(path: str) -> str:
    if not os.path.exists(path):
        return ""
    mime = "image/jpeg" if path.endswith((".jpg", ".jpeg")) else "image/png"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

avatar_b64 = get_base64_img(AVATAR_PATH)
logo_b64 = get_base64_img(LOGO_LANDSCAPE_PATH)

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  width: 1080px;
  height: 1350px;
  background-color: #121212;
  color: #FFFFFF;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow: hidden;
  position: relative;
  -webkit-font-smoothing: antialiased;
}

/* Header persistent */
.header {
  position: absolute;
  top: 72px;
  left: 84px;
  right: 84px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  border: 2px solid #F2EFEB;
  object-fit: cover;
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 24px;
  font-weight: 800;
  color: #F2EFEB;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

.brand-tagline {
  font-size: 15px;
  font-weight: 500;
  color: #F2EFEB;
  opacity: 0.85;
}

.handle {
  font-size: 22px;
  font-style: italic;
  font-weight: 500;
  color: #F2EFEB;
  letter-spacing: -0.01em;
}

/* Main Content Stage */
.stage {
  position: absolute;
  top: 175px;
  bottom: 80px;
  left: 84px;
  right: 84px;
  display: flex;
  flex-direction: column;
}

.headline-lavender {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.25;
  color: #BB86FC;
  letter-spacing: -0.03em;
  margin-bottom: 16px;
}

.subline-white {
  font-size: 26px;
  font-weight: 400;
  line-height: 1.45;
  color: #FFFFFF;
  opacity: 0.92;
  margin-bottom: 36px;
}

/* Footer slide indicator */
.footer-bar {
  position: absolute;
  bottom: 40px;
  left: 84px;
  right: 84px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slide-num {
  font-size: 18px;
  font-weight: 700;
  color: #666666;
  letter-spacing: 0.05em;
}

.swipe-hint {
  font-size: 18px;
  font-weight: 600;
  color: #C1FF72;
  display: flex;
  align-items: center;
  gap: 8px;
}
"""

def generate_slide_1():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.hero-box {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}
.vs-grid {{
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 20px;
}}
.model-card {{
  flex: 1;
  background: #181818;
  border: 2px solid #2E2E2E;
  border-radius: 20px;
  padding: 36px 30px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}}
.model-card.frontier {{
  border-color: #BB86FC;
}}
.model-card.opensource {{
  border-color: #03DAC6;
}}
.card-tag {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 6px 14px;
  border-radius: 999px;
  width: fit-content;
}}
.frontier .card-tag {{
  background: rgba(187, 134, 252, 0.15);
  color: #BB86FC;
}}
.opensource .card-tag {{
  background: rgba(3, 218, 198, 0.15);
  color: #03DAC6;
}}
.card-name {{
  font-size: 34px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.15;
}}
.card-points {{
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 8px;
}}
.card-points li {{
  font-size: 20px;
  color: #CCCCCC;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.card-points svg {{
  flex-shrink: 0;
}}
.vs-circle {{
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #C1FF72;
  color: #121212;
  font-weight: 900;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.hook-badge {{
  display: inline-block;
  background: rgba(193, 255, 114, 0.15);
  color: #C1FF72;
  border: 1px solid #C1FF72;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  padding: 6px 16px;
  margin-bottom: 24px;
  width: fit-content;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <div class="hero-box">
      <div class="hook-badge">AI ARCHITECTURE GUIDE</div>
      <h1 class="headline-lavender" style="font-size: 56px;">
        Pernah ngga....<br>
        <span style="color: #FFFFFF;">Bingung mau pilih API model frontier atau deploy open-source sendiri?</span>
      </h1>
      <p class="subline-white">
        Biar kamu gak salah bakar budget atau pusing mikirin server, yuk kita bedah trade-off aslinya secara transparan!
      </p>

      <div class="vs-grid">
        <div class="model-card frontier">
          <span class="card-tag">Cloud API</span>
          <h2 class="card-name">Frontier LLM</h2>
          <ul class="card-points">
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#BB86FC" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Claude 3.5 Sonnet / GPT-4o
            </li>
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#BB86FC" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Tinggal panggil API (Zero setup)
            </li>
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#BB86FC" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Reasoning & coding level SOTA
            </li>
          </ul>
        </div>

        <div class="vs-circle">VS</div>

        <div class="model-card opensource">
          <span class="card-tag">Self-Hosted</span>
          <h2 class="card-name">Open-Weights</h2>
          <ul class="card-points">
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#03DAC6" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Llama 3.3 70B / Qwen 2.5 72B
            </li>
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#03DAC6" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Data 100% aman di VPC kamu
            </li>
            <li>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#03DAC6" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Bebas fine-tuning & kuantisasi
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <span class="slide-num">01 / 06</span>
    <span class="swipe-hint">Swipe ke kiri bro -></span>
  </div>
</body>
</html>"""

def generate_slide_2():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.friction-container {{
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 10px;
}}
.friction-card {{
  background: #181818;
  border-radius: 18px;
  padding: 30px 32px;
  border-left: 6px solid #BB86FC;
}}
.friction-card.red {{
  border-left-color: #FF5757;
}}
.friction-card.lime {{
  border-left-color: #C1FF72;
}}
.friction-header {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}}
.friction-title {{
  font-size: 26px;
  font-weight: 800;
  color: #FFFFFF;
}}
.friction-desc {{
  font-size: 21px;
  line-height: 1.5;
  color: #CCCCCC;
}}
.highlight-pill {{
  background: rgba(255, 87, 87, 0.15);
  color: #FF5757;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
}}
.highlight-lime {{
  background: rgba(193, 255, 114, 0.15);
  color: #C1FF72;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
}}
.takeaway-strip {{
  margin-top: 16px;
  background: rgba(187, 134, 252, 0.08);
  border: 1px dashed #BB86FC;
  border-radius: 14px;
  padding: 20px 24px;
  font-size: 20px;
  line-height: 1.45;
  color: #F2EFEB;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Dilema Nyata: Biaya Token vs Setup GPU</h1>
    <p class="subline-white">
      Di awal fase MVP semua kelihatan gampang, tapi friksi mulai kerasa pas sistem kamu scale up:
    </p>

    <div class="friction-container">
      <div class="friction-card red">
        <div class="friction-header">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FF5757" stroke-width="2.5"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <span class="friction-title">Jebakan Biaya Frontier API</span>
        </div>
        <p class="friction-desc">
          Model frontier bayarnya per token input dan output. Pas traffic naik ke <span class="highlight-pill">puluhan juta token per hari</span>, tagihan bulanan langsung membengkak linear tanpa ampun. Selain itu, data kamu harus dikirim ke cloud provider pihak ketiga.
        </p>
      </div>

      <div class="friction-card lime">
        <div class="friction-header">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C1FF72" stroke-width="2.5"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
          <span class="friction-title">Tantangan Hosting Open-Source</span>
        </div>
        <p class="friction-desc">
          Model open-source (seperti Llama 3.3 70B) ngasih <span class="highlight-lime">kedaulatan data 100%</span> dan biaya flat. Tapi kamu butuh modal awal GPU cluster (VRAM 80GB+), arsitektur vLLM, serta engineer handal buat monitoring uptime.
        </p>
      </div>

      <div class="takeaway-strip">
        <strong>Poin Kritis:</strong> Jangan sampai kamu bayar mahal API hanya untuk task rutin yang sebenarnya bisa diselesaikan oleh model open-source 8B atau 70B!
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <span class="slide-num">02 / 06</span>
    <span class="swipe-hint">Lanjut ke tabel -></span>
  </div>
</body>
</html>"""

def generate_slide_3():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.matrix-table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
}}
.matrix-table th {{
  background: #03DAC6;
  color: #121212;
  font-size: 20px;
  font-weight: 800;
  text-align: left;
  padding: 18px 20px;
  letter-spacing: -0.01em;
}}
.matrix-table td {{
  padding: 18px 20px;
  font-size: 19px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  color: #E0E0E0;
  vertical-align: middle;
}}
.matrix-table tr:nth-child(even) {{
  background: rgba(255, 255, 255, 0.02);
}}
.aspect-col {{
  font-weight: 700;
  color: #FFFFFF !important;
  width: 28%;
}}
.frontier-col {{
  color: #BB86FC !important;
  width: 36%;
}}
.opensource-col {{
  color: #03DAC6 !important;
  width: 36%;
}}
.pill {{
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 700;
}}
.pill.good {{
  background: rgba(3, 218, 198, 0.15);
  color: #03DAC6;
}}
.pill.warn {{
  background: rgba(255, 87, 87, 0.15);
  color: #FF5757;
}}
.pill.purple {{
  background: rgba(187, 134, 252, 0.15);
  color: #BB86FC;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Matriks Perbandingan Teknis</h1>
    <p class="subline-white">
      Bandingkan 5 kriteria fundamental ini sebelum kamu mengunci arsitektur AI kamu:
    </p>

    <table class="matrix-table">
      <thead>
        <tr>
          <th>Kriteria Evaluasi</th>
          <th>Frontier Cloud API</th>
          <th>Open-Weights LLM</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="aspect-col">Biaya Awal (Capex)</td>
          <td><span class="pill good">Sangat Rendah</span><br>Pay-per-token</td>
          <td><span class="pill warn">Tinggi</span><br>Sewa GPU / Instance</td>
        </tr>
        <tr>
          <td class="aspect-col">Biaya Skala Besar</td>
          <td><span class="pill warn">Naik Linear</span><br>Makin ramai makin mahal</td>
          <td><span class="pill good">Flat Cost</span><br>Biaya server bulanan tetap</td>
        </tr>
        <tr>
          <td class="aspect-col">Kedaulatan Data</td>
          <td>Data dikirim ke server pihak ketiga</td>
          <td><span class="pill good">100% Aman</span><br>Lokal / Private VPC</td>
        </tr>
        <tr>
          <td class="aspect-col">Kustomisasi Model</td>
          <td>Hanya via Prompt & API fine-tuning</td>
          <td><span class="pill purple">Full Weights</span><br>LoRA, Quantize, Pruning</td>
        </tr>
        <tr>
          <td class="aspect-col">Reasoning Peak</td>
          <td><span class="pill purple">Top-Tier</span><br>SOTA di SWE-bench</td>
          <td>Sangat kuat dan mendekati di domain spesifik</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="footer-bar">
    <span class="slide-num">03 / 06</span>
    <span class="swipe-hint">Cek angka benchmark -></span>
  </div>
</body>
</html>"""

def generate_slide_4():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.stat-container {{
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-top: 10px;
}}
.stat-box {{
  background: #181818;
  border: 1px solid #2E2E2E;
  border-radius: 20px;
  padding: 32px;
}}
.stat-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}}
.stat-badge {{
  font-size: 15px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 6px 14px;
  border-radius: 8px;
}}
.stat-badge.teal {{
  background: rgba(3, 218, 198, 0.15);
  color: #03DAC6;
  border: 1px solid #03DAC6;
}}
.stat-badge.lime {{
  background: rgba(193, 255, 114, 0.15);
  color: #C1FF72;
  border: 1px solid #C1FF72;
}}
.stat-main-number {{
  font-size: 44px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.02em;
}}
.stat-desc {{
  font-size: 21px;
  line-height: 1.5;
  color: #CCCCCC;
}}
.highlight-text {{
  color: #C1FF72;
  font-weight: 700;
}}
.highlight-teal {{
  color: #03DAC6;
  font-weight: 700;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Kapan Self-Hosting Jadi Lebih Hemat?</h1>
    <p class="subline-white">
      Data benchmark LMSYS Chatbot Arena dan unit economics inferensi modern membuktikan:
    </p>

    <div class="stat-container">
      <div class="stat-box">
        <div class="stat-header">
          <span class="stat-badge teal">LMSYS Chatbot Arena</span>
          <span class="stat-main-number highlight-teal">Elo 1280+</span>
        </div>
        <p class="stat-desc">
          Model open-weights seperti <span class="highlight-teal">Llama 3.3 70B</span> dan <span class="highlight-teal">Qwen 2.5 72B</span> sudah menembus skor Elo di atas 1280. Kualitas reasoning-nya sudah menempel ketat model frontier proprietary generasi sebelumnya!
        </p>
      </div>

      <div class="stat-box">
        <div class="stat-header">
          <span class="stat-badge lime">Titik Impas (Break-Even)</span>
          <span class="stat-main-number highlight-text">Hemat Hingga 65%</span>
        </div>
        <p class="stat-desc">
          Aturan praktis biaya inferensi:<br>
          - <strong>Di bawah 1 Juta token/hari:</strong> Gunakan API frontier (~$10 sampai $15 per bulan).<br>
          - <strong>Di atas 20 Juta token/hari:</strong> Self-hosting model 70B terkuantisasi (FP8/AWQ) via <span class="highlight-text">vLLM</span> di instance GPU memotong biaya operasional hingga <span class="highlight-text">65%</span> dibanding bayar token API!
        </p>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <span class="slide-num">04 / 06</span>
    <span class="swipe-hint">Yuk cek kodenya -></span>
  </div>
</body>
</html>"""

def generate_slide_5():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.code-card {{
  background: #24292E;
  border-radius: 16px;
  border: 1px solid #3B424C;
  overflow: hidden;
  margin-top: 10px;
}}
.code-chrome {{
  background: #1F2428;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #3B424C;
}}
.dot {{
  width: 12px;
  height: 12px;
  border-radius: 50%;
}}
.dot.red {{ background: #FF5F56; }}
.dot.yellow {{ background: #FFBD2E; }}
.dot.green {{ background: #27C93F; }}
.code-title {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: #959DA5;
  margin-left: 12px;
}}
.code-body {{
  padding: 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 17px;
  line-height: 1.6;
  color: #E1E4E8;
  white-space: pre;
}}
.kw {{ color: #F97583; }}
.str {{ color: #9ECBFF; }}
.cmt {{ color: #6A737D; font-style: italic; }}
.var {{ color: #B392F0; }}
.tip-box {{
  margin-top: 20px;
  background: rgba(193, 255, 114, 0.08);
  border-left: 4px solid #C1FF72;
  border-radius: 0 12px 12px 0;
  padding: 16px 20px;
  font-size: 19px;
  line-height: 1.45;
  color: #FFFFFF;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender">Implementasi: Buat Arsitektur Fleksibel</h1>
    <p class="subline-white">
      Jangan hardcode provider! Gunakan abstraction layer agar kamu bisa switch API vs Lokal tanpa ubah logic aplikasi:
    </p>

    <div class="code-card">
      <div class="code-chrome">
        <span class="dot red"></span>
        <span class="dot yellow"></span>
        <span class="dot green"></span>
        <span class="code-title">app_llm_client.py</span>
      </div>
      <div class="code-body"><span class="kw">import</span> os
<span class="kw">from</span> openai <span class="kw">import</span> OpenAI

<span class="cmt"># Cukup kontrol lewat 1 environment variable!</span>
USE_LOCAL = os.getenv(<span class="str">"USE_LOCAL_LLM"</span>, <span class="str">"false"</span>).lower() == <span class="str">"true"</span>

client = OpenAI(
    base_url=<span class="str">"http://localhost:8000/v1"</span> <span class="kw">if</span> USE_LOCAL <span class="kw">else</span> <span class="str">"https://api.openai.com/v1"</span>,
    api_key=<span class="str">"token-vllm"</span> <span class="kw">if</span> USE_LOCAL <span class="kw">else</span> os.getenv(<span class="str">"OPENAI_API_KEY"</span>)
)

<span class="cmt"># Otomatis panggil model open-source vLLM atau model frontier</span>
model = <span class="str">"meta-llama/Llama-3.3-70B-Instruct"</span> <span class="kw">if</span> USE_LOCAL <span class="kw">else</span> <span class="str">"gpt-4o"</span></div>
    </div>

    <div class="tip-box">
      <strong>Pro Tip Databro:</strong> Gunakan model frontier saat riset dan validasi awal. Begitu produk siap scale dan throughput melonjak, switch ke server vLLM lokal dalam 1 detik!
    </div>
  </div>

  <div class="footer-bar">
    <span class="slide-num">05 / 06</span>
    <span class="swipe-hint">Kesimpulan akhir -></span>
  </div>
</body>
</html>"""

def generate_slide_6():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{COMMON_CSS}
.summary-grid {{
  display: flex;
  gap: 20px;
  margin-top: 10px;
}}
.guide-card {{
  flex: 1;
  background: #181818;
  border: 1px solid #2E2E2E;
  border-radius: 18px;
  padding: 24px;
}}
.guide-card.frontier {{
  border-top: 4px solid #BB86FC;
}}
.guide-card.opensource {{
  border-top: 4px solid #03DAC6;
}}
.guide-title {{
  font-size: 22px;
  font-weight: 800;
  color: #FFFFFF;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}}
.guide-list {{
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}
.guide-list li {{
  font-size: 17px;
  color: #CCCCCC;
  line-height: 1.4;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}}
.guide-list li::before {{
  content: "->";
  color: #C1FF72;
  font-weight: 700;
}}
.quote-box {{
  margin-top: 24px;
  background: #181818;
  border-left: 5px solid #C1FF72;
  border-radius: 0 16px 16px 0;
  padding: 22px 28px;
}}
.quote-label {{
  font-size: 15px;
  font-weight: 800;
  color: #C1FF72;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}}
.quote-text {{
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 23px;
  line-height: 1.45;
  color: #CED3DA;
}}
.cta-box {{
  margin-top: 24px;
  background: rgba(187, 134, 252, 0.1);
  border: 1px solid #BB86FC;
  border-radius: 16px;
  padding: 20px 24px;
  text-align: center;
}}
.cta-text {{
  font-size: 21px;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.4;
}}
.cta-sub {{
  font-size: 17px;
  color: #C1FF72;
  margin-top: 6px;
  font-weight: 600;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="brand-lockup">
      <img src="{avatar_b64}" class="avatar">
      <div class="brand-info">
        <span class="brand-title">Databro</span>
        <span class="brand-tagline">Belajar Data Science</span>
      </div>
    </div>
    <span class="handle">@databro.id</span>
  </div>

  <div class="stage">
    <h1 class="headline-lavender" style="font-size: 46px;">Rule of Thumb: Kapan Pilih Apa?</h1>

    <div class="summary-grid">
      <div class="guide-card frontier">
        <div class="guide-title" style="color: #BB86FC;">Pilih Frontier API</div>
        <ul class="guide-list">
          <li>Fase MVP / riset validasi cepat</li>
          <li>Task butuh deep multi-step reasoning</li>
          <li>Volume token di bawah 1M/hari</li>
          <li>Zero budget maintenance server</li>
        </ul>
      </div>

      <div class="guide-card opensource">
        <div class="guide-title" style="color: #03DAC6;">Pilih Open-Weights</div>
        <ul class="guide-list">
          <li>Data sensitif (Fintech / Healthcare)</li>
          <li>Throughput stabil > 20M token/hari</li>
          <li>Perlu kustomisasi bobot / LoRA</li>
          <li>Ingin kontrol latency 100% di VPC</li>
        </ul>
      </div>
    </div>

    <div class="quote-box">
      <div class="quote-label">Takeaway quote:</div>
      <div class="quote-text">
        "Frontier model membeli kecepatan iterasi dan reasoning tertinggi, sedangkan open-source model membeli kedaulatan data dan efisiensi biaya saat aplikasi kamu scale up."
      </div>
    </div>

    <div class="cta-box">
      <p class="cta-text">Kamu di tim saat ini lebih sering pakai API atau deploy sendiri bro?</p>
      <p class="cta-sub">Tulis di kolom komentar dan save postingan ini ya! 📌</p>
    </div>
  </div>

  <div class="footer-bar">
    <span class="slide-num">06 / 06</span>
    <span style="font-size: 16px; color: #888888;">Belajar AI & Data Science bareng Databro</span>
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
    ]

    print("Starting Playwright to render 6 Databro Carousel slides (1080x1350)...")
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
    print("All slides successfully rendered!")

if __name__ == "__main__":
    main()
