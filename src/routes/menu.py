from src.utility.clearscreen import clear_screen

def menu_utama():
    while True:
        clear_screen()  # Bersihkan terminal sebelum menampilkan menu utama
        print('Selamat Datang Di Menu Program Prediksi Liga Utama Eropa')
        print('\nPilihan Menu Utama:')
        print('1. Ambil Data')
        print('2. Proses Data')
        print('3. Training Model')
        print('4. Validasi')
        print('5. Prediksi')
        print('6. Keluar')
        
        pilihan = input('Masukkan pilihan Anda: ')
        
        if pilihan == '1':
            from src.routes import get
            clear_screen()
            get.get()
        elif pilihan == '2':
            from src.routes import process
            clear_screen()
            process.process()
        elif pilihan == '3':
            from src.routes import training
            clear_screen()
            training.training()
        elif pilihan == '4':
            from src.routes import validasi
            clear_screen()
            validasi.validasi()
        elif pilihan == '5':
            from src.routes import prediksi
            clear_screen()
            prediksi.prediksi()
        elif pilihan == '6':
            clear_screen()
            print('Terima kasih telah menggunakan program.')
            exit()
        else:
            clear_screen()
            print('Pilihan tidak valid. Silakan pilih lagi.')
            menu_utama()