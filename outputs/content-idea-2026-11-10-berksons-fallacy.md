# [Instagram Carousel] Berkson's Fallacy: Jebakan Seleksi Data yang Bikin Fitur Independen Tampak Berkorelasi

> Pernah bertanya-tanya kenapa restoran dengan makanan terlezat sering berada di lokasi tersembunyi? Di data science, ilusi ini dinamakan Berkson's Fallacy atau Collider Bias!

**Category**: Pure Math & Statistics Fundamentals  
**Target Platform**: Instagram Carousel  
**Tone & Audience**: Casual Indonesian ("bro" tone) - Data practitioners & learners  
**Date**: 2026-11-10  
**Status**: Idea 💡  
**Format Type**: Carousel (8-part)  

---

## 1. Title / Headline
Berkson's Fallacy: Jebakan Seleksi Data yang Bikin Fitur Independen Tampak Berkorelasi

## 2. Subtitle / Framing Question
Pernah bertanya-tanya kenapa restoran dengan makanan terlezat sering berada di lokasi tersembunyi? Di data science, ilusi ini dinamakan Berkson's Fallacy atau Collider Bias!

## 3. Background & Relatable Friction (Hook)
Bro, pernah gak kamu memperhatikan kenapa kedai kuliner dengan rasa paling istimewa sering kali berada di gang tersembunyi, sementara restoran di lokasi paling strategis rasanya cenderung biasa saja? Apakah lokasi bagus menurunkan kualitas makanan? Tentu tidak. Restoran yang makanannya biasa dan lokasinya buruk sudah tutup sejak awal, sehingga tidak pernah masuk ke daftar kunjungan kita. Ketika kita hanya mengamati 'restoran yang bertahan', tercipta korelasi negatif semu antara rasa dan lokasi. Di machine learning, bias seleksi serupa sering mengacaukan model kamu tanpa disadari!

## 4. Bridging Explanation & Core Concept
Berkson's Paradox (Collider Bias) terjadi ketika kita mengkondisikan atau memfilter data berdasarkan variabel ketiga (C) yang dipengaruhi oleh dua variabel independen (X dan Y). Ketika X -> C <- Y, memfilter sampel hanya pada kondisi C = True membuka jalur semu (spurious path) yang menciptakan korelasi negatif palsu antara X dan Y.

| Element | Cara Kerja | Catatan |
|---|---|---|
| Populasi Lengkap (Tanpa Filter) | Data mencakup seluruh spektrum (X tinggi, Y tinggi, hingga keduanya rendah) | Korelasi Pearson r = 0.00 (Variabel murni independen). |
| Sampel Terfilter (Kondisi C = True) | Observasi dengan X rendah dan Y rendah otomatis tereliminasi dari sampel | Muncul korelasi negatif palsu (r < 0). Nilai X tinggi 'menjelaskan' lolosnya seleksi. |
| Analisis Kausal (Judea Pearl DAG) | Variabel C bertindak sebagai collider (panah X dan Y sama-sama mengarah ke C) | Mengkondisikan collider membuka blokade kausal dan menciptakan dependensi semu. |

## 5. Real-World Case Study & Benchmark Numbers
Fenomena ini pertama kali diungkap oleh statistikawan Joseph Berkson (1946) di data rumah sakit. Pasien diabetes kelihatannya punya risiko lebih rendah menderita batu empedu (cholecystitis), sehingga dokter sempat menduga diabetes mencegah batu empedu! Padahal, orang dirawat di rumah sakit jika punya penyakit A ATAU penyakit B. Orang yang sehat dari keduanya tidak masuk rumah sakit, sehingga di antara pasien rawat inap muncul korelasi negatif semu. Di machine learning modern, jika startup memfilter resume hanya yang punya (GPA > 3.5 ATAU Pengalaman > 3 Tahun), model klasifikasi kamu akan belajar bahwa GPA tinggi 'mengurangi' pengalaman kerja (explaining-away effect), padahal itu murni artifact dari proses filtering data!

## 6. Actionable Solution / Future Knowledge
Buktikan sendiri ilusi statistik ini di Python dengan 15 baris kode berikut, dan selalu buat causal DAG sebelum memfilter data training:

```python
import numpy as np
import pandas as pd

# 1. Generate 10.000 data populasi independen (Rasa Makanan vs Lokasi Strategis)
np.random.seed(42)
food_quality = np.random.normal(70, 10, 10000)
location_score = np.random.normal(70, 10, 10000)

pop_df = pd.DataFrame({'food': food_quality, 'location': location_score})
r_pop = pop_df['food'].corr(pop_df['location'])
print(f"Korelasi di populasi umum: {r_pop:.3f} (Murni independen)")

# 2. Filter seleksi: Restoran hanya bertahan jika Total Skor > 155 (Collider C)
survived_df = pop_df[(pop_df['food'] + pop_df['location']) > 155]
r_survived = survived_df['food'].corr(survived_df['location'])
print(f"Korelasi pada restoran bertahan: {r_survived:.3f} (Korelasi negatif palsu!)")
```

## 7. Summary Pull-Quote
> "Ketika kamu memotong data hanya pada yang berhasil lolos seleksi, korelasi yang kamu temukan sering kali hanyalah bayangan dari kriteria filter kamu sendiri."

## 8. Closing Call-to-Action (CTA)
Save postingan ini biar kamu gak kejebak bias seleksi saat preprocessing data, dan share ke teman-teman kamu yang lagi belajar machine learning ya bro!

---

## Evidence & Verified Sources
- [Joseph Berkson (1946) : Limitations of the Application of Fourfold Table Analysis to Hospital Data (Biometrics Bulletin)](https://doi.org/10.2307/3002000) - Paper dasar penemu Berkson's Fallacy akibat seleksi pasien rumah sakit.
- [Judea Pearl (2009) : Causality - Models, Reasoning, and Inference (Cambridge University Press)](https://doi.org/10.1017/CBO9780511803161) - Formalisasi grafis Collider Stratification Bias dan d-separation pada Causal DAG.
- [Hernan, Hernandez-Diaz, & Robins (2004) : A structural approach to selection bias (Epidemiology)](https://doi.org/10.1097/01.ede.0000135174.63482.43) - Penjelasan struktural bagaimana pengkondisian collider memicu bias seleksi di dunia nyata.
