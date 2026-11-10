# [Instagram Carousel] Mitos p-value < 0.05: Kenapa 30% Hasil Analisis Lu Bisa Jadi Palsu

> Berapa kali lu denger orang bilang: "p-value 0.03, berarti peluang fitur baru kita berhasil 97%"? Sini kita bedah kenapa itu salah kaprah fatal.

**Category**: Pure Math & Statistics Fundamentals  
**Target Platform**: Instagram Carousel  
**Tone & Audience**: Casual Indonesian ("bro" tone) - Data practitioners & learners  
**Date**: 2026-11-10  
**Status**: Idea 💡  
**Format Type**: Carousel (8-part)  

---

## 1. Title / Headline
Mitos p-value < 0.05: Kenapa 30% Hasil Analisis Lu Bisa Jadi Palsu

## 2. Subtitle / Framing Question
Berapa kali lu denger orang bilang: "p-value 0.03, berarti peluang fitur baru kita berhasil 97%"? Sini kita bedah kenapa itu salah kaprah fatal.

## 3. Background & Relatable Friction (Hook)
Pernah gak lu presentasi hasil A/B testing ke stakeholder atau tim produk, terus dengan bangga bilang: "Bro, p-value kita 0.03, jadi kita yakin 97% fitur baru kita nambah konversi"? Kalau iya, hati-hati bro. Anggapan itu adalah salah satu ilusi statistik paling berbahaya yang bikin banyak startup salah rilis fitur.

## 4. Bridging Explanation & Core Concept
p-value BUKAN probabilitas bahwa hipotesis lu benar, dan BUKAN probabilitas bahwa data lu cuma kebetulan. p-value adalah probabilitas melihat data se-ekstrem itu JIKA kita asumsikan hipotesis nol (H0) benar sejak awal.

| Element | Cara Kerja | Catatan |
|---|---|---|
| Definisi Populer (Salah) | P(H0 benar | Data) = p-value, atau P(Efek nyata) = 1 - p-value | Inverse probability fallacy. Mengabaikan prior probability efek tersebut. |
| Definisi Matematis (Benar) | P(Data teramati atau lebih ekstrem | H0 benar) | Hanya mengukur kompatibilitas data terhadap model nihil, bukan kebenaran hipotesis. |
| Effect Size & Confidence Interval | Mengukur seberapa besar dampak praktis dan rentang estimasi di populasi | Jauh lebih informatif untuk keputusan bisnis daripada sekadar p < 0.05. |

## 5. Real-World Case Study & Benchmark Numbers
Dalam paper klasiknya di Royal Society Open Science (2014), farmakolog dan statistikawan David Colquhoun membuktikan bahwa jika sebuah hipotesis diuji dengan baseline prior odds yang realistis (misal 1:9 atau 10% probabilitas sukses), maka saat lu mendapatkan p-value tepat di ambang batas 0.05 dengan statistical power 80%, False Discovery Rate (FDR) alias risiko false positive-nya minimal mencapai 30% sampai 36%! Artinya, 1 dari 3 fitur yang lu kira 'signifikan' sebenarnya zonk. Ini ditegaskan oleh statement resmi American Statistical Association (ASA, Wasserstein & Lazar 2016): p-value tidak mengukur besar efek praktis, dan threshold p < 0.05 bukan bukti ilmiah bahwa hipotesis itu benar.

## 6. Actionable Solution / Future Knowledge
Jangan cuma laporkan p-value! Di Python, selalu kombinasikan uji signifikansi dengan Effect Size (Cohen's d) dan 95% Confidence Interval agar keputusan bisnis tidak bias sample size:

```python
import numpy as np
from scipy import stats

# Data konversi group A (Control) vs group B (Treatment)
control = np.array([12, 14, 13, 15, 12, 16, 14, 13, 15, 14])
treatment = np.array([16, 17, 15, 18, 17, 19, 16, 17, 18, 17])

# 1. Independent T-Test
t_stat, p_val = stats.ttest_ind(treatment, control)

# 2. Effect Size: Cohen's d (Seberapa besar efek nyatanya)
n1, n2 = len(control), len(treatment)
s_pooled = np.sqrt(((n1 - 1) * np.var(control, ddof=1) + (n2 - 1) * np.var(treatment, ddof=1)) / (n1 + n2 - 2))
cohens_d = (np.mean(treatment) - np.mean(control)) / s_pooled

# 3. 95% Confidence Interval untuk perbedaan mean
diff_mean = np.mean(treatment) - np.mean(control)
se_diff = s_pooled * np.sqrt(1 / n1 + 1 / n2)
ci_low, ci_high = stats.t.interval(0.95, df=n1 + n2 - 2, loc=diff_mean, scale=se_diff)

print(f"p-value: {p_val:.4f} (Signifikan secara statistik)")
print(f"Cohen's d: {cohens_d:.2f} (Effect size besar: > 0.8)")
print(f"95% CI Difference: [{ci_low:.2f}, {ci_high:.2f}] unit")
```

## 7. Summary Pull-Quote
> "p-value memberi tahu lu seberapa aneh data lu di dunia tanpa efek, bukan seberapa benar klaim lu di dunia nyata."

## 8. Closing Call-to-Action (CTA)
Save dulu buat bekal presentasi A/B test lu berikutnya, dan jangan lupa share ke temen satu tim data lu ya bro!

---

## Evidence & Verified Sources
- [Wasserstein & Lazar (2016) : The ASA Statement on p-Values: Context, Process, and Purpose (The American Statistician)](https://doi.org/10.1080/00031305.2016.1154108) - 6 Prinsip resmi American Statistical Association terkait misuse dan batas p-value.
- [David Colquhoun (2014) : An investigation of the false discovery rate and the misinterpretation of p-values (Royal Society Open Science)](https://doi.org/10.1098/rsos.140216) - Kalkulasi matematis False Discovery Rate mencapai >= 30% pada p = 0.05 dengan prior odds 1:9.
- [Amrhein, Greenland, & McShane (2019) : Scientists rise up against statistical significance (Nature)](https://doi.org/10.1038/d41586-019-00857-9) - Seruan >800 ilmuwan untuk menghentikan dikotomi biner signifikan vs tidak signifikan.
