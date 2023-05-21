from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from base.models import Projection, Baranggay, CustomUser

from base.utils.pdf_generator import pdf_generator


# Create your views here.
def print_monthly_report(request, id):
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
    response['Content-Disposition'] = 'filename="monthly_report.pdf"'
    
    return response

def print_barangay_report(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    
    barangay = get_object_or_404(Baranggay, id = id)
    consumers = CustomUser.objects.filter(address = barangay, is_superuser= False)
    
    context = {'barangay': barangay,
               'consumers': consumers
               }
    
    template_path = "./base/print/barangay_report.html"
    
    pdf=pdf_generator(template_path, context).generate()
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="barangay_report.pdf"'
    
    return response


