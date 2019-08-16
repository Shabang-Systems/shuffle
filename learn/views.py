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
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from dbapi.models import Database, LevelDesc, WordProgress, Word
from datetime import datetime, timedelta
import json

def acquireSet(request, db_pk, **kwargs):
    user_id = request.user.id
    wprogresses = WordProgress.objects.all().filter(user_id=user_id).filter(db_id=db_pk)
    wordSet = []
    next_shuffle = datetime.today().date()+timedelta(7)
    if len(wprogresses) > 0:
        for progress in wprogresses:
            if progress.isActive:
                if progress.shuffleCount > 0:
                    shuffle_date = progress.lastShuffle.date()+timedelta(progress.shuffleCount*7)
                else:
                    shuffle_date = progress.lastShuffle.date()+timedelta(7)
                if shuffle_date < (datetime.today()).date():
                    if not kwargs.get("test_request"):
                        return {"status": "error", "response": "shuffle_required", "instruction": "redirect to /learn/t page to shuffle"}
                    else:
                        if progress.word.definition.strip() is not "":
                            wordSet.append(progress.word)
                else:
                    if kwargs.get("test_request"):
                        if shuffle_date-timedelta(2) > (datetime.today()).date():
                            continue
                    if shuffle_date <= (datetime.today()).date()+timedelta(7):
                        if progress.word.definition.strip() is not "":
                            wordSet.append(progress.word)
                        if next_shuffle > shuffle_date:
                            next_shuffle = shuffle_date

    else:
        if "init" in kwargs:
            counter = 0
            db = Database.objects.get(pk=db_pk)
            words = db.words.all()
            size = int(kwargs["init"])
            if size > len(words):
                size = len(words)
            for _ in range(size):
                wp = WordProgress()
                wp.db = db
                wp.user = request.user
                wp.isActive = True
                wp.lastShuffle = datetime.today()
                try:
                    wp.word = words[counter]
                    wp.save()   
                    if words[counter].definition.strip() is not "":
                        if not kwargs.get("test_request"):
                            wordSet.append(words[counter])
                    if next_shuffle > wp.lastShuffle.date()+timedelta(7):
                        next_shuffle = wp.lastShuffle.date()+timedelta(7)
                except IndexError:
                    break
                counter += 1
            while counter <= len(words)-1:
                wp = WordProgress()
                wp.db = db
                wp.user = request.user
                wp.isActive = False
                wp.word = words[counter]
                wp.save()
                counter += 1
        else:
            return {"status": "error", "response": "no_progress", "instruction": "supply a 'init' parameter with initialization size"}
    
    return {"status": "success", "response": wordSet, "body": {"due": next_shuffle}}


# Create your views here.
@csrf_protect
@login_required(login_url='/login')
def learn_view(request, database_id):
    template = loader.get_template('learn/learn.html')
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    database = Database.objects.get(pk=database_id)
    words = []
    for word in database.words.all():
        words.append([word.term, word.definition])
    ls = request.user.user_levels.all().filter(db_id=database_id)
    if len(ls) == 0:
        levelSpec = LevelDesc(db=database, user=request.user, points=0, mastered=0)
    else:
        levelSpec = ls[0]
    levelSpec.lastAccess = datetime.today()
    levelSpec.save()
    owned = []
    databases = request.user.user_levels.all().order_by("-lastAccess")
    for i in databases:
        if i.db.owner == request.user:
            owned.append([i.db.name, i.db.description, i.db.owner.username, i.points, i.db.id])
    autoset_response = acquireSet(request, database_id, init=request.user.setCount)
    if autoset_response["status"] == "error":
        if autoset_response["response"] == "shuffle_required":
            return redirect('/learn/t/'+str(database_id))
    as_words = []
    copy_string = ""
    if autoset_response['status'] == 'success':
        autoSet = autoset_response['response']
        for word in autoSet:
            as_words.append([word.term, word.definition])
            copy_string = copy_string+word.term+"\t"+word.definition+"\n"
        due = autoset_response["body"]["due"]
    
    days = due.day-datetime.today().day
    
    return HttpResponse(template.render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "words": as_words, "dbname": database.name, "dbdesc": database.description, "dbowner": database.owner.username, "dbid": database_id, "dbPoints": levelSpec.points, "mastered":  levelSpec.mastered, "count": len(database.words.all()), "owned": owned, "due":due, "days_to_learn":days, "cp_str":copy_string}, request))

@login_required(login_url='/login')
def level_up_do(request):
    data = request.POST.dict()
    if data:
        words = acquireSet(request, data["dbid"], test_request=True)["response"]
        term_id = data["word-id"]
        answer_supplied = data["answer"]
        current_word = Word.objects.get(pk=term_id)
        if current_word.definition.lower().strip() == answer_supplied.lower().strip():
            index = words.index(current_word)
            prog = WordProgress.objects.all().filter(user=request.user).filter(word=current_word)[0]
            sc = prog.shuffleCount
            prog.shuffleCount = sc+1
            prog.lastShuffle = datetime.today().date() + timedelta(7*sc)
            lvSpec = LevelDesc.objects.all().filter(user=request.user).filter(db_id=data["dbid"])[0]
            pts_award = (9999/len(current_word.database.words.all()))/4
            print("Awarded", pts_award, "points.")
            lvSpec.points = lvSpec.points+pts_award
            request.user.points = request.user.points+pts_award
            request.user.save()
            if sc+1 == 4:
                lvSpec.mastered = lvSpec.mastered+1
                prog.isActive = False
            elif sc+1 == 1:
                try:
                    newProgs = WordProgress.objects.all().filter(user=request.user).filter(isActive=False)[0]
                    newProgs.isActive = True
                    newProgs.lastShuffle = datetime.today()
                    newProgs.save()
                except IndexError:
                    pass
            prog.save()
            lvSpec.save()
            if index == len(words)-1:
                return HttpResponse(json.dumps({"result":"success", "action":"done"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"result":"success", "action":"next", "term": words[index+1].term, "termid": words[index+1].id}), content_type="application/json")
        else:
            index = words.index(current_word)
            prog = WordProgress.objects.all().filter(user=request.user).filter(word=current_word)[0]
            prog.shuffleCount = 0
            prog.lastShuffle = datetime.today().date()
            lvSpec = LevelDesc.objects.all().filter(user=request.user).filter(db_id=data["dbid"])[0]
            pts_dec = (9999/len(current_word.database.words.all()))/4
            print("Penalized", pts_dec, "points.")
            lvSpec.points = lvSpec.points-pts_dec
            prog.save()
            lvSpec.save()
            if index == len(words)-1:
                return HttpResponse(json.dumps({"result":"failed", "action":"done"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"result":"failed", "action":"next", "term": words[index+1].term, "termid": words[index+1].id}), content_type="application/json")
    return HttpResponse(json.dumps({"result":"bad_request", "action":"invalid_api_request"}), content_type="application/json")
    
@csrf_protect
@login_required(login_url='/login')
def level_up_view(request, database_id):
    words = acquireSet(request, database_id, test_request=True, init=request.user.setCount)["response"]
    folders = request.user.folders.all()
    folderContext = []
    for folder in folders:
        folderContext.append([folder.id, folder.name])
    databases = request.user.user_levels.all().order_by("-lastAccess")
    owned = []
    for database in databases:
        if database.db.owner == request.user:
            owned.append([database.db.name, database.db.description, database.db.owner.username, database.points, database.db.id])
    if len(words) == 0:
        return HttpResponse(loader.get_template('learn/levelup_no.html').render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "owned": owned, "dbid":database_id}, request))
    return HttpResponse(loader.get_template('learn/levelup.html').render({"username": request.user.username, "firstname": request.user.first_name, "points": request.user.points, "folders": folderContext, "owned": owned, "firstterm": words[0].term, "firstid": words[0].id, "dbid":database_id, "testsize": len(words)}, request))

def cards_view(request, database_id):
        return HttpResponse("So... Here's the deal. This _WAS_ a prerelease feature, but.... Well.... We screwed up. BEFORE ALPHA TESTING! THIS WILL BE IMPLIMENTED THEN. OK? You happy?")
