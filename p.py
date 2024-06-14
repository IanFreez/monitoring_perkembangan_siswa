import pymongo
import os
import pandas as pd
from pymongo import MongoClient

client = MongoClient('urlconnectionmongodb')
db = client['akt16']

csv_directory = 'D:/Home/BDN/BDN/New2/Kelas9/A'
csv_directory1 = 'D:/Home/BDN/BDN/New2/Kelas9/B'
csv_directory2 = 'D:/Home/BDN/BDN/New2/Kelas9/C'
csv_directory3 = 'D:/Home/BDN/BDN/New2/Kelas9/D'
csv_directory4 = 'D:/Home/BDN/BDN/New2/Kelas9/E'
csv_directory5 = 'D:/Home/BDN/BDN/New2/Kelas9/F'
csv_directory6 = 'D:/Home/BDN/BDN/New2/Kelas9/G'
csv_directory7 = 'D:/Home/BDN/BDN/New2/Kelas9/H'

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9a']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory1):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory1, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9b']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory2):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory2, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9c']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory3):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory3, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9d']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")


# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory4):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory4, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9e']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory5):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory5, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9f']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory6):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory6, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9g']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")

# Loop melalui semua file CSV di direktori
for filename in os.listdir(csv_directory7):
    if filename.endswith('.csv'):
        # Path lengkap ke file CSV
        file_path = os.path.join(csv_directory7, filename)

        # Membaca CSV ke DataFrame pandas
        df = pd.read_csv(file_path)

        # Mengakses koleksi
        collection = db['9h']

        # Mengkonversi DataFrame ke format JSON yang bisa diterima MongoDB
        data = df.to_dict(orient='records')

        # Mengunggah data ke koleksi
        collection.insert_many(data)

        print(f"Data dari {filename} berhasil diunggah ke koleksi")