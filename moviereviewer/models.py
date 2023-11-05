from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    backdrop_path = models.CharField(max_length=255, null=True, default='')
    added_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_movies', null=True)
    genre_ids = models.ManyToManyField(Genre, related_name='movies')
    adult = models.BooleanField()
    original_language = models.CharField(max_length=10)
    overview = models.TextField()
    popularity = models.FloatField()
    release_date = models.DateField()
    vote_average = models.FloatField(default=0, null=True)
    vote_count = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.title


class SimilarMovie(models.Model):
    id = models.IntegerField(primary_key=True)  # ID from the API
    backdrop_path = models.CharField(max_length=255, null=True, default='')
    genre_ids = models.ManyToManyField(Genre, related_name='similar_movies')
    added_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_similar_movies', null=True)
    adult = models.BooleanField()
    original_language = models.CharField(max_length=10)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    similar_to = models.IntegerField()

    def __str__(self):
        return self.title


class Cast(models.Model):
    name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True)
    movie_id = models.IntegerField(null=True)


class Reviews(models.Model):
    added_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_reviews', null=True)
    review_data = models.CharField(max_length=5000, null=True)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(null=True)


class Watchlist(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='watchlists', null=True)
    movies = models.ForeignKey(
        'Movie', on_delete=models.SET_NULL, related_name='watchlists', null=True)
    shared_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='shared_watchlists', null=True)

    def __str__(self):
        return f"Watchlist of {self.owner.username}"
