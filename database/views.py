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

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from dbapi.models import Database


def database_view(request, database_id):
    template = loader.get_template('database/db.html')
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    database = Database.objects.get(pk=database_id)
    words = []
    for word in database.words.all():
        words.append([word.term, word.definition])
    levelSpec = request.user.user_levels.all().filter(db_id=database_id)[0]
    return HttpResponse(template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "words": words, "dbname": database.name, "dbdesc": database.description, "dbowner": database.owner.username, "dbid": database_id, "dbPoints": levelSpec.points, "mastered":  levelSpec.mastered, "count": len(database.words.all())}, request))
