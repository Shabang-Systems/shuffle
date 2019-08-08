'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law
'''

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

@csrf_protect
def createaccount(request):
    template = loader.get_template('account/createaccount.html')
    return HttpResponse(template.render({}, request))

def createaccount_do(request):
    requestItem = request.POST
    user = authenticate(username=requestItem['username'], password=requestItem['password'])
    if user is None:
        user = get_user_model().objects.create_user(username=requestItem['username'], email=requestItem['email'], password=requestItem['password'], first_name=requestItem['firstname'], last_name=requestItem['lastname'])
        user.user_verified = False
        user.save()
        template = loader.get_template('account/createaccount_success.html')
    else:
        template = loader.get_template('account/createaccount_failed.html')
    return HttpResponse(template.render({}, request))

