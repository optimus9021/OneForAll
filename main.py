import os
from Script.routes.menu import menu_utama
from Script.utility.clearscreen import clear_screen

def create_folders(root_path, structure):
    """
    Membuat struktur folder berdasarkan struktur yang diberikan.
    
    Args:
    - root_path (str): Path root di mana struktur folder akan dibuat.
    - structure (dict): Dictionary yang berisi struktur folder yang akan dibuat.
    """
    try:
        for folder, subfolders in structure.items():
            folder_path = os.path.join(root_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            if isinstance(subfolders, list):  # Jika subfolders adalah list, buat langsung
                for subfolder in subfolders:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
            elif isinstance(subfolders, dict):  # Jika subfolders adalah dictionary, panggil fungsi create_folders secara rekursif
                create_folders(folder_path, subfolders)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Struktur folder yang akan dibuat
folder_structure = {
    "database": {
        "model": ["model-xgboost"],
        "data": {
            "data-learning": [],
            "data-processed": ["CombinedData"],
            "data-prediksi": [],
            "data-unprocessed": [],
        },
        "source": ["fixture"]
    },
    "result": ["hasil-prediksi"]
}

# Jalur utama di mana struktur folder akan dibuat
main_path = os.path.abspath(os.path.dirname(__file__))

# Panggil fungsi untuk membuat struktur folder
create_folders(main_path, folder_structure)
clear_screen()  # Bersihkan layar terminal sebelum menampilkan menu
menu_utama()
