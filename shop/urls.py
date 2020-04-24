from django.urls import path
from . import views
from .views import (ProductListView,
                    ProductDetailView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    HomeListView,
                    add_to_cart,
                    buy_now,
                    remove_from_cart,
                    remove_single_product_from_cart,
                    ShoppingCartView,
                    CheckoutView,
                    PaymentView)


urlpatterns = [
    path('', HomeListView.as_view(), name='shop-home'),
    path('products/<category>/', ProductListView.as_view(), name='shop-products'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('new/', ProductCreateView.as_view(), name='product-create'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('buy-now/<slug>/', buy_now, name='buy-now'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>/', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('about/', views.about, name='shop-about'),
]
