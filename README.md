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

