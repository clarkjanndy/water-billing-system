from urllib import response
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password

from django.http import HttpResponse
import json

from base.models import CustomUser, Reading


def make_admin(request):
    data = json.loads(request.body)
    user = CustomUser.objects.get(id=data['id'])
    if request.method == "PUT":
        user.is_superuser = data['superuser']
        user.save()

    return HttpResponse(status=200)
