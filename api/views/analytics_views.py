from django.db.models import Sum, Count
from django.http import JsonResponse

from base.models import Collectible, Reading, Baranggay, CustomUser, Notification, Transaction

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

# transaction history
def transaction_history_count(request):
    queryset = (
        Transaction.objects.all()
        .aggregate(count=Count("id"))
    )
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


def consumption_get(request, id):
    queryset = Reading.objects.filter(user=id).aggregate(Sum("consumption"))
    return JsonResponse(queryset, safe=True)


def consumption_history_get(request, id):
    readings = Reading.objects.filter(user=id).order_by("billing_month")

    series = [reading.consumption for reading in readings.iterator()]
    x_label = [reading.billing_month for reading in readings.iterator()]

    data = {"series": series, "x_label": x_label}
    return JsonResponse(data, safe=True)


# bills/collectibles
def bills_paid_all(request):
    queryset = (    
        Collectible.objects.select_related("reading")
        .filter(status="paid")
        .aggregate(amount__sum=Sum("amount") + Sum("penalty"))
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
