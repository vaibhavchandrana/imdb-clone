from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from user_app.views import RegistrationView, logout_view, get_user_id
urlpatterns = [
    path('login/', obtain_auth_token),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('logout/', logout_view),
    path('get-user-id/', get_user_id, name='get_user_id'),
]
