from new_app.models import (
    Product, Detail, Country, Year, 
    Import_export_for_db, Gdp,
    X_and_C_for_db, Matrix
)
import pandas as pd


def get_data__product_data_for_db(file):
    created_products_len = 0
    created_details_len = 0
    df = pd.read_excel(file)
    df = df.fillna('-')
    for i in df.values:
        try:
            c = Country.objects.get(country_name=i[6])
        except Country.DoesNotExist:
            c = Country.objects.create(country_name=i[6])

        try:
            y = Year.objects.get(year=i[3])
        except Year.DoesNotExist:
            y = Year.objects.create(year=i[3])

        try:
            p = Product.objects.get(code_product=i[0], product_name=i[1].strip(), skp=i[2])
        except Product.DoesNotExist:
            p = Product.objects.create(code_product=i[0], product_name=i[1].strip(), skp=i[2])
            created_products_len += 1
        try:
            if (i[4]=='-' and i[5]=='-'):
                    Detail.objects.get(year=y, price=None, duty=None, product=p, country=c)
            elif i[4]=='-':
                    Detail.objects.get(year=y, price=None, duty=i[5], product=p, country=c)
            elif i[5]=='-':
                    Detail.objects.get(year=y, price=i[4], duty=None, product=p, country=c)
            else:
                    Detail.objects.get(year=y, price=i[4], duty=i[5], product=p, country=c)
        except Detail.DoesNotExist:
            if (i[4]=='-' and i[5]=='-'):
                    Detail.objects.create(year=y, product=p, country=c)
            elif i[4]=='-':
                    Detail.objects.create(year=y, duty=i[5], product=p, country=c)
            elif i[5]=='-':
                    Detail.objects.create(year=y, price=i[4], product=p, country=c)
            else:
                    Detail.objects.create(year=y, price=i[4], duty=i[5], product=p, country=c)
            created_details_len += 1
    created_data = f"created_products_len: {created_products_len}, created_details_len {created_details_len}"
    not_created_data = '0, all data is exist'
    if created_products_len == 0 and created_details_len== 0:
        return not_created_data
    else:
        return created_data

def get_data__import_export_for_db(file):
    created_data_len = 0
    df = pd.read_excel(file)
    df = df.fillna('-')
    for i in df.values:
        try:
            year = Year.objects.get(year=i[2])
        except Year.DoesNotExist:
            year = Year.objects.create(year=i[2])

        try:
            if (i[3]=='-' and i[4]=='-'):
                query = Import_export_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,_import=None,export=None)
            elif i[3]=='-':
                query = Import_export_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,_import=None,export=i[4])
            elif i[4]=='-':
                query = Import_export_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,_import=i[3],export=None)
            else:
                query = Import_export_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,_import=i[3],export=i[4])
        except Import_export_for_db.DoesNotExist:
            if (i[3]=='-' and i[4]=='-'):
                query = Import_export_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year)
            elif i[3]=='-':
                query = Import_export_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,export=i[4])
            elif i[4]=='-':
                query = Import_export_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,_import=i[3])
            else:
                query = Import_export_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,_import=i[3],export=i[4])
            created_data_len += 1
    return created_data_len

def get_data__gdp_for_db(file):
    created_data_len = 0
    df = pd.read_excel(file)
    df = df.fillna('-')
    for i in df.values:
        try:
            year = Year.objects.get(year=i[3])
        except Year.DoesNotExist:
            year = Year.objects.create(year=i[3])

        try:
            if i[2]=='-':
                Gdp.objects.get(name=i[0].strip(),economic_activity=i[1],gdp=None,year=year)
            else:
                Gdp.objects.get(name=i[0].strip(),economic_activity=i[1],gdp=i[2],year=year)
        except Gdp.DoesNotExist:
            if i[2]=='-':
                Gdp.objects.create(name=i[0].strip(),economic_activity=i[1],year=year)
            else:
                Gdp.objects.create(name=i[0].strip(),economic_activity=i[1],gdp=i[2],year=year)
            created_data_len += 1
    return created_data_len

def get_data__X_and_C_for_db(file):
    created_data_len = 0
    df = pd.read_excel(file)
    df = df.fillna('-')
    for i in df.values:
        try:
            year = Year.objects.get(year=i[2])
        except Year.DoesNotExist:
            year = Year.objects.create(year=i[2])

        try:
            if (i[3]=='-' and i[4]=='-'):
                query = X_and_C_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,all_used_resources=None,final_demand=None)
            elif i[3]=='-':
                query = X_and_C_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,all_used_resources=None,final_demand=i[4])
            elif i[4]=='-':
                query = X_and_C_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3],final_demand=None)
            else:
                query = X_and_C_for_db.objects.get(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3],final_demand=i[4])
        except X_and_C_for_db.DoesNotExist:
            if (i[3]=='-' and i[4]=='-'):
                query = X_and_C_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year)
            elif i[3]=='-':
                query = X_and_C_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,final_demand=i[4])
            elif i[4]=='-':
                query = X_and_C_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3])
            else:
                query = X_and_C_for_db.objects.create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3],final_demand=i[4])
            created_data_len += 1
    return created_data_len

def get_data__matrix_db(file):
    created_data_len = 0
    df = pd.read_excel(file)
    df = df.fillna('-')
    for i in df.values:
        try:
            Matrix.objects.get(
                A= i[0], B= i[1], C= i[2], D= i[3], E= i[4], F= i[5], G= i[6], H= i[7], I= i[8], J= i[9], K= i[10], L= i[11], M= i[12], N= i[13], O= i[14], P= i[15], Q= i[16], 
                R= i[17], S= i[18], T= i[19], U= i[20], V= i[21], W= i[22], X= i[23], Y= i[24], Z= i[25], AA= i[26], AB= i[27], AC= i[28], AD= i[29], AE= i[30], AF= i[31], AG= i[32], 
                AH= i[33], AI= i[34], AJ= i[35], AK= i[36], AL= i[37], AM= i[38], AN= i[39], AO= i[40], AP= i[41], AQ= i[42], AR= i[43], AS= i[44], AT= i[45], AU= i[46], AV= i[47], 
                AW= i[48], AX= i[49], AY= i[50], AZ= i[51], BA= i[52], BB= i[53], BC= i[54], BD= i[55], BE= i[56], BF= i[57], BG= i[58], BH= i[59], BI= i[60], BJ= i[61], BK= i[62], 
                BL= i[63], BM= i[64], BN= i[65], BO= i[66], BP= i[67], BQ= i[68], BR= i[69], BS= i[70], BT= i[71], BU= i[72], BV= i[73], BW= i[74], BX= i[75], BY= i[76], BZ= i[77]
            )
        except Matrix.DoesNotExist:
            Matrix.objects.create(
                A= i[0], B= i[1], C= i[2], D= i[3], E= i[4], F= i[5], G= i[6], H= i[7], I= i[8], J= i[9], K= i[10], L= i[11], M= i[12], N= i[13], O= i[14], P= i[15], Q= i[16], 
                R= i[17], S= i[18], T= i[19], U= i[20], V= i[21], W= i[22], X= i[23], Y= i[24], Z= i[25], AA= i[26], AB= i[27], AC= i[28], AD= i[29], AE= i[30], AF= i[31], AG= i[32], 
                AH= i[33], AI= i[34], AJ= i[35], AK= i[36], AL= i[37], AM= i[38], AN= i[39], AO= i[40], AP= i[41], AQ= i[42], AR= i[43], AS= i[44], AT= i[45], AU= i[46], AV= i[47], 
                AW= i[48], AX= i[49], AY= i[50], AZ= i[51], BA= i[52], BB= i[53], BC= i[54], BD= i[55], BE= i[56], BF= i[57], BG= i[58], BH= i[59], BI= i[60], BJ= i[61], BK= i[62], 
                BL= i[63], BM= i[64], BN= i[65], BO= i[66], BP= i[67], BQ= i[68], BR= i[69], BS= i[70], BT= i[71], BU= i[72], BV= i[73], BW= i[74], BX= i[75], BY= i[76], BZ= i[77]
            )
            created_data_len += 1
    return created_data_len

