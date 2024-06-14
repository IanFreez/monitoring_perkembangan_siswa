
import os
import pandas as pd

csv_directory = 'pathoriginal'
output_directory = 'newpath'

# Daftar kode mapel
kodemapel_lists = [
    ['101'] * 30, ['102'] * 30, ['103'] * 30, ['104'] * 30, ['105'] * 30,
    ['106'] * 30, ['107'] * 30, ['108'] * 30, ['109'] * 30, ['110'] * 30,
    ['201'] * 30, ['202'] * 30, ['203'] * 30, ['204'] * 30, ['205'] * 30,
    ['206'] * 30, ['207'] * 30, ['208'] * 30, ['209'] * 30, ['210'] * 30
]

counter = 0

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv') and counter < len(kodemapel_lists):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)
        
        df['Kodemapel'] = kodemapel_lists[counter]
        
        output_path = os.path.join(output_directory, filename)
        
        df.to_csv(output_path, index=False)
        
        print(f"Data dari {filename} berhasil disimpan ke {output_path}")
        
        counter += 1
