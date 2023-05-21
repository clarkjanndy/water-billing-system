from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum

from base.models import CustomUser
from base.models import Baranggay, Transaction

from django.contrib import messages

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    baranggays = Baranggay.objects.all()
    data = {"baranggays": baranggays, 'page': 'barangays'}
    return render(request, "./base/baranggay/baranggays.html", data)


def view_baranggay(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    baranggay = Baranggay.objects.get(id=id)
    consumers = CustomUser.objects.all().filter(address_id=id, is_superuser = 0)
    
    collection = Transaction.objects.filter(user__in = consumers).aggregate(collection=Sum('amount')).get('collection')
    data = {
        "baranggay": baranggay, 
        "consumers": consumers, 
        "page": 'barangays', 
        "collection": collection if collection else 0.00}
    return render(request, "./base/baranggay/view_baranggay.html", data)


def add_baranggay(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")
    
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":

        new_baranggay = Baranggay(
            name=request.POST["name"],
            description=request.POST["description"],
            code=request.POST["code"],
        )
        new_baranggay.save()

        return redirect("/baranggays")
    data= {'page': 'barangays'}
    return render(request, "./base/baranggay/add_baranggay.html", data)


def edit_baranggay(request, id):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")
    
    if not request.user.is_superuser:
        return redirect("/")

    baranggay = Baranggay.objects.get(id=id)
    if request.method == "POST":

        baranggay.name = request.POST["name"]
        baranggay.description = request.POST["description"]
        baranggay.code = request.POST["code"]
        baranggay.save()

        messages.success(request, "Details updated successfully")
        return redirect("/baranggays/" + str(id))

    data = {"baranggay": baranggay, 'page': 'barangays'}
    return render(request, "./base/baranggay/edit_baranggay.html", data)
