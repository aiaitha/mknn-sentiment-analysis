from lib import *

# Cosine similarity function
def cosine_similarity_vector(v, w):
    return np.dot(v, w) / (np.linalg.norm(v) * np.linalg.norm(w) + 1e-8)

# MKNN model function
def mknn(training_data, training_labels, test_data, validities, k, alpha):
    predictions = []

    for test_instance in test_data:
        distances = [cosine_similarity_vector(test_instance, train_instance) for train_instance in training_data]
        neighbors_indices = np.argsort(distances)[-k:]

        weighted_votes = {}
        for idx in neighbors_indices:
            weight = validities[idx] * (1 / (distances[idx] + alpha))
            label = training_labels[idx]
            if label in weighted_votes:
                weighted_votes[label] += weight
            else:
                weighted_votes[label] = weight

        predicted_class = max(weighted_votes, key=weighted_votes.get) if weighted_votes else None
        predictions.append(predicted_class)

    return predictions

# Validity calculation function
def calculate_validity(training_data, training_labels, k, threshold):
    n = len(training_data)
    validities = np.zeros(n)

    for i in range(n):
        distances = [
            cosine_similarity_vector(training_data[i], training_data[j]) if i != j else -np.inf
            for j in range(n)
        ]
        neighbors_indices = np.argsort(distances)[-k:]

        count_same_class = sum(
            1 for idx in neighbors_indices if training_labels[idx] == training_labels[i]
        )
        validities[i] = count_same_class / k

        if validities[i] < threshold:
            validities[i] = 0

    return validities

# Load static training data
def load_static_train_data():
    try:
        train_data = pd.read_excel("tes_model_dataset.xlsx")  # Static file
        return train_data.copy()  # Return a copy
    except Exception as e:
        raise Exception(f"Gagal memuat dataset latih statis: {e}")

# TF-IDF Vectorization function
def vectorize_data(data):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(data).toarray(), vectorizer
