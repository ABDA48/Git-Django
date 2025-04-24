from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from main.models import Avatar, Depot, DepotLivre, HistoriqueDepot, HistoriqueDepotLivre

def home(response):
    return render(response,'main/index.html',{})

def products(request):
    products = Depot.objects.all()
    context = {
        'products': products,
        'title': 'Produits'
    }
    return render(request, 'main/products.html', context)

def books(request):
    books = DepotLivre.objects.all()
    context = {
        'books': books,
        'title': 'Livres'
    }
    return render(request, 'main/books.html', context)

def responsables(request):
    # Get unique responsables from Depot model
    responsables = Depot.objects.values_list('responsable', flat=True).distinct()
    
    # Create a dictionary to store products for each responsable
    responsable_products = {}
    for responsable in responsables:
        responsable_products[responsable] = Depot.objects.filter(responsable=responsable)
    
    context = {
        'responsables': responsables,
        'responsable_products': responsable_products,
        'title': 'Responsables'
    }
    return render(request, 'main/responsables.html', context)


 