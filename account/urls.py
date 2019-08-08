'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law */
'''

from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.createaccount, name="account"),
    path('new', views.createaccount, name="createaccount"),
    path('go', views.createaccount_do, name="createaccount_do"),
    path('login', views.signin, name="login"),
    path('auth', views.signin_do, name="login_do")
]