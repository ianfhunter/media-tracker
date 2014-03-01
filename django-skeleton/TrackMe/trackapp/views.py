from django.shortcuts import render_to_response
from models import Trackable,Review

def home(request):
    d = {}
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
    print value
    item = Trackable.objects.get(pk=int(value))
    reviews = Review.objects.filter(review_of=item)
    d = {
        "item": item,
        "reviews": reviews
    }
    return render_to_response('item.html', d)
