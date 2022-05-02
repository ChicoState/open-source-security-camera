from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from user.forms import JoinForm

from django.contrib.auth import get_user_model
User = get_user_model()

from userconfig.models import CustomUser

# Create your views here.
def join(request):

    if (request.method == "GET"):

        numUser = CustomUser.objects.count()
        if numUser >= 1:
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if (request.method == "POST"):

        numUser = CustomUser.objects.count()
        if numUser < 1:

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
                page_data = {"join_form": join_form}
                return render(request, 'registration/join.html', page_data)

        else:
            redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'registration/join.html', page_data)


@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/login/")
