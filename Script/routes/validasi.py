from Script.modules.validasi.modelValidasi import make_validation
from Script.modules.validasi.ValidasiData import validate_data
from Script.routes.menu import menu_utama
from Script.utility.clearscreen import clear_screen

def validasi():
    print('Menu Validasi:')
    print('1. Jalankan Proses Validasi')
    print('2. Kembali ke Menu Utama')
    print('3. Keluar Aplikasi')
    pilihan = input('Masukkan pilihan Anda: ')
    
    if pilihan == '1':
        clear_screen()
        jalankan_validasi()
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
        validasi()

def jalankan_validasi():

    # Script untuk Evaluasi
    clear_screen()
    print('Evaluating......')
    make_validation()
    input('Tekan Enter')
    clear_screen()
    print('Validating data.')
    validate_data()
    print('Proses Selesai.')
    input('Tekan Enter Untuk Melanjutkan.')
    clear_screen()
    validasi()
