# Sistem Pakar Penilaian Status Gizi dan Rekomendasi Makanan

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Sistem pakar yang membantu pengguna menilai status gizi mereka dan memberikan rekomendasi makanan berdasarkan kebutuhan nutrisi spesifik.

## 🌟 Fitur Utama

- 📊 Perhitungan dan analisis BMI (Body Mass Index)
- 🍽️ Penilaian asupan gizi berdasarkan makanan yang dikonsumsi
- 📈 Perbandingan asupan dengan kebutuhan gizi harian
- 🎯 Rekomendasi makanan berdasarkan status gizi
- 📱 Antarmuka yang responsif dan mudah digunakan

## 🚀 Teknologi yang Digunakan

- **Backend**: Python dengan Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: File CSV untuk data makanan dan kebutuhan gizi
- **Metode**: Forward Chaining untuk sistem pakar

## 📋 Persyaratan Sistem

- Python 3.x
- Flask
- Pandas
- NumPy

## 🛠️ Instalasi dan Penggunaan

1. Clone repositori ini:
```bash
git clone [url-repositori]
```

2. Pindah ke direktori proyek:
```bash
cd pakargizi
```

3. Instal dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:
```bash
python app.py
```

5. Buka browser dan akses:
```
http://localhost:5000
```

## 📖 Cara Penggunaan

1. Masukkan data pribadi:
   - Umur
   - Jenis kelamin
   - Berat badan (kg)
   - Tinggi badan (cm)

2. Pilih makanan yang dikonsumsi:
   - Pilih makanan dari daftar
   - Masukkan jumlah gram

3. Klik tombol "Hitung Kebutuhan Gizi" untuk melihat:
   - Status BMI
   - Status gizi keseluruhan
   - Perbandingan asupan dengan kebutuhan
   - Rekomendasi makanan

## 📊 Basis Pengetahuan

Sistem menggunakan dua sumber data utama:

1. `kebutuhan_gizi_usia_gender.csv`
   - Kebutuhan gizi berdasarkan usia dan jenis kelamin
   - Parameter: kalori, protein, lemak, karbohidrat, serat

2. `daftar_makanan_gizi.csv`
   - Database makanan dengan kandungan gizi per 100 gram
   - Mencakup berbagai jenis makanan lokal Indonesia

## 🧠 Mesin Inferensi

Menggunakan metode forward chaining dengan alur:

1. **Input Processing**
   - Validasi data pengguna
   - Perhitungan BMI
   - Kalkulasi total asupan gizi

2. **Analisis**
   - Evaluasi status BMI
   - Evaluasi status nutrisi
   - Penentuan status gizi keseluruhan

3. **Output**
   - Status gizi
   - Rekomendasi perbaikan
   - Saran makanan

## 📈 Kategori Status Gizi

### BMI Status
- < 18.5: Berat badan kurang
- 18.5 - 24.9: Berat badan normal
- 25 - 29.9: Berat badan berlebih
- ≥ 30: Obesitas

### Status Nutrisi
- < 80%: Kurang
- 80% - 120%: Cukup
- > 120%: Berlebih

## 📝 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
