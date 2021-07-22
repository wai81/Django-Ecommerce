from django.db import models
from category.models import Category
# Create your models here.


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photo/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # каскадное удаление если мы удаляем категорию
    # удаляется все продукты этой категории
    created_date = models.DateTimeField(auto_now_add=True)  # auto_now_add обновляется только при создании
    modified_date = models.DateTimeField(auto_now=True)  # auto_now обновляет поле каждый раз при изменении

    def __str__(self):
        return self.product_name

