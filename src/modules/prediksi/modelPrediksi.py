import pandas as pd
import xgboost as xgb
from tqdm import tqdm
import datetime
from src.utility.config import logika
from src.utility.drop_value import modelPrediksiUtamaDrop, modelPrediksiUtamaSave
import pickle

def make_predictions():
    try:
        total_tasks = 8
        with tqdm(total=total_tasks, desc="Membaca data yang akan diprediksi...") as pbar:    
            # Baca data yang akan diprediksi
            pbar.set_description(f'Membaca data yang akan diprediksi...')
            data1 = pd.read_excel(f'database/data/data-prediksi/processedData-prediksi.xlsx')
            datax = pd.read_excel(f'database/data/data-prediksi/processedData-prediksi.xlsx')
            data2 = pd.read_excel(f'database/data/data-prediksi/processedData-prediksi.xlsx')
            pbar.update(1)

            # Simpan kolom yang dihapus untuk kemudian digabungkan kembali
            pbar.set_description("Menyimpan kolom untuk nanti...")
            deleted_columns = data1[modelPrediksiUtamaSave]
            deleted_columns = datax[modelPrediksiUtamaSave]
            deleted_columns = data2[modelPrediksiUtamaSave]
            pbar.update(1)

            # Hapus kolom yang tidak diperlukan
            pbar.set_description("Menghapus data yang tidak diperlukan untuk prediksi...")
            data1.drop(modelPrediksiUtamaDrop, axis=1, inplace=True)
            datax.drop(modelPrediksiUtamaDrop, axis=1, inplace=True)
            data2.drop(modelPrediksiUtamaDrop, axis=1, inplace=True)
            pbar.update(1)

            # Hapus baris yang mengandung nilai kosong
            pbar.set_description("Menghapus baris yang kosong, jika ada...")
            data1.dropna(axis=0, inplace=True)
            datax.dropna(axis=0, inplace=True)
            data2.dropna(axis=0, inplace=True)
            pbar.update(1)

            data1  = data1.replace(',', '.').astype(float)
            datax  = datax.replace(',', '.').astype(float)
            data2  =  data2.replace(',', '.').astype(float)

            # Lakukan pembacaan model dari file .pkl
            pbar.set_description("Membaca data model untuk prediksi...")
            with open('database/model/model-xgboost/XGBoost-1.pkl', 'rb') as f:
                model1 = pickle.load(f)

            with open('database/model/model-xgboost/XGBoost-x.pkl', 'rb') as f:
                modelx = pickle.load(f)

            with open('database/model/model-xgboost/XGBoost-2.pkl', 'rb') as f:
                model2 = pickle.load(f)
            pbar.update(1)

            # Menghitung Probabilitas
            pbar.set_description("Menghitung probabilitas...")
            probabilities1 = model1.predict_proba(data1)
            positive_probabilities1 = probabilities1[:, 1]  # Ubah probabilitas menjadi persentase
            probabilitiesx = modelx.predict_proba(datax) 
            positive_probabilitiesx = probabilitiesx[:, 1]  # Ubah probabilitas menjadi persentase
            probabilities2 = model2.predict_proba(data2)
            positive_probabilities2 = probabilities2[:, 1]  # Ubah probabilitas menjadi persentase
            pbar.update(1)

            hasil_prediksi = []

            logika(positive_probabilities1, positive_probabilitiesx, positive_probabilities2, hasil_prediksi, datax['AvgD'], data1['AvgH'], data2['AvgA'])

            # Buat DataFrame baru hanya dengan kolom yang diinginkan
            pbar.set_description("Menyimpan hasil prediksi...")
            output_data = pd.DataFrame()
            output_data['Date'] = deleted_columns['Date']
            output_data['Div'] = deleted_columns['Div']
            output_data['HomeTeam'] = deleted_columns['HomeTeam']
            output_data['AwayTeam'] = deleted_columns['AwayTeam']
            output_data['AvgH'] = deleted_columns['AvgH']
            output_data['AvgD'] = deleted_columns['AvgD']
            output_data['AvgA'] = deleted_columns['AvgA']
            output_data['P1'] = positive_probabilities1
            output_data['Px'] = positive_probabilitiesx
            output_data['P2'] = positive_probabilities2
            output_data['Prediksi'] = hasil_prediksi
            pbar.update(1)

            # Simpan hasil prediksi ke file Excel
            pbar.set_description("Menyimpan hasil prediksi...")
            output_data1 = output_data[output_data['Prediksi'] != ''] # Hanya Menyimpan yang nilai prediksi bersih
            nama_folder = 'result/hasil-prediksi'
            nama_file = 'Prediksi'
            file_prediksi1 = f'{nama_folder}/{nama_file}.xlsx'
            file_prediksi2 = f'{nama_folder}/{nama_file}-Full.xlsx'
            output_data1.to_excel(file_prediksi1, index=False)
            output_data.to_excel(file_prediksi2, index=False)
            
            # Membuat file teks untuk menyimpan hasil
            today = datetime.date.today()
            nama_file_txt = f'prediksi-XGBoost-{today}.txt'

            output_data1_sorted1 = output_data1.sort_values(by=['Date'], ascending=True)

            with open(nama_file_txt, 'w') as file:
                for index, row in output_data1_sorted1.iterrows():    
                    file.write(
'''{}, {}, {} vs {}, PrediksiFT: {}, Odds [1]:[{}], [X]:[{}], [2]:[{}].
'''.format(row['Date'].strftime("%d-%m-%Y"), row['Div'], row['HomeTeam'], row['AwayTeam'], row['Prediksi'], row['AvgH'], row['AvgD'], row['AvgA']))    
                pbar.update(1)
                
        print("Proses selesai.")

    except Exception as e:
        print("Terjadi kesalahan:", str(e))
        