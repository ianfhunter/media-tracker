from django.contrib import admin
from django.db import models
from django_enumfield import enum
import datetime
import hashlib

def _createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(datetime.time()))
    return  hash.hexdigest()[:-10]

class ProgressStatus(enum.Enum):
    NOT_STARTED = 0
    FINISHED = 1
    IN_PROGRESS = 2
    DROPPED = 3
    AVOID = 4
    WISHLIST = 5


# Create your models here.
class Trackable(models.Model):
    name = models.CharField(max_length=200)          #Name of the trackable item e.g. "Naruto Shippuden"
    item_type = models.CharField(max_length=200)     #Game, Tv show, etc
    description = models.CharField(max_length=1000)     #Game, Tv show, etc
    amount = models.IntegerField()                   #Amount of episodes, etc
    release_date = models.DateField()                #Release Date
    average_num_stars = models.IntegerField()            #Average user rating
    cover_photo = models.FileField(upload_to="covers")   #Cover 

    #Meta information
    director = models.CharField(max_length=200)
    production = models.CharField(max_length=200)
    runtime = models.IntegerField()                #Measured in minutes

class User(models.Model):
    username = models.CharField(max_length=200)
    date_created = models.DateField(default=datetime.date.today)
    password = models.CharField(max_length=100,unique=True)
    avatar = models.FileField(upload_to="avatars")

class Review(models.Model):
    review_of = models.ForeignKey(Trackable)         #Item being reviewed
    author = models.CharField(max_length=100)         #Item being reviewed
    num_stars = models.IntegerField()                #Reviewer's Rating
    contents = models.CharField(max_length=10000)     #actual review

class Status(models.Model):
    who = models.ForeignKey(User)
    what = models.ForeignKey(Trackable)
    progress = enum.EnumField(ProgressStatus, default=ProgressStatus.NOT_STARTED)
    amount = models.IntegerField()
    class Meta:
        unique_together = ('who', 'what')

class Tag(models.Model):
    items = models.ManyToManyField(Trackable)
    name = models.CharField(max_length=30)

class Background(models.Model):
    obj = models.FileField(upload_to="background")


admin.site.register(Trackable)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Status)
admin.site.register(Tag)
admin.site.register(Background)
