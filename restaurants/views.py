from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Restaurant, FoodItem

def home(request):
    restaurants = Restaurant.objects.filter(is_active=True)[:6]
    return render(request, 'restaurants/home.html', {'restaurants': restaurants})

def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    food_items = restaurant.food_items.filter(is_available=True)
    categories = food_items.values_list('category', flat=True).distinct()
    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'food_items': food_items,
        'categories': categories,
    })
