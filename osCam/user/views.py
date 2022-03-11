from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def join(request):
    return render(request, 'user/join.html')

def login(request):
    return render(request, 'user/login.html')