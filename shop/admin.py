from django.contrib import admin
from .models import Product, OrderProduct, Order, Address, Payment, Category, Brand


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'brand', 'product_price', 'product_rating', 'product_seller', 'list_date']
    list_display_links = ['product_name']
    list_filter = ['product_name', 'category', 'brand', 'product_price', 'product_rating', 'product_seller', 'list_date']
    search_fields = ['product_name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Payment)
