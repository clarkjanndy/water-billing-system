from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


from base.models import (
    CustomUser,
    Collectible,
    PasswordResetRequest,
    Notification,
    Baranggay,
)


def init(request):
    if CustomUser.objects.all().exists():
        return HttpResponse(status=403)

    CustomUser.objects.create_user(
        first_name="Admin",
        middle_name="Admin",
        last_name="Admin",
        ext_name="Admin",
        username="admin",
        password="admin",
        is_superuser = 1
    )
    
    Baranggay.objects.create(name='Poblacion', code='POB')

    messages.info(request,'Database setup successful.')
    return redirect('/login')

# scan for due billings upon landing
def update_due_billings():
    due_billings = (
        Collectible.objects.select_related("reading")
        .filter(due_date__lt=date.today())
        .exclude(status="paid")
    )

    for due in due_billings:

        if not due.status == "due":
            due.penalty = 100
            due.status = "due"
            due.save()

            new_notification = Notification(
                user=CustomUser.objects.get(id=due.reading.user_id),
                content="You have been penalized 100 pesos for not paying your bill for the billing month of "
                + str(due.reading.billing_month.strftime("%B, %Y"))
                + " right on time.",
                link="/bills/" + str(due.id),
                status=0,
            )
            # create notification
            new_notification.save()


# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/consumers/" + str(request.user.id))

    update_due_billings()
    return render(request, "landing_page.html")


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/consumers/" + str(request.user.id))

    message = ""
    username = ""
    password = ""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect("/admin")
            else:
                return redirect("/consumers/" + str(user.id))
        else:
            message = "Invalid username and/or password"

    return render(
        request,
        "login.html",
        {"message": message, "username": username, "password": password},
    )


def change_password(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        me = CustomUser.objects.get(id=request.user.id)
        me.set_password(request.POST["newpassword"])
        me.save()

        messages.success(request, "Your password had been changed")

    return redirect("/admin")


def send_reset_request(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        user = CustomUser.objects.get(username=request.POST["reset_username"])

        password_reset_request = PasswordResetRequest()
        password_reset_request.user = user
        password_reset_request.message = request.POST["reset_message"]
        password_reset_request.status = "pending"
        password_reset_request.save()

    messages.success(
        request,
        "Password reset request succesfully sent. You can log in using the default password as soon as the admin approve the request.",
    )
    return redirect("/login")


def logout(request):
    auth_logout(request)
    return redirect("login")
