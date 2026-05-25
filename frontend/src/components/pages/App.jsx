import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

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
    age: 18
  });

  const [result, setResult] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {

      // BACKEND URL FROM VERCEL ENV VARIABLE
      const API_URL = import.meta.env.VITE_API_URL;

      const response = await axios.post(
        `${API_URL}/predict`,
        formData
      );

      setResult(response.data.prediction);

    } catch (error) {

      console.log(error);

      setResult("Backend not connected");

    }
  };

  return (

    <div className="container">

      {/* LEFT SIDE PANEL */}

      <div className="sidePanel">

        <h1>
          AI-Powered
          <span> Autism Prediction</span>
        </h1>

        <p>
          This intelligent healthcare system
          predicts autism using machine
          learning algorithms trained on
          behavioral assessment patterns.
        </p>

        <div className="panelFeatures">

          <div className="panelBox">
            ⚡ Real-Time Prediction
          </div>

          <div className="panelBox">
            🤖 AI-Based Analysis
          </div>

          <div className="panelBox">
            🔒 Secure Assessment
          </div>

        </div>

      </div>

      {/* RIGHT SIDE FORM */}

      <div className="formContainer">

        <h1>Autism Detection System</h1>

        <form onSubmit={handleSubmit}>

          {Object.keys(formData).map((key) => (

            <div
              key={key}
              style={{ marginBottom: "15px" }}
            >

              <label>{key}</label>

              <input
                type="number"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                style={{
                  marginLeft: "10px",
                  padding: "8px",
                  width: "100px"
                }}
              />

            </div>

          ))}

          <button type="submit">
            Predict
          </button>

        </form>

        <h2>{result}</h2>

      </div>

    </div>

  );
}

export default App;