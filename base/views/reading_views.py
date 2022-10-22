from django.shortcuts import redirect

from base.models import CustomUser
from base.models import Reading

from django.contrib import messages

# Create your views here.
def add_reading(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        new_reading = Reading(
            previous=request.POST["previous"],
            present=request.POST["present"],
            billing_month=request.POST["billing_month"],
            consumption=request.POST["consumption"],
            multiplier=request.POST["multiplier"],  
            user = CustomUser.objects.get(id=request.POST["consumer_id"])
        )        
        new_reading.save()

        messages.success(request, 'Reading added successfully')
        
        return redirect("/consumers/"+ request.POST["consumer_id"] + "/readings")