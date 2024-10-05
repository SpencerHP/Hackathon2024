from flask import Flask, request, jsonify, render_template
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import random

app = Flask(__name__)

# Function to compute similarity with weighted columns
def map_similar_items_with_columns(source_list, target_list, columns, weights, top_n=3):
    field_similarities = {}

    for idx, (column, weight) in enumerate(zip(columns, weights)):
        if isinstance(source_list[column][0], str):  # If the column is text
            vectorizer = TfidfVectorizer().fit_transform(source_list[column] + target_list[column])
            source_matrix = vectorizer[:len(source_list[column])]
            target_matrix = vectorizer[len(source_list[column]):]
            field_similarities[column] = cosine_similarity(source_matrix, target_matrix) * weight
        else:  # If the column is numeric
            scaler = MinMaxScaler()
            source_matrix = scaler.fit_transform(np.array(source_list[column]).reshape(-1, 1))
            target_matrix = scaler.transform(np.array(target_list[column]).reshape(-1, 1))
            field_similarities[column] = cosine_similarity(source_matrix, target_matrix) * weight

    combined_similarity = np.sum([field_similarities[column] for column in columns], axis=0)
    normalized_similarity_matrix = np.interp(combined_similarity, (combined_similarity.min(), combined_similarity.max()), (50, 100))

    mapping = {}
    for i in range(len(source_list[columns[0]])):
        top_indices = np.argsort(normalized_similarity_matrix[i])[::-1][:top_n]
        top_similarities = [(target_list[columns[0]][idx], normalized_similarity_matrix[i][idx]) for idx in top_indices]
        mapping[source_list[columns[0]][i]] = top_similarities

    return mapping

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    source_data = request.form.getlist('source[]')
    target_data = request.form.getlist('target[]')
    column_names = request.form.getlist('columns[]')
    weights = request.form.getlist('weights[]')

    # Prepare the source and target lists for similarity mapping
    source_list = {col: [] for col in column_names}
    target_list = {col: [] for col in column_names}

    for i in range(len(source_data)//len(column_names)):
        for j, col in enumerate(column_names):
            source_list[col].append(source_data[i * len(column_names) + j])

    for i in range(len(target_data)//len(column_names)):
        for j, col in enumerate(column_names):
            target_list[col].append(target_data[i * len(column_names) + j])

    # Perform similarity mapping
    mapped_items = map_similar_items_with_columns(source_list, target_list, column_names, list(map(float, weights)))

    return jsonify(mapped_items)

if __name__ == '__main__':
    app.run(debug=True)
