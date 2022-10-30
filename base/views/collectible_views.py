from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count, Sum

from base.models import Collectible, CustomUser, Reading
from base.models import Baranggay

from django.contrib import messages

# Create your views here.
def view_collectible(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    collectible = Collectible.objects.get(id=id)
    reading = Reading.objects.get(id=collectible.reading_id)
    consumer = CustomUser.objects.get(id=reading.user_id)

    if not request.user.is_superuser and not request.user.id == consumer.id:
        return redirect("/")

    arrear = (
        Collectible.objects.select_related("reading")
        .filter(reading__billing_month__lte=reading.billing_month).exclude(status='paid')
        .aggregate(total_bill = Sum('amount')+Sum('penalty'),
        arrear_amount = (Sum('amount')+Sum('penalty')) - (collectible.amount + collectible.penalty),
        num_arrear=Count('reading__billing_month')-1)
    )

    data = {
        "collectible": collectible,
        "reading": reading,
        "consumer": consumer,
        "arrear": arrear,
    }
    return render(request, "./base/collectible/view_collectible.html", data)

def print_collectible(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    collectible = Collectible.objects.get(id=id)
    reading = Reading.objects.get(id=collectible.reading_id)
    consumer = CustomUser.objects.get(id=reading.user_id)

    if not request.user.is_superuser and not request.user.id == consumer.id:
        return redirect("/")

    arrear = (
        Collectible.objects.select_related("reading")
        .filter(reading__billing_month__lte=reading.billing_month).exclude(status='paid')
        .aggregate(total_bill = Sum('amount')+Sum('penalty'),
        arrear_amount = (Sum('amount')+Sum('penalty')) - (collectible.amount + collectible.penalty),
        num_arrear=Count('reading__billing_month')-1)
    )

    data = {
        "collectible": collectible,
        "reading": reading,
        "consumer": consumer,
        "arrear": arrear,
    }
    return render(request, "./base/print/print_collectible.html", data)

