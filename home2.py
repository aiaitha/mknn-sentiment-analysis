import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Judul Aplikasi
st.title("Perbandingan Aplikasi Marketplace: Shopee vs Lazada")

# Data dummy untuk aplikasi Shopee dan Lazada
data_shopee = {
    'review': [
        "Shopee is great! Love the discounts and fast delivery.",
        "I had a wonderful shopping experience with Shopee.",
        "Shopee has a wide range of products, really happy with it.",
        "The service on Shopee is good, but sometimes the delivery takes time."
    ],
    'sentiment': ['positive', 'positive', 'positive', 'negative']
}

data_lazada = {
    'review': [
        "Lazada is okay, but the delivery service could be better.",
        "I found a lot of good products on Lazada.",
        "The discounts on Lazada are good, but the service is slow.",
        "Lazada needs to improve its customer service, not happy."
    ],
    'sentiment': ['positive', 'positive', 'negative', 'negative']
}

# Convert to DataFrame
df_shopee = pd.DataFrame(data_shopee)
df_lazada = pd.DataFrame(data_lazada)

# Hitung persentase sentimen positif
positive_shopee = len(df_shopee[df_shopee['sentiment'] == 'positive']) / len(df_shopee) * 100
positive_lazada = len(df_lazada[df_lazada['sentiment'] == 'positive']) / len(df_lazada) * 100

# Menampilkan peringkat
st.subheader("Peringkat Aplikasi Berdasarkan Sentimen Positif")
if positive_shopee > positive_lazada:
    st.write("1. **Shopee**: {:.2f}% sentimen positif".format(positive_shopee))
    st.write("2. **Lazada**: {:.2f}% sentimen positif".format(positive_lazada))
else:
    st.write("1. **Lazada**: {:.2f}% sentimen positif".format(positive_lazada))
    st.write("2. **Shopee**: {:.2f}% sentimen positif".format(positive_shopee))

# Fungsi untuk membuat word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(text))
    return wordcloud

# Word Cloud untuk Sentimen Positif Shopee
st.subheader("Word Cloud Sentimen Positif - Shopee")
positive_reviews_shopee = df_shopee[df_shopee['sentiment'] == 'positive']['review']
wordcloud_shopee_positive = generate_wordcloud(positive_reviews_shopee)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_shopee_positive, interpolation='bilinear')
plt.axis("off")
st.pyplot()

# Word Cloud untuk Sentimen Negatif Shopee
st.subheader("Word Cloud Sentimen Negatif - Shopee")
negative_reviews_shopee = df_shopee[df_shopee['sentiment'] == 'negative']['review']
wordcloud_shopee_negative = generate_wordcloud(negative_reviews_shopee)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_shopee_negative, interpolation='bilinear')
plt.axis("off")
st.pyplot()

# Word Cloud untuk Sentimen Positif Lazada
st.subheader("Word Cloud Sentimen Positif - Lazada")
positive_reviews_lazada = df_lazada[df_lazada['sentiment'] == 'positive']['review']
wordcloud_lazada_positive = generate_wordcloud(positive_reviews_lazada)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_lazada_positive, interpolation='bilinear')
plt.axis("off")
st.pyplot()

# Word Cloud untuk Sentimen Negatif Lazada
st.subheader("Word Cloud Sentimen Negatif - Lazada")
negative_reviews_lazada = df_lazada[df_lazada['sentiment'] == 'negative']['review']
wordcloud_lazada_negative = generate_wordcloud(negative_reviews_lazada)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_lazada_negative, interpolation='bilinear')
plt.axis("off")
st.pyplot()

