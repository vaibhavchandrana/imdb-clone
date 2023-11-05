from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, MovieSearchView, WatchlistDeleteView, CastViewSet, ReviewsViewSet, MovieByGenre, GenreViewSet, GetCastByMovie, WatchlistCreateView, GetReviewByMovie, RandomizeRatings, WatchlistDetailView, WatchlistShareView
router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'casts', CastViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'movies/genre', MovieByGenre)
router.register(r'genre', GenreViewSet)
urlpatterns = [
    # Your other URL patterns
    path('', include(router.urls)),
    path('movies/search', MovieSearchView.as_view(), name='movie-search'),
    path('cast/movie/<int:movie_id>/',
         GetCastByMovie.as_view(), name='get-cast-by-movie'),
    path('review/movie/<int:movie_id>/',
         GetReviewByMovie.as_view(), name='get-cast-by-movie'),
    path('randomize_ratings/', RandomizeRatings.as_view(),
         name='randomize-ratings'),
    path('add/movie/watchlist/', WatchlistCreateView.as_view(),
         name='create-watchlist'),
    path('get/movies/watchlist/<int:userId>/',
         WatchlistDetailView.as_view(), name='watchlist-detail'),
    path('share/watchlist/', WatchlistShareView.as_view(), name='create-watchlist'),
    path('watchlist/delete/<int:watchlist_id>/',
         WatchlistDeleteView.as_view(), name='watchlist-delete'),

]
