from email.headerregistry import Group
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path
from django.shortcuts import render
from django import forms
import nested_admin
from get_data import (
    get_data__product_data_for_db,
    get_data__import_export_for_db,
    get_data__gdp_for_db,
    get_data__X_and_C_for_db,
    get_data__matrix_db,
    get_data__skp_values_for_db
)
from .models import (
    Gdp,
    Product, 
    Detail, 
    Country, 
    Import_export_for_db, 
    X_and_C_for_db, 
    Matrix,
    Gdp,
    SkpValues,
    Year
)
from django.contrib import messages

admin.site.unregister(Group)

admin.site.register(Year)

class ExcelImportForm(forms.Form):
    upload_excel_file = forms.FileField(label="Загрузить excel файл")

class DetailInline(nested_admin.NestedStackedInline):
    model = Detail
    search_fields = ('product',)
    list_filter = ('product', 'year')
    extra = 0

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [DetailInline,]
    search_fields = ('product_name', 'id')
    list_filter = ('skp',)
    list_display = ('id', 'code_product','product_name', 'skp')

    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__product_data_for_db(excel_file)
                    if count == "0, all data is exist":
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)


@admin.register(SkpValues) 
class SkpValuesAdmin(admin.ModelAdmin): 
    list_display = 'id', 'code', 'name'

    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__skp_values_for_db(excel_file)
                    if count == "0, all data is exist":
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)

@admin.register(X_and_C_for_db) 
class X_and_C_Admin(admin.ModelAdmin): 
    list_display = ('name', 'skp', 'year', 'all_used_resources', 'final_demand')
    
    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__X_and_C_for_db(excel_file)
                    if count == 0:
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)

 
@admin.register(Gdp) 
class GdpAdmin(admin.ModelAdmin): 
    list_display = ('name', 'economic_activity', 'gdp', 'year') 

    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__gdp_for_db(excel_file)
                    if count == 0:
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)
 
@admin.register(Import_export_for_db) 
class Import_export_Admin(admin.ModelAdmin): 
    list_display = ('name', 'skp', 'year', '_import', 'export')

    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__import_export_for_db(excel_file)
                    if count == 0:
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)

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
    
    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload-excel/',self.upload_excel)]
        return new_url + urls

    def upload_excel(self,request):
        if request.method == "POST":
            excel_file = request.FILES["upload_excel_file"]
            if excel_file.name.endswith('.xlsx'):
                try:
                    count = get_data__matrix_db(excel_file)
                    if count == 0:
                        messages.warning(request,f"{count} data added")
                    else:
                        messages.info(request,f"{count} data added")
                except:
                    messages.error(request,"The wrong excel file. It is not suitable for this model!")
            else:
                messages.error(request,"The wrong file type uploaded")

        form = ExcelImportForm()
        data = {'form':form}
        return render(request, 'admin/excel_upload.html', data)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_filter = ('country_name',)
    search_fields = ('country_name',)

    