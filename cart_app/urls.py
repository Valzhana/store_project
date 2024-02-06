from django.urls import path

from .views import add_to_cart_page, cart_page, hx_menu_cart, update_cart, hx_cart_total

urlpatterns = [
    path('', cart_page, name='cart_page'),
    path('add_to_cart/<int:product_id>/', add_to_cart_page, name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', hx_cart_total, name='hx_cart_total'),
]