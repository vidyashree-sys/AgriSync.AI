from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Farm
from .utils import get_coords_from_image, get_environmental_data, calculate_market_logic


from django.shortcuts import render, get_object_or_404
from .models import Farm

import random # To simulate AI market data
from django.shortcuts import render, get_object_or_404
from .models import Farm

def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    
    # 1. Simulate "Market Intelligence" Logic
    # In a real app, this would come from an API or ML model
    saturation_val = random.randint(30, 85)
    risky_status = saturation_val > 70
    
    # 2. Logic-based Advice
    if risky_status:
        advice_text = f"High competition detected for {farm.intended_crop}. We suggest diversifying to avoid a price crash."
        suggested_crop = "Ginger or Turmeric" # High value alternatives
    else:
        advice_text = f"Market conditions are stable. {farm.intended_crop} is a safe bet for this season."
        suggested_crop = farm.intended_crop

    # 3. Environmental Data (Placeholder - You can connect OpenWeather here later)
    environmental_data = {
        'temp': 28,
        'humidity': 65
    }

    context = {
        'farm': farm,
        'saturation': saturation_val,
        'is_risky': risky_status,
        'advice': advice_text,
        'crop': suggested_crop,
        'env': environmental_data,
    }
    
    return render(request, 'farms/result.html', context)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        image = request.FILES.get('farm_image')
        # Simulate Satellite GPS extraction from image
        lat, lon = get_coords_from_image(image) if image else (request.POST.get('lat'), request.POST.get('lon'))
        
        Farm.objects.create(
            user=request.user,
            farm_name=request.POST.get('farm_name'),
            image=image,
            intended_crop=request.POST.get('intended_crop'),
            latitude=lat,
            longitude=lon,
            soil_type=request.POST.get('soil_type'),
            nitrogen=request.POST.get('n', 0),
            phosphorus=request.POST.get('p', 0),
            potassium=request.POST.get('k', 0),
            ph_level=request.POST.get('ph', 7.0)
        )
        return redirect('dashboard')
    
    farms = Farm.objects.filter(user=request.user)
    return render(request, 'farms/dashboard.html', {'farms': farms})

@login_required
def predict_crop(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    env_data = get_environmental_data(farm.latitude, farm.longitude)
    
    # Calculate logic using the updated utils.py
    crop, advice, saturation, is_risky = calculate_market_logic(farm)
    
    return render(request, 'farms/result.html', {
        'farm': farm,
        'crop': crop,
        'advice': advice,
        'saturation': saturation,
        'is_risky': is_risky,
        'env': env_data
    })