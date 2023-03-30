from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

from ..models import Projection

from datetime import datetime

def add(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        Projection.objects.create(
            month = datetime.strptime(request.POST['month'], "%Y-%m"),
            released_water = request.POST['released_water'],
            expected_income = request.POST['expected_income']
        )
                
        messages.success(request, "New Entry added")
        return redirect("/admin/projections") 
        
        
    return HttpResponse(status=405)

def update(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        projection = Projection.objects.get(
            id = request.POST['id']
        )
        projection.released_water = request.POST['released_water']
        projection.expected_income = request.POST['expected_income']
        projection.save()
                  
        messages.success(request, "Entry has been updated")
        return redirect("/admin/projections") 
        
        
    return HttpResponse(status=405)
    