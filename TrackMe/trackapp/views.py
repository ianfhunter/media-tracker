from django.shortcuts import render_to_response
from models import Trackable,Review,Tag,Background,User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

import hashlib, uuid
def createHash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()

def home(request):
    img = Background.objects.get(id=1)
    d = {"image":img}
    return render_to_response('home.html', d)

def search(request):
    query =  request.GET.get('q')
    results =  Trackable.objects.filter(name__contains=query)

    if len(results) > 0:
        d = {"results": results}
    else:
        d = {}
    return render_to_response('search.html', d)

def item(request,value):
    item = Trackable.objects.get(pk=int(value))
    reviews = Review.objects.filter(review_of=item)
    tags = Tag.objects.filter(items=item)

    d = {
        "item": item,
        "reviews": reviews,
        "tags":tags
    }
    return render_to_response('item.html', d)

@csrf_exempt
def login(request):
    print request.POST["username"]

    user = User(username=request.POST['username'], password=createHash(request.POST['password']),email=request.POST['email'])
    user.save()
    img = Background.objects.get(id=1)
    d = {"image":img}
    return redirect('/trackapp/home')
