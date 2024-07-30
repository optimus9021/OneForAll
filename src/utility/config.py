from src.utility.accuracy import p_H, p_A, p_D

test_size = 0.2

# Fungsi logika ada di modelPrediksi.py dan modelvalidasi.py
def logika(positive_probabilities1, positive_probabilitiesx, positive_probabilities2, hasil_prediksi, avgD, avgH, avgA):
    for i in range(len(positive_probabilitiesx)):
        if positive_probabilities1[i] > p_H:
            hasil_prediksi.append("H")
        elif positive_probabilities2[i] > p_A:
            hasil_prediksi.append("A")
        elif positive_probabilitiesx[i] > p_D:
            hasil_prediksi.append("D")
        # elif positive_probabilities1[i] > HD:
        #     hasil_prediksi.append("HD")
        # elif positive_probabilities2[i] > DA:
        #     hasil_prediksi.append("DA")
        # elif positive_probabilities1[i] > 0.80:
        #     hasil_prediksi.append("HA")
        
        else:
            hasil_prediksi.append("")


max_depth = 20
learning_rate = 0.1
n_estimators = 500


# param_grid1 = {
#                     'learning_rate': [0.01, 0.1, 0,3],  # List nilai yang akan di-cari
#                     'max_depth': [5, 10, 15],  # List nilai yang akan di-cari
#                     'n_estimators': [250, 500, 750],  # List nilai yang akan di-cari
#                 }
# param_gridx = {
#                     'learning_rate': [0.01, 0.1, 0,3],  # List nilai yang akan di-cari
#                     'max_depth': [5, 10, 15],  # List nilai yang akan di-cari
#                     'n_estimators': [250, 500, 750],  # List nilai yang akan di-cari
#                 }
# param_grid2 = {
#                     'learning_rate': [0.01, 0.1, 0,3],  # List nilai yang akan di-cari
#                     'max_depth': [5, 10, 15],  # List nilai yang akan di-cari
#                     'n_estimators': [250, 500, 750],  # List nilai yang akan di-cari
#                 }
