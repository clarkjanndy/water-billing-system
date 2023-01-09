from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from base.models import Transaction, CustomUser, PasswordResetRequest

from base.utils.pdf_generator import pdf_generator


# Create your views here.
def print_consumption(request, name):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    data = {'name': "as"}
    template_path = "./base/print/monthly_collection.html"
    
    pdf=pdf_generator(template_path, data).generate()
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="monthly_collection.pdf"'
    
    return response


