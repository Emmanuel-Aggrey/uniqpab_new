from .models import MainCategory,Product

def category(request):
    nav = MainCategory.objects.all()
    popular = Product.objects.filter(num_views__gte=2)

    return {'nav':nav,'popular':popular}

