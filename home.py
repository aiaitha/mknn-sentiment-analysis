import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Analisis Ulasan Aplikasi Marketplace")

# Penjelasan
st.markdown("""
Aplikasi ini untuk menganalisis ulasan dan membandingkan pada suatu aplikasi. 
Unggah satu atau lebih file CSV dengan format berikut:
- **review**: Teks ulasan aplikasi.
""")

# Komponen File Uploader (multi-file)
uploaded_files = st.file_uploader("Unggah file CSV berisi ulasan aplikasi", type="csv", accept_multiple_files=True)

# Jika file diunggah
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Membaca file CSV
            data = pd.read_csv(uploaded_file)
            
            # Menampilkan data yang diunggah
            st.subheader(f"Data Ulasan dari File: {uploaded_file.name}")
            st.write(data.head())

            # Cek apakah kolom 'review' ada
            if 'review' not in data.columns:
                st.error(f"File {uploaded_file.name} tidak memiliki kolom 'review'. Pastikan file memiliki kolom 'review'.")
            else:
                # Jika tidak ada kolom 'application', minta input nama aplikasi
                if 'application' not in data.columns:
                    app_name = st.text_input(f"Masukkan Nama Aplikasi untuk file {uploaded_file.name}:")
                    if app_name:
                        data['application'] = app_name
                    else:
                        st.warning(f"Silakan masukkan nama aplikasi untuk file {uploaded_file.name}.")
                
                # Menampilkan informasi jumlah ulasan
                total_reviews = len(data)
                st.write(f"Total ulasan di file {uploaded_file.name}: **{total_reviews}**")
                st.success("File valid! Data siap untuk diproses lebih lanjut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file {uploaded_file.name}: {e}")
else:
    st.info("Silakan unggah satu atau lebih file CSV untuk memulai analisis.")
