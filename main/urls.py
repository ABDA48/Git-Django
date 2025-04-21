from django.urls import path
from main import views
urlpatterns = [
     path('',views.home,name="home"),
     path('upload-avatar/',views.upload_avatar,name='upload_avatar'),
     path('delete-avatar/<str:filename>',views.delete_avatar,name='delete_avatar')
]