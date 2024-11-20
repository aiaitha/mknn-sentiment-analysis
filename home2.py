import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Judul Aplikasi
st.title("Analisis Ulasan Aplikasi Marketplace")

# Membuat Data Dummy
data = {
    "application": ["Shopee", "Lazada"],
    "sentiment_positive": [75, 60],  # Persentase sentimen positif untuk setiap aplikasi
    "sentiment_negative": [15, 25],  # Persentase sentimen negatif
    "review_positive": ["easy, great, love, fast, good service", "excellent, user friendly, amazing, good product"],
    "review_negative": ["bad, slow, expensive, poor quality", "not good, expensive, bad experience"]
}

# Mengubah data ke DataFrame
df = pd.DataFrame(data)

# Menampilkan Peringkat Aplikasi Berdasarkan Sentimen Positif
st.subheader("Peringkat Aplikasi Berdasarkan Sentimen Positif")
df_sorted = df.sort_values(by="sentiment_positive", ascending=False)
st.write(df_sorted[["application", "sentiment_positive"]])

# Membuat Word Cloud untuk Sentimen Positif dan Negatif
st.subheader("Word Cloud Sentimen Positif dan Negatif")

# Untuk Shopee
shopee_reviews_positive = " ".join(df_sorted[df_sorted["application"] == "Shopee"]["review_positive"].values)
shopee_reviews_negative = " ".join(df_sorted[df_sorted["application"] == "Shopee"]["review_negative"].values)

# Untuk Lazada
lazada_reviews_positive = " ".join(df_sorted[df_sorted["application"] == "Lazada"]["review_positive"].values)
lazada_reviews_negative = " ".join(df_sorted[df_sorted["application"] == "Lazada"]["review_negative"].values)

# Membuat WordCloud untuk Shopee
st.subheader("Word Cloud Shopee (Sentimen Positif)")
wordcloud_shopee_positive = WordCloud(width=800, height=400, background_color='white').generate(shopee_reviews_positive)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_shopee_positive, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

st.subheader("Word Cloud Shopee (Sentimen Negatif)")
wordcloud_shopee_negative = WordCloud(width=800, height=400, background_color='white').generate(shopee_reviews_negative)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_shopee_negative, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# Membuat WordCloud untuk Lazada
st.subheader("Word Cloud Lazada (Sentimen Positif)")
wordcloud_lazada_positive = WordCloud(width=800, height=400, background_color='white').generate(lazada_reviews_positive)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_lazada_positive, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

st.subheader("Word Cloud Lazada (Sentimen Negatif)")
wordcloud_lazada_negative = WordCloud(width=800, height=400, background_color='white').generate(lazada_reviews_negative)
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_lazada_negative, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)
