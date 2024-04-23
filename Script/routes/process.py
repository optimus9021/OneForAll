from Script.modules.dataproses.learningDataProcess import process_data
from Script.modules.dataproses.combineData import combine_processed_data
from Script.modules.dataproses.combineDataProcess import sorting_script_1
from Script.modules.dataproses.splittingData import sorting_script_2
from Script.modules.dataproses.nextFixtureProcess import process_nextFixture
from Script.routes.menu import menu_utama
from Script.utility.clearscreen import clear_screen
from Script.utility.delete_files import delete_file

def process():
    print('Menu Proses Data:')
    print('1. Proses Data Learning')
    print('2. Proses Data Prediksi')
    print('3. Combining Data Learning')
    print('4. Kembali ke Menu Utama')
    print('5. Keluar Aplikasi')
    print('6. Hanya Bagi Data Per-Divisi')
    pilihan = input('Masukkan pilihan Anda: ')
    
    if pilihan == '1':
        clear_screen()
        proses_data_learning()
    elif pilihan == '2':
        clear_screen()
        proses_data_prediksi()
    elif pilihan == '3':
        clear_screen()
        combining_data_learning()
    elif pilihan == '4':
        clear_screen()
        print('Kembali ke Menu Utama.')
        menu_utama()
    elif pilihan == '5':
        clear_screen()
        exit()
    elif pilihan == '6':
        clear_screen()
        bagi_data_perdivisi()
    else:
        clear_screen()
        print('Pilihan tidak valid. Silakan pilih lagi.')
        process()

def proses_data_learning():
    print('Proses Data Learning.')
    konfirmasi = input('Apakah Anda ingin melanjutkan proses? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        print('Silahkan Menunggu Proses Selesai')
        print('Processing Data')
        n = int(input('Masukkan Nomor File awal yang akan diproses dari 20 sampai 24: '))
        print(f'Nomor file {n} dipilih.')
        process_data(n)
        print('Proses Selesai')
        input('Tekan Enter Untuk Melanjutkan.')
    else:
        clear_screen()
        process()

def combining_data_learning():
    print('Combining Data Learning.')
    konfirmasi = input('Apakah Anda ingin melanjutkan proses? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        print('Silahkan Menunggu Proses Selesai')
        delete_file(
            folder_path='database/data/data-learning/')
        combine_processed_data()
        clear_screen()
        sorting_script_1()
        clear_screen()
        sorting_script_2()
        print('Proses Selesai.')
        input('Tekan Enter Untuk Melanjutkan')
    else:  
        clear_screen()
        process()

def bagi_data_perdivisi():
    sorting_script_2()
    print('Proses Selesai')
    input('Tekan Enter Untuk Melanjutkan.')

def proses_data_prediksi():
    print('Proses Data Prediksi Dipilih')
    nomor_file = int(input('Masukkan Nomor File terakhir untuk digabungkan dengan next match yang akan diproses: '))
    print(f'Nomor file {nomor_file} dipilih.')
    konfirmasi = input('Apakah Anda ingin melanjutkan proses? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        print('Proses Data Prediksi.')
        print('Silahkan Menunggu Proses Selesai')
        process_nextFixture(nomor_file=nomor_file)
        print('Proses Selesai.')
        input('Tekan Enter Untuk Melanjutkan')
    else:
        clear_screen()
        process()
