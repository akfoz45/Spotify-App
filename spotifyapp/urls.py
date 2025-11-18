from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="spotify_login"),
    path('callback/', views.callback_view, name='spotify_callback'),
    path('profile/', views.profile_view, name='spotify_profile'),
    path('logout/', views.logout_view, name='spotify_logout')
]