from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .forms import ProductAdd
# Register your models here.
from .models import Product, Category, ProductImages, Viewer

class ProductAdd(admin.ModelAdmin):
    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass
@admin.register(ProductImages)
class ProductImagesAdmin(ImportExportModelAdmin):
    pass
@admin.register(Viewer)
class ViewerAdmin(ImportExportModelAdmin):
    pass
