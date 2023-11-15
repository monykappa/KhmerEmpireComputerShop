from django.contrib import admin
from django.urls import reverse
from .models import Category, Product, LaptopSpec, HeadphoneSpec, Stock, Order, OrderItem, brand_category
from django.utils.html import format_html


class HeadphoneSpecInline(admin.StackedInline):
    model = HeadphoneSpec
    max_num = 1
    extra = 0

class LaptopSpecInline(admin.StackedInline):
    model = LaptopSpec
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [HeadphoneSpecInline, LaptopSpecInline]
    list_display = ('display_image', 'brand_name', 'brand_category', 'model', 'year', 'formatted_price', 'category', 'id')
    list_filter = ('brand_category', 'year', 'category')

    def display_image(self, obj):
        url = reverse('admin:home_product_change', args=[obj.id])
        return format_html('<a href="{}"><img src="{}" style="width: 70px; height: 70px; object-fit: contain;" /></a>'.format(url, obj.images.url)) if obj.images else "No Image"

    display_image.short_description = 'Product Image'
    display_image.allow_tags = True 

    def formatted_price(self, obj):
        print(f"DEBUG: Original Price: {obj.price}")
        formatted_price = f"${obj.price}" if obj.price % 1 != 0 else f"${int(obj.price)}"
        print(f"DEBUG: Formatted Price: {formatted_price}")
        return formatted_price
    formatted_price.short_description = 'Price'


class LaptopSpecAdmin(admin.ModelAdmin):
    list_display = ('product_brand_name', 'product_model','display_product_image', 'price_with_dollar', 'cpu', 'memory', 'storage', 'graphics_card', 'display', 'operating_system')

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

    product_model.short_description = 'Model'

    def price_with_dollar(self, obj):
        return f"${int(obj.product.price)}" if obj.product else ""
    
    price_with_dollar.short_description = 'Price'

    def display_product_image(self, obj):
        if obj.product and obj.product.images:
            return format_html('<img src="{}" style="width: 70px; height: 70px; object-fit: contain;" />', obj.product.images.url)
        return "N/A" 

    display_product_image.short_description = 'Product Image'


class HeadphoneSpecAdmin(admin.ModelAdmin):
    list_display = ('product_brand_name', 'product_model', 'display_images','driver_size', 'frequency_response', 'impedance', 'noise_cancellation', 'connector_type', 'weight', 'battery_life')

    def product_brand_name(self, obj):
        if obj.product:
            return obj.product.brand_name if obj.product.brand_name else "N/A"
        return "N/A"

    product_brand_name.short_description = 'Brand Name'

    def product_model(self, obj):
        if obj.product:
            return obj.product.model if obj.product.model else "N/A"
        return "N/A"

    product_model.short_description = 'Model'

    def display_images(self, obj):
        if obj.product and obj.product.images:
            return format_html('<img src="{}" style="width: 70px; height: 70px; object-fit: contain;" />'.format(obj.product.images.url))
        return "No Image"

    display_images.short_description = 'Product Images'

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

from django import forms
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the widget for the product field to display brand_name, model, and year
        self.fields['product'].queryset = self.fields['product'].queryset.select_related('brand_category')
        self.fields['product'].label_from_instance = lambda obj: f"{obj.brand_name} - Model: {obj.model} - Year: {obj.year}"

class StockAdmin(admin.ModelAdmin):
    form = StockForm
    list_display = ('product_display', 'display_image', 'quantity', 'price_per_unit_with_dollar', 'total_price_with_dollar')

    def product_display(self, obj):
        return f"{obj.product.brand_name} - {obj.product.model} - {obj.product. year}"
    product_display.short_description = 'Product'

    def display_image(self, obj):
        url = reverse('admin:home_product_change', args=[obj.product.id])
        return format_html('<a href="{}"><img src="{}" style="width: 70px; height: 70px; object-fit: contain;" /></a>'.format(url, obj.product.images.url)) if obj.product.images else "No Image"
    display_image.short_description = 'Product Image'
    display_image.allow_tags = True 

    def price_per_unit_with_dollar(self, obj):
        formatted_price_per_unit = "${}".format(obj.price_per_unit())
        return formatted_price_per_unit.rstrip('0').rstrip('.') if '.' in formatted_price_per_unit else formatted_price_per_unit
    price_per_unit_with_dollar.short_description = 'Price per Unit'

    def total_price_with_dollar(self, obj):
        formatted_total_price = "${}".format(obj.total_price())
        return formatted_total_price.rstrip('0').rstrip('.') if '.' in formatted_total_price else formatted_total_price
    total_price_with_dollar.short_description = 'Total Price'





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
admin.site.register(LaptopSpec, LaptopSpecAdmin)
admin.site.register(HeadphoneSpec, HeadphoneSpecAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(brand_category)