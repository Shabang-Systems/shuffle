from django.contrib import admin

from django.contrib import admin
from .models import Database, Word, Folder, LevelDesc

admin.site.register(Database)
admin.site.register(Word)
admin.site.register(Folder)
admin.site.register(LevelDesc)
