from django.shortcuts import render

from .cart import Cart
from product_app.models import Product


def add_to_cart_page(request, product_id):
    """
    Page element with cart and product counter
    """
    cart = Cart(request)
    cart.add_to_cart(product_id)
    return render(request, 'cart_app/partials/menu_cart.html')


def cart_page(request):
    """
    View for cart page
    """
    return render(request, 'cart_app/cart.html')


def update_cart(request, product_id, action):
    """
    Page element for changing the number of products in the cart
    """
    cart = Cart(request)
    if action == 'increment':
        cart.add_to_cart(product_id, 1, True)
    else:
        cart.add_to_cart(product_id, -1, True)
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart_app/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response


def hx_menu_cart(request):
    """
    Page element to show cart and number of items in it
    """
    return render(request, 'cart_app/partials/menu_cart.html')


def hx_cart_total(request):
    """
    Page element to show total price of items in the cart
    """
    return render(request, 'cart_app/partials/cart_total.html')
