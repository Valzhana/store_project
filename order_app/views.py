from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart_app.cart import Cart


@login_required
def create_order(request):
    """
    Checkout page
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                OrderItem.objects.create(order=order,
                                         product=product,
                                         price=price,
                                         quantity=quantity)
            cart.empty_cart()
            return render(request, 'order_app/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order_app/create.html',
                  {'cart': cart, 'form': form})
