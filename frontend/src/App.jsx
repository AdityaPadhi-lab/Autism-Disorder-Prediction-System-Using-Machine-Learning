import { useState } from "react";
import "./App.css";

function App() {

  const [page, setPage] = useState("home");

  const [prediction, setPrediction] = useState("");

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [formData, setFormData] = useState({
    A1: 0,
    A2: 0,
    A3: 0,
    A4: 0,
    A5: 0,
    A6: 0,
    A7: 0,
    A8: 0,
    A9: 0,
    A10: 0,
    age: 18,
  });

  const questions = [
    "Do you overthink your eye contact or blinking ?",
    "Is it hard to tell why people are laughing ?",
    "Do you laugh at times others find unusual ?",
    "Do sudden changes to your routine upset you ?",
    "Are certain sounds, lights, or textures physically overwhelming ?",
    "Do you have intense, hyper-focused interests ?",
    "Do you consciously copy others to fit in ?",
    "Do you make repetitive movements to calm down ?",
    "Is it difficult to read body language or social cues ?",
    "Do social interactions leave you completely exhausted ?"
  ];

  const handleAnswer = (question, value) => {

    setFormData({
      ...formData,
      [question]: value
    });

    setCurrentQuestion(currentQuestion + 1);
  };

  const handleSubmit = async () => {

  try {

    const API_URL = import.meta.env.VITE_API_URL;

    // ADD REQUIRED BACKEND FIELDS
    const finalData = {
      ...formData,

      gender: 1,
      jaundice: 0,
      austim: 0
    };

    const response = await fetch(
      `${API_URL}/predict`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(finalData),
      }
    );

    const data = await response.json();

    console.log(data);

    if (data.prediction) {

      setPrediction(data.prediction);

    } else if (data.error) {

      setPrediction(`Error: ${data.error}`);

    }

  } catch (error) {

    console.log(error);

    alert("Backend not connected");
  }
};

  return (

    <div className="main">

      {/* NAVBAR */}

      <nav className="navbar">

        <div className="logo">
          🧠 Autism Prediction System
        </div>

        <div className="navLinks">

          <button onClick={() => setPage("home")}>
            Home
          </button>

          <button onClick={() => setPage("about")}>
            About
          </button>

          <button onClick={() => setPage("works")}>
            How it Works
          </button>

          <button
            className="predictNav"
            onClick={() => {
              setPage("predict");
              setCurrentQuestion(0);
              setPrediction("");
            }}
          >
            Predict
          </button>

        </div>

      </nav>

      {/* HOME */}

      {page === "home" && (

        <div className="homePage">

          <div className="leftSection">

            <h1>
              AI-Powered
              <span> Autism Prediction</span>
            </h1>

            <p>
              This project uses machine learning
              algorithms to predict autism based
              on behavioral assessment data.
            </p>

            <div className="featureList">

              <div className="featureItem">
                ⚡ Instant Prediction
              </div>

              <div className="featureItem">
                🔒 Secure Assessment
              </div>

              <div className="featureItem">
                🤖 AI-Based Analysis
              </div>

            </div>

            <button
              className="startBtn"
              onClick={() => setPage("predict")}
            >
              Start Prediction
            </button>

          </div>

          <div className="rightSection">

            <div className="heroCard">

              <h2>Smart Healthcare AI</h2>

              <p>
                Modern autism prediction dashboard
                powered by machine learning.
              </p>

            </div>

          </div>

        </div>

      )}

      {/* ABOUT */}

      {page === "about" && (

        <div className="pageCard">

          <h1>About Project</h1>

          <p>
            The Autism Prediction System is an
            AI-powered healthcare application
            developed as a Final Year Project.
          </p>

          <div className="aboutGrid">

            <div className="infoBox">

              <h2>🎯 Objective</h2>

              <p>
                Predict autism using behavioral
                assessment analysis.
              </p>

            </div>

            <div className="infoBox">

              <h2>🤖 Technologies</h2>

              <p>
                React JS, Flask, Python,
                Machine Learning.
              </p>

            </div>

            <div className="infoBox">

              <h2>📊 ML Model</h2>

              <p>
                Ensemble Voting Classifier
                with high prediction accuracy.
              </p>

            </div>

          </div>

        </div>

      )}

      {/* HOW IT WORKS */}

      {page === "works" && (

        <div className="pageCard">

          <h1>How It Works</h1>

          <div className="steps">

            <div className="stepBox">

              <h2>1️⃣ Assessment</h2>

              <p>
                User answers autism-related
                behavioral questions.
              </p>

            </div>

            <div className="stepBox">

              <h2>2️⃣ AI Analysis</h2>

              <p>
                Data is processed using
                trained ML algorithms.
              </p>

            </div>

            <div className="stepBox">

              <h2>3️⃣ Prediction</h2>

              <p>
                The system predicts autism
                probability instantly.
              </p>

            </div>

            <div className="stepBox">

              <h2>4️⃣ Final Result</h2>

              <p>
                Result displayed with
                modern healthcare UI.
              </p>

            </div>

          </div>

        </div>

      )}

      {/* PREDICT PAGE */}

      {page === "predict" && (

        <div className="sliderPage">

          <div className="questionCard">

            <div className="progressBar">

              <div
                className="progress"
                style={{
                  width: `${((currentQuestion + 1) / 11) * 100}%`
                }}
              ></div>

            </div>

            {currentQuestion < 10 ? (

              <>

                <div className="questionNumber">
                  Question {currentQuestion + 1} / 10
                </div>

                <h2 className="questionTitle">
                  Autism Assessment
                </h2>

                <p className="questionText">
                  {questions[currentQuestion]}
                </p>

                <div className="optionButtons">

                  <button
                    className="yesBtn"
                    onClick={() =>
                      handleAnswer(
                        `A${currentQuestion + 1}`,
                        1
                      )
                    }
                  >
                    Yes
                  </button>

                  <button
                    className="noBtn"
                    onClick={() =>
                      handleAnswer(
                        `A${currentQuestion + 1}`,
                        0
                      )
                    }
                  >
                    No
                  </button>

                </div>

              </>

            ) : (

              <>

                <h2 className="questionTitle">
                  Enter Age
                </h2>

                <input
                  type="number"
                  className="ageInput"
                  value={formData.age}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      age: Number(e.target.value)
                    })
                  }
                />

                <button
                  className="predictBtn"
                  onClick={handleSubmit}
                >
                  Predict Result
                </button>

              </>

            )}

            {prediction && (

              <div className="resultCard">

                <h3>Prediction Result</h3>

                <h1>{prediction}</h1>

              </div>

            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default App;