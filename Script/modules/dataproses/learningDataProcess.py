import pandas as pd
from tqdm import tqdm

def process_data(n):
    try:
        for nomor_file in range(n, 25):
            print(f'Membaca data dari file Excel dengan nomor file-{nomor_file}')
            file_path = f'database/data/data-unprocessed/data-{nomor_file}.xlsx'

            try:
                df = pd.read_excel(file_path)
                # Lakukan sesuatu dengan dataframe, misalnya:
                print(f"Jumlah baris dan kolom untuk file nomor-{nomor_file}: {df.shape}")
                
                # Mengurutkan data berdasarkan tanggal dan nama HomeTeam
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

                    df.loc[index, 'HomeWin5'] = home_win_last_5
                    df.loc[index, 'HomeLose5'] = home_lose_last_5

                print('Menghitung total kemenangan dan kekalahan lima pertandingan terakhir untuk tim tamu')
                for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Last 5 Matches for Away Teams"):
                    away_team = row['AwayTeam']
                    ftr = row['FTR']

                    away_matches = df[(df['AwayTeam'] == away_team) & (df['Date'] < row['Date'])].tail(5)
                    away_win_last_5 = away_matches[away_matches['FTR'] == 'A'].shape[0]
                    away_lose_last_5 = away_matches[away_matches['FTR'] == 'H'].shape[0]

                    df.loc[index, 'AwayWin5'] = away_win_last_5
                    df.loc[index, 'AwayLose5'] = away_lose_last_5

                print('Menghitung total gol home team dan away team untuk setiap pertandingan dalam lima pertandingan terakhir')
                for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating Total Goals for Last 5 Matches for Home & Away Teams"):
                    home_team = row['HomeTeam']
                    away_team = row['AwayTeam']

                    home_matches = df[(df['HomeTeam'] == home_team) & (df['Date'] < row['Date'])].tail(5)
                    away_matches = df[(df['AwayTeam'] == away_team) & (df['Date'] < row['Date'])].tail(5)

                    total_goals_home_last_5 = home_matches['FTHG'].sum()
                    total_goals_away_last_5 = away_matches['FTAG'].sum()

                    df.loc[index, 'GHLast5'] = total_goals_home_last_5
                    df.loc[index, 'GALast5'] = total_goals_away_last_5

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

                    df.loc[index, 'Avg.GHome'] = home_goals
                    df.loc[index, 'Avg.GAway'] = away_goals

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

                        df.loc[index, 'HomePoints'] = home_team_points[home_team]
                        df.loc[index, 'AwayPoints'] = away_team_points[away_team]

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
        
                # Menyimpan hasil ke file Excel
                print('Menyimpan hasil ke file Excel')
                nama_folder = 'database/data/data-processed'
                df.to_excel(f'{nama_folder}/processedData-{nomor_file}.xlsx', index=False)

            except FileNotFoundError:
                print(f"File nomor-{nomor_file} tidak ditemukan.")
            except Exception as e:
                print(f"Terjadi kesalahan saat membaca file nomor-{nomor_file}: {str(e)}")

        print("Proses selesai.")
    except Exception as e:
        print("Terjadi kesalahan:", str(e))

