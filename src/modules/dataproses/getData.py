import pandas as pd
import requests
from io import BytesIO

def get_data(nomor_file):
    
    print('Ambil data dari URL file Excel')
    n_f2 = nomor_file
    n_f1 = n_f2 - 1
    url = f'https://www.football-data.co.uk/mmz4281/{n_f1}{n_f2}/all-euro-data-20{n_f1}-20{n_f2}.xlsx'
    nama_folder = 'database/data/data-unprocessed'
    nama_file = f'{nama_folder}/data-{nomor_file}.xlsx'

    print('Lakukan permintaan untuk mengunduh file Excel')
    response = requests.get(url)

    print('Periksa status respons')
    if response.status_code == 200:
        print('status ', response.status_code)
        print('Baca file Excel dari respons')
        excel_data = response.content
        excel_file = BytesIO(excel_data)
        all_data = pd.read_excel(excel_file, sheet_name=None)

        # Inisialisasi dictionary untuk menyimpan data dari setiap sheet
        all_data_combined = {}

        # Tentukan kolom yang ingin Anda pertahankan
        kolom_yang_diinginkan = ['Div', 'Date', 'HomeTeam', 'AwayTeam',
                                'FTHG', 'FTAG', 'FTR',
                                'MaxH', 'MaxD', 'MaxA',
                                'AvgH', 'AvgD', 'AvgA',
                                'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA'
                                ]  # Ganti dengan nama kolom yang Anda inginkan

        print('Gabungkan data dari semua sheet')
        for sheet_name, df in all_data.items():
            # Buang semua kolom kecuali yang diinginkan
            df = df[kolom_yang_diinginkan]
            all_data_combined[sheet_name] = df

        print('Gabungkan semua data dari dictionary menjadi satu DataFrame tunggal')
        combined_df = pd.concat(all_data_combined.values(), ignore_index=True)

        print('Simpan data gabungan ke dalam file Excel')
        combined_df.to_excel(nama_file, index=False)

        print(f'Data dari semua lembar kerja telah digabungkan dan disimpan dalam file "data-{nomor_file}.xlsx"')
        return combined_df
    else:
        print("Gagal mengunduh file Excel.", response.status_code)
        return None
