from django.contrib import admin
from .models import Category, Product, ProductSpec, Stock, Order, OrderItem

class ProductSpecInline(admin.StackedInline):
    model = ProductSpec
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSpecInline]
    
    list_display = ('id', 'brand_name', 'model', 'year', 'price_with_dollar', 'category')
    list_filter = ('year', 'category')

    def price_with_dollar(self, obj):
        return f"${obj.price}"
    price_with_dollar.short_description = 'Price'



class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ('product_brand_name', 'product_model', 'price_with_dollar', 'cpu', 'memory', 'storage', 'graphics_card', 'display', 'operating_system')

    list_select_related = ('product',)  # Specify the related model to retrieve

    def product_brand_name(self, obj):
        if obj.product:
            return obj.product.brand_name if obj.product.brand_name else "N/A"
        return "N/A"  # Handle cases where there is no related product

    product_brand_name.short_description = 'Brand Name'

    def product_model(self, obj):
        if obj.product:
            return obj.product.model if obj.product.model else "N/A"
        return "N/A"  # Handle cases where there is no related product

    product_model.short_description = 'Product Model'

    def price_with_dollar(self, obj):
        return f"${obj.product.price}" if obj.product else ""
    price_with_dollar.short_description = 'Price'


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1


class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price_per_unit_with_dollar', 'total_price_with_dollar')

    def price_per_unit_with_dollar(self, obj):
        return f"${obj.product.price}"  # Assuming product has a price field
    price_per_unit_with_dollar.short_description = 'Price per Unit'

    def total_price(self, obj):
        return f"${obj.quantity * obj.product.price}" if obj.product else ""
    total_price.short_description = 'Total Price'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'total_price')

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'User'

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSpec, ProductSpecAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
