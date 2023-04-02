from django.db.models import Sum, Count
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models.functions import TruncMonth, TruncYear, TruncDate

from datetime import date, datetime

from base.models import (
    Collectible,
    Reading,
    Baranggay,
    CustomUser,
    Notification,
    Transaction,
    PasswordResetRequest,
    Projection
)

# consumer
def consumer_count(request):
    queryset = (
        CustomUser.objects.all().filter(is_superuser=0).aggregate(count=Count("id"))
    )
    return JsonResponse(queryset, safe=True)


# barangay
def barangay_count(request):
    queryset = Baranggay.objects.all().aggregate(count=Count("id"))
    return JsonResponse(queryset, safe=True)


# admin
def admin_count(request):
    queryset = (
        CustomUser.objects.all().filter(is_superuser=1).aggregate(count=Count("id"))
    )
    return JsonResponse(queryset, safe=True)

#password reset requests
def password_reset_request_count(request):
    queryset = (
        PasswordResetRequest.objects.exclude(status='approved').aggregate(count=Count("id"))
    )
    return JsonResponse(queryset, safe=True)


# transaction history
def transaction_history_count(request):
    queryset = Transaction.objects.all().aggregate(count=Count("id"))
    return JsonResponse(queryset, safe=True)


# notification
def notification_unseen_get(request, id):
    queryset = (
        Notification.objects.all()
        .filter(user_id=id)
        .exclude(status=1)
        .aggregate(count=Count("id"))
    )
    return JsonResponse(queryset, safe=True)


# consumption
def consumption_all(request):
    queryset = Reading.objects.all().aggregate(Sum("consumption"))
    return JsonResponse(queryset, safe=True)


def consumption_all_by_month(request):
    queryset = (
        Reading.objects.all()
        .filter(billing_month__month=date.today().month)
        .aggregate(Sum("consumption"))
    )
    return JsonResponse(queryset, safe=True)


def consumption_get(request, id):
    queryset = Reading.objects.filter(user=id).aggregate(Sum("consumption"))
    return JsonResponse(queryset, safe=True)


def consumption_history_get(request, id):
    readings = Reading.objects.filter(user=id).order_by("billing_month")

    series = [reading.consumption for reading in readings.iterator()]
    x_label = [reading.billing_month for reading in readings.iterator()]

    data = {"series": series, "x_label": x_label}
    return JsonResponse(data, safe=True)


def consumption_history_all(request):
    readings = (
        Reading.objects.values("billing_month")
        .annotate(
            month=Count("billing_month", distinct=True), consumption=Sum("consumption")
        )
        .order_by("billing_month")
    )


    series = [reading["consumption"] for reading in readings.iterator()]
    x_label = [reading["billing_month"] for reading in readings.iterator()]

    data = {"series": series, "x_label": x_label}
    return JsonResponse(data, safe=True)

def consumption_pie_chart(request):
    released_water = Projection.objects.aggregate(released_water = Sum('released_water')).get('released_water')
    consumed_water = Reading.objects.aggregate(consumed_water = Sum('consumption')).get('consumed_water')
    water_loss = 0 if released_water - consumed_water < 0 else released_water - consumed_water
    
    data = {'released_water': released_water,
            "consumed_water": consumed_water,
            'water_loss': water_loss}
    return JsonResponse(data, safe=True)



# bills/collectibles
def bills_paid_all(request):
    queryset = (
        Collectible.objects.select_related("reading")
        .filter(status="paid")
        .aggregate(amount__sum=Sum("amount") + Sum("penalty"))
    )

    return JsonResponse(queryset, safe=True)

# bills/collectibles
def bills_paid_all(request):
    queryset = (
        Collectible.objects.select_related("reading")
        .filter(status="paid")
        .aggregate(amount__sum=Sum("amount") + Sum("penalty"))
    )

    return JsonResponse(queryset, safe=True)


def bills_paid_all_by_month(request):
    queryset = (
        Transaction.objects.all()
        .filter(created_on__month=date.today().month)
        .aggregate(amount__sum=Sum("amount"))
    )   
    return JsonResponse(queryset, safe=True)


def bills_unpaid_all(request):
    queryset = (
        Collectible.objects.select_related("reading")
        .exclude(status="paid")
        .aggregate(amount__sum=Sum("amount") + Sum("penalty"))
    )
    return JsonResponse(queryset, safe=True)


def bills_unpaid_get(request, id):
    queryset = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id)
        .exclude(status="paid")
        .aggregate(amount__sum=Sum("amount") + Sum("penalty"))
    )
    return JsonResponse(queryset, safe=True)


def bills_paid_vs_unpaid_get(request, id):
    paid = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id, status="paid")
        .aggregate(paid_sum=Sum("amount") + Sum("penalty"))
    )

    unpaid = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id)
        .exclude(status="paid")
        .aggregate(unpaid_sum=Sum("amount") + Sum("penalty"))
    )

    data = {"paid": paid["paid_sum"], "unpaid": unpaid["unpaid_sum"]}
    return JsonResponse(data, safe=False)

def collection_histogram(request):
    transaction = (
        Transaction.objects
        .annotate(
            month=TruncMonth('created_on__date')
        )
        .values('month')
        .annotate(count = Count('id'), total=Sum('amount'))
        .order_by("created_on__month")
    )
    
    series = [transaction["total"] for transaction in transaction.iterator()]
    x_label = [transaction["month"] for transaction in transaction.iterator()]

    data = {"series": series, "x_label": x_label}

    return JsonResponse(data, safe=True)

def collection_radial(request):
    
    projected_income = Projection.objects.aggregate(projected_income = Sum('expected_income')).get('projected_income')
    total_collection = Transaction.objects.aggregate(total_collection = Sum('amount')).get('total_collection')
    percentage = round((total_collection / projected_income)  * 100, 2)
    
    data = {'projected_income': projected_income,
            "total_collection": total_collection,
            'percentage': percentage}

    return JsonResponse(data, safe=True)
