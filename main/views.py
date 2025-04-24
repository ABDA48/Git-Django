from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from main.models import Avatar, Depot, DepotLivre, HistoriqueDepot, HistoriqueDepotLivre
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

def home(response):
    return render(response,'main/index.html',{})

def products(request):
    # Get filter parameters
    type_filter = request.GET.get('type', '')
    centre_filter = request.GET.get('centre', '')
    responsable_filter = request.GET.get('responsable', '')
    search_query = request.GET.get('search', '')
    
    # Start with all products
    products = Depot.objects.all()
    
    # Apply filters
    if type_filter:
        products = products.filter(type=type_filter)
    if centre_filter:
        products = products.filter(centre=centre_filter)
    if responsable_filter:
        products = products.filter(responsable=responsable_filter)
    
    # Apply search
    if search_query:
        products = products.filter(
            Q(reference__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Get total count before pagination
    total_count = products.count()
    
    # Pagination
    paginator = Paginator(products, 30)  # Show 30 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'title': 'Produits',
        'total_count': total_count,
        'type_filter': type_filter,
        'centre_filter': centre_filter,
        'responsable_filter': responsable_filter,
        'search_query': search_query,
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

def view_product(request, reference):
    try:
        product = Depot.objects.get(reference=reference)
        history = HistoriqueDepot.objects.filter(reference=product).order_by('-date')
        context = {
            'product': product,
            'history': history,
            'title': f'Produit - {product.reference}'
        }
        return render(request, 'main/viewproduct.html', context)
    except Depot.DoesNotExist:
        return render(request, 'main/404.html', {'title': 'Produit non trouvé'})

def view_book(request, reference):
    try:
        book = DepotLivre.objects.get(reference=reference)
        history = HistoriqueDepotLivre.objects.filter(reference=book).order_by('-date')
        context = {
            'book': book,
            'history': history,
            'title': f'Livre - {book.reference}'
        }
        return render(request, 'main/viewbook.html', context)
    except DepotLivre.DoesNotExist:
        return render(request, 'main/404.html', {'title': 'Livre non trouvé'})

def dashboard(request):
    # Products by Type
    products_by_type = dict(Depot.objects.values_list('type').annotate(count=Count('type')))
    
    # Products by Centre
    products_by_centre = dict(Depot.objects.values_list('centre').annotate(count=Count('centre')))
    
    # Books by Category
    books_by_category = dict(DepotLivre.objects.values_list('category').annotate(count=Count('category')))
    
    # Books by Language
    books_by_language = dict(DepotLivre.objects.values_list('language').annotate(count=Count('language')))
    
    # Stock Levels (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Get monthly stock levels for products
    product_stock = Depot.objects.filter(
        date_entree__gte=six_months_ago
    ).annotate(
        month=TruncMonth('date_entree')
    ).values('month').annotate(
        total=Sum('quantite_entree') - Sum('quantite_sortie')
    ).order_by('month')
    
    # Get monthly stock levels for books
    book_stock = DepotLivre.objects.filter(
        date_entree__gte=six_months_ago
    ).annotate(
        month=TruncMonth('date_entree')
    ).values('month').annotate(
        total=Sum('quantite_entree') - Sum('quantite_sortie')
    ).order_by('month')
    
    # Prepare stock levels data and convert Decimal to float
    stock_levels = {
        'labels': [entry['month'].strftime('%B %Y') for entry in product_stock],
        'products': [float(entry['total'] or 0) for entry in product_stock],
        'books': [float(entry['total'] or 0) for entry in book_stock]
    }
    
    # Additional statistics
    total_products = Depot.objects.count()
    total_books = DepotLivre.objects.count()
    total_centres = len(products_by_centre)
    total_responsables = len(Depot.objects.values_list('responsable', flat=True).distinct())
    
    context = {
        'title': 'Tableau de Bord',
        'products_by_type': products_by_type,
        'products_by_centre': products_by_centre,
        'books_by_category': books_by_category,
        'books_by_language': books_by_language,
        'stock_levels': stock_levels,
        'total_products': total_products,
        'total_books': total_books,
        'total_centres': total_centres,
        'total_responsables': total_responsables
    }
    
    return render(request, 'main/dashboard.html', context)


 