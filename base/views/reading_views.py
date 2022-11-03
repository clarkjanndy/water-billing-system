from datetime import datetime
from django.shortcuts import redirect, render

from base.models import CustomUser
from base.models import Reading
from base.models import Collectible
from base.models import Notification

from django.contrib import messages

from datetime import date, datetime, timedelta

def formatdate(date, format):
    return datetime.strptime(date, format)

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
            billing_month=datetime.strptime(request.POST["billing_month"], "%Y-%m"),
            consumption=request.POST["consumption"],
            multiplier=request.POST["multiplier"],
            user=CustomUser.objects.get(id=request.POST["consumer_id"]),
        )
        # reading added
        new_reading.save()

        new_collectibles = Collectible(
            penalty=0,  # 0 for regular, 1 for penalty
            amount=request.POST["total_bill"],
            due_date=date.today() + timedelta(days=30),
            status="unpaid",  # 0 for unpaid, 1 for penalty
            reading=new_reading,
        )
        # collectibles added
        new_collectibles.save()

        new_notification = Notification(
            user = CustomUser.objects.get(id=request.POST["consumer_id"]),
            content= "You have been charged a total of " + str(new_collectibles.amount) + " pesos for your " + str(new_reading.billing_month.strftime('%B, %Y'))
            + " billing. Due date is on " + str(new_collectibles.due_date.strftime('%B %d, %Y')) +". Thank You!",
            link="/bills/"+ str(new_collectibles.id),
            status=0
        )
        #create notification
        new_notification.save()

        messages.success(request, "Reading added successfully")
        return redirect("/consumers/" + request.POST["consumer_id"] + "/readings")

    consumer = CustomUser.objects.get(id=request.GET["user_id"])
    last_reading = Reading.objects.all().filter(user_id=request.GET["user_id"]).order_by('billing_month').last()
    data = {"consumer": consumer, "last_reading": last_reading}
    return render(request, "./base/reading/add_reading.html", data)

def edit_reading(request, id):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    reading = Reading.objects.get(id=id)
    consumer = CustomUser.objects.get(id=reading.user_id)
    collectible = Collectible.objects.get(reading_id=id)

    if collectible.status == 'paid':
            messages.success(request, "You cannot edit a reading with a paid status")
            return redirect("/consumers/" + str(consumer.id) + "/readings")

    if request.method == "POST":
        reading.previous = request.POST["previous"]
        reading.present = request.POST["present"]
        reading.billing_month = datetime.strptime(request.POST["billing_month"], "%Y-%m")
        reading.consumption=request.POST["consumption"]
        reading.multiplier=request.POST["multiplier"]
       
        # reading edited
        reading.save()

        collectible.amount = request.POST["total_bill"]
        # collectibles edited
        collectible.save()

        new_notification = Notification(
            user = CustomUser.objects.get(id=request.POST["consumer_id"]),
            content= "Your billing for the month of "+ str(reading.billing_month.strftime('%B, %Y')) + " has been updated. Your new bill for the month of " +
            str(reading.billing_month.strftime('%B, %Y')) +" is now " + str(collectible.amount) +" pesos. Thank You",
            link="/bills/"+ str(collectible.id),
            status=0
        ) 
        #create notification
        new_notification.save()

        messages.success(request, "Reading updated successfully")
        return redirect("/consumers/" + request.POST["consumer_id"] + "/readings")

    data = {"consumer": consumer, "reading": reading, 'collectible': collectible}
    return render(request, "./base/reading/edit_reading.html", data)
