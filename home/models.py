from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import uuid
import os


def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filenamecd
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def product_directory_path(instance, filename):
    # Generate a unique identifier for the directory
    unique_id = str(uuid.uuid4())
    # Construct the directory path
    directory_path = f'content/{unique_id}/'
    
    # Return the complete file path
    return os.path.join(directory_path, filename)

# Create a model for the Category of products (e.g., laptops, desktops).
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class Product(models.Model):
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=[(str(year), str(year)) for year in range(2015, 2056)], null=True, blank=True)

    def __str__(self):
        return self.brand_name

class LaptopSpec(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='laptopspec')
    cpu = models.CharField(max_length=100, null=True, blank=True)
    cpu_detail = models.CharField(max_length=200, null=True, blank=True)
    memory = models.CharField(max_length=100, null=True, blank=True)
    memory_detail =models.CharField(max_length=200, null=True, blank=True)
    storage = models.CharField(max_length=100, null=True, blank=True)
    storage_detail = models.CharField(max_length=100, null=True, blank=True)
    graphics_card = models.CharField(max_length=100, null=True, blank=True)
    graphics_card_detail = models.CharField(max_length=100, null=True, blank=True)
    display = models.CharField(max_length=100, null=True, blank=True)
    display_detail = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.product:
            return f"Specifications for Product #{self.product.pk}"
        else:
            return "Unassociated Product Specification"




class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # The initial stock quantity

    def __str__(self):
        return f"{self.product.brand_name} - {self.product.model} - {self.product.year}"

    def price_per_unit(self):
        return self.product.price if self.product else 0

    def total_price(self):
        return self.price_per_unit() * self.quantity

    def price_per_unit_with_dollar(self):
        return f"${self.price_per_unit()}"

    def total_price_with_dollar(self):
        return f"${self.total_price()}"
    
# Create a model for customer orders.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ordered_products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order #{self.id} - {self.customer_name}'

# Create a model for the items in an order.
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

