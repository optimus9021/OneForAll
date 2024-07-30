import pandas as pd
import datetime

def validate_data():
    try:
        # Baca file data
        print('Baca file data')
        file1 = pd.read_excel(f'database/data/data-learning/data.xlsx')
        file1['Date'] = pd.to_datetime(file1['Date'])
        
        # Baca file prediksi
        print('Baca file prediksi')
        file2 = pd.read_excel(f'result/hasil-prediksi/Prediksi-Full-Val.xlsx')
        file2['Date'] = pd.to_datetime(file2['Date'])
        
        # Gabungkan data dari kedua file berdasarkan kolom-kolom yang sesuai
        print('Gabungkan data dari kedua file berdasarkan kolom-kolom yang sesuai')
        merged_data = pd.merge(file1, file2, on=['Div', 'Date', 'HomeTeam', 'AwayTeam'], how='inner')
        
        # Hapus baris yang memiliki nilai null di salah satu kolom
        print('Hapus baris yang memiliki nilai null di salah satu kolom')
        merged_data = merged_data.dropna()
        merged_dataFT = merged_data
        
        # Menghitung jumlah data prediksi yang benar dan salah
        print('Menghitung jumlah data prediksi yang benar dan salah')
        total_dataFT = len(merged_dataFT)
        benarFT = merged_dataFT[
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'HD')) | 
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'HD')) |
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'HA')) |
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'HA')) |
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'DA')) |
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'DA')) | 
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'H' )) |
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'D' )) |
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'A' )) 
                            ]
        salahFT = merged_dataFT[
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'HD')) | 
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'HA')) |
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'DA')) |
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'H' )) |
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'H' )) |
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'D' )) |
                            ((merged_dataFT['FTR'] == 'A') & (merged_dataFT['FTR2'] == 'D' )) |
                            ((merged_dataFT['FTR'] == 'H') & (merged_dataFT['FTR2'] == 'A' )) |
                            ((merged_dataFT['FTR'] == 'D') & (merged_dataFT['FTR2'] == 'A' )) 
                            ]
        jumlah_benarFT = len(benarFT)
        jumlah_salahFT = len(salahFT)
        
        # Menghitung presentase prediksi yang benar dan salah
        print('Menghitung presentase prediksi yang benar dan salah')
        presentase_benarFT = (jumlah_benarFT / total_dataFT) * 100
        presentase_salahFT = (jumlah_salahFT / total_dataFT) * 100
        
        # Menghitung total jumlah data yang benar dan salah
        print('Menghitung total jumlah data yang benar dan salah')
        total_data_benarFT = len(benarFT)
        total_data_salahFT = len(salahFT)
        
        # Hitung jumlah data yang salah per tahun
        print('Hitung jumlah data yang salah per tahun')
        jumlah_salah_per_tahunFT = salahFT.groupby(salahFT['Date'].dt.year).size()
        jumlah_benar_per_tahunFT = benarFT.groupby(benarFT['Date'].dt.year).size()
        
        # Membuat file teks untuk menyimpan hasil
        print('Membuat file teks untuk menyimpan hasil')
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        nama_file_txt = f'validasi-data.txt'
        salahFT_sorted = salahFT.sort_values(by='Date', ascending=True)
        
        # Menampilkan progress bar untuk proses penyimpanan
        print('Menyimpan hasil evaluasi')
        with open(nama_file_txt, 'w') as file:
            file.write(f'Berikut adalah kesimpulan data prediksi \n')
            file.write('\n')
            file.write("Presentase benar FT: {:.2f}%\n".format(presentase_benarFT))
            file.write("Presentase salah FT: {:.2f}%\n".format(presentase_salahFT))
            file.write('\n')
            file.write("Total data prediksi FT: {}\n".format(total_dataFT))
            file.write("Total jumlah data yang benar FT: {}\n".format(total_data_benarFT))
            file.write("Total jumlah data yang salah FT: {}\n".format(total_data_salahFT))
            file.write('\n')
            file.write("FT Selama {} tahun, {} data benar, {} data salah\n".format(len(jumlah_benar_per_tahunFT), sum(jumlah_benar_per_tahunFT), sum(jumlah_salah_per_tahunFT)))
            file.write('\n')
            file.write("Jumlah data yang salah per tahun FT:\n")
            for year, jumlah in jumlah_salah_per_tahunFT.items():
                file.write("{}: {}\n".format(year, jumlah))
            file.write('\n')
            file.write("Jumlah data yang benar per tahun FT:\n")
            for year, jumlah in jumlah_benar_per_tahunFT.items():
                file.write("{}: {}\n".format(year, jumlah))
            file.write('\n')
            file.write("Informasi tambahan FT:\n")
            for year, jumlah in jumlah_salah_per_tahunFT.items():
                benar_tahun = len(benarFT[benarFT['Date'].dt.year == year])
                file.write("Tahun {}: Benar: {}, Salah: {}\n".format(year, benar_tahun, jumlah))
            file.write('\n')      
            file.write("Data FT yang salah:\n")
            for index, row in salahFT_sorted.iterrows():
                file.write('''
{}, {};
    {} vs {}, FTR: {}, Preds: {}. 
    FTHG: {}, FTAG: {}.
    Odds[1]: {}, Odds[x]: {}, Odds[2]: {}.
    Home Point: {}, Away Point: {}. 
'''.format(row['Date'].strftime('%d-%m-%y'),row['Div'], row['HomeTeam'], row['AwayTeam'], row['FTR'], row['FTR2'], row['FTHG'], row['FTAG'], row['MaxH'], row['MaxD'], row['MaxA'], row['HomePoints'], row['AwayPoints']))

        print(f'Proses selesai Data validasi telah disimpan kedalam file: {nama_file_txt}')

    except Exception as e:
        print("Terjadi kesalahan:", str(e))