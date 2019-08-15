from django.contrib import admin

from django.contrib import admin
from .models import Database, Word, Folder, LevelDesc, WordProgress

admin.site.register(Database)
admin.site.register(Word)
admin.site.register(Folder)
admin.site.register(LevelDesc)
admin.site.register(WordProgress)
