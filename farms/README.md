# AgriSync AI 🌾
**Satellite-Driven Crop Recommendation System**

AgriSync AI is a full-stack web application designed to help farmers make data-driven decisions. By combining user-submitted soil data with real-time satellite environmental data, the platform uses a logic-based engine to recommend the most profitable crops for a specific location.

## 🚀 Key Features
- **User Authentication:** Secure registration and login system for individual farmers.
- **Farm Profile Management:** Save multiple farm locations with specific soil NPK and pH levels to a SQL database.
- **Satellite Integration:** Fetches real-time temperature, humidity, and weather conditions based on GPS coordinates.
- **AI Recommendation Engine:** Analyzes soil composition and environmental factors to suggest optimal crops (Rice, Wheat, Maize, etc.) with a confidence score.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive UI)
- **Backend:** Django 5.x (Python)
- **Database:** SQLite3 (Relational)
- **APIs:** OpenWeatherMap API (Environmental Data)
- **Libraries:** Requests, Django-Auth

## 📦 Installation & Setup
1. **Clone the repository:**
   `git clone <your-repo-link>`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Run Migrations:**
   `python manage.py migrate`
4. **Start the Server:**
   `python manage.py runserver`

## 🧠 AI Logic Overview
The recommendation engine follows a heuristic decision tree:
- **Input:** Nitrogen (N), Phosphorus (P), Potassium (K), pH, Temperature, and Humidity.
- **Process:** Checks soil acidity (pH) against climate thresholds (Temp) to determine crop viability.
- **Output:** Crop Name, Expert Advice, and Match Score.