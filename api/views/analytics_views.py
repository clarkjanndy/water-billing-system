from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect

from base.models import Collectible, Reading

# consumption
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
def bills_unpaid_get(request, id):
    queryset = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id, status="unpaid")
        .aggregate(amount__sum = Sum("amount") + Sum("penalty"))
    )
    return JsonResponse(queryset, safe=True)


def bills_paid_vs_unpaid_get(request, id):
    paid = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id, status="paid")
        .aggregate(paid_sum=Sum("amount")+Sum('penalty'))
    )
    unpaid = (
        Collectible.objects.select_related("reading")
        .filter(reading__user_id=id, status="unpaid")
        .aggregate(unpaid_sum=Sum("amount")+Sum('penalty'))
    )

    data = {"paid": paid["paid_sum"], "unpaid": unpaid["unpaid_sum"]}
    return JsonResponse(data, safe=False)
