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
    path('do_edit/', views.edit_do, name="edit_do"),
    path('do_add/', views.edit_do, name="edit_apply"),
    path('delete/<int:database_id>/', views.delete_do, name="delete_do"),
    path('<slug:database_id>/', views.edit_view, name="edit_view"),
]