from flask import Flask, request, jsonify, render_template_string

# --- Flask app ---
app = Flask(__name__)

# Simple HTML form with basic Tailwind CSS and background image
form_html = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent background for readability */
            padding: 2.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            width: 100%;
            max-width: 28rem;
            text-align: center;
        }
        input[type="number"] {
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            border: 1px solid #d1d5db;
            width: 100%;
            box-sizing: border-box;
            margin-bottom: 1rem;
        }
        button[type="submit"] {
            background-color: #4f46e5;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        button[type="submit"]:hover {
            background-color: #4338ca;
        }
        .result-box {
            background-color: #e0f2fe;
            border: 1px solid #90cdf4;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1.5rem;
            text-align: left;
        }
        .error-message {
            color: #ef4444;
            background-color: #fee2e2;
            border: 1px solid #fca5a5;
            padding: 0.75rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Diabetes Prediction</h2>
        <form action="/predict" method="post" class="space-y-4">
            {% for col in cols %}
                <div class="flex flex-col items-start">
                    <label for="{{col}}" class="text-sm font-medium text-gray-700 mb-1">{{ col.replace('_', ' ').title() }}:</label>
                    <input type="number" step="any" id="{{col}}" name="{{col}}" required
                           class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                </div>
            {% end for %}
            <button type="submit"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Predict
            </button>
        </form>
        {% if result %}
            <div class="result-box">
                <p class="text-lg font-semibold text-gray-900">Prediction Result:</p>
                <p class="text-gray-700">Probability: <span class="font-bold">{{ result.probability }}</span></p>
                <p class="text-gray-700">Outcome: <span class="font-bold">{{ result.meaning }}</span></p>
            </div>
        {% endif %}
        {% if error %}
            <div class="error-message">
                <p class="text-red-700">{{ error }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# These are the features expected by your trained model, in order.
# Ensure this matches the order of columns in your 'diabetes (1).csv'
feature_cols = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]


@app.route('/')
def index():
    # Pass an empty result and no error for the initial page load
    return render_template_string(form_html, cols=feature_cols, result=None, error=None)


@app.route('/predict', methods=['POST'])
def predict():
    # Handle both JSON and form requests
    try:
        if request.is_json:
            data = request.get_json()
            values = [data[col] for col in feature_cols]
        else:
            values = [float(request.form[col]) for col in feature_cols]

        # --- Placeholder for prediction logic as model/scaler are not included ---
        # In a real scenario, you would load and use your model/scaler here.
        # For now, we'll return a dummy prediction.
        # Example: if Glucose > 120, predict diabetic (just for demonstration)
        glucose_index = feature_cols.index('Glucose')
        if values[glucose_index] > 120:
            dummy_proba = 0.75
            dummy_pred = 1
        else:
            dummy_proba = 0.25
            dummy_pred = 0
        # --- End of Placeholder ---

        result = {
            'probability': round(dummy_proba, 3),
            'prediction': dummy_pred,  # 1 = diabetic, 0 = non-diabetic
            'meaning': 'Diabetic' if dummy_pred else 'Not Diabetic'
        }

        # Always render HTML with result for non-JSON requests
        if not request.is_json:
            return render_template_string(form_html, cols=feature_cols, result=result, error=None)

        # Return JSON for API calls
        return jsonify(result)

    except Exception as e:
        error_message = f"An error occurred: {e}. Please ensure all fields are filled correctly."
        print(error_message)  # Log the error for debugging
        if request.is_json:
            return jsonify({'error': error_message}), 500
        else:
            # Render the form again with an error message
            return render_template_string(form_html, cols=feature_cols, result=None, error=error_message)


if __name__ == '__main__':
    # No need to check for model directory if model/scaler are not used
    app.run(host='0.0.0.0', port=5000, debug=False)

