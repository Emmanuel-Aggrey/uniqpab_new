from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, MainCategory, SubCategory, Review
from cart.forms import CartAddProductForm
from .forms import ReviewForm
from datetime import date, timedelta
from django.utils import timezone
from cart.cart import Cart

def product_list(request):
    subcategory = SubCategory.objects.all()
    products = Product.objects.filter(available=True)[0:10]

    # paginating main display
    main_products = Product.objects.filter(available=True).order_by('?')
    paginator = Paginator(main_products, 10)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    context = {
        'category': subcategory,
        'products': products,
        'banner': products_page,
    }
    return render(request, 'shop/index.html', context)


def allRelated(request, id, slug):
    allrelated = SubCategory.objects.get(id=id, slug=slug)

    products = allrelated.products.filter(available=True)

    price = request.GET.get('price')
    if price:

        products = products.filter(price__lte=price)

    context = {
        'allrelated': products,
        'similar_items': allrelated

    }
    return render(request, 'shop/relatedproducts.html', context)


def unique_faqs(request):
    context = {

    }
    return render(request, 'shop/product/faq.html', context)


def product_detail(request, id, slug):

    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # passing this session variable to reviews
    request.session['product'] = product.id
    # end here

    num_views = int(product.num_views)
    num_views += 1

    Product.objects.filter(id=id).update(num_views=num_views)

    cart_product_form = CartAddProductForm()

    # recomendation = Product.objects.filter(name__icontains=product.name)

    # may_like = Product.objects.filter(price__lte=product.price)
    context = {
        'product': product,

        'cart_product_form': cart_product_form,
        'review': Review.objects.filter(product=product)
        # 'recomendation': recomendation,
        # 'may_like': may_like,
    }

    return render(request, 'shop/detail.html', context)


def search_product(request):

    # queryset_list = Product.objects.filter(available=True)
    queryset_list = Product.objects.order_by('-created_at')

    query = request.GET.get('q')

    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query))

    price = request.GET.get('price')

    if price:
        queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'search_result': queryset_list,

    }

    return render(request, 'shop/search.html', context)


def review(request):

    if request.method == 'POST':
        product = request.session.get('product')
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Review.objects.create(product_id=product, name=name,
                              email=email, message=message)

    return HttpResponse()


def error404(request, exception):
    context = {
        'date': 'IT LOOKS LIKE YOU\'R MISSING',
    }
    return render(request, 'error_pages/error404.html', context)


def error500(request):

    return render(request, 'error_pages/error404.html')
