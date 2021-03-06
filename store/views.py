from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Order, OrderItem, ShippingAddress
from user.models import Profile
from wardrobe.models import Item
import datetime
from django.contrib.auth.decorators import login_required
from .utils import cartData, searchItems
from django.contrib import messages
from django.conf import settings

# Create your views here.

@login_required(login_url="login")
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    items, search_query = searchItems(request)
    context = {'items': items, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)
    

@login_required(login_url="login")
def saleItem(request, pk):
    itemObj = Item.objects.get(id=pk)
    print('ITEM', itemObj)
    tags = itemObj.tags.all()
    context = {'item': itemObj, 'tags': tags}
    return render(request, 'store/sale_item.html', context)


@login_required(login_url="login")
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    orderItems = data['orderItems']
        
    context = {'orderItems': orderItems, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@login_required(login_url="login")
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    orderItems = data['orderItems']
        
    context = {'orderItems': orderItems, 'order': order, 'cartItems': cartItems, 'PAYPAL': settings.PAYPAL}
    return render(request, 'store/checkout.html', context)


@login_required(login_url="login")
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.profile
    item = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)

    if action == 'add':
        if orderItem.quantity == 0:
            orderItem.quantity = 1
            messages.success(request, 'Item added to cart')

        elif orderItem.quantity == 1:
            messages.error(request, 'Item already in cart!')
    
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request, 'Item removed from cart')
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

@login_required(login_url="login")
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print('ORDER:', order)
        
        

    else:
        return redirect('login')

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )

    shipping = ShippingAddress.objects.get(order=order)
    items = order.orderitem_set.filter(order=order)
   
    for item in items:
        item.item.delete()

    messages.success(request, 'Congrats on your new threads!')


    return JsonResponse('Payment complete!', safe=False)