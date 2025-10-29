import pandas as pd

# Baca file Excel
df1 = pd.read_excel('database/data/data-learning/data-copy.xlsx')
df2 = pd.read_excel('database/data/data-prediksi/processedData-prediksi.xlsx')

# Convert ke JSON (orientasi records/list of dict per baris)
df1.to_json('data-copy.json', orient='records', force_ascii=False, indent=2)
df2.to_json('processedData-prediksi.json', orient='records', force_ascii=False, indent=2)

print("File data-copy.xlsx berhasil di-convert menjadi data-copy.json!")
print("File processedData-prediksi.xlsx berhasil di-convert menjadi processedData-prediksi.json!")
