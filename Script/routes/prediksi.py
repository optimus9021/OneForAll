from Script.routes.menu import menu_utama
from Script.utility.clearscreen import clear_screen
from Script.utility.delete_files import delete_file
from Script.modules.prediksi.forebet import forebet
from Script.modules.prediksi.statarea import statarea

def prediksi():
    print('Menu Prediksi:')
    print('1. Jalankan Proses Prediksi Utama')
    print('2. Ambil Prediksi dari situs')
    print('3. Kembali ke Menu Utama')
    print('4. Keluar Aplikasi')
    pilihan = input('Masukkan pilihan Anda: ')
    
    if pilihan == '1':
        clear_screen()
        jalankan_prediksi_utama()
    elif pilihan == '2':
        print('Ambil Prediksi dari situs')
        clear_screen()
        # forebet()
        statarea()
        input('Proses Selesai Silahkan Enter Untuk Melanjutkan, dan kembali ke menu sebelumnya')
        clear_screen()
        prediksi()
    elif pilihan == '3':
        print('Kembali ke Menu Utama.')
        clear_screen()
        menu_utama()
    elif pilihan == '4':
        clear_screen()
        exit()  
    else:
        clear_screen()
        print('Pilihan tidak valid. Silakan pilih lagi.')
        prediksi()

def jalankan_prediksi_utama():
    print('Jalankan Proses Prediksi utama.')
    konfirmasi_prediksi = input('Apakah Anda ingin melakukan prediksi? (y/n): ')
    if konfirmasi_prediksi.lower() == 'y':
        clear_screen()
        print('Silahkan Menunggu Proses Selesai')
        print('Predicting......')
        delete_file(
            folder_path='result/hasil-prediksi/')
        from Script.modules.prediksi.modelPrediksi import make_predictions
        make_predictions()
        print('Proses Selesai.')
        input('Tekan Enter Untuk Melanjutkan')
        clear_screen()
        prediksi()
    else:
        clear_screen()
        prediksi()


