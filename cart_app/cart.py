from decimal import Decimal

from django.conf import settings

from product_app.models import Product


class Cart(object):
    def __init__(self, request):
        """Cart initialization"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ Sorts through items in the cart and provides access to class Product from database"""
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        for item in self.cart.values():
            item['product'].price = Decimal(item['product'].price)
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self):
        """Counting the number of items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """Updating session for user when editing cart"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add_to_cart(self, product_id, quantity=1, update_quantity=False):
        """Adding an item to the cart or updating its quantity"""
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()

    def remove(self, product_id):
        """Removing items from cart"""
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Emptying the cart in session"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        """Calculating the total cost of items in the cart"""
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))

    def get_item(self, product_id):
        """Return item by id"""
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None

