from django.urls import path
from . import views

urlpatterns = [
    path('notes', views.note_list_create, name='note-list-create'),
    path('notes/<int:pk>', views.note_detail, name='note-detail'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
]