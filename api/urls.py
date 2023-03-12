from django.urls import path,include
from api.views import WatchDetailAV,WatchListAV,StreamPlateformListAV,StreamDetailAV
from api.views import ReviewList,ReviewDetail,ReviewCreate
urlpatterns = [
    path('movielist/',WatchListAV.as_view(),name='movie-list'),
    path('plateform/',StreamPlateformListAV.as_view(),name='plateform-list'),
    path('movie/<int:pk>/',WatchDetailAV.as_view(),name='movie-detail'),
    path('plateform/<int:pk>',StreamDetailAV.as_view(),name='plateform-detail'),
    #movieid/reviews
    path('<int:pk>/review/',ReviewList.as_view(),name='movie-review-list'),
    #movie-id/create-review
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create-for-movie'),
]
