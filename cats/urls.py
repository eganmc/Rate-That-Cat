from django.urls import path
from . import views

urlpatterns = [
    path('', views.cat_list, name='cat_list'),
    path('cat/<int:pk>/', views.cat_detail, name='cat_detail'),
    path('cat/new/', views.cat_create, name='cat_create'),
    path('cat/<int:pk>/edit/', views.cat_update, name='cat_update'),
    path('cat/<int:pk>/delete/', views.cat_delete, name='cat_delete'),
]