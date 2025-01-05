from lib import *

# Fungsi untuk memuat daftar kata dasar
def load_kata_dasar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

# Fungsi stemming
def simple_stemming(word, kata_dasar):
    if not isinstance(word, str):
        return word

    if word in kata_dasar:
        return word

    # Daftar imbuhan
    suffixes = ["lah", "kah", "ku", "mu", "nya", "kan", "an", "i"]
    prefixes = ["meng", "peng", "mem", "pem", "meny", "peny", "men", "pen", 
                "ber", "ter", "se", "di", "ke", "per", "me", "pe"]

    # Hapus prefiks
    for prefix in prefixes:
        if word.startswith(prefix):
            if prefix in ["meng", "peng"] and len(word) > 4 and word[4] in "aiueo":
                word = "k" + word[4:]
            elif prefix in ["mem", "pem"] and len(word) > 3 and word[3] in "aiueo":
                word = "p" + word[3:]
            elif prefix in ["meny", "peny"] and len(word) > 4 and word[4] in "aiueo":
                word = "s" + word[4:]
            elif prefix in ["men", "pen"] and len(word) > 3 and word[3] in "aiueo":
                word = "t" + word[3:]
            else:
                word = word[len(prefix):]
            break

    if word in kata_dasar:
        return word

    # Hapus sufiks
    for suffix in suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            if word in kata_dasar:
                return word
            break

    return word

# Fungsi untuk stemming daftar token
def stemming(tokens, kata_dasar):
    """
    Melakukan stemming pada daftar token.
    Args:
        tokens (list): Daftar token.
        kata_dasar (set): Set kata dasar.
    Returns:
        list: Daftar token setelah stemming.
    """
    return [simple_stemming(word, kata_dasar) for word in tokens]



# Fungsi preprocess untuk seluruh dataset
def preprocess_data(data):
    if 'reviews' not in data.columns:
        raise ValueError("Kolom 'reviews' tidak ditemukan dalam dataset.")

    data['stemming'] = data['reviews'].apply(
        lambda text: preprocess_text(text, normalize_words, stopwords_words, kata_dasar)
    )
    return data

# Memuat data tambahan
kata_dasar = load_kata_dasar("kata-dasar-all.txt")
normalize_words = pd.read_excel("normalisasi.xlsx").set_index("before")["after"].to_dict()
stopwords_words = set(pd.read_excel("stopwords.xlsx")['stopwords'].dropna())


# # Memuat data utama
# data = pd.read_excel("coba.xlsx")

# # Proses preprocessing
# data['processed_reviews'] = data['reviews'].apply(lambda x: preprocess_text(x, normalize_words, stopwords_words, kata_dasar))

# # Menampilkan hasil
# print(data)
