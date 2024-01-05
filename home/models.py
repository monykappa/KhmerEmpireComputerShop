from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import uuid
from decimal import Decimal
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

# does not count
def product_related_images_directory_path(instance, filename):
    # Generate a unique identifier for the directory
    unique_id = str(uuid.uuid4())
    # Construct the directory path
    directory_path = f'product_related_images/{unique_id}/'

    # Return the complete file path
    return os.path.join(directory_path, filename)


# Create a model for the Category of products (e.g., laptops, desktops).
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class brand_category(models.Model):
    company_name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    brand_category = models.ForeignKey(brand_category, on_delete=models.CASCADE, null=True, blank=True, related_name='brand_category')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    image_2 = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    image_3 = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    image_4 = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    image_5 = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    image_6 = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=4, choices=[(str(year), str(year)) for year in range(2015, 2056)], null=True, blank=True)
    warranty_months = models.IntegerField(null=True, blank=True)
    warranty_years = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.brand_name} - ${self.price}" if self.price % 1 != 0 else f"{self.brand_name} - ${int(self.price)}"

class HeadphoneSpec(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='headphonespec')
    driver_size = models.CharField(max_length=100, null=True, blank=True)
    frequency_response = models.CharField(max_length=100, null=True, blank=True)
    impedance = models.CharField(max_length=100, null=True, blank=True)
    noise_cancellation = models.CharField(max_length=100, null=True, blank=True)
    connector_type = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    battery_life = models.CharField(max_length=100, null=True, blank=True)
    additional_features = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        if self.product:
            return f"{self.product.brand_name} - {self.product.model} - Headphone Specifications"
        return "HeadphoneSpec (No Product)"

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
    port = models.CharField(max_length=500, null=True, blank=True)
    wireless_connectivity = models.CharField(max_length=500, null=True, blank=True)
    webcam = models.CharField(max_length=100, null=True, blank=True)
    battery = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.product:
            return f"Specifications for Product #{self.product.pk}"
        else:
            return "Unassociated Product Specification"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total_price}"
    
class CartItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Set a default value here
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Update subtotal based on product price and quantity
        self.subtotal = self.product.price * self.quantity

        super().save(*args, **kwargs)

        # Update the total price of the associated order
        order_items = self.order.cartitem_set.all()
        self.order.total_price = sum(item.subtotal for item in order_items)
        self.order.save()




class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # The initial stock quantity

    def __str__(self):
        return f"{self.product.brand_name} - {self.product.model} - {self.product.year} - {self.quantity} units in stock"

    def price_per_unit(self):
        return self.product.price if self.product else 0

    def total_price(self):
        return self.price_per_unit() * self.quantity

    def price_per_unit_with_dollar(self):
        return f"${self.price_per_unit()}"

    def total_price_with_dollar(self):
        return f"${self.total_price()}"
    

