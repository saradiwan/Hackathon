
🌞 Solar Site Suitability Portal

AI-powered real-time solar feasibility analysis for any location in India

A full-stack solar analytics platform that fetches  NASA POWER solar irradiance, applies  Machine Learning , combines AHP-based multi-criteria decision making, and displays results on an interactive map with charts.

This project helps users evaluate how suitable a location is for installing solar panels — using a mix of real-time data + predictive modelling + geospatial analysis.



 🚀 Features

🔐 Authentication (Node.js + MongoDB)

* User Signup/Login
* MongoDB local storage
* Secure routing to analytics dashboard

🗺️ Interactive Solar Suitability Map (Flask + Leaflet.js)

* Click any point on the map OR select a city
* Fetches NASA solar irradiance
* Generates slope, elevation, land-score (synthetic)
* AHP multi-criteria ranking (irradiance + slope + landAI + elevation + accessibility)
* ML model predicts suitability label + confidence

🤖 Machine Learning Model (Python)

* Random Forest Classifier trained on synthetic dataset
* Predicts:
  Not Suitable / Moderately Suitable / Highly Suitable
* Uses irradiance, slope, land-score

 📊 Solar Analytics Dashboard (Chart.js)

For the selected city, the dashboard shows:

* Monthly Irradiance Line Graph
* Slope Bar Graph
* Elevation Bar Graph
* AI Land Score Bar Graph

All charts auto-fetch real-time values from `/charts-data`.



 🏗️ Project Structure


/project
│── index.html          → Authentication page (Login + Signup)
│── server.js           → Node.js backend + MongoDB auth
│── test.html           → Main real-time suitability dashboard
│── chart.html          → Solar analytics charts dashboard
│── test.py             → Flask backend + ML model + NASA API
│── static/
│── templates/


 How the Prediction Works

1. NASA POWER API

Fetches daily ALLSKY_SFC_SW_DWN irradiance
(Fallback: synthetic irradiance if API fails)

2. ML Prediction

Model uses:

* Solar irradiance
* Terrain slope
* Land score

Predicts suitability label + confidence.

3. AHP Scoring (Weighted Method)

Weights:

* Irradiance → 60%
* Slope → 25%
* Land Score → 15%

Outputs the final suitability percentage  shown on UI.



🧪 Tech Stack

Frontend

* HTML, TailwindCSS
* Leaflet.js (interactive map)
* Chart.js
* Vanilla JS

Backend

* Node.js + Express + MongoDB (Authentication)
* Python + Flask (ML + NASA API + Suitability engine)

Machine Learning

* Random Forest Classifier
* Synthetic dataset generation

---

📂 Installation & Setup

 1️⃣ Install Node.js dependencies


npm install
node server.js


Runs at:
[http://localhost:5000](http://localhost:5000)

 2️⃣ Install Python dependencies


pip install flask requests scikit-learn numpy
python test.py


Runs at:
[http://127.0.0.1:5000](http://127.0.0.1:5000)



🖥️ Usage Flow

1. Open the main portal


http://localhost:5000


2. Login / Signup

Redirects to the solar dashboard.

3. Choose a city OR click the map

* Fetch irradiance (NASA)
* Generate slope, elevation, land score
* ML model predicts suitability
* AHP final score is calculated

4. View Charts

Click View Analytics Charts
See four analytical graphs for the selected city.



 📈 Dashboard Outputs (for selected city)

 📌 Solar Analytics Dashboard

* Irradiance Trend (12 months)
* Slope Bar Graph
* Elevation Bar Graph
* AI Land Score Bar Graph

📌 Real-time Fields

* Latitude / Longitude
* Irradiance (NASA / fallback synthetic)
* Slope (synthetic)
* Elevation (synthetic)
* ML Suitability Label
* ML Confidence
* AHP-based Final Score



⚡ APIs

POST /predict

Inputs: latitude, longitude
Returns:

* irradiance
* slope
* elevation
* landAI
* ML label + confidence
* AHP score
* Sub-criteria breakdown

GET /charts-data?city=CityName

Returns synthetic data for charts.



Final Notes

* NASA API provides real irradiance but slope/elevation/land scores are  synthetic for hackathon demo.
* ML model uses synthetic dataset trained at runtime.
* Ideal for hackathons, prototypes, research demos.


