from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.forms import JoinForm
from django.conf import settings
from django.core.mail import send_mail
import time

# Create your views here.
def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'registration/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'registration/join.html', page_data)

@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/login/")

def send_email(request):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file = open("./videos/tmp.txt","r")
    numVideos = 0

    # Reading from file
    content = file.read()
    contentList = content.split("\n")

    for i in contentList:
        if i:
            numVideos += 1

    subject = 'Home Security Camera Notifications'
    message = 'Hello ' + str(request.user.username) + \
                       ',\n\nMotion was detected ' + \
                       str(numVideos) + ' times.'

    # send an send_email
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[settings.RECIPIENT_ADDRESS])

    return redirect("/")
    #return HttpResponse(html)
