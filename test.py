from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import random
from math import radians, sin, cos, sqrt, atan2

# ML imports
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = Flask(__name__)

# ---------- HELPER FUNCTIONS ----------
def haversine_distance_km(lat, lon):
    city_lat, city_lon = 28.6139, 77.2090
    R = 6371
    dlat = radians(city_lat - lat)
    dlon = radians(city_lon - lon)
    a = sin(dlat/2)**2 + cos(radians(lat))*cos(radians(city_lat))*sin(dlon/2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))

def compute_ahp_score(irr, slope, landai):
    def norm(v,a,b): return max(0, min(1,(v-a)/(b-a)))
    s_irr = norm(irr,3.5,7.5)
    s_slope = 1 - norm(slope,0,30)
    s_land = norm(landai,0,1)
    return round(0.6*s_irr + 0.25*s_slope + 0.15*s_land,3)

# Heuristic function for generating synthetic training data
def heuristic_label(irr, slope, landai):
    if irr >= 5.2 and slope <= 7 and landai >= 0.5: return 2
    elif irr >= 4.2 and slope <= 15: return 1
    return 0

label_map = {0:"Not Suitable",1:"Moderately Suitable",2:"Highly Suitable"}

# ---------- ML MODEL ----------
# Generate synthetic dataset based on heuristic
def train_ml_model():
    X, y = [], []
    for _ in range(1000):
        irr = round(random.uniform(3.5,7.5),2)
        slope = round(random.uniform(0,20),2)
        landai = round(random.uniform(0.3,1.0),2)
        X.append([irr, slope, landai])
        y.append(heuristic_label(irr, slope, landai))
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf

ml_model = train_ml_model()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/test')
def test_page():
    return send_from_directory('.', 'test.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        body = request.get_json()
        lat = float(body.get('lat'))
        lon = float(body.get('lon'))

        NASA_API = "https://power.larc.nasa.gov/api/temporal/daily/point"
        params = {"latitude": lat, "longitude": lon, "start": "20220101", "end": "20220101",
                  "parameters": "ALLSKY_SFC_SW_DWN", "format": "JSON"}
        try:
            r = requests.get(NASA_API, params=params, timeout=5)
            r.raise_for_status()
            data = r.json()
            irr = round(float(list(data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"].values())[0])/1000, 2)
        except Exception as e:
            print("NASA API failed:", e)
            irr = round(random.uniform(3.5,7.5),2)

        slope = round(random.uniform(0,20),2)
        elev = round(random.uniform(50,500),1)
        landai = round(random.uniform(0.3,1.0),2)

        # Use ML model for prediction instead of heuristic
        pred = int(ml_model.predict([[irr, slope, landai]])[0])
        probability = round(max(ml_model.predict_proba([[irr, slope, landai]])[0]),2)
        label = label_map[pred]
        ahp_score = compute_ahp_score(irr, slope, landai)

        site_values = {
            "Irradiance Score": round(irr / 7.0,3),
            "Slope Score": round(max(0,1-slope/30),3),
            "Elevation Score": round(max(0,1-elev/3500),3),
            "Land Use Score": round(landai,3),
            "Accessibility Score": round(max(0,1-haversine_distance_km(lat, lon)/50),3),
        }

        return jsonify({
            "label": label,
            "probability": probability,
            "irradiance": irr,
            "slope": slope,
            "elevation": elev,
            "landai": landai,
            "ahp_score": ahp_score,
            "site_values": site_values
        })

    except Exception as e:
        print("Predict Error:", e)
        return jsonify({"error":"Server error"}),500

@app.route("/charts")
def charts_page():
    return render_template("chart.html")

@app.route("/charts-data")
def charts_data():
    city_name = request.args.get("city", "Delhi")

    # Lookup for city coordinates
    city_coords = {c['name']: (c['lat'], c['lon']) for c in [
        {"name":"Delhi","lat":28.7041,"lon":77.1025},
        {"name":"Hyderabad","lat":17.3850,"lon":78.4867},
        {"name":"Mumbai","lat":19.0760,"lon":72.8777},
    ]}

    lat, lon = city_coords.get(city_name, (28.7041, 77.1025))

    irr = round(random.uniform(3.5,7.5),2)
    slope = round(random.uniform(0,20),2)
    elev = round(random.uniform(50,500),1)
    landai = round(random.uniform(0.3,1.0),2)

    return jsonify({
        "irradiance": irr,
        "slope": slope,
        "elevation": elev,
        "landai": landai
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
