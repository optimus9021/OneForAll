# OneForAll - Dokumentasi Lengkap Aplikasi

## 📋 Ringkasan Proyek

**OneForAll** adalah aplikasi prediksi pertandingan sepak bola liga utama Eropa yang dikembangkan menggunakan Python. Aplikasi ini menggunakan machine learning dengan algoritma XGBoost untuk memprediksi hasil pertandingan berdasarkan data historis dan statistik odds dari bookmarkers.

### 🎯 Tujuan Utama
- Memprediksi hasil pertandingan sepak bola (Home Win, Draw, Away Win)
- Menggunakan machine learning untuk analisis odds dari bookmarkers
- Menyediakan interface yang mudah digunakan untuk proses training dan prediksi

## 🏗️ Struktur Folder

```
OneForAll/
├── database/                          # Database utama
│   ├── data/
│   │   ├── data-learning/            # Data untuk training model
│   │   ├── data-processed/           # Data yang telah diproses
│   │   │   └── CombinedData/         # Data gabungan
│   │   ├── data-prediksi/            # Data untuk prediksi
│   │   └── data-unprocessed/         # Data mentah
│   ├── model/
│   │   └── model-xgboost/            # Model XGBoost (.pkl files)
│   └── source/
│       └── fixture/                  # Data fixture pertandingan
├── result/
│   └── hasil-prediksi/               # Hasil prediksi (.xlsx)
├── src/                              # Source code
│   ├── modules/
│   │   ├── dataproses/               # Modul pemrosesan data
│   │   ├── prediksi/                 # Modul prediksi
│   │   ├── training/                 # Modul training model
│   │   └── validasi/                 # Modul validasi
│   ├── routes/                       # Routing aplikasi
│   └── utility/                      # Utility functions
├── main.py                           # Entry point utama
├── sitepred.py                       # Script prediksi otomatis
├── requirements.txt                  # Dependencies
└── README.md                         # Dokumentasi singkat
```

## 🚀 Cara Instalasi dan Penggunaan

### Instalasi
```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python main.py
```

### Penggunaan Manual
Aplikasi memiliki menu interaktif dengan 6 pilihan utama:
1. **Ambil Data** - Mengambil data untuk learning atau prediksi
2. **Proses Data** - Memproses data yang sudah diambil
3. **Training Model** - Melatih model XGBoost
4. **Validasi** - Memvalidasi model
5. **Prediksi** - Melakukan prediksi pertandingan
6. **Keluar** - Keluar dari aplikasi

## 📊 Arsitektur Aplikasi

### Entry Points

#### 1. `main.py` - Aplikasi Utama
- **Fungsi**: Membuat struktur folder otomatis dan menjalankan menu utama
- **Fitur**:
  - Otomatis membuat folder yang diperlukan
  - Membersihkan layar terminal
  - Menjalankan menu interaktif

#### 2. `sitepred.py` - Script Otomatis
- **Fungsi**: Script prediksi otomatis dengan pengecekan koneksi internet
- **Fitur**:
  - Mengecek koneksi internet setiap 30 menit
  - Otomatis menjalankan prediksi saat konek
  - Mengambil data dari Statarea

### Sistem Routing

#### Menu Utama (`src/routes/menu.py`)
```
1. Ambil Data → src/routes/get.py
2. Proses Data → src/routes/process.py
3. Training Model → src/routes/training.py
4. Validasi → src/routes/validasi.py
5. Prediksi → src/routes/prediksi.py
6. Keluar
```

#### Route Details:

**`src/routes/get.py` - Data Collection**
- Menu ambil data untuk learning (file 6-24)
- Menu ambil data untuk prediksi
- Auto delete existing files

**`src/routes/process.py` - Data Processing**
- Proses data learning
- Proses data prediksi
- Combine data learning
- Bagi data per-divisi

**`src/routes/training.py` - Model Training**
- Pembuatan model utama XGBoost
- Konfigurasi iterasi (rekomendasi: 1000)
- Auto delete existing models

**`src/routes/prediksi.py` - Prediction**
- Proses prediksi utama
- Ambil prediksi dari situs (Statarea)
- Generate output Excel dan text

## 🤖 Core Modules

### 1. Data Processing (`src/modules/dataproses/`)

#### `getData.py`
- Mengambil data historis pertandingan
- Input: nomor file (6-24)
- Output: Excel files di `database/data/data-unprocessed/`

#### `combineData.py`
- Menggabungkan multiple Excel files
- Progress tracking dengan tqdm
- Output: `combined-data.xlsx`

#### `learningDataProcess.py`
- Memproses data untuk training
- Input: nomor file awal (20-24)
- Output: processed data untuk learning

#### `nextFixtureProcess.py`
- Memproses data pertandingan mendatang
- Menggabungkan dengan data historis
- Output: data siap prediksi

### 2. Machine Learning (`src/modules/training/`)

#### `xgBoost.py`
- **Algoritma**: XGBoost Classifier
- **Parameter**:
  - `max_depth`: 20
  - `learning_rate`: 0.1
  - `n_estimators`: 500
  - `test_size`: 0.2
- **Features**:
  - 3 model terpisah (1, X, 2)
  - Cross-validation dengan iterasi configurable
  - Auto save model ke .pkl files
  - Generate accuracy metrics

### 3. Prediction (`src/modules/prediksi/`)

#### `modelPrediksi.py`
- Load 3 model XGBoost (.pkl files)
- Proses prediksi dengan probabilitas
- Logic filtering untuk hasil prediksi
- Output: Excel dan text files

#### `statarea.py`
- **Web Scraping**: old.statarea.com
- **Features**:
  - Auto date-based URL generation
  - Parse match data (time, teams, percentages)
  - Remove duplicates dengan set
  - Save ke text file dengan format khusus
  - Sort by match time

### 4. Validation (`src/modules/validasi/`)
- `ValidasiData.py` - Validasi dataset
- `modelValidasi.py` - Validasi model accuracy

## ⚙️ Konfigurasi

### `src/utility/config.py`
```python
# Model Parameters
max_depth = 20
learning_rate = 0.1
n_estimators = 500
test_size = 0.2

# Prediction Logic Thresholds (dari accuracy.py)
p_H, p_A, p_D = probabilities thresholds
```

### `src/utility/accuracy.py`
- Auto-generated dari training results
- Menghitung accuracy thresholds untuk prediksi
- Logic: `p_H = (mean_acc + n_H)/2`

## 📄 Data Flow

### Training Flow:
1. **Get Data** → Download historical match data
2. **Process Data** → Clean dan combine data
3. **Training** → Train 3 XGBoost models
4. **Validation** → Test model accuracy
5. **Generate Accuracy** → Save thresholds

### Prediction Flow:
1. **Get Next Fixtures** → Download upcoming matches
2. **Process Prediction Data** → Prepare features
3. **Load Models** → Load 3 trained models
4. **Predict** → Generate probabilities
5. **Apply Logic** → Filter results menggunakan thresholds
6. **Save Results** → Export Excel dan text

## 🔧 Dependencies Utama

### Machine Learning:
- `xgboost==2.0.3` - Algoritma ML utama
- `scikit-learn==1.4.1` - Preprocessing dan metrics
- `numpy==1.26.4` - Numerical computation
- `pandas==2.2.1` - Data manipulation

### Data Processing:
- `openpyxl==3.1.2` - Excel file handling
- `xlrd==2.0.1` - Excel reading
- `tqdm==4.66.2` - Progress bars

### Web Scraping:
- `requests==2.31.0` - HTTP requests
- `beautifulsoup4==4.12.3` - HTML parsing
- `selenium==4.19.0` - Browser automation (backup)

### Utilities:
- `pickle` - Model serialization
- `datetime` - Date handling
- `os` - File system operations

## 📈 Output Files

### Prediction Results:
- `result/hasil-prediksi/Prediksi.xlsx` - Filtered results only
- `result/hasil-prediksi/Prediksi-Full.xlsx` - All predictions
- `prediksi-XGBoost-YYYY-MM-DD.txt` - Text format output

### Model Files:
- `database/model/model-xgboost/xgboost-1.pkl` - Home win model
- `database/model/model-xgboost/xgboost-x.pkl` - Draw model
- `database/model/model-xgboost/xgboost-2.pkl` - Away win model

### Data Files:
- `database/data/data-learning/data-1.xlsx` - Training data model 1
- `database/data/data-learning/data-X.xlsx` - Training data draw
- `database/data/data-learning/data-2.xlsx` - Training data model 2
- `database/data/data-prediksi/processedData-prediksi.xlsx` - Prediction data

## 🔍 Prediksi Logic

### Threshold Logic (`src/utility/config.py:6-23`):
```python
def logika(positive_probabilities1, positive_probabilitiesx, positive_probabilities2, hasil_prediksi, avgD, avgH, avgA):
    for i in range(len(positive_probabilitiesx)):
        if positive_probabilities1[i] > p_H:
            hasil_prediksi.append("H")  # Home Win
        elif positive_probabilities2[i] > p_A:
            hasil_prediksi.append("A")  # Away Win
        elif positive_probabilitiesx[i] > p_D:
            hasil_prediksi.append("D")  # Draw
        else:
            hasil_prediksi.append("")  # No prediction
```

### Output Format:
```
DD-MM-YYYY, League, HomeTeam vs AwayTeam, PrediksiFT: H/X/A, Odds [1]:[value], [X]:[value], [2]:[value]
```

## 🛡️ Keamanan

Aplikasi ini tidak memiliki sistem autentikasi atau fitur keamanan khusus karena merupakan aplikasi CLI standalone. File disimpan lokal tanpa koneksi database eksternal.

## 🚨 Error Handling

Setiap module memiliki try-catch blocks yang menangani exception dan menampilkan error message yang informatif. Progress tracking dengan tqdm memberikan visual feedback untuk long-running processes.

## 🔄 Maintenance

### Auto Cleanup:
- Auto delete old prediction results
- Auto delete old models before training
- Auto delete existing data before new downloads

### Manual Operations:
- Pilih nomor file untuk data collection
- Konfirmasi sebelum setiap proses besar
- Input iterasi untuk training process

## 📝 Notes

1. **Data Source**: football-data.co.uk untuk historical data
2. **Prediction Source**: Statarea untuk comparison
3. **Model Focus**: XGBoost dengan 3 binary classifiers
4. **Output Format**: Excel dan text files
5. **Internet Required**: Untuk data collection dan web scraping

---

*Dokumentasi ini dibuat berdasarkan analisis lengkap source code OneForAll versi saat ini.*