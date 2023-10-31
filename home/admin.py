from django.contrib import admin
from .models import Category, Product, LaptopSpec, HeadphoneSpec, Stock, Order, OrderItem, brand_category


class HeadphoneSpecInline(admin.StackedInline):
    model = HeadphoneSpec
    max_num = 1
    extra = 0

class LaptopSpecInline(admin.StackedInline):
    model = LaptopSpec
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [HeadphoneSpecInline, LaptopSpecInline]
    list_display = ('id', 'brand_name', 'brand_category', 'model', 'year', 'formatted_price', 'category')
    list_filter = ('brand_category', 'year', 'category')

    def formatted_price(self, obj):
        price_str = "${:,.2f}".format(obj.price)
        return price_str.rstrip('.00').rstrip('0').rstrip('.') if '.' in price_str else price_str

    formatted_price.short_description = 'Price'

class LaptopSpecAdmin(admin.ModelAdmin):
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
admin.site.register(LaptopSpec, LaptopSpecAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(brand_category)
admin.site.register(HeadphoneSpec)