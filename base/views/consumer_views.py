from django.shortcuts import HttpResponse, render
from django.shortcuts import redirect

from base.models import CustomUser
from base.models import Baranggay
from base.models import Reading

from django.contrib import messages

from django.db.models import F, Func, Value, CharField

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return HttpResponse(status=403)

    consumers = CustomUser.objects.filter(is_superuser=False)

    data = {"consumers": consumers}
    return render(request, "./base/consumer/consumers.html", data)


def view_consumer(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return HttpResponse(status=403)

    consumer = CustomUser.objects.get(id=id)
    baranggays = Baranggay.objects.all()
    last_reading = Reading.objects.all().filter(user_id=id).last()

    data = {
        "baranggays": baranggays,
        "consumer": consumer,
        "last_reading": last_reading,
    }

    return render(request, "./base/consumer/view_consumer.html", data)


def view_consumer_readings(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return HttpResponse(status=403)

    consumer = CustomUser.objects.get(id=id)
    last_reading = Reading.objects.all().filter(user_id=id).last()
    readings = Reading.objects.all().filter(user_id=id)

    data = {
        "readings": readings,
        "consumer": consumer,
        "last_reading": last_reading,
    }

    return render(request, "./base/consumer/view_consumer_readings.html", data)


def add_consumer(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser:
        return HttpResponse(status=403)

    if request.method == "POST":
        baranggay = Baranggay.objects.get(id=request.POST["address"])

        # add the consumer
        new_consumer = CustomUser.objects.create_user(
            first_name=request.POST["first_name"],
            middle_name=request.POST["middle_name"],
            last_name=request.POST["last_name"],
            ext_name=request.POST["ext_name"],
            gender=request.POST["gender"],
            civil_status=request.POST["civil_status"],
            address=baranggay,
            religion=request.POST["religion"],
            contact_no=request.POST["contact_no"],
            meter_no=request.POST["meter_no"],
            email=request.POST["email"],
            username=(
                request.POST["first_name"] + "_" + request.POST["last_name"]
            ).lower(),
            password="Password123",
        )

        return redirect("/consumers")

    baranggays = Baranggay.objects.all()
    data = {"baranggays": baranggays}
    return render(request, "./base/consumer/add_consumer.html", data)


def edit_consumer(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return HttpResponse(status=403)

    consumer = CustomUser.objects.get(id=id)
    if request.method == "POST":
        baranggay = Baranggay.objects.get(id=request.POST["address"])

        consumer.first_name = request.POST["first_name"]
        consumer.middle_name = request.POST["middle_name"]
        consumer.last_name = request.POST["last_name"]
        consumer.ext_name = request.POST["ext_name"]
        consumer.gender = request.POST["gender"]
        consumer.civil_status = request.POST["civil_status"]
        consumer.address = baranggay
        consumer.religion = request.POST["religion"]
        consumer.contact_no = request.POST["contact_no"]
        consumer.meter_no = request.POST["meter_no"]
        consumer.email = request.POST["email"]
        consumer.username = request.POST["username"]
        consumer.save()

        messages.success(request, "Details updated successfully")
        return redirect("/consumers/" + str(id))

    baranggays = Baranggay.objects.all()
    data = {"baranggays": baranggays, "consumer": consumer}
    return render(request, "./base/consumer/edit_consumer.html", data)
