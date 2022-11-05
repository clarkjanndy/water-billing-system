from urllib import response
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password

from base.models import CustomUser, Reading

# 
def validate_password(request):
    if not check_password(request.GET['password'], request.user.password):
        return JsonResponse({'valid': False})

    return JsonResponse({'valid': True})

def validate_username(request):
    user = CustomUser.objects.all().filter(username = request.GET['username'])
    if not user.exists():
         return JsonResponse({'valid': True})
    
    return JsonResponse({'valid': False})

def validate_meter(request):
    user = CustomUser.objects.all().filter(meter_no = request.GET['meter_no'])
    if not user.exists():
         return JsonResponse({'valid': True})
    
    return JsonResponse({'valid': False})

def validate_billing_month(request):
    reading = Reading.objects.all().filter(billing_month = request.GET['billing_month'], user_id = request.GET['user_id'])
    if not reading.exists():
         return JsonResponse({'valid': True})
    
    return JsonResponse({'valid': False})
