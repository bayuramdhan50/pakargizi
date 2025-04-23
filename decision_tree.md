# Pohon Keputusan Sistem Pakar Gizi

## I. Perhitungan BMI
```
Input: Berat badan (kg), Tinggi badan (cm)
│
└── Validasi Input:
    ├── Berat < 20kg atau Tinggi < 100cm: "Nilai tidak valid"
    └── Input Valid
        │
        └── BMI = Berat (kg) / (Tinggi (m))²
            │
            ├── BMI < 18.5: Status = "Berat badan kurang"
            │   └── Rekomendasi:
            │       ├── Tingkatkan asupan kalori harian
            │       ├── Konsumsi makanan tinggi protein
            │       ├── Makan dengan porsi lebih sering
            │       └── Konsultasikan dengan dokter untuk program penambahan berat badan
            │
            ├── 18.5 ≤ BMI < 25: Status = "Berat badan normal"
            │   └── Rekomendasi:
            │       ├── Pertahankan pola makan sehat
            │       ├── Konsumsi makanan seimbang
            │       └── Jaga aktivitas fisik rutin
            │
            ├── 25 ≤ BMI < 30: Status = "Berat badan berlebih"
            │   └── Rekomendasi:
            │       ├── Kurangi asupan kalori harian
            │       ├── Tingkatkan aktivitas fisik
            │       ├── Batasi makanan tinggi lemak dan gula
            │       └── Konsumsi lebih banyak sayur dan buah
            │
            └── BMI ≥ 30: Status = "Obesitas"
                └── Rekomendasi:
                    ├── Konsultasikan dengan dokter untuk program penurunan berat badan
                    ├── Kurangi porsi makan secara bertahap
                    ├── Hindari makanan tinggi kalori dan lemak
                    └── Lakukan olahraga teratur sesuai kemampuan
```

## II. Analisis Asupan Gizi Per Nutrisi
```
Input: Makanan + Gram
│
└── Untuk setiap nutrisi (Kalori, Protein, Lemak, Karbohidrat, Serat):
    │
    ├── Hitung persentase: (Asupan saat ini / Kebutuhan) × 100%
    │   │
    │   ├── Persentase < 80%: Status = "Kurang"
    │   │   │
    │   │   └── Jika nutrient = "Kalori":
    │   │       │
    │   │       ├── Persentase < 60%:
    │   │       │   └── Rekomendasi:
    │   │       │       ├── Segera tingkatkan asupan kalori
    │   │       │       ├── Perbanyak frekuensi makan dalam porsi sedang
    │   │       │       └── Pilih makanan padat energi
    │   │       │
    │   │       └── Persentase ≥ 60%:
    │   │           └── Rekomendasi:
    │   │               ├── Tingkatkan porsi makan secara bertahap
    │   │               └── Tambahkan makanan selingan bergizi
    │   │
    │   │   └── Jika nutrient = "Protein":
    │   │       │
    │   │       ├── Persentase < 60%:
    │   │       │   └── Rekomendasi:
    │   │       │       ├── Prioritaskan konsumsi protein hewani
    │   │       │       └── Konsumsi protein nabati
    │   │       │
    │   │       └── Persentase ≥ 60%:
    │   │           └── Rekomendasi:
    │   │               ├── Tambahkan asupan protein dari kacang-kacangan
    │   │               └── Konsumsi produk susu dan daging tanpa lemak
    │   │
    │   │   └── Jika nutrient = "Lemak":
    │   │       └── Rekomendasi:
    │   │           ├── Tambahkan sumber lemak sehat seperti minyak zaitun
    │   │           ├── Konsumsi alpukat
    │   │           └── Konsumsi kacang-kacangan
    │   │
    │   │   └── Jika nutrient = "Karbohidrat":
    │   │       │
    │   │       ├── Persentase < 60%:
    │   │       │   └── Rekomendasi:
    │   │       │       ├── Segera tingkatkan asupan karbohidrat
    │   │       │       └── Konsumsi nasi, roti, kentang
    │   │       │
    │   │       └── Persentase ≥ 60%:
    │   │           └── Rekomendasi:
    │   │               ├── Tambahkan porsi karbohidrat kompleks
    │   │               └── Pilih makanan berserat tinggi
    │   │
    │   ├── 80% ≤ Persentase ≤ 120%: Status = "Cukup"
    │   │   └── Rekomendasi:
    │   │       ├── Asupan sudah sesuai dengan kebutuhan
    │   │       └── Pertahankan pola makan saat ini
    │   │
    │   └── Persentase > 120%: Status = "Berlebih"
    │       │
    │       └── Jika nutrient = "Kalori":
    │           │
    │           ├── Persentase > 150%:
    │           │   └── Rekomendasi:
    │           │       ├── Segera kurangi asupan kalori secara signifikan
    │           │       ├── Konsultasikan dengan ahli gizi
    │           │       └── Tingkatkan aktivitas fisik
    │           │
    │           └── Persentase ≤ 150%:
    │               └── Rekomendasi:
    │                   ├── Kurangi porsi makan secara bertahap
    │                   └── Pilih makanan rendah kalori
    │
    │       └── Jika nutrient = "Lemak":
    │           │
    │           ├── Persentase > 150%:
    │           │   └── Rekomendasi:
    │           │       ├── Segera kurangi konsumsi makanan berlemak
    │           │       ├── Hindari gorengan dan fast food
    │           │       └── Pilih metode memasak yang lebih sehat
    │           │
    │           └── Persentase ≤ 150%:
    │               └── Rekomendasi:
    │                   ├── Kurangi konsumsi makanan berlemak
    │                   └── Pilih metode memasak yang lebih sehat
    │
    │       └── Jika nutrient = "Karbohidrat":
    │           └── Rekomendasi:
    │               ├── Kurangi porsi makanan sumber karbohidrat
    │               ├── Ganti dengan sayuran
    │               └── Pilih karbohidrat kompleks
```

## III. Penentuan Status Gizi Keseluruhan
```
Input: Status semua nutrisi (Kalori, Protein, Lemak, Karbohidrat, Serat)
│
├── Hitung jumlah nutrisi dengan status "Kurang"
├── Hitung jumlah nutrisi dengan status "Berlebih"
├── Hitung jumlah nutrisi dengan status "Cukup"
│
└── Evaluasi Status Gizi:
    │
    ├── Jika jumlah nutrisi "Kurang" ≥ 2: Status Gizi = "Gizi Kurang"
    │   └── Badge warna merah
    │
    ├── Jika jumlah nutrisi "Berlebih" ≥ 2: Status Gizi = "Gizi Berlebih"
    │   └── Badge warna oranye
    │
    └── Lainnya: Status Gizi = "Gizi Cukup"
        └── Badge warna hijau
```

## Catatan Implementasi

* Sistem menggunakan forward chaining untuk:
  - Mengevaluasi BMI berdasarkan berat dan tinggi badan
  - Mengevaluasi asupan nutrisi relatif terhadap kebutuhan berdasarkan umur dan gender
  - Memberi rekomendasi spesifik untuk setiap jenis nutrisi dan statusnya
  - Menentukan status gizi keseluruhan berdasarkan status masing-masing nutrisi

* Kebutuhan gizi (target) ditentukan dari `kebutuhan_gizi_usia_gender.csv` berdasarkan:
  - Gender (male/female)
  - Kelompok usia

* Nilai gizi makanan diambil dari `daftar_makanan_gizi.csv` dan dihitung berdasarkan:
  - Nilai gizi per 100 gram
  - Jumlah gram yang diinput pengguna
