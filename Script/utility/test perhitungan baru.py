import pandas as pd
from tqdm import tqdm
from datetime import datetime

def add_additional_columns(df):
    try:
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

    except Exception as e:
        print("Terjadi kesalahan:", str(e))
    return df

n = 20
# Contoh penggunaan:
file_path = f'database/data/data-processed/processedData-{n}.xlsx'
df = pd.read_excel(file_path)
df = add_additional_columns(df)
# Simpan DataFrame yang sudah dimodifikasi ke dalam file Excel
df.to_excel(f'database/data/data-processed/processedData-{n}_modified.xlsx', index=False)
