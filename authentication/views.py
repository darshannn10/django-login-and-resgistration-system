from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from login import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, 'username already exist! try another username')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, 'email already exists! please use another email address')
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, 'username should be under 10 characters')

        if pass1 != pass2:
            messages.error(request, 'passwords do not match')

        if not username.isalnum():
            messages.error(request, 'username must be Alpha-numeric')
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account")
        
        #Welcom E-mail
        subject = "Welcome to Authenticator"
        message = "Hello " + myuser.first_name + "! \n" + "We're glad to have you her \n Thank you for joining us \n We have sent you a confirmation email, Please confirm you email to avail our benefits"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        
        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(request, username=username, password=pass1)


        if user is not None:
            login(request,user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')