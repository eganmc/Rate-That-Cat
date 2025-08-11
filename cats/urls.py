from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.cat_list, name='cat_list'),
    path('cat/<int:pk>/', views.cat_detail, name='cat_detail'),
    path('cat/new/', views.cat_create, name='cat_create'),
    path('cat/<int:pk>/edit/', views.cat_update, name='cat_update'),
    path('cat/<int:pk>/delete/', views.cat_delete, name='cat_delete'),
    path('cat/<int:pk>/rate/', views.rate_cat, name='rate_cat'),
    path('cat/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
]