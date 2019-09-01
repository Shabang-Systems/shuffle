'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@csrf_protect
def createaccount(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        template = loader.get_template('account/createaccount.html')
        return HttpResponse(template.render({"regstatus":"new"}, request))

def createaccount_do(request):
    requestItem = request.POST
    user = authenticate(username=requestItem['username'], password=requestItem['password'])
    if user is None:
        user = get_user_model().objects.create_user(username=requestItem['username'], email=requestItem['email'], password=requestItem['password'], first_name=requestItem['firstname'], last_name=requestItem['lastname'])
        user.user_verified = False
        user.save()
        template = loader.get_template('account/createaccount_success.html')
        return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('account/createaccount.html')
        return HttpResponse(template.render({"regstatus":"failed-nameexist", "uname":requestItem['username']}, request))

@csrf_protect
def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        template = loader.get_template('account/login.html')
        return HttpResponse(template.render({"authstatus":"new"}, request))

def signin_do(request):
    template = loader.get_template('account/login.html')
    requestItem = request.POST
    user = authenticate(username=requestItem['username'], password=requestItem['password'])
    if user is None:
        template = loader.get_template('account/login.html')
        return HttpResponse(template.render({"authstatus":"invalid"}, request))
    else:
        login(request, user)
        return redirect('/')

@login_required(login_url='/login')
def signout(request):
    logout(request)
    return redirect('/')

