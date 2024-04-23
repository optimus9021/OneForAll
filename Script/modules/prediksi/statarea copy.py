import requests
from bs4 import BeautifulSoup
from datetime import date

# Function to get match data from the webpage
def get_match_data():
    # Create URL based on today's date
    today = date.today()
    url = f"https://old.statarea.com/predictions/{today}"

    # Send request to the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with class 'gradientGrey_v'
    league_titles = soup.find_all('tr', class_='gradientGrey_v')

    # Initialize list to store match data
    match_data_list = []

    for title in league_titles:
        # Extract league name from the first cell of the row
        league_name = title.find('b').text.strip()

        # Find the next row (tr) for match data
        match_row = title.find_next_sibling('tr')

        # Skip the second row
        match_row = match_row.find_next_sibling('tr')

        if match_row and match_row.find('td'):
            columns = match_row.find_all('td')
            if len(columns) >= 9:
                match_time = columns[0].text.strip()
                host = columns[1].text.strip()
                guest = columns[2].text.strip()
                home_win_percentage = columns[6].text.strip()
                draw_percentage = columns[7].text.strip()
                away_win_percentage = columns[8].text.strip()
                ftr = columns[5].text.strip()
                match_info = {
                    'league_name': league_name,
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
    with open(file_name, 'w') as file:
        for match in data:
            file.write(f"{match['league_name']}\n")
            file.write(f"{match['match_time']}, {match['host']} vs {match['guest']}, Home Win: {match['home_win_percentage']}, Draw: {match['draw_percentage']}, Away Win: {match['away_win_percentage']}, FTR: {match['FTR']} \n\n")
    return file_name

# Main function
def statarea():
    match_data = get_match_data()
    if match_data:
        file_name = save_to_txt(match_data)
        print(f"Data berhasil disimpan ke dalam file {file_name}")
    else:
        print("Tidak ada data yang ditemukan.")


statarea()
