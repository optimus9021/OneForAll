import os

def delete_file(folder_path):
    try:
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f'Semua file di dalam folder {folder_path} Berhasil di hapus.')
        else:
            print('Path yang di berikan bukan sebuah folder.')
    except Exception as e:
        print(f'Error: {e}')
