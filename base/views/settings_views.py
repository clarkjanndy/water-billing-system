from datetime import datetime
from django.shortcuts import redirect, render

from base.models import Setting

from django.contrib import messages


def formatdate(date, format):
    return datetime.strptime(date, format)

# Create your views here.
def add_setting(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        setting = Setting.objects.create(
            variable=request.POST["variable"].upper(),
            name=request.POST["name"],
            value=request.POST["value"],
            created_by=request.user
        )
       
        messages.success(request, "Setting added successfully")
        return redirect("/admin/settings")


def edit_reading(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect("/")

    if not request.user.is_superuser:
        return redirect("/")
    
    if request.method == "POST":
        setting = Setting.objects.filter(id=request.POST["id"])
        
        setting.update(
            variable=request.POST["variable"],
            name=request.POST["name"],
            value=request.POST["value"],
        )
       
        messages.success(request, "Setting updated successfully")
        return redirect("/admin/settings")
