# pylint: disable=maybe-no-member

'''
Bada Bing, Bada Boom
The thoughts, ideas, and opinions both spoken and internalized
are the forces, that traverse all platforms, all standards
and all norms to form their unique class, unique style, and a
unique kind of ideology that future generations will look up to.
We are #!/Shabang. (c) 2019/2020 Shabang Systems, LLC. All rights reserved
unless explicitly stated otherwise or where it is prohibited by law */
'''

from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from dbapi.models import Database

@csrf_protect
@login_required(login_url='/login')
def index(request):
    template = loader.get_template('home/index.html')
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    databases = request.user.user_levels.all().order_by("-lastAccess")
    today = []
    yesterday = []
    thisweek = []
    older = []
    owned = []
    for database in databases:
        if database.lastAccess.date() >= datetime.today().date():
            today.append([database.db.name, database.db.description, database.db.owner.username, database.points, database.db.id])
        elif database.lastAccess.date() == (datetime.today()- timedelta(1)).date():
            yesterday.append([database.db.name, database.db.description, database.db.owner.username, database.points, database.db.id])
        elif database.lastAccess.date() >= (datetime.today()- timedelta(7)).date() and database.lastAccess.date() <= (datetime.today()- timedelta(1)).date():
            thisweek.append([database.db.name, database.db.description, database.db.owner.username, database.points, database.db.id])
        else:
            older.append([database.db.name, database.db.description, database.db.owner.username,database.points, database.db.id])
    for database in databases:
        if database.db.owner == request.user:
            owned.append([database.db.name, database.db.description, database.db.owner.username, database.points, database.db.id])
    return HttpResponse(template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "databases": [today, yesterday, thisweek, older], "owned": owned}, request))
