from django.http import HttpResponse
import json

from base.models import CustomUser, Notification

from django.contrib import messages


def make_admin(request):
    data = json.loads(request.body)
    user = CustomUser.objects.get(id=data['id'])

    role = [1,0]
    if request.method == "PUT":
        user.is_superuser = role[user.is_superuser]
        user.save()

        messages.success(request, "Role updated successfully.")

    return HttpResponse(status=200)

def read_notification(request):
    data = json.loads(request.body)
    notification = Notification.objects.get(id=data['id'])

    if request.method == "PUT":
        notification.status = 1
        notification.save()

    return HttpResponse(status=200)

def notification_mark_all_as_read(request):
    data = json.loads(request.body)
    notifications = Notification.objects.filter(user_id=data['id'])
    

    if request.method == "PUT":
        for notif in notifications:
            notif.status = 1
            notif.save()

    return HttpResponse(status=200)

def notification_delete_all(request):
    data = json.loads(request.body)
    
    if request.method == "DELETE":
        Notification.objects.filter(user_id=data['id']).delete()

    return HttpResponse(status=200)

