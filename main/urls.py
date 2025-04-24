from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('books/', views.books, name="books"),
    path('responsables/', views.responsables, name="responsables"),
    path('product/<str:reference>/', views.view_product, name="view_product"),
    path('book/<str:reference>/', views.view_book, name="view_book"),
    path('dashboard/', views.dashboard, name="dashboard"),
]