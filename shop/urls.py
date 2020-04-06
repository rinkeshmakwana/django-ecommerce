from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name='shop-home'),
    path('products/', ProductListView.as_view(), name='shop-products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('about/', views.about, name='shop-about'),
]