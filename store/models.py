from django.db import models
from django.core.validators import MinValueValidator
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from .validators import validate_product_price
from uuid import uuid4
from .validators import validate_product_price

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self) -> str:
        return self.username


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_product_price])
    stock = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ProductImage(models.Model):
    image = models.ImageField(upload_to=f'store/images/products')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')


class Customer(models.Model):
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def first_name(self):
        return self.user.first_name 
    
    @property
    def last_name(self):
        return self.user.last_name
    
    @property
    def email(self):
        return self.user.email
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def items_count(self):
        return self.items.count()

    class Meta:
        ordering =['-created_at']


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    class Meta:
        unique_together = [
            ['product', 'cart']
        ]


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Canceled')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    cost = models.DecimalField(max_digits=20, decimal_places=5)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-placed_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()