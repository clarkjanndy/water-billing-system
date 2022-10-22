from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

def landing_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/consumers/" + str(request.user.id))

    return render(request, 'landing_page.html')

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/consumers/" + str(request.user.id))

    message = ''
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect("/admin")
            else:
                return redirect("/consumers/" + str(user.id))
        else:
            message = "Invalid username and/or password"

    return render(request, 'login.html', {'message': message, 'username': username, 'password': password})


def logout(request):
    auth_logout(request)
    return redirect('login')
