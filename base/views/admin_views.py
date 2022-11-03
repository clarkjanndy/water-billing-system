from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from base.models import Transaction, CustomUser

# Create your views here.

def admin(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    return render(request, './base/admin_panel.html')

def admins(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    admins = CustomUser.objects.all().filter(is_superuser = 1)
    
    data = {'admins':admins}
    return render(request, './base/admins.html', data)

def transaction_history(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    transactions = Transaction.objects.all().order_by('-created_on')
    
    data = {'transactions':transactions}
    return render(request, './base/transaction-history.html', data)
    



