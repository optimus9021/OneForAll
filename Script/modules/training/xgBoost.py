import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import train_test_split, GridSearchCV
from Script.utility.config import test_size
from Script.utility.config import max_depth, learning_rate, n_estimators
from Script.utility.drop_value import modelTrainingDrop
import pickle

def make_model(cv):
    try:
            print(f'Membaca Data')

            excel_file1 = f'database/data/data-learning/data-1.xlsx' 
            excel_filex = f'database/data/data-learning/data-X.xlsx' 
            excel_file2 = f'database/data/data-learning/data-2.xlsx'

            data1  = pd.read_excel(excel_file1)
            datax  = pd.read_excel(excel_filex)
            data2  = pd.read_excel(excel_file2)

            label_encoder = LabelEncoder()

            print("Menghapus kolom yang tidak diperlukan...")
            data1.drop(modelTrainingDrop, axis=1, inplace=True)
            datax.drop(modelTrainingDrop, axis=1, inplace=True)
            data2.drop(modelTrainingDrop, axis=1, inplace=True)

            print("Menghapus baris dengan nilai kosong...")
            data1.dropna(axis=0, inplace=True)
            datax.dropna(axis=0, inplace=True)
            data2.dropna(axis=0, inplace=True)

            print("Membuat kolom margin berdasarkan kolom 'FTR'...")
            margin1  = data1['FTR']
            data1.drop(['FTR'], axis=1, inplace=True)
            marginx  = datax['FTR']
            datax.drop(['FTR'], axis=1, inplace=True)
            margin2  = data2['FTR']
            data2.drop(['FTR'], axis=1, inplace=True)

            print("Mengganti koma dengan titik untuk kolom yang berisi angka desimal...")
            data1  = data1.replace(',', '.').astype(float)
            datax  = datax.replace(',', '.').astype(float)
            data2  =  data2.replace(',', '.').astype(float)

            print("Konversi dataset ke dalam bentuk array NumPy...")
            data1  = data1.values.astype(float)
            datax  = datax.values.astype(float)
            data2  = data2.values.astype(float)

            print("Mengubah target prediksi menjadi 0 atau 1...")
            margin1 = label_encoder.fit_transform(margin1)
            marginx = label_encoder.fit_transform(marginx)
            margin2 = label_encoder.fit_transform(margin2)

            x1_train, x1_test, y1_train, y1_test = train_test_split(data1, margin1, test_size=test_size)
            xx_train, xx_test, yx_train, yx_test = train_test_split(datax, marginx, test_size=test_size)
            x2_train, x2_test, y2_train, y2_test = train_test_split(data2, margin2, test_size=test_size)
            
            print("Inisialisasi model XGBoost dengan parameter yang telah ditentukan...")

            xgb_model1 = xgb.XGBClassifier(
                objective='binary:logistic',
                learning_rate= learning_rate,
                max_depth= max_depth,
                n_estimators= n_estimators
            )
            xgb_modelx = xgb.XGBClassifier(
                objective='binary:logistic',
                learning_rate= learning_rate,
                max_depth= max_depth,
                n_estimators= n_estimators
            )
            xgb_model2 = xgb.XGBClassifier(
                objective='binary:logistic',
                learning_rate= learning_rate,
                max_depth= max_depth,
                n_estimators= n_estimators
            )

            print('Inisialisasi list untuk menyimpan hasil akurasi dan presisi')
            accuracy1_results = []
            precision1_results = []
            accuracyx_results = []
            precisionx_results = []
            accuracy2_results = []
            precision2_results = []

            # Lakukan iterasi sebanyak n kali untuk melatih model
            num_iterations = cv

            print('Melatih Model')
            for i in tqdm(range(num_iterations), desc=f"Training Model 1"):

                # Latih model XGBoost
                xgb_model1.fit(x1_train, y1_train)
                # Lakukan prediksi menggunakan model yang telah dilatih
                predictions1 = xgb_model1.predict(x1_test)
                # Hitung akurasi dari prediksi
                accuracy1 = accuracy_score(y1_test, predictions1)
                accuracy1_results.append(accuracy1)
                # Hitung presisi dari prediksi
                precision1 = precision_score(y1_test, predictions1)
                precision1_results.append(precision1)

            avg_accuracy1 = np.mean(accuracy1_results) * 100
            avg_precision1 = np.mean(precision1_results) * 100

            print(f"Average Accuracy1: {avg_accuracy1:.2f}%")
            print(f"Average Precision1: {avg_precision1:.2f}%")

            for i in tqdm(range(num_iterations), desc=f"Training Model x"):  

                # Latih model XGBoost
                xgb_modelx.fit(xx_train, yx_train)
                # Lakukan prediksi menggunakan model yang telah dilatih
                predictionsx = xgb_modelx.predict(xx_test)
                # Hitung akurasi dari prediksi
                accuracyx = accuracy_score(yx_test, predictionsx)
                accuracyx_results.append(accuracyx)
                # Hitung presisi dari prediksi
                precisionx = precision_score(yx_test, predictionsx)
                precisionx_results.append(precisionx)

            avg_accuracyx = np.mean(accuracyx_results) * 100
            avg_precisionx = np.mean(precisionx_results) * 100

            print(f"Average Accuracyx: {avg_accuracyx:.2f}%")
            print(f"Average Precisionx: {avg_precisionx:.2f}%")

            for i in tqdm(range(num_iterations), desc=f"Training Model 2"):  

                # Latih model XGBoost
                xgb_model2.fit(x2_train, y2_train)
                # Lakukan prediksi menggunakan model yang telah dilatih
                predictions2 = xgb_model2.predict(x2_test)
                # Hitung akurasi dari prediksi
                accuracy2 = accuracy_score(y2_test, predictions2)
                accuracy2_results.append(accuracy2)
                # Hitung presisi dari prediksi
                precision2 = precision_score(y2_test, predictions2)
                precision2_results.append(precision2)

            avg_accuracy2 = np.mean(accuracy2_results) * 100
            avg_precision2 = np.mean(precision2_results) * 100

            print(f"Average Accuracy2: {avg_accuracy2:.2f}%")
            print(f"Average Precision2: {avg_precision2:.2f}%")

            print("---------------------------------------------------")

            nama_folder = 'database/model/model-xgboost'
            print(f"Menyimpan model ke dalam file pickle...")
            with open(f'{nama_folder}/xgboost-1.pkl', 'wb') as f:
                pickle.dump(xgb_model1, f)
            with open(f'{nama_folder}/xgboost-x.pkl', 'wb') as f:
                pickle.dump(xgb_modelx, f)
            with open(f'{nama_folder}/xgboost-2.pkl', 'wb') as f:
                pickle.dump(xgb_model2, f)

            nama_file = 'Script/utility/accuracy.py'

            acc1 = avg_accuracy1/100
            accx = avg_accuracyx/100
            acc2 = avg_accuracy2/100

            with open(nama_file, 'w') as file:
                file.write(f'Accuracy1 = {acc1}')
                file.write('\n')
                file.write(f'Accuracyx = {accx}')
                file.write('\n')
                file.write(f'Accuracy2 = {acc2}')
                file.write('\n')
                file.write('mean_acc = (Accuracy1+Accuracy2+Accuracyx)/3')
                file.write('\n')
                file.write('n_H = mean_acc/Accuracy1')
                file.write('\n')
                file.write('n_A = mean_acc/Accuracy2')
                file.write('\n')
                file.write('n_D = mean_acc/Accuracyx')
                file.write('\n')
                file.write('p_H = (mean_acc + n_H)/2')
                file.write('\n')
                file.write('p_A = (mean_acc + n_A)/2')
                file.write('\n')
                file.write('p_D = (mean_acc + n_D)/2')
                
            print("Proses selesai.")

    except Exception as e:
        print("Terjadi kesalahan:", str(e))