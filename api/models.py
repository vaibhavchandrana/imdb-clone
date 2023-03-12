from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Plateform(models.Model):
    name=models.CharField(max_length=20)
    about=models.CharField(max_length=200)
    website=models.URLField(max_length=200)

    def __str__(self):
        return self.name

class MovieList(models.Model):
    name=models.CharField(max_length=200)
    storyline=models.CharField(max_length=5000)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    plateform=models.ForeignKey(Plateform, on_delete=models.CASCADE,related_name='MovieList')
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    imageurl=models.URLField(max_length=500)
    year=models.IntegerField()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    review_user=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.FloatField(default=0)
    comment=models.CharField(max_length=200,null=True)
    movielist=models.ForeignKey(MovieList, on_delete=models.CASCADE,related_name='movieReview')
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)+' | '+self.movielist.name