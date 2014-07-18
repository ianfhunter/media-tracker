from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import TrackItem,Background,Status,MediaType
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import urllib,urllib2
import datetime
import json
from xml.dom import minidom
import hashlib, uuid
import datetime

def to_enum(word):
    if word == "anime":
        return MediaType.ANIME
    if word == "manga":
        return MediaType.MANGA
    if word == "game":
        return MediaType.GAME
    if word == "music":
        return MediaType.MUSIC
    if word == "book":
        return MediaType.BOOK
    if word == "TV":
        return MediaType.TV

    if word == "wishlist":
        return Status.WISHLIST
    if word == "completed":
        return Status.COMPLETED
    if word == "in_progress":
        return Status.IN_PROGRESS
    if word == "avoid":
        return Status.AVOID
    if word == "dropped":
        return Status.DROPPED


def home(request):
    imgs = Background.objects.order_by('?')
    if not imgs:
        imgs = Background(obj="background/default_background.jpg")
        imgs.save()
        imgs = [imgs]
    d = {}
    d["image"] = imgs[0]
    return render_to_response('home.html', d)

@csrf_exempt
def add_item(request):

    if (request.method == "POST"):
        data = request.POST
        new_item = TrackItem(
            name=data["title"],
            alt_names=data["alttitle"],
            item_type=to_enum(data["mediatype"]),
            cover_photo=data["coverphoto"],
            progress=to_enum(data["progress"]),
            rating=data["rating"],
            amount=data["amount"],
            time=data["length"],
            tags=data["genre"],
            notes=data["notes"],
            created_at=datetime.datetime.today()
            )
        new_item.save()
        return HttpResponse("Submitted")
    else:
        return HttpResponse("No.")

def item(request):
    d = {}
    return render_to_response('item.html', d)

def stats(request):
    d = {}
    items = TrackItem.objects.all()
    d = {"item_list":items} 
    return render_to_response('stats.html', d)

def settings(request):
    d = {}
    return render_to_response('settings.html', d)

def library(request):
    d = {}
    items = TrackItem.objects.all()
    d = {"item_list":items} 
    return render_to_response('library.html', d)
