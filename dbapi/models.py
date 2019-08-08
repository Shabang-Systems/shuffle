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

class Database(models.Model):
    name = models.CharField(max_length=50, default="", help_text='Name')
    description = models.CharField(max_length=50, null=True, blank=True, help_text='Description')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete="SET_NULL", related_name='databases')

    def __str__(self):
        return self.name+" ("+str(self.id)+")"

class Word(models.Model):
    term = models.CharField(max_length=100, default="", help_text='Term')
    definition = models.CharField(max_length=100, default="", help_text='Definition')
    image_url = models.CharField(max_length=500, null=True, blank=True, help_text='Image URL')
    database = models.ForeignKey(Database, null=True, blank=True, on_delete="CASCADE", related_name='words')

    def __str__(self):
        return self.term
