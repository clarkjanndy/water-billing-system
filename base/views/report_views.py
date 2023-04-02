from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from base.models import Transaction, CustomUser, PasswordResetRequest, Projection

from base.utils.pdf_generator import pdf_generator


# Create your views here.
def print_report(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    report = get_object_or_404(Projection, id = id)
    transactions = report.transactions
    readings = report.readings
    
    context = {'report': report,
               'transactions': transactions,
               'readings': readings}
    template_path = "./base/print/monthly_report.html"
    
    pdf=pdf_generator(template_path, context).generate()
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="monthly_collection.pdf"'
    
    return response


