from Script.modules.prediksi.forebet import forebet
from Script.modules.prediksi.statarea import statarea
import socket
import time

def check_internet():
    try:
        # Coba membuat koneksi ke server DNS Google
        socket.create_connection(("8.8.8.8", 53), timeout=10)
        return True
    except OSError:
        pass
    return False

def main():
    # Periksa koneksi internet
    while not check_internet():
        print("Tidak ada koneksi internet. Menunda eksekusi selama 30 menit.")
        time.sleep(1800)  # Tunda selama 30 menit (1800 detik)

    # Ketika ada koneksi internet
    print("Koneksi internet ditemukan. Menjalankan skrip.")

    forebet()
    statarea()

if __name__ == "__main__":
    main()

