import requests
import pandas as pd
import datetime

def get_nextFixture_data():
    try:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        url = "https://www.football-data.co.uk/fixtures.xlsx"
        nama_folder = 'database/source/fixture'
        file_name = f"{nama_folder}/fixtures-{timestamp}.xlsx"
        
        # Mengambil respons dari URL
        response = requests.get(url)

        # Mengecek apakah respons sukses (status kode 200)
        if response.status_code == 200:
            print('Status code', response.status_code)
            # Menulis konten respons ke file
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"File '{file_name}' berhasil diunduh.")

            # Setelah unduhan, olah data sesuai kebutuhan
            df = pd.read_excel(file_name)

            # Tentukan kolom yang ingin Anda pertahankan
            kolom_yang_diinginkan = ['Div', 'Date', 'HomeTeam', 'AwayTeam',
                                    # 'FTHG', 'FTAG', 'FTR',
                                    'MaxH', 'MaxD', 'MaxA',
                                    'AvgH', 'AvgD', 'AvgA',
                                    'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA'
                                    ]

            # Buang semua kolom kecuali yang diinginkan
            df = df[kolom_yang_diinginkan]

            df.to_excel('database/data/data-prediksi/data-prediksi.xlsx', index=False)

            print("Data telah disimpan dalam file 'data-prediksi.xlsx'.")
        else:
            print("Gagal mengunduh file. Status respons:", response.status_code)
            
    except Exception as e:
        print("Terjadi kesalahan:", str(e))

