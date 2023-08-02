from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),

    path('detail_page/<str:pk>/', views.detail_page, name='detail_page'),
    path('detail_full/<str:pk>/', views.detail_full, name='detail_full'),

    path('profile/', views.profile, name='profile'),

    path('save_coin/<str:pk>/', views.save_coin, name='save_coin'),
    path('remove_coin/<str:pk>/', views.remove_coin, name='remove_coin'),

    path('test_endpoints/', views.test_endpoints, name='test_endpoints'),
]