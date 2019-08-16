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
    path('l/<int:database_id>/', views.learn_view, name="learn_view"),
    path('t/<int:database_id>/', views.level_up_view, name="level_up_view"),
    path('do_t/', views.level_up_do, name="level_up_do"),
    path('cards/<int:database_id>/', views.cards_view, name="learn_cards_view"),
]
