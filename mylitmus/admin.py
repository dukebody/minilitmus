from django.contrib import admin

# Register your models here.
from mylitmus.models import Product, Category, Test, Result

class TestInline(admin.StackedInline):
    model = Test

class CategoryAdmin(admin.ModelAdmin):
    inlines = [TestInline]
    extra = 3

class ResultAdmin(admin.ModelAdmin):
    list_display = ('testID', 'locale', 'passed', 'comments')
    list_filter = ('testID', 'passed', 'locale')

admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Result, ResultAdmin)