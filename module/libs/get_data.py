from module.models import (
    Product, Detail, Country, Year, 
    Import_export_for_db, Gdp,
    X_and_C_for_db, Matrix, SkpValues
)
import pandas as pd

class DATA:
    def get_data__skp_values_for_db(file):
        created_data_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')
        for i in df.values:
            
            skp, created_skp = SkpValues.objects.get_or_create(code=i[0], name=i[1])
            
            if created_skp==True:
                created_data_len += 1
                
        return created_data_len   

    def get_data__product_data_for_db(file):
        created_products_len = 0
        created_details_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')
        for i in df.values:
            c, created_country = Country.objects.get_or_create(country_name=i[6])

            y, created_year = Year.objects.get_or_create(year=i[3])

            p, created_product = Product.objects.get_or_create(code_product=i[0], product_name=i[1].strip(), skp=i[2])

            if created_product==True:
                created_products_len += 1


            if (i[4]=='-' and i[5]=='-'):
                detail, created_detail = Detail.objects.get_or_create(year=y, price=None, duty=None, product=p, country=c)
            elif i[4]=='-':
                detail, created_detail = Detail.objects.get_or_create(year=y, price=None, duty=i[5], product=p, country=c)
            elif i[5]=='-':
                detail, created_detail = Detail.objects.get_or_create(year=y, price=i[4], duty=None, product=p, country=c)
            else:
                detail, created_detail = Detail.objects.get_or_create(year=y, price=i[4], duty=i[5], product=p, country=c)
            
            if created_detail==True:
                created_details_len += 1

        if created_products_len == 0 and created_details_len== 0:
            return '0, all data is exist'
        else:
            return f"created_products_len: {created_products_len}, created_details_len {created_details_len}"


    def get_data__import_export_for_db(file):
        created_data_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')
        for i in df.values:
            year, created_year = Year.objects.get_or_create(year=i[2])

            if (i[3]=='-' and i[4]=='-'):
                import_export, created_import_export = Import_export_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,_import=None,export=None)
            elif i[3]=='-':
                import_export, created_import_export = Import_export_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,_import=None,export=i[4])
            elif i[4]=='-':
                import_export, created_import_export = Import_export_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,_import=i[3],export=None)
            else:
                import_export, created_import_export = Import_export_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,_import=i[3],export=i[4])
            
            if created_import_export==True:
                created_data_len += 1

        return created_data_len


    def get_data__gdp_for_db(file):
        created_data_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')
        for i in df.values:
            year, created_year = Year.objects.get_or_create(year=i[3])

            if i[2]=='-':
                gdp, created_gdp = Gdp.objects.get_or_create(name=i[0].strip(),economic_activity=i[1],gdp=None,year=year)
                if created_gdp==True:
                    created_data_len += 1
            else:
                gdp, created_gdp = Gdp.objects.get_or_create(name=i[0].strip(),economic_activity=i[1],gdp=i[2],year=year)
                if created_gdp==True:
                    created_data_len += 1

        print(created_data_len)
        return created_data_len

    def get_data__X_and_C_for_db(file):
        created_data_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')

        for i in df.values:
            year, created_year = Year.objects.get_or_create(year=i[2])

            if (i[3]=='-' and i[4]=='-'):
                x_c, created_x_c = X_and_C_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=None,final_demand=None)
            elif i[3]=='-':
                x_c, created_x_c = X_and_C_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=None,final_demand=i[4])
            elif i[4]=='-':
                x_c, created_x_c = X_and_C_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3],final_demand=None)
            else:
                x_c, created_x_c = X_and_C_for_db.objects.get_or_create(name=i[0].strip(),skp=i[1],year=year,all_used_resources=i[3],final_demand=i[4])
            
            if created_x_c==True:
                created_data_len += 1

        return created_data_len


    def get_data__matrix_db(file):
        created_data_len = 0
        df = pd.read_excel(file)
        df = df.fillna('-')
        for i in df.values:
            matrix, created_x_c = Matrix.objects.get_or_create(
                A= i[0], B= i[1], C= i[2], D= i[3], E= i[4], F= i[5], G= i[6], H= i[7], I= i[8], J= i[9], K= i[10], L= i[11], M= i[12], N= i[13], O= i[14], P= i[15], Q= i[16], 
                R= i[17], S= i[18], T= i[19], U= i[20], V= i[21], W= i[22], X= i[23], Y= i[24], Z= i[25], AA= i[26], AB= i[27], AC= i[28], AD= i[29], AE= i[30], AF= i[31], AG= i[32], 
                AH= i[33], AI= i[34], AJ= i[35], AK= i[36], AL= i[37], AM= i[38], AN= i[39], AO= i[40], AP= i[41], AQ= i[42], AR= i[43], AS= i[44], AT= i[45], AU= i[46], AV= i[47], 
                AW= i[48], AX= i[49], AY= i[50], AZ= i[51], BA= i[52], BB= i[53], BC= i[54], BD= i[55], BE= i[56], BF= i[57], BG= i[58], BH= i[59], BI= i[60], BJ= i[61], BK= i[62], 
                BL= i[63], BM= i[64], BN= i[65], BO= i[66], BP= i[67], BQ= i[68], BR= i[69], BS= i[70], BT= i[71], BU= i[72], BV= i[73], BW= i[74], BX= i[75], BY= i[76], BZ= i[77]
            )
            if created_x_c==True:
                created_data_len += 1

        return created_data_len

