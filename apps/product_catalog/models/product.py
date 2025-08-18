from django.db import models

from apps.core.models import AbstractModel


class Category(AbstractModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Tag(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(AbstractModel):
    name = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default='0.0')
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self):
        return self.name