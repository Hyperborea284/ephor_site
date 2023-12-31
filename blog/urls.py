from django.urls import path, include

from .views import *
from . import views

urlpatterns = [
    path('', blog_post_list_view),
    path('<str:slug>/', blog_post_detail_view),
    path('<str:slug>/edit/', blog_post_update_view),
    path('<str:slug>/delete/', blog_post_delete_view),
    path('salvar_geolocalizacao/', views.salvar_geolocalizacao, name='salvar_geolocalizacao'),
]
