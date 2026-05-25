from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# INITIALIZE FLASK APP
app = Flask(__name__)
CORS(app)

# LOAD TRAINED MODEL
model = joblib.load("model/fresh_model.pkl")

# PRINT MODEL FEATURE ORDER
print("MODEL FEATURES:")
print(model.feature_names_in_)

# HOME ROUTE
@app.route("/")
def home():
    return "Autism Prediction API Running"


# PREDICTION ROUTE
@app.route("/predict", methods=["POST"])
def predict():

    try:

        # GET JSON DATA
        data = request.json

        # CALCULATE TOTAL SCORE
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

        # CREATE DATAFRAME IN EXACT MODEL FEATURE ORDER
        features = pd.DataFrame([[

            data["age"],
            data["jaundice"],
            data["austim"],
            data["gender"],

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
        print(features)

        # PREDICT
        prediction = model.predict(features)[0]

        # RESULT
        result = "Autistic" if prediction == 1 else "Non-Autistic"

        return jsonify({
            "prediction": result
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# RUN APP
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)