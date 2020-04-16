from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Gallary,MainCategory,SubCategory
from cart.forms import CartAddProductForm
from datetime import date, timedelta
from django.utils import timezone
from cart.cart import Cart



def product_list(request):
    subcategory = SubCategory.objects.all()
    products = Product.objects.all()
    context = {
       'category':subcategory,
       'products':products,
    }
    return render(request, 'shop/index.html', context)


def allCategory(request):
    queryset_list = Category.objects.all()
    sugest = Product.objects.order_by('-updated_at')
    best_buy = sugest.order_by('created_at')

    query = request.GET.get('keyword')
    if query:
        queryset_list = queryset_list.filter(name__icontains=query)
    notfound = 'nothing much your search result'

    context = {
        'categorys': queryset_list,
        'sugest': sugest,
        'best_buy': best_buy,

    }

    return render(request, 'shop/product/allcategory.html', context)


def allRelated(request,id,slug):
    allrelated = get_list_or_404(SubCategory,id=id,slug=slug)
    context = {
        'allrelated': allrelated,
       
    }
    return render(request,'shop/relatedproducts.html', context)


def unique_faqs(request):
    context = {

    }
    return render(request, 'shop/product/faq.html', context)


def product_detail(request, id, slug):

    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    num_views = int(product.num_views )
    num_views +=1

    Product.objects.filter(id=id).update(num_views=num_views)
    
    cart_product_form = CartAddProductForm()

    # recomendation = Product.objects.filter(name__icontains=product.name)

    # may_like = Product.objects.filter(price__lte=product.price)
    context = {
        'product': product,
        
        'cart_product_form': cart_product_form,
        # 'recomendation': recomendation,
        # 'may_like': may_like,
    }
    return render(request, 'shop/detail.html', context)


def search_product(request):
    # queryset_list = Product.objects.filter(available=True)
    queryset_list = Product.objects.order_by('-created_at')

    query = request.GET.get('keyword')
    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) | Q(price__lte=query))
    size = len(queryset_list)

    context = {
        'search_result': queryset_list,
        'resultSize': size,
    }

    return render(request, 'shop/product/search.html', context)


def checkout(request):
    return render(request,'shop/checkout.html')


def mygallery(request):

    gallary = Gallary.objects.all()

    context = {
        'gallary': gallary,
    }
    return render(request, 'shop/partials/carousel.html', context)
