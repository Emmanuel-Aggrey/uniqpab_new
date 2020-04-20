from django.shortcuts import render,redirect

from django.conf import settings
from uniqstore.settings import EMAIL_HOST_USER
from  django.contrib import  messages
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart



def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_number = order.order_number
           
           
            # 
            # subject = 'order placed'
            # message = ' A customer just sent a request to purchase a product get to admin for more info '
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = ['aggrey.en@live.com',]
            # send_mail( subject, message, email_from, recipient_list,fail_silently=False )

           
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

               
                # for key, value in request.POST.items():
                    # pass
                   
                alldate = form.cleaned_data
                name = form.cleaned_data.get('name')
                customer_email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                phone_number = form.cleaned_data.get('phone_number')
                city = form.cleaned_data.get('city')
                
                # subject = 'order placed'
                # message = ' A customer just sent a request to purchase a product get to admin for more info '
                # recepient = [customer_email]
                # # email_from = settings.EMAIL_HOST_USER
                # send_mail(subject, 
                # message, EMAIL_HOST_USER, ['aggrey.en@live.com'], fail_silently = False)
            
                # print(first_name,email,address,phone_number,city)
                
                # mass email
                email_from = settings.EMAIL_HOST_USER
                message1 = ('Hello aggrey ', f'a customer with phone { phone_number } and name { name } from {city} having { order_number } as order number had ordered for a product sign in to admin for more info use the phone,email,name order number to search', email_from, ['aggrey.en@live.com','aggrey.en@gmail.com',])
                message2 = ('Hello ' f'{ name } your order number is {order_number}','\n\tOrder placed successfully we will call u soon please keep the order number safe. Thanks for shopping with us', email_from, [customer_email])
                try:
                    send_mass_mail((message1, message2), fail_silently=False)

                except:
                    messages.info(request,f'email not sent but your order was placed successfully your order number is\t{order_number}\tkindly feel free to give us a call on\
                    <b>0240699506</b> please keep the order number safe')
                    cart.clear()
                    return redirect('orders:checkout')

          
            cart.clear()
        return render(request, 'order/checkoout_success.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/checkoout.html', {'form': form})