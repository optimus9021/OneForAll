import pandas as pd

# Membaca data dari file Excel
data = pd.read_excel('data/processedData/CombinedData/combined-data.xlsx')

# Mendapatkan daftar unik tim dari kolom HomeTeam dan AwayTeam
home_teams = data['HomeTeam'].unique()
away_teams = data['AwayTeam'].unique()

# Menggabungkan kedua daftar tim tanpa duplikasi
list_teams = list(set(list(home_teams) + list(away_teams)))

# Membuat daftar kode tim berdasarkan gabungan HomeTeam dan AwayTeam
kode_teams = {team: i + 1 for i, team in enumerate(list_teams)}  # Menggunakan indeks dimulai dari 1

# Menyimpan daftar kode tim ke dalam file teks
with open('kode_teams.txt', 'w') as file:
    for team, kode in kode_teams.items():
        file.write('"%s" : %d,\n' % (team, kode))
