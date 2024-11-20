import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Analisis Ulasan Aplikasi")

# Penjelasan
st.markdown("""
Aplikasi ini memungkinkan Anda untuk menganalisis ulasan aplikasi berdasarkan file CSV. 
Unggah file CSV dengan format berikut:
- **application**: Nama aplikasi
- **review**: Teks ulasan
- **sentiment**: Sentimen ulasan (positif, negatif, atau netral)
""")

# Komponen File Uploader
uploaded_file = st.file_uploader("Unggah file CSV berisi ulasan aplikasi", type="csv")

# Jika file diunggah
if uploaded_file:
    try:
        # Membaca file CSV
        data = pd.read_csv(uploaded_file)
        
        # Menampilkan data yang diunggah
        st.subheader("Data Ulasan yang Diupload:")
        st.write(data.head())

        # Memastikan kolom wajib tersedia
        required_columns = {'application', 'review', 'sentiment'}
        if not required_columns.issubset(data.columns):
            st.error("File Anda tidak memiliki kolom yang sesuai. Pastikan file memiliki kolom: 'application', 'review', dan 'sentiment'.")
        else:
            st.success("File valid! Data siap untuk diproses lebih lanjut.")
            # Menampilkan informasi jumlah aplikasi dan ulasan
            unique_apps = data['application'].nunique()
            total_reviews = len(data)
            st.write(f"Jumlah aplikasi unik: **{unique_apps}**")
            st.write(f"Total ulasan: **{total_reviews}**")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan unggah file CSV untuk memulai analisis.")
