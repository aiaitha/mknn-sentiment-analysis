from lib import *
from model4 import *
from preprocessing import*
from sklearn.feature_extraction.text import TfidfVectorizer

# Judul Aplikasi
st.title("Analisis Sentimen Aplikasi Marketplace")

# Penjelasan
st.markdown("""
Aplikasi ini untuk menganalisis sentimen dari suatu ulasan pada satu atau beberapa aplikasi. 
Unggah satu atau lebih file CSV atau XLSX dengan format berikut:

-harap mengunggah file yang berisi ulasan dengan nama kolom "reviews"
""")

# Static training dataset (tes_model_dataset.xlsx)
@st.cache_data
def load_static_train_data():
    try:
        train_data = pd.read_excel("datalatih200.xlsx")  # Static file
        return train_data.copy()  # Return a copy
    except Exception as e:
        st.error(f"Gagal memuat dataset latih statis: {e}")
        st.stop()

train_data = load_static_train_data()

# Prepare static training data
X_train = train_data["stemming"].tolist()  # Data latih
y_train = train_data["rating"].apply(
    lambda x: 'negatif' if x in [1, 2] else ('netral' if x == 3 else 'positif')
).tolist()  # Label latih

# TF-IDF Vectorization for training data
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train).toarray()

# Komponen File Uploader (multi-file)
uploaded_files = st.file_uploader("Unggah file CSV/XLSX berisi ulasan aplikasi", type=["csv", "xlsx"], accept_multiple_files=True)


if uploaded_files:
    # Proses setiap file satu per satu
    for file in uploaded_files:
            @st.cache_data
            def load_test_data(file):
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                else:
                    data = pd.read_excel(file)
                return data.copy()

            try:
                test_data = load_test_data(file)
                st.success(f"Dataset uji dari {file.name} berhasil dimuat!")
                st.write(f"Dataset Uji yang Diunggah dari {file.name}:")
                # st.dataframe(test_data)

            except Exception as e:
                st.error(f"Error saat memuat dataset uji dari {file.name}: {e}")
                continue

            # Preprocessing function
            def preprocess_data(data):
                # Mengubah teks ke huruf kecil
                return data.apply(lambda x: x.lower() if isinstance(x, str) else x)

            # Preprocessing untuk dataset uji
            try:
                test_data["cleaned_reviews"] = preprocess_data(test_data["reviews"])
                X_test_cleaned = test_data["cleaned_reviews"].tolist()  # Data uji yang sudah dibersihkan
                X_test_tfidf = vectorizer.transform(X_test_cleaned).toarray()
            except Exception as e:
                st.error(f"Error saat memproses dataset uji dari {file.name}: {e}")
                continue

            # Parameters
            k = 3
            alpha = 0.5
            threshold = 0.7

            # Calculate Validity and Run MKNN with spinner
            with st.spinner(f"Sedang memproses prediksi untuk {file.name}..."):
                try:
                    validities = calculate_validity(X_train_tfidf, y_train, k, threshold)
                    predictions = mknn(X_train_tfidf, y_train, X_test_tfidf, validities, k, alpha)

                    test_data["Sentimen"] = predictions
                    st.success(f"Prediksi selesai untuk {file.name}!")
                    st.write(f"Hasil Prediksi untuk {file.name}:")
                    # st.dataframe(test_data[['reviews', 'Sentimen']])

                    # Unduh hasil prediksi sebelum visualisasi
                    output_file = f"hasil_prediksi_{file.name}.xlsx"
                    test_data[["reviews", "Sentimen"]].to_excel(output_file, index=False)
                    st.download_button(f"Unduh Hasil Prediksi {file.name}", data=open(output_file, "rb").read(), file_name=output_file)

                    # Menghitung jumlah prediksi untuk setiap sentimen
                    prediksi_positif = (np.array(predictions) == 'positif').sum()
                    prediksi_negatif = (np.array(predictions) == 'negatif').sum()
                    prediksi_netral = (np.array(predictions) == 'netral').sum()

                    # Data untuk visualisasi
                    labels = ['Positif', 'Negatif', 'Netral']
                    sizes = [prediksi_positif, prediksi_negatif, prediksi_netral]
                    colors = ['#66B3FF', '#FFA500', '#578E7E']  # Warna biru, oranye, dan hijau

                    # Membuat pie chart menggunakan matplotlib
                    fig, ax = plt.subplots(figsize=(5, 5))
                    ax.pie(
                        sizes,
                        labels=labels,
                        colors=colors,
                        autopct=lambda p: f'{p:.1f}%\n({int(p*sum(sizes)/100)})'
                    )
                    ax.set_title(f'Hasil Klasifikasi Sentimen Data Uji Baru ({file.name})')

                    # Menampilkan plot di Streamlit
                    st.pyplot(fig)

                #     # WordCloud untuk setiap sentimen
                #     def generate_wordcloud(data, labels, label, title):
                #         text = " ".join([doc for doc, lbl in zip(data, labels) if lbl == label])
                #         if text.strip():  # Hanya jika teks tidak kosong
                #             wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
                #             plt.figure(figsize=(7, 4))
                #             plt.imshow(wordcloud, interpolation="bilinear")
                #             plt.axis("off")
                #             plt.title(title, fontsize=16)
                #             st.pyplot(plt)

                #     X_test_word = test_data["cleaned_reviews"].tolist()
                #     generate_wordcloud(X_test_word, predictions, 'positif', f'WordCloud: Positif ({file.name})')
                #     generate_wordcloud(X_test_word, predictions, 'negatif', f'WordCloud: Negatif ({file.name})')
                #     generate_wordcloud(X_test_word, predictions, 'netral', f'WordCloud: Netral ({file.name})')

                except Exception as e:
                    st.error(f"Error saat menjalankan MKNN untuk {file.name}: {e}")
                    continue
