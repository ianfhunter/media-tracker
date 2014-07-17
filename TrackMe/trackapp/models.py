from django.contrib import admin
from django.db import models
from django_enumfield import enum
import datetime
import hashlib

class Status(enum.Enum):
    NO_STATUS = 0
    WISHLIST = 1
    COMPLETED = 2
    IN_PROGRESS = 3
    AVOID = 4
    DROPPED = 5

class MediaType(enum.Enum):
    UNASSIGNED = 0
    ANIME = 1
    MANGA = 2
    GAME = 3
    MUSIC = 4
    BOOK = 5
    TV = 6

# Create your models here.
class TrackItem(models.Model):
    name = models.CharField(max_length=200)                          #Name of the TrackItem item e.g. "Naruto Shippuden"
    alt_names = models.CharField(blank=True,max_length=1000)         #Alternate Names in Comma Delimited Format.

    item_type = enum.EnumField(MediaType, default=MediaType.UNASSIGNED)     #Game, Tv show, etc

    cover_photo = models.FileField(upload_to="covers",blank=True)    #Cover 

    progress = enum.EnumField(Status, default=Status.NO_STATUS)

    rating = models.IntegerField()
    
    amount = models.IntegerField()                                   #Amount of episodes, etc
    time = models.IntegerField()                                     #In minutes

    tags = models.CharField(blank=True,max_length=1000)              #Comma Delimited Format.

    notes = models.CharField(max_length=1000)

class Background(models.Model):
    obj = models.FileField(upload_to="background")


admin.site.register(TrackItem)
admin.site.register(Background)
