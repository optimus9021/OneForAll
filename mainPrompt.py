"""
Football Match Research Prompt Generator
Converts prediction file into research prompt for LLM analysis
"""

def read_prediction_file(input_file):
    """Read and parse prediction file"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def parse_match_data(lines):
    """Parse each line and extract match information"""
    matches = []
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 3:
            date = parts[0].strip()
            league = parts[1].strip()
            match = parts[2].strip()
            matches.append(f"{date} - {league} - {match}")
        else:
            matches.append(line)
    return matches


def generate_prompt(matches):
    """Generate comprehensive research prompt"""
    template = '''Research and list all possible factors and considerations that could affect the outcome of the following football match predictions. For each match, consider: injuries, lineups, suspensions, historical head-to-head data, tactical trends, weather, transfers, news, team motivation, fixture congestion, external influences, squad mental/physical condition, home/away factors, and statistical anomalies. Ignore the ML prediction; instead, focus on researching from all available sources any factor that could realistically affect the result, no matter how unlikely.

Format:
[Date] - [League] - [Match]
Detail: lakukan research apapun yang bisa mempengaruhi hasil pertandingan ini, urutkan dari yang paling berdampak seperti cedera, lineup, motivasi, berita, jadwal padat, cuaca, peristiwa di luar lapangan, rumor, apapun yang muncul dari research relevan.

Matches:
'''
    
    matches_string = '\n'.join(matches)
    footer = '\n\nUntuk setiap pertandingan di atas, research semua kemungkinan faktor apapun yang bisa mempengaruhi hasil akhir tanpa terkecuali.'
    
    return template + matches_string + footer


def export_prompt(prompt, output_file):
    """Export prompt to text file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"âœ“ Prompt berhasil di-export ke: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def main():
    # Configuration
    input_file = 'prediksi-XGBoost-2025-10-27.txt'  # Ganti dengan nama file input
    output_file = 'research_matches_prompt.txt'     # Nama file output
    
    print("=" * 60)
    print("Football Match Research Prompt Generator")
    print("=" * 60)
    
    # Step 1: Read input file
    print(f"\n[1/4] Reading file: {input_file}")
    lines = read_prediction_file(input_file)
    if not lines:
        return
    print(f"âœ“ Found {len(lines)} matches")
    
    # Step 2: Parse match data
    print("\n[2/4] Parsing match data...")
    matches = parse_match_data(lines)
    print(f"âœ“ Parsed {len(matches)} matches")
    
    # Step 3: Generate prompt
    print("\n[3/4] Generating research prompt...")
    prompt = generate_prompt(matches)
    print(f"âœ“ Prompt generated ({len(prompt)} characters)")
    
    # Step 4: Export to file
    print(f"\n[4/4] Exporting to: {output_file}")
    if export_prompt(prompt, output_file):
        print("\n" + "=" * 60)
        print("Process completed successfully!")
        print("=" * 60)
        print(f"\nFile ready: {output_file}")
        print("Copy the prompt and use it with any LLM for comprehensive research.")


if __name__ == "__main__":
    main()