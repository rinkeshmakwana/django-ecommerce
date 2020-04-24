from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_category_url(self):
        return reverse('shop-products', kwargs={'slug': self.slug})


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    product_description = models.TextField()
    product_price = models.PositiveIntegerField()
    product_mrp = models.PositiveIntegerField(null=True, blank=True)
    discount_tag = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(default='default.jpg', upload_to='product_images')
    product_rating = models.IntegerField()
    product_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_buy_now_url(self):
        return reverse('buy-now', kwargs={'slug': self.slug})

    def get_discount_percentage(self):
        if self.product_mrp:
            discounted_percentage = ((self.product_mrp - self.product_price)/self.product_price)*100
            return discounted_percentage


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_product_price(self):
        return self.quantity * self.product.product_price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()

        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f"{self.address} {self.city} {self.state} {self.country} - {self.zip}"

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
