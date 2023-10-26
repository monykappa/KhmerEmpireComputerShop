from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_laptop = models.BooleanField(default=False)  # This field identifies laptops
    specifications = models.OneToOneField('ProductSpec', on_delete=models.CASCADE, null=True, blank=True)
    stock = models.OneToOneField('Stock', on_delete=models.CASCADE, related_name='product_stock')


class ProductSpec(models.Model):
    brand = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    ram = models.CharField(max_length=20)
    storage = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
    graphics_card = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=255)
    battery_life = models.CharField(max_length=20)
    ports_connectivity = models.TextField()
    weight = models.CharField(max_length=20)
    dimensions = models.CharField(max_length=255)
    additional_features = models.TextField()
    warranty = models.CharField(max_length=255)

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_product')
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class EmployeeRole(models.Model):
    name = models.CharField(max_length=255)

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    roles = models.ManyToManyField(EmployeeRole, through='EmployeeAssignment')

class EmployeeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.ForeignKey(EmployeeRole, on_delete=models.CASCADE)
    assigned_date = models.DateField()

