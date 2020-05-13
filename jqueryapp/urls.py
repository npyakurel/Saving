from django.urls import path
from .views import *

app_name = 'jqueryapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/detail/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('order/summery/', OrderSummeryView.as_view(), name='ordersummery'),
    path('remove_single_item_from_cart<int:pk>/',
         remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),






]
