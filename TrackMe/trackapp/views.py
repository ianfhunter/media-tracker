from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Trackable,Review,Tag,Background,User,Status,ProgressStatus
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import urllib,urllib2
import json
import hashlib, uuid

def createHash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()

def home(request):
    imgs = Background.objects.order_by('?')
    if not imgs:
        imgs = Background(obj="background/default_background.jpg")
        imgs.save()
        imgs = [imgs]
    users = User.objects.order_by('id')
    d = {}
    d["image"] = imgs[0]

    if len(users) > 0:
        d["user"] = users[0]

    return render_to_response('home.html', d)

def search(request):
    #Should be passing the type of media so we can do different api calls
    query = request.GET.get('q')

    #Search for Items using OpenMovie DB API
    response = urllib2.urlopen('http://www.omdbapi.com/?s=' + query.replace(' ','+'))
    data = json.load(response)   

    results = []
    for item in data['Search']:
        results.append(Trackable(name=item['Title'],id=item['imdbID']))

    if len(results) > 0:
        d = {"results": results}
    else:
        d = {}
    return render_to_response('search.html', d)

def item(request,value):

    response = urllib2.urlopen("http://www.omdbapi.com/?i=" + value + "&tomatoes=true")
    data = json.load(response)   
    print data
    try:
        rating = float(data["tomatoRating"])
    except ValueError:
        rating = 0

    item = Trackable(id=int(value[2:]),
                    name=data["Title"],
                    amount=10,
                    average_num_stars=rating,
                    item_type="TV Show",
                    description=data["Plot"],
                    director=data["Director"],
                    production=data["Production"],
                    runtime=int(''.join(i for i in data["Runtime"] if i.isdigit()))
                    )
    # item = Trackable.objects.get(pk=int(value))
    # reviews = Review.objects.filter(review_of=item)
    # tags = Tag.objects.filter(items=item)
    
    tags = []
    for genre in data["Genre"].split(","):
        tags.append(Tag(name=genre))
    reviews = [Review(author="Rotten Tomatoes",contents=data["tomatoConsensus"])]

    user = User.objects.order_by('id')
    if user:
        user = user[0]
    else:
        user = None


    #scrape Google Images for cover
    if not item.cover_photo:   
        print item.name
        data = json.load(urllib2.urlopen('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+urllib.quote(item.name.encode("utf8"))))
        if data and data["responseData"] and data["responseData"]["results"]:
            print "yes"
            urllib.urlretrieve(data["responseData"]["results"][0]["url"], "documents/covers/"+str(item.id) + ".jpg")
            item.cover_photo = "covers/"+str(item.id)+".jpg"
            item.release_date = "2014-02-04"    #Why is this here? :o
            item.save()
        else:
            print "no"
            #Default image to be assigned here

    d = {
        "item": item,
        "reviews": reviews,
        "tags":tags
    }
    if(user):
        status = Status.objects.filter(who=user,what=item)
        if status:
            d["status"] = status[0]
        d["user"] = user
    return render_to_response('item.html', d)

def user(request,value):
    user = User.objects.get(pk=int(value))
    statuses = Status.objects.filter(who=user)

    d = {
            "user":user,
            "statuses":statuses
        }
    return render_to_response('user.html',d)

@csrf_exempt
def login(request):
    print request.POST["username"]

    user = User(username=request.POST['username'], password=createHash(request.POST['password']),email=request.POST['email'])
    user.save()
    return redirect('/home')

@csrf_exempt
def status_update(request,value):
    everything_ok = True
    if not "user_id" in request.POST or not "type" in request.POST or not "episode" in request.POST:
        #noone is logged in
        everything_ok = False
    else:
        status = Status.objects.filter(what=value,who=request.POST["user_id"])
        if status.count() == 0:
            #create new status
            active_user = User.objects.get(pk=request.POST["user_id"])
            active_item = Trackable.objects.get(pk=value)
            active_type = request.POST["type"]
            StatusEnum = ProgressStatus.NOT_STARTED

            if active_type == "watching":
                StatusEnum = ProgressStatus.IN_PROGRESS
            if active_type == "watched":
                StatusEnum = ProgressStatus.FINISHED
            if active_type == "towatch":
                StatusEnum = ProgressStatus.WISHLIST
            if active_type == "dropped":
                StatusEnum = ProgressStatus.DROPPED
            if active_type == "avoid":
               StatusEnum = ProgressStatus.AVOID

            status = Status(who=active_user, what=active_item,progress=StatusEnum,amount=int(request.POST["episode"]))
            status.save()
        else:
            #we have a status for this already
            active_user = User.objects.get(pk=request.POST["user_id"])
            active_item = Trackable.objects.get(pk=value)
            active_type = request.POST["type"]
            StatusEnum = ProgressStatus.NOT_STARTED

            if active_type == "watching":
                StatusEnum = ProgressStatus.IN_PROGRESS
            if active_type == "watched":
                StatusEnum = ProgressStatus.FINISHED
            if active_type == "towatch":
                StatusEnum = ProgressStatus.WISHLIST
            if active_type == "dropped":
                StatusEnum = ProgressStatus.DROPPED
            if active_type == "avoid":
               StatusEnum = ProgressStatus.AVOID

            status = Status.objects.get(who=active_user,what=active_item)
            status.progress = StatusEnum
            status.amount = int(request.POST["episode"])
            status.save()
    
    return HttpResponse({"submitted": everything_ok})