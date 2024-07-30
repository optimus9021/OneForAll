import pandas as pd
from tqdm import tqdm

def sorting_script_2():
    try:
        # Baca data dari file Excel
        print('Baca data dari file Excel')
        filePath = "database/data/data-learning/data.xlsx"
        data1 = pd.read_excel(filePath)
        data2 = pd.read_excel(filePath)
        datax = pd.read_excel(filePath)
    
        # Filter data berdasarkan divisi
        dataH = data1
        dataA = data2
        dataD = datax

        # Ubah nilai H, A, dan D menjadi nilai yang diinginkan hanya di kolom "FTR"
        dataH['FTR'] = dataH['FTR'].apply(lambda x: 1 if x == 'H' else 0)
        dataA['FTR'] = dataA['FTR'].apply(lambda x: 1 if x == 'A' else 0)
        dataD['FTR'] = dataD['FTR'].apply(lambda x: 1 if x == 'D' else 0)

        # Simpan ke dalam tiga file Excel terpisah
        file_names = [
            f"database/data/data-learning/data-1.xlsx",
            f"database/data/data-learning/data-2.xlsx",
            f"database/data/data-learning/data-X.xlsx"
        ]

        # Inisialisasi loop penyimpanan file
        for df, file_name in zip([dataH, dataA, dataD], file_names):
            df.to_excel(file_name, index=False)
        
        print('Semua proses selesai.')
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
