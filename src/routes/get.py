from src.modules.dataproses.getData import get_data
from src.modules.dataproses.getNextFixture import get_nextFixture_data
from src.routes.menu import menu_utama
from src.utility.clearscreen import clear_screen
from src.utility.delete_files import delete_file

def get():
    while True:
        print('Menu Ambil Data:')
        print('1. Ambil Data untuk Learning')
        print('2. Ambil Data untuk Prediksi')
        print('3. Kembali ke Menu Utama')
        print('4. Keluar Aplikasi')
        pilihan = input('Masukkan pilihan Anda: ')
        
        if pilihan == '1':
            clear_screen()
            ambil_data_learning()
        elif pilihan == '2':
            clear_screen()
            ambil_data_prediksi()
        elif pilihan == '3':
            clear_screen()
            menu_utama()
        elif pilihan == '4':
            clear_screen()
            exit()    
        else:
            clear_screen()
            print('Pilihan tidak valid. Silakan pilih lagi.')
            get()

def ambil_data_learning():
    print('Ambil Data untuk Learning.')
    nomor_file = int(input('Masukkan Nomor File yang ingin di Ambil [6-24]: '))
    print(f'Nomor file {nomor_file} dipilih.')
    konfirmasi = input('Apakah Anda ingin melanjutkan proses? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        print('Mengambil Data Untuk Learning.')
        print('Silahkan Menunggu Proses Selesai.')
        get_data(nomor_file=nomor_file)
        print('Proses Selesai.')
        input('Tekan Enter Untuk Melanjutkan')
    else:
        clear_screen()
        get()
        
    konfirmasi = input('Apakah Anda ingin ambil data yang lain? (y/n): ')
    if konfirmasi.lower() == 'y':
        clear_screen()
        ambil_data_learning()  
    else:
        clear_screen()
        get()
            
  
def ambil_data_prediksi():

    clear_screen()
    
    print('Ambil Data untuk Prediksi.')
    print('Silahkan Menunggu Proses Selesai')
    
    delete_file(
            folder_path='database/data/data-prediksi/')
    get_nextFixture_data()
    
    print('Proses Selesai.')
    input('Tekan Enter Untuk Melanjutkan')
    clear_screen()
    get()
        
