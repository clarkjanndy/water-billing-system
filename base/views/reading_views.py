from django.shortcuts import redirect

from base.models import CustomUser
from base.models import Reading
from base.models import Collectibles

from django.contrib import messages

from datetime import date, datetime, timedelta

# Create your views here.
def add_reading(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        new_reading = Reading(
            previous=request.POST["previous"],
            present=request.POST["present"],
            billing_month= datetime.strptime(request.POST["billing_month"], '%Y-%m') ,
            consumption=request.POST["consumption"],
            multiplier=request.POST["multiplier"],  
            user = CustomUser.objects.get(id=request.POST["consumer_id"])
        )  
        #reading added      
        new_reading.save()

        new_collectibles = Collectibles(
            category='regular', #0 for regular, 1 for penalty
            amount=request.POST["total_bill"],
            due_date= date.today() + timedelta(days=30),
            status='unpaid', #0 for unpaid, 1 for penalty
            reading=new_reading
        ) 

        #collectibles added 
        new_collectibles.save()

        messages.success(request, 'Reading added successfully')
        
        return redirect("/consumers/"+ request.POST["consumer_id"] + "/readings")