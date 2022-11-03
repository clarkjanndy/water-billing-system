from django.shortcuts import render
from django.shortcuts import redirect

from base.models import  CustomUser, Notification, Transaction

# Create your views here.
def get_notifications(request):
    if not request.user.is_authenticated:
        return redirect("/")

    consumer = CustomUser.objects.get(id=request.user.id)
    notifications = Notification.objects.all().filter(user_id=consumer.id).order_by( 'status', '-created_on',)

    data = {
        "consumer": consumer,
        "notifications": notifications
    }

    return render(request, "./base/consumer/notifications.html", data)

def get_transaction_history(request):
    if not request.user.is_authenticated:
        return redirect("/")

    consumer = CustomUser.objects.get(id=request.user.id)
    transactions = Transaction.objects.all().filter(user_id=consumer.id).order_by('-created_on',)

    data = {
        "consumer": consumer,
        "transactions": transactions
    }

    return render(request, "./base/consumer/transaction-history.html", data)