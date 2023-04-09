
from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('land', views.land, name='land'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('intro', views.intro, name='about'),

]
