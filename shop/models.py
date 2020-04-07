from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.PositiveIntegerField()
    product_image = models.ImageField(default='abc.jpg', upload_to='product_images')
    product_rating = models.IntegerField()
    product_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})