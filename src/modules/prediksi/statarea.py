import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime

# Function to get match data from the webpage
def get_match_data():
    # Create URL based on today's date
    today = date.today()
    url = f"https://old.statarea.com/predictions/{today}"

    # Send request to the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with class 'gradientGrey_v'
    bariss = soup.find_all('tr', class_='gradientGrey_v')

    # Initialize set to store unique match data
    match_data_set = set()

    # Initialize list to store match data
    match_data_list = []

    for baris in bariss:
        # Find all rows (tr) for match data
        match_rows = baris.find_next_siblings('tr')

        for match_row in match_rows:
            columns = match_row.find_all('td')
            if len(columns) >= 25:
                match_time = columns[0].text.strip()
                host = columns[1].text.strip()
                guest = columns[2].text.strip()
                home_win_percentage = columns[6].text.strip()
                draw_percentage = columns[7].text.strip()
                away_win_percentage = columns[8].text.strip()
                ftr = columns[5].text.strip()

                # Create a unique identifier for each match
                match_identifier = (match_time, host, guest)

                # Check if the match is already in the set
                if match_identifier not in match_data_set:
                    match_data_set.add(match_identifier)
                    match_info = {
                        'match_time': match_time,
                        'host': host,
                        'guest': guest,
                        'home_win_percentage': home_win_percentage,
                        'draw_percentage': draw_percentage,
                        'away_win_percentage': away_win_percentage,
                        'FTR' : ftr
                    }
                    match_data_list.append(match_info)

    return match_data_list

# Function to save data to a .txt file
def save_to_txt(data):
    today = date.today()
    file_name = f'prediksi-StatArea-{today}.txt'

    # Sort the match data by match time
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x['match_time'], '%H:%M'))

    # Find the index where the match time starts from 06:59
    start_index = 0
    for i, match in enumerate(sorted_data):
        if datetime.strptime(match['match_time'], '%H:%M') >= datetime.strptime('06:59', '%H:%M'):
            start_index = i
            break

    # Reorder the sorted data to start from the match time at 06:59
    sorted_data = sorted_data[start_index:] + sorted_data[:start_index]

    with open(file_name, 'w') as file:
        for match in sorted_data:
            file.write(f"{match['match_time']}, {match['host']} {match['guest']}, Home Win: {match['home_win_percentage']}, Draw: {match['draw_percentage']}, Away Win: {match['away_win_percentage']}, FTR: {match['FTR']} \n")
    return file_name

# Main function
def statarea():
    match_data = get_match_data()
    if match_data:
        file_name = save_to_txt(match_data)
        print(f"Data berhasil disimpan ke dalam file {file_name}")
    else:
        print("Tidak ada data yang ditemukan.")
