from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from base.models import Transaction, CustomUser, PasswordResetRequest, Reading, Projection, Setting, Baranggay


from django.db.models import Sum, Count, Value, F, Q
from django.db.models.functions import TruncMonth, ExtractYear

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    consumers = CustomUser.objects.filter(is_superuser = 0)
    
    paid_count = len([consumer for consumer in consumers if consumer.get_status == 'paid'])
    unpaid_count =  len([consumer for consumer in consumers if consumer.get_status == 'unpaid'])    
    
    years =  Transaction.objects.annotate(year=ExtractYear('created_on')).values('year').distinct().order_by('-year')
  
    data = {'paid_count': paid_count,
            'unpaid_count': unpaid_count,   
            'consumers': consumers,
            "years": years,
            "page": "dashboard"}
    
    return render(request, './base/dashboard.html', data)

def users(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    admins = CustomUser.objects.all().filter(is_superuser = 1)
    
    data = {'admins':admins,'page': 'administration'}
    return render(request, './base/users.html', data)

def view_user(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    admin = CustomUser.objects.get(id = id)
    
    if  not admin.is_superuser:
        return redirect (f'/consumers/{admin.id}')    
    
    data = {'admin':admin,'page': 'administration'}
    return render(request, './base/view_user.html', data)

def transaction_history(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    transactions = Transaction.objects.select_related('user').order_by('-created_on')
    
    collections = Transaction.objects.annotate(month=TruncMonth('created_on')).values('month').annotate(amount=Sum('amount')).order_by('-month')
    
    data = {'transactions':transactions,
            'collections': collections}
    
    return render(request, './base/transaction-history.html', data)

def consumption_histogram(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    readings = (
    Reading.objects.values("billing_month")
    .annotate(
        month=Count("billing_month", distinct=False), consumption=Sum("consumption")
    )
    .order_by("-billing_month")
    )
    
    data = {'readings': readings}    
    return render(request, './base/consumption-histogram.html', data)

def password_reset_requests(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    password_requests = PasswordResetRequest.objects.all()
    
    data = {'password_requests': password_requests, 'page': 'administration'}

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


def treasury_and_transactions(request):
     if not request.user.is_authenticated:
        return redirect("/")
    
     if not request.user.is_superuser:
        return HttpResponse(status=403)
    
     transactions = Transaction.objects.all().order_by('-created_on')
     consumers = CustomUser.objects.exclude(is_superuser=1)
     
     data = {'page': 'administration',
             'transactions': transactions,
             'consumers': consumers}
     
     return render(request, './base/treasury-and-transactions.html', data)

def projections(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    projections = Projection.objects.all().order_by("-month")
    
    data = {"page": "reports",
            "projections": projections}
    return render(request, './base/projections.html', data)
    
def reports(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    reports = Projection.objects.all().order_by('-month')
    barangays = Baranggay.objects.all().order_by('name')
    barangays_dropdown = barangays
    
    if request.GET.get('year'):
        reports = reports.filter(month__year = request.GET.get('year'))
        
    if request.GET.get('barangay'):
        barangays = barangays.filter(name__icontains = request.GET.get('barangay'))
        
    years =  Projection.objects.annotate(year=ExtractYear('month')).values('year').distinct().order_by('-year')
    
    data = {'reports':reports,
            "barangays": barangays,
            "years": years,
            "barangays_dropdown": barangays_dropdown,
            "selected_year": int(request.GET.get('year')) if request.GET.get('year') else '',
            "selected_barangay":  request.GET.get('barangay'),
            "page": "reports",}
    return render(request, './base/reports.html', data)

def settings(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    settings = Setting.objects.all()
    
    data = {'settings':settings,
            'page': 'administration'}
    return render(request, './base/settings.html', data)

