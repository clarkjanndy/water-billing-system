from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from base.models import CustomUser
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

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        me = CustomUser.objects.get(id=request.user.id)
        me.set_password(request.POST['newpassword'])
        me.save()

        messages.success(request, "Your password had been changed")
    
    return redirect("/admin")



def logout(request):
    auth_logout(request)
    return redirect('login')
