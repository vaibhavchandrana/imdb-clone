from django.contrib import admin
from .models import Genre, Movie, SimilarMovie, Cast, Reviews, Watchlist
# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(SimilarMovie)
admin.site.register(Cast)
admin.site.register(Reviews)
admin.site.register(Watchlist)
