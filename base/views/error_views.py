from django.shortcuts import render

# Create your views here.
def error_403(request, exception):
    return render(request, 'errors/403.html')