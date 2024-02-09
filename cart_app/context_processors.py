from .cart import Cart


def cart(request):
    """
    Context processor to transfer global information to all templates
    """
    return {'cart': Cart(request)}
