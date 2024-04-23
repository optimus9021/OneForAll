import pandas as pd
from tqdm import tqdm

def sorting_script_1():
    try:
        # Baca file Excel
        file_path = 'database/data/data-processed/CombinedData/combined-data.xlsx'
        
        print("Membaca file Excel...")
        df = pd.read_excel(file_path)
        
        # Konversi kolom tanggal ke tipe datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Fungsi untuk menentukan kategori berdasarkan hari
        print('Inisiasi menentukan kategori berdasarkan hari')
        def categorize_day(day):
            if day.weekday() in [4, 5, 6, 0]:   # Jumat (4), Sabtu (5), Minggu (6), Senin (0)
                return '1'
            if day.weekday() in [1, 2, 3]:   # Selasa (1), Rabu (2), Kamis (3), Jumat (4)
                return '0'
        
        # Tambahkan kolom kategori
        print("Menambahkan kolom kategori")
        df['Kategori'] = df['Date'].apply(categorize_day)
        
        # Pisahkan data berdasarkan kategori
        print("Memisahkan data berdasarkan kategori")
        df_weekend = df[df['Kategori'] == '1']
        df_midweek = df[df['Kategori'] == '0']
        df_combined = pd.concat([df_weekend, df_midweek], ignore_index=True) 
        
        # Simpan ke file Excel dengan lembar kerja yang berbeda
        print('Menyimpan ke file Excel')
        nama_folder = 'database/data/data-learning'
        nama_file = 'data.xlsx'
        combined_file = f'{nama_folder}/{nama_file}'
        
        print("Menyimpan data gabungan...")
        with tqdm(total=1, desc="Saving Combined Data") as pbar:
            with pd.ExcelWriter(combined_file) as writer:
                df_combined.to_excel(writer, sheet_name='Combined', index=False)
            pbar.update(1)
        
        print("Proses selesai.")
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
