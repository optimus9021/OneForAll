import pandas as pd
import os
from tqdm import tqdm

def combine_processed_data():
    try:
        print('Dapatkan jalur direktori saat ini (direktori skrip Python berada)')
        directory = 'database/data/data-processed/'

        print('Inisialisasi list untuk menyimpan DataFrame dari setiap file Excel')
        dfs = []

        print('Hitung jumlah file Excel dalam direktori')
        num_files = sum(1 for filename in os.listdir(directory) if filename.endswith('.xlsx'))

        # Inisialisasi tqdm progress bar
        with tqdm(total=num_files, desc="Combining Excel Files") as pbar:
            # Loop melalui setiap file dalam direktori
            for filename in os.listdir(directory):
                if filename.endswith('.xlsx'):
                    # Baca file Excel dan tambahkan DataFrame ke dalam list
                    file_path = os.path.join(directory, filename)
                    df = pd.read_excel(file_path)
                    dfs.append(df)
                    
                    # Update progress bar
                    pbar.update(1)

        print('Gabungkan semua DataFrame menjadi satu DataFrame tunggal')
        combined_df = pd.concat(dfs, ignore_index=True)

        print('Tulis DataFrame gabungan ke dalam file Excel baru')
        nama_folder = 'database/data/data-processed/CombinedData'
        combined_file_path = f'{nama_folder}/combined-data.xlsx'  # Ganti dengan nama file Excel yang diinginkan
        combined_df.to_excel(combined_file_path, index=False)

        print('Proses selesai.')
    except Exception as e:
        print("Terjadi kesalahan:", str(e))

