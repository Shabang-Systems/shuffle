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

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json

from dbapi.models import Database, Word, LevelDesc

@csrf_protect
@login_required(login_url='/login')
def edit_view(request, database_id):
    template = loader.get_template('edit/edit.html')
    panic_template = loader.get_template('edit/error.html')
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    if database_id == "new":
        database = Database(name="Untitled Database", description="", owner=request.user)
        database.save()
        LevelDesc(db=database, user=request.user, points=0, mastered=0).save()
        database_id = database.id
        return redirect("/edit/"+str(database_id))
    else:
        database = Database.objects.get(pk=int(database_id))
    if request.user != database.owner:
        return HttpResponse(panic_template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext}, request))
    words = []
    for word in database.words.all():
        words.append([[word.term, word.definition], word.id])
    return HttpResponse(template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "words": words, "dbname": database.name, "dbdesc": database.description, "dbowner": database.owner.username, "dbid": database_id, "count": len(database.words.all())}, request))


@login_required(login_url='/login')
def delete_do(request, database_id):
    db = Database.objects.get(pk=database_id)
    ld = LevelDesc.objects.filter(db=db)
    ld.filter(user=request.user).delete()
    if len(ld) < 1:
        db.delete()
    return redirect("/")

@login_required(login_url='/login')
def edit_do(request):
    data = request.POST.dict()
    if data:
        t = data["type"]
        db = Database.objects.get(pk=int(data["db-id"]))
        if request.user != db.owner:
            return HttpResponse(json.dumps({"status":"error", "detail":"permission denied"}), content_type="application/json")
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
            elif data["request"] == "word_full":
                w = Word(database=db)
                w.term = data["term"]
                w.definition = data["definition"]
                w.save()
                latest = Word.objects.latest('id').id
                responseObj = json.dumps({"status":"success", "id":latest})
                return HttpResponse(responseObj, content_type="application/json")
    return HttpResponse(json.dumps({"result":"bad_request", "action":"invalid_api_request"}), content_type="application/json")

