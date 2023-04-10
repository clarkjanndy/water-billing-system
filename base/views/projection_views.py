from django.core.exceptions import ValidationError
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
        
        try:
            Projection.objects.create(
                month = datetime.strptime(request.POST['month'], "%Y-%m"),
                released_water = request.POST['released_water'],
                expected_income = request.POST['expected_income']
            )
        except ValidationError as e:
             messages.success(request, e.message)
             return redirect("/admin/projections") 
            
                
        messages.success(request, "New Entry added")
        return redirect("/admin/projections") 
        
        
    return HttpResponse(status=405)

def update(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        
        try:
            projection = Projection.objects.get(
                id = request.POST['id']
            )
            projection.remaining_water = request.POST['remaining_water']
            projection.save()
        except ValidationError as e:
             messages.success(request, e.message)
             return redirect("/admin/projections") 
        
                  
        messages.success(request, "Entry has been updated")
        return redirect("/admin/projections") 
        
        
    return HttpResponse(status=405)


def delete(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    Projection.objects.get(id = id).delete()
    messages.success(request, "Entry has been deleted")   
        
    return redirect('/admin/projections')
    