import pandas as pd
from tqdm import tqdm

def process_nextFixture(nomor_file):
    try:
        print('Membaca Data')
        file_path1 = 'database/data/data-prediksi/data-prediksi.xlsx'
        file_path2 = f'database/data/data-unprocessed/data-{nomor_file}.xlsx'  
        df1 = pd.read_excel(file_path1)
        df2 = pd.read_excel(file_path2)

        df = pd.concat([df1, df2], ignore_index=True)

        print('Mengurutkan data berdasarkan tanggal dan nama HomeTeam')
        df['Date'] = pd.to_datetime(df['Date'])  
        df = df.sort_values(by=['Date', 'HomeTeam', 'AwayTeam'])

        print('Menginisialisasi kolom baru untuk data baru')
        df['HomeWin5'] = 0
        df['HomeLose5'] = 0
        df['AwayWin5'] = 0
        df['AwayLose5'] = 0
        df['GHLast5'] = 0
        df['GALast5'] = 0
        df['Avg.GHome'] = 0
        df['Avg.GAway'] = 0
        df['HomePoints'] = 0
        df['AwayPoints'] = 0

        print('Menghitung total kemenangan dan kekalahan lima pertandingan terakhir untuk tim tuan rumah')
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Last 5 Matches for Home Teams"):
            home_team = row['HomeTeam']
            ftr = row['FTR']

            home_matches = df[(df['HomeTeam'] == home_team) & (df['Date'] < row['Date'])].tail(5)
            home_win_last_5 = home_matches[home_matches['FTR'] == 'H'].shape[0]
            home_lose_last_5 = home_matches[home_matches['FTR'] == 'A'].shape[0]

            df.at[index, 'HomeWin5'] = home_win_last_5
            df.at[index, 'HomeLose5'] = home_lose_last_5

        print('Menghitung total kemenangan dan kekalahan lima pertandingan terakhir untuk tim tamu')
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Last 5 Matches for Away Teams"):
            away_team = row['AwayTeam']
            ftr = row['FTR']

            away_matches = df[(df['AwayTeam'] == away_team) & (df['Date'] < row['Date'])].tail(5)
            away_win_last_5 = away_matches[away_matches['FTR'] == 'A'].shape[0]
            away_lose_last_5 = away_matches[away_matches['FTR'] == 'H'].shape[0]

            df.at[index, 'AwayWin5'] = away_win_last_5
            df.at[index, 'AwayLose5'] = away_lose_last_5

        print('Menghitung total gol home team dan away team untuk setiap pertandingan dalam lima pertandingan terakhir')
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Total Goals for Last 5 Matches for Home & Away Teams"):
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']

            home_matches = df[(df['HomeTeam'] == home_team) & (df['Date'] < row['Date'])].tail(5)
            away_matches = df[(df['AwayTeam'] == away_team) & (df['Date'] < row['Date'])].tail(5)

            total_goals_home_last_5 = home_matches['FTHG'].sum()
            total_goals_away_last_5 = away_matches['FTAG'].sum()

            df.at[index, 'GHLast5'] = total_goals_home_last_5
            df.at[index, 'GALast5'] = total_goals_away_last_5

        print('Menghitung rata-rata goal home team dan away team')
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Avg Goals for Home & Away Teams"):
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            date = row['Date']

            home_goals = df[(df['HomeTeam'] == home_team) & (df['Date'] < date)]['FTHG'].mean()
            away_goals = df[(df['AwayTeam'] == away_team) & (df['Date'] < date)]['FTAG'].mean()

            # Memastikan hasil minimal 0
            home_goals = max(0, home_goals)
            away_goals = max(0, away_goals)

            df.at[index, 'Avg.GHome'] = home_goals
            df.at[index, 'Avg.GAway'] = away_goals

        print('Menghitung poin home team dan away team untuk setiap pertandingan dalam setiap divisi')
        for divisi in tqdm(df['Div'].unique(), desc="Calculating Points for Each Team in Each Divisions"):
            div_df = df[df['Div'] == divisi]
            home_team_points = {}
            away_team_points = {}

            for index, row in div_df.iterrows():
                home_team = row['HomeTeam']
                away_team = row['AwayTeam']
                ftr = row['FTR']

                if home_team not in home_team_points:
                    home_team_points[home_team] = 0
                if away_team not in away_team_points:
                    away_team_points[away_team] = 0

                if ftr == 'H':
                    home_team_points[home_team] += 3
                elif ftr == 'A':
                    away_team_points[away_team] += 3
                elif ftr == 'D':
                    home_team_points[home_team] += 1
                    away_team_points[away_team] += 1

                df.at[index, 'HomePoints'] = home_team_points[home_team]
                df.at[index, 'AwayPoints'] = away_team_points[away_team]

        print("Menambahkan kolom matchweek...")
        df['Date'] = pd.to_datetime(df['Date'])
        df['MatchWeek'] = 0
        matchweeks = {}
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Adding Matchweek"):
            div = row['Div']
            date = row['Date']
            if div not in matchweeks:
                matchweeks[div] = {}
                matchweeks[div]['start_date'] = date
                matchweeks[div]['matchweek'] = 1
            elif (date - matchweeks[div]['start_date']).days >= 7:
                matchweeks[div]['start_date'] = date
                matchweeks[div]['matchweek'] += 1
            df.loc[index, 'MatchWeek'] = matchweeks[div]['matchweek']
            
        print("Menambahkan kolom home last match dan away last match...")
        df['HomeLastMatch'] = 0
        df['AwayLastMatch'] = 0
        last_matches = {}
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Adding Last Matches"):
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            date = row['Date']
            
            if home_team not in last_matches:
                last_matches[home_team] = date
            else:
                df.loc[index, 'HomeLastMatch'] = (date - last_matches[home_team]).days
                last_matches[home_team] = date
            
            if away_team not in last_matches:
                last_matches[away_team] = date
            else:
                df.loc[index, 'AwayLastMatch'] = (date - last_matches[away_team]).days
                last_matches[away_team] = date
        
        print('Buat fungsi untuk menentukan kategori berdasarkan hari')
        def categorize_day(day):
            if day.weekday() in [4, 5, 6, 0]:   # Jumat (4), Sabtu (5), Minggu (6), Senin (0)
                return '1'
            if day.weekday() in [1, 2, 3]:   # Selasa (1), Rabu (2), Kamis (3), Jumat (4)
                return '0'
            
        print('Tambahkan kolom kategori')
        df['Kategori'] = df['Date'].apply(categorize_day)
        df_weekend = df[df['Kategori'] == '1']
        df_midweek = df[df['Kategori'] == '0']
        df_gabungan = pd.concat([df_weekend, df_midweek], ignore_index=True)

        df.drop(['FTHG', 'FTAG', 'FTR'], axis=1, inplace=True)
        df_filter = df[df['Date'].isin(df1['Date'])]

        print(f'Menyimpan hasil ke file Excel')
        df_filter.to_excel(f'database/data/data-prediksi/processedData-prediksi.xlsx', index=False)

        print('Proses selesai.')

    except Exception as e:
        print("Terjadi kesalahan:", str(e))
