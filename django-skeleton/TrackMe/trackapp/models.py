from django.contrib import admin
from django.db import models
import datetime

# Create your models here.
class Trackable(models.Model):
    name = models.CharField(max_length=200)          #Name of the trackable item e.g. "Naruto Shippuden"
    item_type = models.CharField(max_length=200)     #Game, Tv show, etc
    description = models.CharField(max_length=1000)     #Game, Tv show, etc
    amount = models.IntegerField()                   #Amount of episodes, etc
    release_date = models.DateField()                #Release Date
    average_num_stars = models.IntegerField()        #Average user rating
    total_views = models.IntegerField()              #Total User Views
    plus_ones = models.IntegerField()                #would you recommend this series?
    cover_photo = models.FileField()   #would you recommend this series?
    # def __unicode__(self):
    #     return self.name

class User(model.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    date_created = models.DateField(_("Date"), default=datetime.date.today)
    passwordHash = models.CharField(max_length=10,default=_createHash,unique=True)
    avatar = models.FileField()
    amount_of_reviews = models.IntegerField()

class Review(models.Model):
    review_of = models.ForeignKey(Trackable)         #Item being reviewed
    author = models.ForeignKey(User)         #Item being reviewed
    num_stars = models.IntegerField()                #Reviewer's Rating
    plus_ones = models.IntegerField()                #likes, upvotes, etc of this review
    contents = models.CharField(max_length=10000)     #actual review


admin.site.register(Trackable)
admin.site.register(Review)