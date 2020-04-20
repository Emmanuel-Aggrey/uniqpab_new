from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.product_list, name ='product_list'),
    path('uniqpab_faqs/',views.unique_faqs,name ='faq'),
    path('allrelated/<int:id>/<slug:slug>/',views.allRelated,name ='allrelated'),
    path('detail/<int:id>/<slug:slug>/',views.product_detail, name='product_detail'),
    path('search',views.search_product,name='search'),
    path('review/',views.review,name='review'),
    
]
