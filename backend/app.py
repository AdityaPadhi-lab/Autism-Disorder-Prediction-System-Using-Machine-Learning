from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
CORS(app)

# LOAD MODEL
model = joblib.load("model/fresh_model.pkl")

# PRINT MODEL FEATURE ORDER
print("MODEL FEATURES:")
print(model.feature_names_in_)

# HOME ROUTE
@app.route("/")
def home():
    return "Autism Prediction API Running"


# PREDICT ROUTE
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    # TOTAL SCORE
    total_score = (
        data["A1"] +
        data["A2"] +
        data["A3"] +
        data["A4"] +
        data["A5"] +
        data["A6"] +
        data["A7"] +
        data["A8"] +
        data["A9"] +
        data["A10"]
    )

    # EXACT FEATURE ORDER
    features = pd.DataFrame([[
    data["age"],
    0,  # jaundice
    0,  # austim
    1,  # gender

    data["A1"],
    data["A2"],
    data["A3"],
    data["A4"],
    data["A5"],
    data["A6"],
    data["A7"],
    data["A8"],
    data["A9"],
    data["A10"],

    total_score
]], columns=[
    "age",
    "jaundice",
    "austim",
    "gender",

    "A1_Score",
    "A2_Score",
    "A3_Score",
    "A4_Score",
    "A5_Score",
    "A6_Score",
    "A7_Score",
    "A8_Score",
    "A9_Score",
    "A10_Score",

    "total_score"
])

    print("\nINPUT FEATURES:")
    print(features.columns.tolist())

    prediction = model.predict(features)[0]

    result = "Autistic" if prediction == 1 else "Non-Autistic"

    return jsonify({
        "prediction": result
    })


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
