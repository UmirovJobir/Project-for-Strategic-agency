from email.headerregistry import Group
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import admin
import nested_admin
from .models import (
    Gdp,
    Product, 
    Detail, 
    Country, 
    Import_export_for_db, 
    X_and_C_for_db, 
    Matrix,
    Gdp
)
admin.site.unregister(Group)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_filter = ('country_name',)
    search_fields = ('country_name',)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('code_product','product_name', 'skp')
#     search_fields = ('product_name',)

# @admin.register(Detail)
# class DetailAdmin(admin.ModelAdmin):
#     list_filter = ('product_id',)
#     search_fields = ('product_id',)

@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_filter = ('A',)
    search_fields = ('A',)
    list_display = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
                    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 
                    'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 
                    'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 
                    'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 
                    'BV', 'BW', 'BX', 'BY', 'BZ')


class DetailInline(nested_admin.NestedStackedInline):
    model = Detail
    search_fields = ('product',)
    list_filter = ('product', 'year')
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [DetailInline,]
    search_fields = ('product_name',)
    list_filter = ('skp',)
    list_display = ('code_product','product_name', 'skp')
admin.site.register(Product, ProductAdmin)

@admin.register(X_and_C_for_db) 
class X_and_C_Admin(admin.ModelAdmin): 
    list_display = ('name', 'skp', 'year', 'all_used_resources', 'final_demand') 
 
@admin.register(Gdp) 
class GdpAdmin(admin.ModelAdmin): 
    list_display = ('name', 'economic_activity', 'gdp', 'year') 
 
 
@admin.register(Import_export_for_db) 
class Import_export_Admin(admin.ModelAdmin): 
    list_display = ('name', 'skp', 'year', '_import', 'export')