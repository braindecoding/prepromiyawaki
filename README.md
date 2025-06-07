# Prepromiyawaki

**Data Preprocessing Dataset Miyawaki**

Repositori ini berisi script untuk preprocessing dataset Miyawaki berdasarkan `create_conditions_2to5_sharp.py`.

## 📋 Deskripsi

Script ini memproses dataset Miyawaki original untuk menghasilkan dataset yang telah difilter dan diproses untuk berbagai kondisi (2-5) dengan format yang telah distandarisasi.

## 📁 Input Files

### File Input Utama
```
data/de_s1_V1_Ecc1to11_baseByRestPre_smlr_s1071119ROI_resol10_leave0_1x1_preprocessed.mat
```

**Dataset Miyawaki ORIGINAL** yang berisi:
- ✅ Semua 5 conditions (1, 2, 3, 4, 5)
- ✅ Semua 32 sessions (1-32)
- ✅ Total 1,152 trials
- ✅ Format 10x10 pixel stimulus asli

## ⚙️ Parameter Konfigurasi

### Threshold Filtering
- `threshold_variance = 0.01` - Minimum variance untuk filter homogeneous
- `threshold_range = 0.1` - Minimum range (max-min) untuk filter homogeneous

### Target Dataset Size
- `target_train_size = 150` - Jumlah sample training yang diinginkan
- `target_test_size = 18` - Jumlah sample testing yang diinginkan

## � Proses Preprocessing

1. **Load** file original Miyawaki
2. **Filter** untuk masing-masing condition (2, 3, 4, 5)
3. **Filter homogeneous stimuli** (menghapus stimulus abu-abu polos)
4. **Resize** dari 10x10 ke 28x28 dengan sharp integer scaling
5. **Standardize** fMRI data
6. **Split** menjadi train/test
7. **Save** ke file terpisah

## � Output Files

Script akan menghasilkan file-file berikut:

```
miyawaki_condition2_geometrical_sharp.mat
miyawaki_condition3_alphabet_1a_sharp.mat
miyawaki_condition4_alphabet_1b_sharp.mat
miyawaki_condition5_alphabet_2_sharp.mat
miyawaki_conditions_2to5_combined_sharp.mat
```

### 📋 Struktur Atribut Output Files

Setiap file `.mat` yang dihasilkan memiliki struktur atribut sebagai berikut:

#### 🔹 File Individual (Condition 2, 3, 4, 5)

| Atribut | Dimensi | Deskripsi |
|---------|---------|-----------|
| `fmriTrn` | (n_train, 967) | Data fMRI training yang telah distandarisasi |
| `stimTrn` | (n_train, 784) | Stimulus training (28x28 pixels, flattened) |
| `fmriTest` | (n_test, 967) | Data fMRI testing yang telah distandarisasi |
| `stimTest` | (n_test, 784) | Stimulus testing (28x28 pixels, flattened) |
| `labelTrn` | (n_train, 1) | Label kondisi untuk training data |
| `labelTest` | (n_test, 1) | Label kondisi untuk testing data |

#### 🔹 File Combined (Conditions 2-5)

| Atribut | Dimensi | Deskripsi |
|---------|---------|-----------|
| `fmriTrn` | (107, 967) | Data fMRI training gabungan semua kondisi |
| `stimTrn` | (107, 784) | Stimulus training gabungan (28x28 pixels, flattened) |
| `fmriTest` | (12, 967) | Data fMRI testing gabungan semua kondisi |
| `stimTest` | (12, 784) | Stimulus testing gabungan (28x28 pixels, flattened) |
| `labelTrn` | (107, 1) | Label kondisi untuk training data (2, 3, 4, atau 5) |
| `labelTest` | (12, 1) | Label kondisi untuk testing data (2, 3, 4, atau 5) |

### 📊 Detail Ukuran Dataset per Kondisi

| Kondisi | Deskripsi | Sessions | Original Trials | Filtered Trials | Train | Test |
|---------|-----------|----------|----------------|----------------|-------|------|
| **2** | Geometrical figures | 21-24 | 84 | 40 (47.6%) | 35 | 4 |
| **3** | Alphabet letters-1A | 25-26 | 42 | 20 (47.6%) | 17 | 2 |
| **4** | Alphabet letters-1B | 27-28 | 42 | 20 (47.6%) | 17 | 2 |
| **5** | Alphabet letters-2 | 29-32 | 84 | 40 (47.6%) | 35 | 4 |
| **2-5** | Combined | 21-32 | 252 | 120 (47.6%) | 107 | 12 |

### 🎯 Karakteristik Data

- **fMRI Data**: 967 voxels dari area V1, telah distandarisasi
- **Stimulus**: Diubah dari 10x10 ke 28x28 pixels menggunakan sharp integer scaling
- **Range Stimulus**: Dinormalisasi ke [0.0, 1.0]
- **Filtering**: Homogeneous stimuli (abu-abu polos) telah dihapus
- **Format**: MATLAB `.mat` files yang kompatibel dengan scipy.io

## 📋 Persyaratan

### File yang Diperlukan
- `data/de_s1_V1_Ecc1to11_baseByRestPre_smlr_s1071119ROI_resol10_leave0_1x1_preprocessed.mat`

### Dependencies
- `scipy.io` - untuk load/save .mat files
- `numpy` - untuk array operations
- `matplotlib.pyplot` - untuk visualisasi

## 🚀 Cara Penggunaan

Pastikan file dataset Miyawaki original sudah tersedia di folder `data/` sebelum menjalankan script preprocessing.

---

*Input utama adalah file dataset Miyawaki original yang sudah ada di folder data/.*

