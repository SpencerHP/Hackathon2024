from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the canvas page
@app.route('/canvas')
def canvas():
    return render_template('canvas.html')

# Route for the output page
@app.route('/output')
def output():
    return render_template('output.html')

# Route for handling the data from the Handsontable widget
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()  # Receive the JSON payload

    # Extract the source data, target data, and column weights
    source_data = data['source']
    target_data = data['target']
    weights = data['weights']

    # Convert weights to float
    weights = {key: float(value) for key, value in weights.items()}

    # Convert the source and target data into Pandas DataFrames
    source_df = pd.DataFrame(source_data)
    target_df = pd.DataFrame(target_data)

    # Remove the first row (header)
    source_df = source_df.iloc[1:]  # Skip the first row for source data
    target_df = target_df.iloc[1:]  # Skip the first row for target data

    # Remove rows where all elements are None
    source_df = source_df.dropna(how='all')
    target_df = target_df.dropna(how='all')

    # Calculate compatibility percentage
    compatibility_results = calculate_compatibility(source_df, target_df, weights)

    # Save the compatibility results to an Excel file without headers or indices
    save_to_excel(compatibility_results)

    # Return a response indicating successful receipt of the data
    return jsonify({"status": "success", "message": "Data received and compatibility results saved to Excel."})

def calculate_compatibility(source_df, target_df, weights):
    compatibility_results = []
    
    # Define an inflation factor (greater than 1 to inflate scores)
    inflation_factor = 2.0  # You can adjust this factor as needed

    # Iterate through each source row
    for idx1, source_row in source_df.iterrows():
        source_name = source_row[0]  # Get the actual name from the first column

        if pd.isna(source_name) or source_name.strip() == "":
            continue

        # Iterate through each target row
        for idx2, target_row in target_df.iterrows():
            target_name = target_row[0]  # Get the actual name from the first column

            if pd.isna(target_name) or target_name.strip() == "":
                continue

            # Initialize the total weighted similarity and weight sum
            total_weighted_similarity = 0
            weight_sum = 0

            # Loop through each column for similarity calculation
            for column in source_df.columns:
                source_value = source_row[column]
                target_value = target_row[column]

                # Check for empty values
                if pd.isna(source_value) or pd.isna(target_value) or source_value.strip() == "" or target_value.strip() == "":
                    continue  # Skip this comparison if either value is empty

                if isinstance(source_value, str) and isinstance(target_value, str):
                    # Vectorization of the texts using TF-IDF
                    vectorizer = TfidfVectorizer()
                    tfidf_matrix = vectorizer.fit_transform([source_value, target_value])

                    if tfidf_matrix.shape[0] > 1:
                        source_vector = tfidf_matrix[0].toarray()
                        target_vector = tfidf_matrix[1].toarray()

                        # Calculate cosine similarity
                        similarity = cosine_similarity(source_vector, target_vector)[0][0]

                        # Apply the weight to the similarity score
                        weight = weights.get(column, 1.0)  # Default to 1 if column not in weights
                        total_weighted_similarity += similarity * weight
                        weight_sum += weight

            # Calculate the weighted average similarity as a decimal
            if weight_sum > 0:
                inflated_score = (total_weighted_similarity / weight_sum) * inflation_factor  # Inflate the score
                inflated_score = min(inflated_score, 1.0)  # Ensure the score doesn't exceed 1
                compatibility_results.append((source_name, target_name, inflated_score))
            else:
                compatibility_results.append((source_name, target_name, 0))  # No valid similarity

    return compatibility_results


def save_to_excel(compatibility_results):
    """Save the compatibility results to an Excel file without headers and indices."""
    df_results = pd.DataFrame(compatibility_results)

    # Create the output directory if it doesn't exist
    output_directory = 'output'
    os.makedirs(output_directory, exist_ok=True)

    # Save the DataFrame to an Excel file without headers and index
    output_file_path = os.path.join(output_directory, 'compatibility_results.xlsx')
    df_results.to_excel(output_file_path, index=False, header=False)  # Save without headers or index

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
