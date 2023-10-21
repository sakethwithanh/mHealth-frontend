from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
def HomePage(request):
    return render(request,'home.html')
def SignupPage(request):
    error_message = None  # Initialize error_message to None

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if the username is already in use
        if User.objects.filter(username=uname).exists():
            error_message = 'This username is already taken. Please choose a different one.'
        else:
            # Use EmailValidator to validate the email
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except ValidationError:
                error_message = 'Invalid email address'
            
            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                error_message = 'This email is already registered.'

            # Check if passwords match and are at least 8 characters long
            if pass1 != pass2:
                error_message = 'Passwords do not match.'
            elif len(pass1) < 8:
                error_message = 'Password must be at least 8 characters long.'

            if error_message is None:  # No error, create the user
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                return redirect('login')

    return render(request, 'signup.html', {'error_message': error_message})



def LoginPage(request):
    error_message = ''  # Initialize error_message to an empty string

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Username or password is incorrect'

    return render(request, 'login.html', {'error_message': error_message})

def LogoutPage(request):
    logout(request)
    return redirect('login')
