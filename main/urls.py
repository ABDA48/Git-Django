from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('books/', views.books, name="books"),
    path('responsables/', views.responsables, name="responsables"),
]