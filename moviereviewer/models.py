from django.db import models

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # ID from the API
    backdrop_path = models.CharField(max_length=255,null=True,default='')
    genre_ids = models.ManyToManyField(Genre, related_name='movies')
    adult = models.BooleanField()
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class SimilarMovie(models.Model):
    id = models.IntegerField(primary_key=True)  # ID from the API
    backdrop_path = models.CharField(max_length=255,null=True,default='')
    genre_ids = models.ManyToManyField(Genre, related_name='similar_movies')
    adult = models.BooleanField()
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    similar_to=models.IntegerField()

    def __str__(self):
        return self.title
    
class Cast(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)
    character_name=models.CharField(max_length=255)
    profile_path=models.CharField(max_length=255,null=True)
    movie_id=models.IntegerField()

class Reviews(models.Model):
    name=models.CharField(max_length=255)
    review_data=models.CharField(max_length=5000,null=True)
    movie_id=models.IntegerField()
    created_at=models.DateTimeField()

class WatchList(models.Model):
    movie_id=models.ManyToManyField(Movie,related_name='movies')
    share_by=models.CharField(max_length=255)
    added_at=models.DateTimeField(auto_now=True)