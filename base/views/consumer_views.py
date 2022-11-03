from django.shortcuts import render
from django.shortcuts import redirect

from base.models import Collectible, CustomUser, Notification
from base.models import Baranggay
from base.models import Reading

from django.contrib import messages

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return redirect("/")

    consumers = CustomUser.objects.filter(is_superuser=False)

    data = {"consumers": consumers}
    return render(request, "./base/consumer/consumers.html", data)


def view_consumer(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return redirect("/")

    consumer = CustomUser.objects.get(id=id)
    baranggays = Baranggay.objects.all()
    latest_bill = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=consumer.id)
        .order_by("-reading__billing_month").first()
    )

    data = {
        "baranggays": baranggays,
        "consumer": consumer,
        "latest_bill": latest_bill
    }

    return render(request, "./base/consumer/view_consumer.html", data)


def view_consumer_readings(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return redirect("/")

    consumer = CustomUser.objects.get(id=id)
    readings = (
        Reading.objects.select_related("collectible")
        .filter(user=id)
        .order_by("-billing_month")
    )

    data = {
        "readings": readings,
        "consumer": consumer,
    }

    return render(request, "./base/consumer/view_consumer_readings.html", data)


def view_consumer_bills(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return redirect("/")

    consumer = CustomUser.objects.get(id=id)
    bills = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id)
        .order_by("-reading__billing_month")
    )

    data = {
        "bills": bills,
        "consumer": consumer,
    }

    return render(request, "./base/consumer/view_consumer_bills.html", data)


def add_consumer(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

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

        messages.success(request, "Consumer added successfully")
        return redirect("/consumers/" + str(new_consumer.id))

    baranggays = Baranggay.objects.all()
    data = {"baranggays": baranggays}
    return render(request, "./base/consumer/add_consumer.html", data)


def edit_consumer(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser and not request.user.id == id:
        return redirect("/")

    consumer = CustomUser.objects.get(id=id)

    if consumer == None:
        return redirect("/")

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

def get_notifications(request):
    if not request.user.is_authenticated:
        return redirect("/")

    consumer = CustomUser.objects.get(id=request.user.id)
    notifications = Notification.objects.all().filter(user=consumer).order_by('created_on', 'status')

    data = {
        "consumer": consumer,
        "notifs": notifications
    }

    return render(request, "./base/consumer/notifications.html", data)