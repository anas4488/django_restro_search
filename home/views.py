from django.shortcuts import render
from django.http import JsonResponse
from .models import *
# Create your views here.
from geopy.distance import  great_circle


def home(request):
    return render(request , 'home.html')





def api(request):
    restaurant_objs = Restaurant.objects.all()
    
    pincode = request.GET.get('pincode')
    km = request.GET.get('km')
    user_lat = None
    user_long = None
    
    if pincode:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(pincode))
        user_lat = location.latitude
        user_long = location.longitude 
    
    
    payload = []
    for restaurant_obj in restaurant_objs:
        result = {}
        result['name'] = restaurant_obj.name
        result['image'] = restaurant_obj.image
        result['description'] = restaurant_obj.description
        result['pincode'] = restaurant_obj.pincode
        if pincode:
            first = (float(user_lat) , float(user_long))
            second = (float(restaurant_obj.lat) , float(restaurant_obj.lon))
            result['distance'] = int( great_circle(first , second).miles)
        
        payload.append(result)
        
        if km:
            if result['distance'] > int(km):
                payload.pop()
             
                
             
                    
        
        
    return JsonResponse(payload , safe=False)
    
    
