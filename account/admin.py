'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law
'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User

class UChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUAdmin(UserAdmin):
    form = UChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (('Shuffle Status'), {'fields': ('verified', 'points')}),
        (('Shuffle Preferences'), {'fields': ('setCount', )}),
    )


admin.site.register(User, CustomUAdmin)