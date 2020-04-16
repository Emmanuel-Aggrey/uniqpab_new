from django.conf.urls import url
from django.urls import  path
from . import views

app_name = 'cart'

urlpatterns = [
    path('yourcart', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/<slug:slug>/', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]

