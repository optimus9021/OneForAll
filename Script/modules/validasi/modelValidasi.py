import pandas as pd
import xgboost as xgb
from tqdm import tqdm
import datetime
from Script.utility.config import logika
from Script.utility.drop_value import modelValidasiUtamaDrop, modelPrediksiUtamaSave
import pickle

def make_validation():
    try:
        total_tasks = 8
        with tqdm(total=total_tasks, desc="Membaca data yang akan diprediksi...") as pbar:    
            # Baca data yang akan diprediksi
            pbar.set_description(f'Membaca data yang akan diprediksi...')
            data1 = pd.read_excel(f'database/data/data-learning/data-1.xlsx')
            datax = pd.read_excel(f'database/data/data-learning/data-X.xlsx')
            data2 = pd.read_excel(f'database/data/data-learning/data-2.xlsx')
            pbar.update(1)

            # Simpan kolom yang dihapus untuk kemudian digabungkan kembali
            pbar.set_description("Menyimpan kolom untuk nanti...")
            deleted_columns = data1[modelPrediksiUtamaSave]
            deleted_columns = datax[modelPrediksiUtamaSave]
            deleted_columns = data2[modelPrediksiUtamaSave]
            pbar.update(1)

            # Hapus kolom yang tidak diperlukan
            pbar.set_description("Menghapus data yang tidak diperlukan untuk prediksi...")
            data1.drop(modelValidasiUtamaDrop, axis=1, inplace=True)
            datax.drop(modelValidasiUtamaDrop, axis=1, inplace=True)
            data2.drop(modelValidasiUtamaDrop, axis=1, inplace=True)
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
            pbar.set_description("Menyimpan hasil evaluasi...")
            output_data = pd.DataFrame()
            output_data['Date'] = deleted_columns['Date']
            output_data['Div'] = deleted_columns['Div']
            output_data['HomeTeam'] = deleted_columns['HomeTeam']
            output_data['AwayTeam'] = deleted_columns['AwayTeam']
            output_data['FTR2'] = hasil_prediksi
            pbar.update(1)
            
            # Simpan hasil prediksi ke file Excel
            pbar.set_description("Menyimpan hasil evaluasi...")
            nama_folder = 'result/hasil-prediksi'
            nama_file = 'Prediksi'
            file_evaluasi = f"{nama_folder}/{nama_file}-Full-Val.xlsx"
            output_data.to_excel(file_evaluasi, index=False)
            pbar.update(1)

        print("Proses selesai.")

    except Exception as e:
        print("Terjadi kesalahan:", str(e))