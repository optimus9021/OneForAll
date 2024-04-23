import datetime
import requests
from bs4 import BeautifulSoup
from datetime import timezone


def forebet():
    # URL dari halaman web
    url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"

    # Header HTTP untuk mengatasi masalah otentikasi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Mengirim permintaan GET ke URL dengan header HTTP
    response = requests.get(url, headers=headers)

    # Memastikan permintaan berhasil
    if response.status_code == 200:
        # Mengurai halaman menggunakan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari semua elemen div dengan kelas "rcnt"
        match_elements = soup.find_all('div', class_='rcnt')

        today = datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=5)  # Menambahkan 5 jam untuk GMT+7
        namafile = f'prediksi-Forbet-{today.strftime("%Y-%m-%d")}.txt'

        # Menyiapkan file teks untuk menyimpan output
        with open(namafile, 'w', encoding='utf-8') as file:
            # Loop melalui setiap elemen pertandingan dan mengekstrak informasi yang diperlukan
            matches = []

            for match in match_elements:
                home_team = match.find('span', class_='homeTeam').get_text(strip=True)
                away_team = match.find('span', class_='awayTeam').get_text(strip=True)
                date_time = match.find('span', class_='date_bah').get_text(strip=True)

                # Add default time if date doesn't include time component
                if len(date_time.split()) == 1:
                    date_time += ' 00:00'

                # Menambahkan 7 jam pada waktu yang diperoleh untuk menyesuaikan dengan GMT+7
                date_time = datetime.datetime.strptime(date_time, '%d/%m/%Y %H:%M') + datetime.timedelta(hours=5)
                date_time_str = date_time.strftime('%d-%m-%Y %H:%M')

                # Mencari elemen prediksi
                prediction_value = None
                for prediction_class in ['predict_no', 'predict_y', 'predict']:
                    prediction_element = match.find('div', class_=prediction_class)
                    if prediction_element:
                        prediction_value = prediction_element.get_text(strip=True)
                        break
                    
                # Memeriksa apakah elemen prediksi ditemukan
                if prediction_value is None:
                    prediction_value = "Prediction not available"

                # Mencari elemen prediksi
                pscore_value = None
                for pscore_class in ['ex_sc exact_yes tabonly', 'ex_sc tabonly']:
                    pscore_element = match.find('div', class_=pscore_class)
                    if pscore_element:
                        pscore_value = pscore_element.get_text(strip=True)
                        break
                    
                # Memeriksa apakah elemen prediksi ditemukan
                if pscore_value is None:
                    pscore_value = "Prediction score not available"

                # Mencari elemen prediksi
                score_value = None
                score_element = match.find('div', class_='lscr_td')
                if score_element:
                    score_value = score_element.find('b', class_='l_scr').get_text(strip=True)

                # Memeriksa apakah elemen prediksi ditemukan
                if score_value is None:
                    score_value = "Score not available"

                # Menambahkan informasi pertandingan ke dalam list matches
                matches.append((date_time_str, home_team, away_team, prediction_value, pscore_value, score_value))

            # Mengurutkan pertandingan berdasarkan tanggal dan jam
            sorted_matches = sorted(matches, key=lambda x: datetime.datetime.strptime(x[0], '%d-%m-%Y %H:%M'))

            # Menyimpan informasi pertandingan yang telah diurutkan ke dalam file teks
            for match in sorted_matches:
                file.write("{}, {} vs {}, Prediction: {}, Pred Score: {}, FT Score: {}\n".format(*match))

        print(f"Data telah disimpan dalam file {namafile}.")
    else:
        print("Failed to retrieve the webpage.")
