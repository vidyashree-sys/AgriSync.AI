import requests
from django.conf import settings
from PIL import Image

def get_coords_from_image(image_file):
    """Simulates extracting GPS from photo metadata."""
    try:
        # In a real-world scenario, we use PIL to read EXIF GPS tags
        # For the demo, we simulate the 'Satellite' finding the coordinates
        return 12.9716, 77.5946 
    except:
        return 15.3173, 75.7139 # Fallback coordinates

def get_environmental_data(lat, lon):
    """Fetches real-time weather from OpenWeatherMap."""
    try:
        api_key = getattr(settings, 'WEATHER_API_KEY', 'your_api_key_here')
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5).json()
        return {
            "temp": response['main']['temp'],
            "humidity": response['main']['humidity'],
            "condition": response['weather'][0]['description'],
            "success": True
        }
    except:
        # Fallback dictionary so the HTML doesn't crash
        return {"temp": 28, "humidity": 60, "condition": "Cloudy", "success": False}

def calculate_market_logic(farm):
    """The 'Anti-Herd' Logic: Checks if too many people are growing the same crop."""
    from .models import Farm
    
    total_farms = Farm.objects.count()
    # Count how many OTHER farmers chose the same intended crop (case-insensitive)
    others = Farm.objects.filter(intended_crop__iexact=farm.intended_crop).exclude(id=farm.id).count()
    
    saturation = (others / total_farms * 100) if total_farms > 1 else 0
    ph = float(farm.ph_level)
    
    # Logic: If > 30% farmers grow the same thing, it's a risk!
    if saturation > 30:
        is_risky = True
        suggested_crop = "Rice" if ph < 6.5 else "Millets"
        advice = f"Market Alert! {int(saturation)}% of nearby farmers are growing {farm.intended_crop}. To prevent a price crash and surplus wastage, we recommend switching to {suggested_crop}."
    else:
        is_risky = False
        suggested_crop = farm.intended_crop
        advice = f"Market stable. Only {int(saturation)}% of neighbors are growing this. {farm.intended_crop} is a safe and profitable choice for your soil."

    return suggested_crop, advice, int(saturation), is_risky