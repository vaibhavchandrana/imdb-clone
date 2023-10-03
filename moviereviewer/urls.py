# from .views import FetchAndStoreGenres,FetchAndStoreMovies,FetchAndStoreSimilarMovies,FetchAndStoreCast,FetchAndStoreReview
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet,MovieSearchView,CastViewSet,ReviewsViewSet,MovieByGenre,GenreViewSet,SaveCastData,ReviewData,WatchListCreateView

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'casts', CastViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'movies/genre', MovieByGenre)
router.register(r'genre', GenreViewSet)
# urlpatterns = [
#     # path('fetch-genres/', FetchAndStoreGenres.as_view(), name='fetch-genres'),
#     # path('fetch-movies/', FetchAndStoreMovies.as_view(), name='fetch-movies'),
#     # path('fetch-similar-movies/', FetchAndStoreSimilarMovies.as_view(), name='fetch-similar'),
#     # path('fetch-similar-cast/', FetchAndStoreCast.as_view(), name='fetch-cast'),
#     # path('fetch-reviews/', FetchAndStoreReview.as_view(), name='fetch-review'),
#     # Other URL patterns
# ]
urlpatterns = [
    # Your other URL patterns
    path('api/', include(router.urls)),
    path('api/movies/search', MovieSearchView.as_view(), name='movie-search'),
     path('save_cast_data/<int:movie_id>/', SaveCastData.as_view(), name='save_cast_data'),
     path('review_data/<int:movie_id>/', ReviewData.as_view(), name='save_review_data'),
    path('watchlist/create/', WatchListCreateView.as_view(), name='watchlist-create'),

]