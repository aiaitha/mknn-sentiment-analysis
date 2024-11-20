import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Analisis Ulasan Aplikasi Marketplace")

# Penjelasan
st.markdown("""
Aplikasi ini untuk menganalisis ulasan dan membandingkan pada suatu aplikasi. 
Unggah satu atau lebih file CSV atau XLSX dengan format berikut:
- Kolom yang berisi teks ulasan aplikasi.
""")

# Komponen File Uploader (multi-file)
uploaded_files = st.file_uploader("Unggah file CSV/XLSX berisi ulasan aplikasi", type=["csv", "xlsx"], accept_multiple_files=True)

# Jika file diunggah
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Membaca file CSV atau XLSX
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
            
            # Menampilkan data yang diunggah
            st.subheader(f"Data Ulasan dari File: {uploaded_file.name}")
            st.write(data.head())

            # Cek kolom yang tersedia
            if len(data.columns) == 0:
                st.error("File tidak memiliki kolom apapun.")
            else:
                # Meminta pengguna memilih kolom untuk review
                review_column = st.selectbox("Pilih kolom yang berisi teks ulasan:", data.columns)

                # Cek apakah kolom yang dipilih tidak kosong
                if review_column:
                    # Cek apakah kolom 'application' ada
                    if 'application' not in data.columns:
                        # Jika tidak ada kolom 'application', biarkan kosong atau gunakan nama file sebagai aplikasi
                        data['application'] = uploaded_file.name
                    
                    # Menampilkan informasi jumlah ulasan
                    total_reviews = len(data)
                    st.write(f"Total ulasan di file {uploaded_file.name}: **{total_reviews}**")
                    st.success("File valid! Data siap untuk diproses lebih lanjut.")
                else:
                    st.error("Kolom yang dipilih kosong. Pastikan untuk memilih kolom ulasan yang benar.")
        
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file {uploaded_file.name}: {e}")
else:
    st.info("Silakan unggah satu atau lebih file CSV atau XLSX untuk memulai analisis.")
