from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path("lista_productos/", views.lista_productos, name="lista_productos"),
    path('crear/', views.crear_producto, name='crear_producto'),
]
