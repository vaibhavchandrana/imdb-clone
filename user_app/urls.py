from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include
from user_app.views import registration_view,logout_view
urlpatterns = [
    path('login/', obtain_auth_token),
    path('registration/', registration_view),
    path('logout/', logout_view),
]