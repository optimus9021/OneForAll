from src.modules.training.xgBoost import make_model
from src.routes.menu import menu_utama
from src.utility.clearscreen import clear_screen
from src.utility.delete_files import delete_file

def training():
    print('Menu Training Model:')
    print('1. Jalankan Proses Pembuatan Model Utama Untuk Prediksi Dan Validasi')
    print('2. Kembali ke Menu Utama')
    print('3. Keluar Aplikasi')
    pilihan = input('Masukkan pilihan Anda: ')
    
    if pilihan == '1':
        clear_screen()
        jalankan_pembuatan_model_utama()
    elif pilihan == '2':
        clear_screen()
        print('Kembali ke Menu Utama.')
        menu_utama()
    elif pilihan == '3':
        clear_screen()
        exit()   
    else:
        clear_screen()
        print('Pilihan tidak valid. Silakan pilih lagi.')
        training()

def jalankan_pembuatan_model_utama():
    print('Pembuatan Model Utama Untuk Prediksi dan Validasi')
    cv_input = int(input('Silahkan Masukkan Jumlah Iterasi yang diinginkan rekomendasi (1000): '))
    konfirmasi = input('Apakah Anda ingin melanjutkan proses? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        print('Silahkan Menunggu Proses Selesai')
        delete_file(folder_path='database/model/model-xgboost/')
        make_model(
            cv=cv_input
        )
        print('Proses Selesai.')
        input('Tekan Enter Untuk Melanjutkan.')
    else:
        clear_screen()
        training()
            

