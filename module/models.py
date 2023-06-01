from django.db import models

class SkpValues(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Значение Скп'
        verbose_name_plural = 'Значения Скп'


class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.year}'


class Country(models.Model):
    country_name = models.CharField(max_length=200, unique=True, verbose_name='Страна')

    def __str__(self):
        return self.country_name
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Product(models.Model):
    code_product = models.CharField(max_length=50)
    product_name = models.TextField(verbose_name='Продукт')
    skp          = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Detail(models.Model):
    price   = models.FloatField(null=True, blank=True)
    duty    = models.FloatField(null=True, blank=True)
    year    = models.ForeignKey(Year, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='countries')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

class Gdp(models.Model):
    name              = models.CharField(max_length=300)
    economic_activity = models.CharField(max_length=50)
    gdp               = models.FloatField(null=True, blank=True)
    year              = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'ВВП'
        verbose_name_plural = 'ВВП'

class Import_export_for_db(models.Model):
    name    = models.CharField(max_length=300)
    skp     = models.CharField(max_length=50)
    year    = models.ForeignKey(Year, on_delete=models.CASCADE)
    _import	= models.FloatField(null=True, blank=True)
    export  = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Импорт-Экспорт'
        verbose_name_plural = 'Импорт-Экспорт'

class X_and_C_for_db(models.Model):
    name                = models.CharField(max_length=300)
    skp                 = models.CharField(max_length=50)
    year                = models.ForeignKey(Year, on_delete=models.CASCADE)
    all_used_resources	= models.FloatField(null=True, blank=True)
    final_demand        = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'X-C'
        verbose_name_plural = 'X-C'

    def __str__(self):
        return self.name

class Matrix(models.Model):
    A  = models.FloatField(null=True, blank=True)
    B  = models.FloatField(null=True, blank=True)
    C  = models.FloatField(null=True, blank=True)
    D  = models.FloatField(null=True, blank=True)
    E  = models.FloatField(null=True, blank=True)
    F  = models.FloatField(null=True, blank=True)
    G  = models.FloatField(null=True, blank=True)
    H  = models.FloatField(null=True, blank=True)
    I  = models.FloatField(null=True, blank=True)
    J  = models.FloatField(null=True, blank=True)
    K  = models.FloatField(null=True, blank=True)
    L  = models.FloatField(null=True, blank=True)
    M  = models.FloatField(null=True, blank=True)
    N  = models.FloatField(null=True, blank=True)
    O  = models.FloatField(null=True, blank=True)
    P  = models.FloatField(null=True, blank=True)
    Q  = models.FloatField(null=True, blank=True)
    R  = models.FloatField(null=True, blank=True)
    S  = models.FloatField(null=True, blank=True)
    T  = models.FloatField(null=True, blank=True)
    U  = models.FloatField(null=True, blank=True)
    V  = models.FloatField(null=True, blank=True)
    W  = models.FloatField(null=True, blank=True)
    X  = models.FloatField(null=True, blank=True)
    Y  = models.FloatField(null=True, blank=True)
    Z  = models.FloatField(null=True, blank=True)
    AA = models.FloatField(null=True, blank=True)
    AB = models.FloatField(null=True, blank=True)
    AC = models.FloatField(null=True, blank=True)
    AD = models.FloatField(null=True, blank=True)
    AE = models.FloatField(null=True, blank=True)
    AF = models.FloatField(null=True, blank=True)
    AG = models.FloatField(null=True, blank=True)
    AH = models.FloatField(null=True, blank=True)
    AI = models.FloatField(null=True, blank=True)
    AJ = models.FloatField(null=True, blank=True)
    AK = models.FloatField(null=True, blank=True)
    AL = models.FloatField(null=True, blank=True)
    AM = models.FloatField(null=True, blank=True)
    AN = models.FloatField(null=True, blank=True)
    AO = models.FloatField(null=True, blank=True)
    AP = models.FloatField(null=True, blank=True)
    AQ = models.FloatField(null=True, blank=True)
    AR = models.FloatField(null=True, blank=True)
    AS = models.FloatField(null=True, blank=True)
    AT = models.FloatField(null=True, blank=True)
    AU = models.FloatField(null=True, blank=True)
    AV = models.FloatField(null=True, blank=True)
    AW = models.FloatField(null=True, blank=True)
    AX = models.FloatField(null=True, blank=True)
    AY = models.FloatField(null=True, blank=True)
    AZ = models.FloatField(null=True, blank=True)
    BA = models.FloatField(null=True, blank=True)
    BB = models.FloatField(null=True, blank=True)
    BC = models.FloatField(null=True, blank=True)
    BD = models.FloatField(null=True, blank=True)
    BE = models.FloatField(null=True, blank=True)
    BF = models.FloatField(null=True, blank=True)
    BG = models.FloatField(null=True, blank=True)
    BH = models.FloatField(null=True, blank=True)
    BI = models.FloatField(null=True, blank=True)
    BJ = models.FloatField(null=True, blank=True)
    BK = models.FloatField(null=True, blank=True)
    BL = models.FloatField(null=True, blank=True)
    BM = models.FloatField(null=True, blank=True)
    BN = models.FloatField(null=True, blank=True)
    BO = models.FloatField(null=True, blank=True)
    BP = models.FloatField(null=True, blank=True)
    BQ = models.FloatField(null=True, blank=True)
    BR = models.FloatField(null=True, blank=True)
    BS = models.FloatField(null=True, blank=True)
    BT = models.FloatField(null=True, blank=True)
    BU = models.FloatField(null=True, blank=True)
    BV = models.FloatField(null=True, blank=True)
    BW = models.FloatField(null=True, blank=True)
    BX = models.FloatField(null=True, blank=True)
    BY = models.FloatField(null=True, blank=True)
    BZ = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.A
    class Meta:
        verbose_name_plural = 'Матрица'







