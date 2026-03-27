import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Farm

# --- API HELPERS ---

def get_village_osm(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        headers = {'User-Agent': 'AgriSync_Project'}
        res = requests.get(url, headers=headers, timeout=3)
        data = res.json()
        address = data.get('address', {})
        return address.get('village') or address.get('suburb') or address.get('city') or "Local Area"
    except:
        return "Location Sync Failed"

def get_nasa_moisture(lat, lon):
    try:
        # Note: In a real project, you'd want to use a dynamic date, but this works for testing
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=GWETROOT&community=AG&longitude={lon}&latitude={lat}&format=JSON&start=20240101&end=20240101"
        res = requests.get(url, timeout=3).json()
        val = list(res['properties']['parameter']['GWETROOT'].values())[0]
        return val
    except:
        return 0.25

# --- MAIN VIEWS ---

@login_required
def dashboard(request):
    farms = Farm.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'farms/dashboard.html', {'farms': farms})

@login_required
def add_farm(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        
        # We fetch the API data during creation
        Farm.objects.create(
            user=request.user,
            farm_name=request.POST.get('farm_name'),
            intended_crop=request.POST.get('intended_crop'),
            latitude=lat,
            longitude=lon,
            location_name=get_village_osm(lat, lon),
            soil_moisture=get_nasa_moisture(lat, lon),
            nitrogen=request.POST.get('nitrogen', 0) or 0,
            phosphorus=request.POST.get('phosphorus', 0) or 0,
            potassium=request.POST.get('potassium', 0) or 0,
            ph_level=request.POST.get('ph_level', 7.0) or 7.0,
            soil_type=request.POST.get('soil_type', 'Loamy')
        )
        return redirect('dashboard')
    return render(request, 'farms/add_farm.html')

@login_required
def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Simple AI Logic
    suggested = "Rice/Sugarcane" if farm.soil_moisture > 0.4 else "Millets/Pulses"
    
    # Herd Mentality check (How many people nearby are growing the same thing?)
    neighbors = Farm.objects.filter(location_name=farm.location_name, intended_crop=farm.intended_crop).count()
    saturation = min(neighbors * 25, 100)

    context = {
        'farm': farm,
        'moisture_level': round(farm.soil_moisture * 100, 1),
        'saturation': saturation,
        'ai_recommendation': suggested,
        'is_risky': saturation > 50,
    }
    return render(request, 'farms/result.html', context)

@login_required
def market_trends(request):
    """Fetches Live Mandi Prices from Agmarknet API"""
    api_url = "https://api.data.gov.in/resource/9ef2718d-35fe-45a0-a30f-adcf01620391?api-key=579b464db66ec23bdd000001cdd3946e448c48ef711a433445d2e7b7&format=json"
    
    market_data = []
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
        market_data = data.get('records', [])[:10]
    except:
        market_data = [{"market": "N/A", "commodity": "Data Offline", "modal_price": "0"}]

    return render(request, 'farms/market_trends.html', {'markets': market_data})

# --- AUTH & OTHERS ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def disease_lab(request):
    return render(request, 'farms/disease_lab.html')

@login_required
def blockchain_ledger(request):
    return render(request, 'farms/blockchain_ledger.html')