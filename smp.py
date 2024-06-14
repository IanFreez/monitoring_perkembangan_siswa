from time import time as current_time
import numpy as np
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio
import pymongo
from multiprocessing import Pool, cpu_count
import base64
from base64 import b64encode

#Mongo Connection
client = pymongo.MongoClient("urlconnectionmongodb")
db = client['akt16']
dguru = client['guru']
plotdb = client['plot']

#*************************************************************************************************************************
def generate_plot_chunks(plot_data, chunk_size):
  chunks = []
  for i in range(0, len(plot_data), chunk_size):
    chunk = plot_data[i:i + chunk_size]
    encoded_chunk = b64encode(chunk.encode()).decode()  # Base64 encode the chunk
    chunks.append(encoded_chunk)
  return chunks

def encode_plot_to_base64(plot_html):
    return base64.b64encode(plot_html.encode()).decode()

def retrieve_data(collection, query):
    return list(collection.find(query))

def save_plot_html(plot, plot_name):
    collection = plotdb['plotsaves']

    # Check if a document with the same name already exists
    existing_document = collection.find_one({"plot_name": plot_name})

    plot_html = pio.to_html(plot)

    document = {
        "plot_name": plot_name,
        "plot_html": plot_html
    }

    if existing_document:
        # Update the existing document
        collection.replace_one({"plot_name": plot_name}, document)
        print(f"Existing document with plot name '{plot_name}' replaced.")
    else:
        # Insert a new document
        collection.insert_one(document)
        print(f"New document with plot name '{plot_name}' inserted.")

    return True

#******************************************************************************************************************************
#Individu
def calculate_total_nilai(entry):
    activity_score = (entry["TotalHadir"] / 16) * 0.1
    pm_score = (sum([entry[f"PM{i}"] for i in range(1, 17)]) / 16) * 0.3
    uts_score = entry["UTS"] * 0.3
    uas_score = entry["UAS"] * 0.3
    total_score = activity_score + pm_score + uts_score + uas_score
    return total_score

def extract_total_nilai(data, id_siswa): #Ekstrak Nilai smt1
    scores = []
    course_code = 101
    
    for i in range(101, 111):
        for entry in data:
            if entry["Id"] == id_siswa and entry["Kodemapel"] == course_code:
                total = calculate_total_nilai(entry)
                scores.append(total)
        course_code += 1
    return scores

def extract_total_nilai2(data, id_siswa): #Ekstrak Nilai smt2
    scores = []
    course_code = 201
    
    for i in range(201, 211):
        for entry in data:
            if entry["Id"] == id_siswa and entry["Kodemapel"] == course_code:
                total = calculate_total_nilai(entry)
                scores.append(total)
        course_code += 1
    return scores

def plotsemuamapel(scores1, scores2, average_scores, nama): #Plot Semua Mapel
    courses = ["Bahasa Indonesia", "Bahasa Jawa", "Bahasa Inggris", "IPA", "IPS",
               "Matematika", "PKN", "Penjaskes", "Seni Budaya", "TIK"]
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=courses,
        x=scores1,
        orientation='h',
        name='Semester 1',
        marker=dict(color='skyblue')
    ))
    
    fig.add_trace(go.Bar(
        y=courses,
        x=scores2,
        orientation='h',
        name='Semester 2',
        marker=dict(color='lightgreen')
    ))
    
    fig.add_trace(go.Bar(
        y=courses,
        x=average_scores,
        orientation='h',
        name='Average',
        marker=dict(color='lightcoral')
    ))

    fig.update_layout(
        title=f'Ringkasan Nilai {nama}',
        xaxis=dict(title='Nilai Akhir', range=[0, 100]),
        yaxis=dict(title='Mata Pelajaran'),
        margin=dict(l=100, r=20, t=40, b=40),
        height=500,
        width=800,
        barmode='group',
        hovermode='y unified',
    )

    save_plot_html(fig, "plotsemuamapel.html")
    fig.show()

# Ekstrak nilai individual berdasarkan Kode Mapel + Semester
def extract_scores(data, id_siswa, code, semester):
    scores = []
    if semester == 1:
        course_code = int('1'+code)
    elif semester == 2:
        course_code = int('2'+code)
    
    for entry in data:
        if entry["Id"] == id_siswa and entry["Kodemapel"] == course_code:
            scores = [
                entry["PM1"], entry["PM2"], entry["PM3"], entry["PM4"],
                entry["PM5"], entry["PM6"], entry["PM7"], entry["PM8"],
                entry["UTS"], entry["PM9"], entry["PM10"], entry["PM11"],
                entry["PM12"], entry["PM13"], entry["PM14"], entry["PM15"],
                entry["PM16"], entry["UAS"]
            ]
    return scores

# Rata-Rata 2 Semester - 1 Mapel
def calculate_average(scores_semester1, scores_semester2):
    average_scores = []
    for s1, s2 in zip(scores_semester1, scores_semester2):
        average_scores.append((s1 + s2) / 2)
    return average_scores

# Rata-Rata 2 Semester - Semua Total Nilai Mapel
def average_total_nilai(scores_semester1, scores_semester2):
    average_scores = []
    for s1, s2 in zip(scores_semester1, scores_semester2):
        average_scores.append((s1 + s2) / 2)
    return average_scores

#Image Plot individu
def plot_scoreint(scores_semester1, scores_semester2, average_scores, nama, detail, kelas):
    exam_titles = [f"PM{i}" for i in range(1, 9)] + ["UTS"] + [f"PM{i}" for i in range(9,17)] + ["UAS"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=exam_titles, y=scores_semester1, mode='lines+markers', name='Semester 1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=exam_titles, y=scores_semester2, mode='lines+markers', name='Semester 2', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=exam_titles, y=average_scores, mode='lines+markers', name='Average', line=dict(color='red')))

    fig.update_layout(
        title=f'Perkembangan Nilai {detail} - {nama} ({kelas})',
        yaxis=dict(range=[0, 100]),
        xaxis=dict(tickangle=-45),
        hovermode='x unified'
    )
    
    fig.update_traces(hoverinfo='name+x+y', mode='lines+markers', opacity=0.7)
    
    save_plot_html(fig, "plotsatumapel.html")
    fig.show()

#********************************************************************************************************************
#Set Condition

def setdetailmapel(kodemapel):
    if kodemapel == '01':
        detilmapel = "Bahasa Indonesia"
    elif kodemapel == '02':
        detilmapel = "Bahasa Jawa"
    elif kodemapel == '03':
        detilmapel = "Bahasa Inggris"
    elif kodemapel == '04':
        detilmapel = "IPA"
    elif kodemapel == '05':
        detilmapel = "IPS"
    elif kodemapel == '06':
        detilmapel = "Matematika"
    elif kodemapel == '07':
        detilmapel = "PKN"
    elif kodemapel == '08':
        detilmapel = "Penjaskes"
    elif kodemapel == '09':
        detilmapel = "Seni Budaya"
    elif kodemapel == "10":
        detilmapel = "TIK"
    return detilmapel

def setdbcollection(id):
    if id in range (160001, 160031):
        col1 = '7a'
        col2 = '8a'
        col3 = '9a'
    elif id in range (160031, 160061):
        col1 = '7b'
        col2 = '8b'
        col3 = '9b'
    elif id in range (160061, 160091):
        col1 = '7c'
        col2 = '8c'
        col3 = '9c'
    elif id in range (160091, 160121):
        col1 = '7d'
        col2 = '8d'
        col3 = '9d'
    elif id in range (160121, 160151):
        col1 = '7e'
        col2 = '8e'
        col3 = '9e'
    elif id in range (160151, 160181):
        col1 = '7f'
        col2 = '8f'
        col3 = '9f'
    elif id in range (160181, 160211):
        col1 = '7g'
        col2 = '8g'
        col3 = '9g'
    elif id in range (160211, 160241):
        col1 = '7h'
        col2 = '8h'
        col3 = '9h'
    return col1, col2, col3

def setsubject(choice):
    if choice == 1:
        sub = ["Bahasa Indonesia"]
    elif choice == 2:
        sub = ["Bahasa Jawa"]
    elif choice == 3:
        sub = ["Bahasa Inggris"]
    elif choice == 4:
        sub = ["IPA"]
    elif choice == 5:
        sub = ["IPS"]
    elif choice == 6:
        sub = ["Matematika"]
    elif choice == 7:
        sub = ["PKN"]
    elif choice == 8:
        sub = ["Penjaskes"]
    elif choice == 9:
        sub = ["Seni Budaya"]
    elif choice == 10:
        sub = ["TIK"]
    return sub

def setkelas(id):
    if id in range (160001, 160031):
        abjad = 'a'
    elif id in range (160031, 160061):
        abjad = 'b'
    elif id in range (160061, 160091):
        abjad = 'c'
    elif id in range (160091, 160121):
        abjad = 'd'
    elif id in range (160121, 160151):
        abjad = 'e'
    elif id in range (160151, 160181):
        abjad = 'f'
    elif id in range (160181, 160211):
        abjad = 'g'
    elif id in range (160211, 160241):
        abjad = 'h'
    return abjad

def setnamaguru(id):
    if id == 1:
        nama = "Dr. Anwar Setiawan, M.Pd."
    elif id == 2:
        nama = "Prof. Dr. Maria Anggraini, M.Hum."
    elif id == 3:
        nama = "Dwi Santoso, S.Pd., M.Pd."
    elif id == 4:
        nama = "Agus Prasetyo, S.Pd., M.Pd."
    elif id == 5:
        nama = "Ratih Widyaningsih, S.S., M.Si."
    elif id == 6:
        nama = "Dr. Budi Hartono, M.Hum."
    elif id == 7:
        nama = "Dr. Linda Permata, M.Ed."
    elif id == 8:
        nama = "David Sugiharto, S.Pd., M.A."
    elif id == 9:
        nama = "Prof. Dr. Anita Wijaya, M.A."
    elif id == 10:
        nama = "Dr. Rina Kusuma, M.Si."
    elif id == 11:
        nama = "Anton Wijaya, S.Pd., M.Pd."
    elif id == 12:
        nama = "Prof. Dr. Widodo, M.Si."
    elif id == 13:
        nama = "Dr. Hendra Nugroho, M.Si."
    elif id == 14:
        nama = "Siti Aisyah, S.Pd., M.Pd."
    elif id == 15:
        nama = "Prof. Dr. Rahmat Hidayat, M.Si."
    elif id == 16:
        nama = "Dr. Surya Darmawan, M.Sc."
    elif id == 17:
        nama = "Intan Lestari, S.Pd., M.Pd."
    elif id == 18:
        nama = "Prof. Dr. Budi Santoso, M.Sc."
    elif id == 19:
        nama = "Dr. Putri Amelia, M.Si."
    elif id == 20:
        nama = "Agus Wibowo, S.Pd., M.Pd."
    elif id == 21:
        nama = "Prof. Dr. Wahyu Kurniawan, M.Si."
    elif id == 22:
        nama = "Dr. Andi Setiawan, M.Pd."
    elif id == 23:
        nama = "Rina Susanti, S.Pd., M.Pd."
    elif id == 24:
        nama = "Prof. Dr. Ahmad Fauzi, M.Pd."
    elif id == 25:
        nama = "Dr. Iwan Nugraha, M.Sn."
    elif id == 26:
        nama = "Sinta Marlina, S.Pd., M.Sn."
    elif id == 27:
        nama = "Prof. Dr. Yulia Wulandari, M.Sn."
    elif id == 28:
        nama = "Dr. Bayu Wijaya, M.Kom."
    elif id == 29:
        nama = "Anisa Putri, S.Kom., M.T."
    elif id == 30:
        nama = "Prof. Dr. Herman Susanto, M.Kom"
    return nama
#*****************************************************************************************************************************************
# Plot Rata2 semua kelas
def plot_class_averages(averages, subjects):
    semester_traces = {  
        "Semester 1": [],
        "Semester 2": [],
        "Average": [],
    }
    legend_names = list(semester_traces.keys())  # Legend

    fig = go.Figure()

    for class_name, subject_averages in averages.items():
        for i, subject in enumerate(subjects):
            avg_sem1, avg_sem2, avg_both = subject_averages[subject]

            semester_traces["Semester 1"].append(go.Bar(  # Append to Semester 1 list
                x=[class_name],
                y=[avg_sem1],
                marker_color='blue'
            ))
            semester_traces["Semester 2"].append(go.Bar(  # Append to Semester 2 list
                x=[class_name],
                y=[avg_sem2],
                marker_color='green'
            ))
            semester_traces["Average"].append(go.Bar(  # Append to Average list
                x=[class_name],
                y=[avg_both],
                marker_color='red'
            ))

    # Merge traces for each category
    for category, traces in semester_traces.items():
        merged_trace = go.Bar(x=[t.x[0] for t in traces], y=[sum(t.y) for t in traces], name=category)  # Merge x and y data
        fig.add_trace(merged_trace)

    fig.update_layout(
        title=f'Rata-rata nilai {subject} per kelas',
        barmode='group',
        xaxis_title='Class',
        yaxis_title='Rata-Rata',
        xaxis={'categoryorder':'category ascending'},
        height=600,
        width=1200,
    )

    save_plot_html(fig, "plotkelas.html")
    fig.show()
    
#************
def calculate_class_averages(class_name):
    print(f"Computing averages for class {class_name}...")
    collection = db[class_name]
    class_averages = {}
    subjects = ["Bahasa Indonesia", "Bahasa Jawa", "Bahasa Inggris", 
                "IPA", "IPS", "Matematika", "PKN", "Penjaskes", "Seni Budaya", "TIK"]
    
    for i in range(10):
        subject_code_sem1 = 101 + i
        subject_code_sem2 = 201 + i
        scores_sem1 = []
        scores_sem2 = []
        
        for entry in collection.find():
            if entry["Kodemapel"] == subject_code_sem1:
                total_nilai = calculate_total_nilai(entry)
                scores_sem1.append(total_nilai)
                print(f"Total nilai appended for subject {subjects[i]} in semester 1 for class {class_name}: {total_nilai}")
            if entry["Kodemapel"] == subject_code_sem2:
                total_nilai = calculate_total_nilai(entry)
                scores_sem2.append(total_nilai)
                print(f"Total nilai appended for subject {subjects[i]} in semester 2 for class {class_name}: {total_nilai}")
        
        subject = subjects[i]
        avg_sem1 = np.mean(scores_sem1) if scores_sem1 else 0
        avg_sem2 = np.mean(scores_sem2) if scores_sem2 else 0
        avg_both = (avg_sem1 + avg_sem2) / 2
        
        class_averages[subject] = (avg_sem1, avg_sem2, avg_both)
    
    print(f"Averages computed for class {class_name}.")
    return class_averages

# Function to retrieve data and compute averages in sequence
def compute_averages_sequential(classes):
    averages = {}
    for class_name in classes:
        averages[class_name] = calculate_class_averages(class_name)
    return averages

#******************************************
#Guru
def cari_id(kode_mapel, kelas):
    colg = dguru['dataguru']
    query = {
        "Kode Mapel": kode_mapel,
        kelas: "yes"
    }
    hasil = colg.find(query, {"Id": 1})
    ids = [doc["Id"] for doc in hasil]
    return ids

def getpenilaianguru(id_guru):
    colnguru = dguru['penilaian']
    query = {"Id": id_guru}
    data_guru = colnguru.find_one(query)
    return data_guru

def plot_penilaian_guru(data_guru, nama):
    if data_guru:
        penilaian = {
            "KemampuanMengajar": data_guru["KemampuanMengajar"],
            "PenguasaanMateri": data_guru["PenguasaanMateri"],
            "Perangkat Pembelajaran": data_guru["Perangkat Pembelajaran"],
            "FeedbackSiswa": data_guru["FeedbackSiswa"],
            "Kedisiplinan": data_guru["Kedisiplinan"]
        }

        labels = list(penilaian.keys())
        values = list(penilaian.values())

        fig = go.Figure([go.Bar(x=labels, y=values)])
        fig.update_layout(
            title=f"Penilaian Guru: {nama}",
            xaxis_title='Aspek Penilaian',
            yaxis_title='Nilai',
            yaxis=dict(range=[0, 10])
        )
        fig.show()
    else:
        print("Data guru tidak ditemukan.")

if __name__ == "__main__":
    selesai = False
    cek = False
    
    while selesai == False:
        print("Pilihan : ")
        print("1. Cek Siswa")
        print("2. Cek Kelas")
        choice = int(input("Masukkan Pilihan : "))

        if choice == 1:
            while cek == False:
                idsiswa = int(input("Masukkan id Siswa : "))
                if idsiswa > 160000 and idsiswa < 160241:
                    cek = True
            cek = False
            
            while cek == False:
                kelaschoice = int(input("Masukkan Kelas : "))
                if kelaschoice > 6 and kelaschoice < 10:
                    cek = True
            cek = False
            
            abjadkelas = setkelas(idsiswa)
            kls = f"{kelaschoice}{abjadkelas}"
            print("Abjad kelas set...")
            
            kelas7, kelas8, kelas9 = setdbcollection(idsiswa)
            collection1 = db[kelas7]
            collection2 = db[kelas8]
            collection3 = db[kelas9]
            print("Collection set...")
            
            query = {"Id": {"$in": [idsiswa]}}
            results = collection1.find(query)
            for doc in results:
                namasiswa = doc["Nama"]
                break
            print("Query Nama done...")
            
            # Retrieve data from MongoDB
            if kelaschoice == 7:
                data1 = list(collection1.find())
            elif kelaschoice == 8:
                data1 = list(collection2.find())
            elif kelaschoice == 9:
                data1 = list(collection3.find())
            print("Retrieval collection done...")
            
            nilaitotal1 = extract_total_nilai(data1, idsiswa)
            nilaitotal2 = extract_total_nilai2(data1, idsiswa)
            avgnilaitotal = average_total_nilai(nilaitotal1, nilaitotal2)
            plotsemuamapel(nilaitotal1, nilaitotal2, avgnilaitotal, namasiswa)
            
            selesai2 = False
            while selesai2 == False:
                while cek == False:
                    kodemapel = input("Masukkan Kode Mapel :")
                    if kodemapel in {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10"}:
                        detilmapel = setdetailmapel(kodemapel)
                        print("Detail mapel set...")
                        
                        if kelaschoice == 7:
                            kelas7sem1 = extract_scores(data1, idsiswa, kodemapel, 1)
                            print("Extracted score smt 1...")
                            kelas7sem2 = extract_scores(data1, idsiswa, kodemapel, 2)
                            print("Extracted score smt 2...")
                            averagekelas7 = calculate_average(kelas7sem1, kelas7sem2)
                            print("Average calculation done...")
                            plot_scoreint(kelas7sem1, kelas7sem2, averagekelas7, namasiswa, detilmapel, 'Kelas 7')
                        elif kelaschoice == 8:
                            kelas8sem1 = extract_scores(data1, idsiswa, kodemapel, 1)
                            print("Extracted score smt 1...")
                            kelas8sem2 = extract_scores(data1, idsiswa, kodemapel, 2)
                            print("Extracted score smt 2...")
                            averagekelas8 = calculate_average(kelas8sem1, kelas8sem2)
                            print("Average calculation done...")
                            plot_scoreint(kelas8sem1, kelas8sem2, averagekelas8, namasiswa, detilmapel, 'Kelas 8')
                        elif kelaschoice == 9:
                            kelas9sem1 = extract_scores(data1, idsiswa, kodemapel, 1)
                            print("Extracted score smt 1...")
                            kelas9sem2 = extract_scores(data1, idsiswa, kodemapel, 2)
                            print("Extracted score smt 2...")
                            averagekelas9 = calculate_average(kelas9sem1, kelas9sem2)
                            print("Average calculation done...")
                            plot_scoreint(kelas9sem1, kelas9sem2, averagekelas9, namasiswa, detilmapel, 'Kelas 9')
                        
                        ids = cari_id(int(kodemapel), kls)
                        print("ID yang ditemukan:", ids)
                        idguru = ids[0]
                        namaguru = setnamaguru(idguru)
                        data_guru = getpenilaianguru(idguru)
                        plot_penilaian_guru(data_guru, namaguru)
                        
                    elif kodemapel == "x":
                        selesai2 = True
                        cek = True
                        
            cek = False
                
        elif choice == 2:
            selesai2 = False
            
            while selesai2 == False:
                while cek == False:
                    kelas = int(input("Masukkan Kelas : "))
                    if kelas > 6 and kelas < 10:
                        cek = True
                cek = False
                classes = []
                if kelas == 7:
                    classes = ['7a', '7b', '7c', '7d', '7e', '7f', '7g', '7h']
                elif kelas == 8:
                    classes = ['8a', '8b', '8c', '8d', '8e', '8f', '8g', '8h']
                elif kelas == 9:
                    classes = ['9a', '9b', '9c', '9d', '9e', '9f', '9g', '9h']
                print("Class Collection Set...")

                averages = compute_averages_sequential(classes)
                print("Average calculation done...")
                
                selesai3 = False
                while selesai3 == False:
                    while cek == False:
                        subchoice = int(input("Masukkan KodeMapel : "))
                        if subchoice in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}:
                            cek = True
                    cek = False
                    subjects = setsubject(subchoice)
                    print("Subject set...")
                    plot_class_averages(averages, subjects)
                    end = input("Selesai?: tekan y untuk selesai")
                    if end == "y":
                        selesai3 = True
                    else:
                        selesai3 = False
        elif choice == 0:
            selesai = True