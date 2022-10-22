from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def admin(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if not request.user.is_superuser and not request.user.id == id:
        return HttpResponse(status=403)

    page = 'admin-panel'
    
    data = {'page':page}
    return render(request, './base/admin-panel.html', data)



