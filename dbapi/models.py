# pylint: disable=maybe-no-member

'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law
'''

from django.db import models
from account.models import User
from datetime import datetime

class Folder(models.Model):
    name = models.CharField(max_length=255, default="", help_text='Name')
    description = models.TextField(default="", help_text='Description')
    owner = models.ForeignKey(User, null=True, on_delete="CASCADE", related_name='folders')

    def __str__(self):
        return self.name+" ("+str(self.id)+")"

class Database(models.Model):
    name = models.CharField(max_length=255, default="", help_text='Name')
    description = models.TextField(default="", help_text='Description')
    owner = models.ForeignKey(User, null=True, on_delete="CASCADE", related_name='databases')
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete="SET_NULL", related_name='databases')

    def __str__(self):
        return self.name+" ("+str(self.id)+")"

class Word(models.Model):
    term = models.TextField(default="", help_text='Term')
    definition = models.TextField(default="", help_text='Definition')
    image_url = models.CharField(max_length=500, null=True, blank=True, help_text='Image URL')
    database = models.ForeignKey(Database, null=True, on_delete="CASCADE", related_name='words')

    def __str__(self):
        return self.term

class LevelDesc(models.Model):
    db = models.ForeignKey(Database, null=True, on_delete="CASCADE", related_name='user_levels')
    user = models.ForeignKey(User, null=True, on_delete="CASCADE", related_name='user_levels')
    points = models.IntegerField(null=False, default=0)
    mastered = models.IntegerField(null=False, default=0)
    lastAccess = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def __str__(self):
        return "UL "+self.user.username+" | "+str(self.db.id)
