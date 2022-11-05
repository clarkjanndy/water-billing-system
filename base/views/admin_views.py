from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from base.models import Transaction, CustomUser, PasswordResetRequest

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

    transactions = Transaction.objects.select_related('user').order_by('-created_on')
    
    data = {'transactions':transactions}
    return render(request, './base/transaction-history.html', data)

def consumption_histogram(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    # transactions = Transaction.objects.select_related('user').order_by('-created_on')
    
    # data = {'transactions':transactions}
    return render(request, './base/consumption-histogram.html')

def password_reset_requests(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    password_requests = PasswordResetRequest.objects.all()
    
    data = {'password_requests': password_requests}

    return render(request, './base/password_reset_request.html', data)

def approve_password_reset_request(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    password_requests = PasswordResetRequest.objects.get(id=id)
    password_requests.status='approved'
    password_requests.save()
    
    consumer = CustomUser.objects.get(id=password_requests.user_id)
    consumer.set_password('Password123')
    consumer.save()
    
    messages.success(request, "Password reset request has been approved")
    return redirect("/admin/password-reset-requests")
    
def delete_password_reset_request(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    password_requests = PasswordResetRequest.objects.get(id=id)
    password_requests.delete()
    
    messages.success(request, "Password reset request has been deleted")
    return redirect("/admin/password-reset-requests")
    



