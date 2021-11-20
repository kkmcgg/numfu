# a function that computes cosine similarity between two vectors
def cosine_similarity(v1, v2):
    numerator = np.dot(v1, v2)
    denominator = np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2))
    return numerator / denominator
