from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Trackable,Review,Tag,Background,User,Status,ProgressStatus
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import urllib,urllib2
import datetime
import json
from xml.dom import minidom
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
    media_type = request.GET.get('type')
    print query, media_type

    if media_type == "TV Show":
        #Search for Items using OpenMovie DB API
        response = urllib2.urlopen('http://www.omdbapi.com/?s=' + query.replace(' ','+'))
        data = json.load(response)   

        results = []
        if 'Search' in data:
            for item in data['Search']:
                show = Trackable(name=item['Title'],
                                 id=int("1" + item['imdbID'][2:]),
                                 item_type="TV Show",
                                 #filler
                                 amount=1,
                                 release_date=datetime.datetime.strptime("01-JAN-2000", "%d-%b-%Y"),
                                 average_num_stars=0,
                                 cover_photo=None,
                                 director="",
                                 production="",
                                 runtime=0
                                 )
                show.save()
                results.append(show)

    elif media_type == "Game":
        print 
        req = urllib2.Request('http://thegamesdb.net/api/GetGamesList.php?name=' + query.replace(' ','+'))

        #Need this, as some user agents are blocked
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        source = urllib2.urlopen(req).read()

        data = minidom.parseString(source)   

        game = data.getElementsByTagName("Game")
        results = []

        for node in game:
            for child in node.childNodes:
                if child.localName == "GameTitle":
                    name=child.childNodes[0].nodeValue
                if child.localName == "id":
                    game_id=child.childNodes[0].nodeValue

            print name, "-" ,game_id
            if name and game_id:
                item = Trackable(name=name,
                                 id=game_id,
                                 item_type="Game",
                                 #filler
                                 amount=1,
                                 release_date=datetime.datetime.strptime("01-JAN-2000", "%d-%b-%Y"),
                                 average_num_stars=0,
                                 cover_photo=None,
                                 director="",
                                 production="",
                                 runtime=0
                                 )
                item.save()
                results.append(item)
            name = None
            game_id = None
    else:
        results = []

    if len(results) > 0:
        d = {"results": results}
    else:
        d = {}
    return render_to_response('search.html', d)

def item(request,value):


    item = Trackable.objects.get(pk=int(value))

    if item.item_type == "TV Show":
        response = urllib2.urlopen("http://www.omdbapi.com/?i=" + ("tt" + value[1:]) + "&tomatoes=true")
        data = json.load(response)   
        try:
            rating = float(data["tomatoRating"])
        except Exception:
            rating = 0
      
        print data
        item = Trackable(id=item.id,    #Adding a 1 at the start, as IMDB ids can contain 'tt'
                        name=data["Title"],
                        amount=10,
                        average_num_stars=rating,
                        item_type="TV Show",
                        description=data["Plot"],
                        director=data["Director"],
                        production=data["Production"],
                        runtime=int(''.join(i for i in data["Runtime"] if i.isdigit()))
                        )
        
        tags = []
        for genre in data["Genre"].split(","):
            tags.append(Tag(name=genre))
        reviews = [Review(author="Rotten Tomatoes",contents=data["tomatoConsensus"])]

    elif item.item_type == "Game":
        req = urllib2.Request("http://thegamesdb.net/api/GetGame.php?id=" + value)
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        source = urllib2.urlopen(req).read()
        data = minidom.parseString(source)   

        results = []


        rating = data.getElementsByTagName("Rating")
        if rating and len(rating[0].childNodes) != 0:
            rating = rating[0].childNodes[0].nodeValue
        else:
            rating = 0

        description = data.getElementsByTagName("Overview")
        if description and len(description[0].childNodes) != 0:
            description = description[0].childNodes[0].nodeValue
        else:
            description = ""

        director = data.getElementsByTagName("Developer")
        if director and len(director[0].childNodes) != 0:
            director = director[0].childNodes[0].nodeValue
        else:
            director = ""         

        publisher = data.getElementsByTagName("Publisher")
        if publisher and len(publisher[0].childNodes) != 0:
            publisher = publisher[0].childNodes[0].nodeValue
        else:
            publisher = "" 

        item = Trackable(id=item.id,    #Adding a 1 at the start, as IMDB ids can contain 'tt'
                        name=item.name,
                        amount=0,
                        average_num_stars=rating,
                        item_type="Game",
                        description=description,
                        director=director,
                        production=publisher,
                        release_date= item.release_date,
                        runtime=0
                        )
        tags = []
        reviews = []

    user = User.objects.order_by('id')
    if user:
        user = user[0]
    else:
        user = None


    #scrape Google Images for cover
    if not item.cover_photo:   
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

    user = User(username=request.POST['username'], password=createHash(request.POST['password']))
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