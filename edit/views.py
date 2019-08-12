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
from django.views.decorators.csrf import csrf_protect
import json

from dbapi.models import Database, Word

@csrf_protect
def edit_view(request, database_id):
    template = loader.get_template('edit/edit.html')
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    database = Database.objects.get(pk=database_id)
    words = []
    for word in database.words.all():
        words.append([[word.term, word.definition], word.id])
    return HttpResponse(template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "words": words, "dbname": database.name, "dbdesc": database.description, "dbowner": database.owner.username, "dbid": database_id, "count": len(database.words.all())}, request))

def edit_do(request):
    data = request.POST.dict()
    if data:
        t = data["type"]
        db = Database.objects.get(pk=int(data["db-id"]))
        if t == "title-text":
            db.name = data["content"]
            db.save()
            return HttpResponse("success")
        elif t == "desc-text":
            db.description = data["content"]
            db.save()
            return HttpResponse("success")
        elif "word-name" in t:
            wid = t.split("-")[2]
            word = Word.objects.get(pk=wid)
            word.term = data["content"]
            word.save()
            return HttpResponse("success")
        elif "word-def" in t:
            wid = t.split("-")[2]
            word = Word.objects.get(pk=wid)
            word.definition = data["content"]
            word.save()
            return HttpResponse("success")
        elif "del" in t:
            word = Word.objects.get(pk=data["content"])
            word.delete()
            return HttpResponse("success")
        elif t == "new":
            if data["request"] == "word_id":
                w = Word(database=db)
                w.save()
                latest = Word.objects.latest('id').id
                responseObj = json.dumps({"status":"success", "id":latest})
                return HttpResponse(responseObj, content_type="application/json")

