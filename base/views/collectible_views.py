from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count, Sum, Min

from datetime import date

from base.models import (
    Collectible,
    CustomUser,
    Invoice,
    Reading,
    Transaction,
    Notification
)

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
    
    if collectible.status == 'paid':
        messages.success(request, "No current billing for this user yet")

        if request.GET['from'] == 'profile':
            return redirect("/consumers/" + str(consumer.id))

        return redirect("/consumers/" + str(consumer.id) + '/bills')

    arrear = (
        Collectible.objects.select_related("reading")
        .filter(
            reading__billing_month__lte=reading.billing_month,
            reading__user_id=consumer.id,
        )
        .exclude(status="paid")
        .aggregate(
            total_bill=Sum("amount") + Sum("penalty"),
            arrear_amount=(Sum("amount") + Sum("penalty"))
            - (collectible.amount + collectible.penalty),
            num_arrear=Count("reading__billing_month") - 1,
            start_month=Min("reading__billing_month"),
        )
    )

    data = {
        "collectible": collectible,
        "reading": reading,
        "consumer": consumer,
        "arrear": arrear,
        'page': 'consumers'
        
    }
    return render(request, "./base/collectible/view_collectible.html", data)


def transact(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    collectible = Collectible.objects.get(id=id)
    reading = Reading.objects.get(id=collectible.reading_id)
    consumer = CustomUser.objects.get(id=reading.user_id)

    choices = (
        Collectible.objects.select_related("reading")
        .filter(
            reading__user_id=consumer.id,
        )
        .exclude(status="paid")
        .order_by("reading__billing_month")
    )

    arrear = (
        Collectible.objects.select_related("reading")
        .filter(
            reading__billing_month__lte=reading.billing_month,
            reading__user_id=consumer.id,
        )
        .exclude(status="paid")
        .aggregate(
            total_bill=Sum("amount") + Sum("penalty"),
            arrear_amount=(Sum("amount") + Sum("penalty"))
            - (collectible.amount + collectible.penalty),
            num_arrear=Count("reading__billing_month") - 1,
            start_month=Min("reading__billing_month"),
        )
    )

    data = {
        "collectible": collectible,
        "choices": choices,
        "reading": reading,
        "consumer": consumer,
        "arrear": arrear,
        'page': 'consumers'
    }
    return render(request, "./base/collectible/transact.html", data)


def transact_complete(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        consumer = CustomUser.objects.get(id=request.POST["consumer_id"])
        collectible = Collectible.objects.get(id=request.POST["collectible_id"])
        reading = Reading.objects.get(id=collectible.reading_id)

        paids = (
            Collectible.objects.select_related("reading")
            .filter(
                reading__billing_month__lte=reading.billing_month,
                reading__user_id=consumer.id,
            )
            .exclude(status="paid")
        )

        # create new transaction
        new_transaction = Transaction(
            user=consumer,
            amount=request.POST["total"],
            tendered=request.POST["tendered"],
            change=request.POST["change"],
            content="{firstname} {middlename} {lastname} {extname} had payed a total of {total} on {date}".format(
                firstname=consumer.first_name,
                middlename=consumer.middle_name,
                lastname=consumer.last_name,
                extname=consumer.ext_name,
                total=request.POST["total"],
                date=date.today().strftime("%B %d, %Y")
            ),
        )
        new_transaction.save()

        # change the status of every collectible selected and insert them in invoice
        for paid in paids:
            paid.status = "paid"
            paid.save()

            invoice = Invoice(collectible=paid, transaction=new_transaction)
            invoice.save()
        
        new_notification = Notification(
            user = consumer,
            content= "You succesfulyy paid a total of {total} pesos on {date}"
            .format(total=new_transaction.amount, date=new_transaction.created_on.strftime('%B %d, %Y')),
            link="",
            status=0
        ) 
        #create notification
        new_notification.save()

        messages.success(request, "Transaction complete")
        return redirect("/transact/view/" + str(new_transaction.id))

    return HttpResponse(status = 400)

def transact_view(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    transaction = Transaction.objects.get(id=id)
    consumer = CustomUser.objects.get(id = transaction.user_id)
    invoices = Invoice.objects.filter(transaction=transaction)

    if not request.user.is_superuser and not request.user.id == consumer.id:
        return redirect("/")
    
    data = {
        'transaction':transaction,
        'consumer':consumer,
        'invoices': invoices,
        'page': 'consumers'
        
    }

    return render(request, "./base/collectible/transact_view.html", data)

def print_reciept(request, id):
    if not request.user.is_authenticated:
        return redirect("/")
    
    transaction = Transaction.objects.get(id=id)
    consumer = CustomUser.objects.get(id = transaction.user_id)
    invoices = Invoice.objects.filter(transaction=transaction)

    if not request.user.is_superuser and not request.user.id == consumer.id:
        return redirect("/")
    
    data = {
        'transaction':transaction,
        'consumer':consumer,
        'invoices': invoices
    }

    return render(request, "./base/print/print_reciept.html", data)

    
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
        .filter(
            reading__billing_month__lte=reading.billing_month,
            reading__user_id=consumer.id,
        )
        .exclude(status="paid")
        .aggregate(
            total_bill=Sum("amount") + Sum("penalty"),
            arrear_amount=(Sum("amount") + Sum("penalty"))
            - (collectible.amount + collectible.penalty),
            num_arrear=Count("reading__billing_month") - 1,
            start_month=Min("reading__billing_month"),
        )
    )

    data = {
        "collectible": collectible,
        "reading": reading,
        "consumer": consumer,
        "arrear": arrear,
    }
    return render(request, "./base/print/print_collectible.html", data)
