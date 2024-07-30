import os

def clear_screen():
    # Cek sistem operasi
    if os.name == 'nt':  # Jika sistem operasi Windows
        os.system('cls')
    else:  # Untuk sistem operasi lain seperti Linux dan macOS
        os.system('clear')
