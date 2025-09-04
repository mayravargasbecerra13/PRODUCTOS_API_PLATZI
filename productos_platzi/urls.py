from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path("lista_productos/", views.lista_productos, name="lista_productos"),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto' ),
    path('producto/<int:producto_id>editar/', views.update_producto, name="update_producto" ),
    path('productos/<int:producto_id>eliminar/', views.delete_producto, name="delete_producto"),
]
