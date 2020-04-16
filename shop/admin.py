from django.contrib import admin
from .models import Category, Product,Gallary,MainCategory,SubCategory



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category','name',]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['category']
    # autocomplete_fields = ['category']


admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category','name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['category','name']


admin.site.register(SubCategory,SubCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(MainCategory)
admin.site.register(Product, ProductAdmin)

admin.site.register(Gallary)

