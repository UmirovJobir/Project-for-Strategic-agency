import os,django
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()

from new_app.libs.psql import db_clint
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from numpy import inner, ndarray, product
from pandas import DataFrame
import warnings
warnings.filterwarnings('ignore')

def swap_columns(df,col1,col2):
    col_list = list(df.columns)
    x,y = col_list.index(col1),col_list.index(col2)
    col_list[y],col_list[x] = col_list[x],col_list[y]
    df = df[col_list]
    return df

#FIRST MODUL

def data_reading(countries:list,skp:list): #returning filtered DataFrame with all skp and country product groups entered by the user (lists from Djobir)
    database = db_clint.read_sql()
    country_filter = database['country_name'].isin(countries)
    df_with_filter = database[country_filter]
    skp_filter = df_with_filter['skp'].isin(skp)
    df_with_filter = df_with_filter[skp_filter]
    return df_with_filter

def year(data:DataFrame): #func to know in which year we now
    return data['year'].unique()

def creating_duties(years:ndarray,data:DataFrame,skp:list): #creating skp groups duties
    columns = ['skp','value','year']
    duty = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = data[(data['year'] == i) & (data['skp'] == j)]
            duty.loc[len(duty.index)] = [frame['skp'].unique(),frame['duty'].mean(),frame['year'].unique()]
    return duty

def creating_import(years:ndarray,data:DataFrame,skp:list): #creating skp groups import
    columns = ['skp','value','year']
    imp = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = data[(data['year'] == i) & (data['skp'] == j)]
            new_skp = frame['skp'].unique()
            new_year = frame['year'].unique()
            imp.loc[len(imp.index)] = [new_skp[0],frame['price'].sum(),new_year[0]]
    return imp

def elasticity_calculating(duty:DataFrame,imp:DataFrame,skp:list): #calculating elasticity for skp groups
    coef = np.empty((len(skp),2))
    elast = np.empty(len(skp))
    row = 0
    for i in skp:
        j = 0
        kol = 0
        x_frame = duty[duty['skp'] == i]
        y_frame = imp[imp['skp'] == i]
        for elem_x in x_frame['value']:
            if np.isnan(elem_x):
                kol+=1
        for elem_y in y_frame['value']:
            if np.isnan(elem_y):
                kol+=1
        if kol>0:
            coef[row,j]='NaN'
            j+=1
            coef[row,j]='NaN'
        else:
            x = x_frame['value'].values.reshape((-1,1))
            y = y_frame['value'].values
            x = np.log(x.astype('float'))
            y = np.log(y.astype('float'))
            model=LinearRegression().fit(x,y)
            coef[row,j]=model.intercept_
            j+=1
            coef[row,j]=model.coef_
        row += 1
    row = 0
    for i in skp:
        duty_frame = duty[duty['skp'] == i]
        imp_frame = imp[imp['skp'] == i]
        if not (np.isnan(coef[row,1])):
            elast[row] = coef[row,1]*(duty_frame['value'].mean()/imp_frame['value'].mean())
        else:
            elast[row] = 'NaN' # or NULL
        row += 1
    return elast

def adding_new_duties_to_df(data:DataFrame,products:list,duties:list,years:ndarray): #adding new duties from user to DF (lists from Djobir)
    new_duties = data[data['year'] == years[-2]]
    new_duties.set_index('product_name',drop=False,inplace=True)
    j = 0
    for i in products:
        new_duties.loc[i,'duty'] = duties[j]
        j += 1
    new_duties.reset_index(drop=True,inplace=False)
    new_duties.loc[:,'year'] = years[-1]
    data = pd.concat([data,new_duties])
    return data

def adding_new_import(years:ndarray,skp:list,elasticity:ndarray,alpha:float,duty:DataFrame,imp:DataFrame): #import forecast for the new year
    j = 0
    for i in skp:
        new_duty = duty.loc[(duty['skp'] == i) & (duty['year'] == years[-1])]
        old_duty = duty.loc[(duty['skp'] == i) & (duty['year'] == years[-2])]
        old_import = imp.loc[(imp['skp'] == i) & (imp['year'] == years[-2])]
        new_duty = new_duty['value'].values
        old_duty = old_duty['value'].values
        old_import = old_import['value'].values
        new_value = (1 + alpha + elasticity[j] * (new_duty[0] - old_duty[0]))*old_import[0]
        imp.loc[(len(imp.index))] = [i,new_value,years[-1]]
        j += 1
    return imp

def dollars_to_million_sums(imp:DataFrame,exchange_rate:float):
    imp.loc[:,'value'] *= exchange_rate
    imp.loc[:,'value'] /= 1000
    return imp

def first_modul_main(countries:list,skp:list,products:list,duties:list,user_year:int,alpha:float,exchange_rate:float): #we need alpha and end year of prediction
    data = data_reading(countries,skp)
    years = year(data)
    duty = creating_duties(years,data,skp)
    imp = creating_import(years,data,skp)
    elasticity = elasticity_calculating(duty,imp,skp)
    starting_point = years[-1]
    j = 0
    for i in range(starting_point,user_year):
        years = np.append(years,i+1)
        print(i)
        data = adding_new_duties_to_df(data,products,duties[j],years)
        duty = creating_duties(years,data,skp)
        imp = adding_new_import(years,skp,elasticity,alpha,duty,imp)
        elasticity = elasticity_calculating(duty,imp,skp)
        j += 1
    elasticity_for_API = elasticity.tolist()
    imp = dollars_to_million_sums(imp,exchange_rate)
    return {"imp":imp, "elasticity": elasticity_for_API}

#SECOND MODUL

def creating_all_import(all_import_export:DataFrame): #creating import dataframe from DB to all skp groups
    all_import = all_import_export.drop(columns=['export'],axis=1)
    all_import.rename(columns={'year': 'year'},inplace=True)
    all_import = swap_columns(all_import,'_import','year')
    return all_import

def creating_all_export(all_import_export:DataFrame): #creating export dataframe from DB to all skp groups
    all_export = all_import_export.drop(columns=['_import'],axis=1)
    all_export.rename(columns={'year': 'year'},inplace=True)
    all_export = swap_columns(all_export,'export','year')
    return all_export

def creating_all_used_resources(all_used_resources_final_demand:DataFrame): #creating all_used_resources dataframe from DB to all skp groups
    all_used_resources = all_used_resources_final_demand.drop(columns=['final_demand'],axis=1)
    all_used_resources.rename(columns={'year': 'year'},inplace=True)
    all_used_resources = swap_columns(all_used_resources,'all_used_resources','year')
    return all_used_resources

def creating_all_final_demand(all_used_resources_final_demand:DataFrame): #creating all_final_demand dataframe from DB to all skp groups
    all_final_demand = all_used_resources_final_demand.drop(columns=['all_used_resources'],axis=1)
    all_final_demand.rename(columns={'year': 'year'},inplace=True)
    return all_final_demand

def other_import(all_imp:DataFrame,imp:DataFrame,skp:list,years:ndarray): #deduction of modified import to selected countries from total import
    import_frame = imp.loc[imp['year'] == years[-1]]
    all_imp_frame = all_imp.loc[all_imp['year'] == years[-1]]
    all_imp = all_imp.loc[all_imp['year'] != years[-1]]
    all_imp_frame.set_index('skp',drop=False,inplace=True)
    import_frame.set_index('skp',drop=False,inplace=True)
    for i in skp:
        all_imp_frame.loc[i,'_import'] -= import_frame.loc[i,'value']
    all_imp_frame.reset_index(drop=True,inplace=True)
    all_imp = pd.concat([all_imp,all_imp_frame])
    return all_imp

def import_forecast(other_imp:DataFrame,years:ndarray,alpha:float): #forecasting total import excluding import to selected countries
    skp = other_imp['skp'].unique()
    new_imp = other_imp[other_imp['year'] == years[-2]]
    new_imp.set_index('skp',drop=False,inplace=True)
    for i in skp:
        if ((i.find('F') != -1 or i.find('H') != -1 or i.find('G') != -1 or i.find('B') != -1 or i.find('L') != -1 or i.find('O') != -1 or i.find('P') != -1) and years[-1] >= 2030):
            new_imp.loc[i,'_import'] *= (1 + alpha)
        elif ((i.find('Q') != -1 or i.find('D') != -1 or i.find('J') != -1 or i.find('K') != -1 or i.find('S') != -1 or i.find('I') != -1 or i.find('N') != -1 or i.find('M') != -1 or i.find('R') != -1 or i.find('E') != -1) and years[-1] >= 2025):
            new_imp.loc[i,'_import'] *= (1 + alpha)
    new_imp.reset_index(drop=True,inplace=True)
    new_imp['year'] = years[-1]
    other_imp = pd.concat([other_imp,new_imp])
    return other_imp

def export_forecast(all_exp:DataFrame,years:ndarray,alpha_exp:float): #forecasting total export
    skp = all_exp['skp'].unique()
    new_exp = all_exp[all_exp['year'] == years[-2]]
    new_exp.set_index('skp',drop=False,inplace=True)
    for i in skp:
        if ((i.find('F') != -1 or i.find('H') != -1 or i.find('G') != -1 or i.find('B') != -1 or i.find('L') != -1 or i.find('O') != -1 or i.find('P') != -1) and years[-1] >= 2030):
            new_exp.loc[i,'export'] *= (1 + alpha_exp)
        elif ((i.find('Q') != -1 or i.find('D') != -1 or i.find('J') != -1 or i.find('K') != -1 or i.find('S') != -1 or i.find('I') != -1 or i.find('N') != -1 or i.find('M') != -1 or i.find('R') != -1 or i.find('E') != -1) and years[-1] >= 2025):
            new_exp.loc[i,'export'] *= (1 + alpha_exp)
    new_exp.reset_index(drop=True,inplace=True)
    new_exp['year'] = years[-1]
    all_exp = pd.concat([all_exp,new_exp])
    return all_exp    

def final_import_forecast(other_imp:DataFrame,imp:DataFrame,starting_year:int,skp:list): #forecasting total import, taking into account import to selected countries
    all_imp = other_imp.loc[other_imp['year'] < starting_year + 1]
    import_frame = imp.loc[imp['year'] >= starting_year + 1]
    all_imp_frame = other_imp.loc[other_imp['year'] >= starting_year + 1]
    all_imp_frame.set_index('skp',drop=False,inplace=True)
    import_frame.set_index('skp',drop=False,inplace=True)
    for i in skp:
        all_imp_frame.loc[i,'_import'] += import_frame.loc[i,'value']
    all_imp_frame.reset_index(drop=True,inplace=True)
    all_imp = pd.concat([all_imp,all_imp_frame])
    return all_imp

def final_demand_forecast(final_demand:DataFrame,all_imp:DataFrame,years:ndarray): #forecasting final demand
    skp = final_demand['skp'].unique()
    new_final_demand = final_demand[final_demand['year'] == years[-2]]
    old_import = all_imp[all_imp['year'] == years[-2]]
    new_final_demand.set_index('skp',drop=False,inplace=True)
    old_import.set_index('skp',drop=False,inplace=True)
    old_final_demand = new_final_demand
    for i in skp:
        new_final_demand.loc[i,'final_demand'] = old_final_demand.loc[i,'final_demand'] + 0.2 * old_import.loc[i,'_import']
    new_final_demand.reset_index(drop=True,inplace=True)
    new_final_demand['year'] = years[-1]
    final_demand = pd.concat([final_demand,new_final_demand])
    return final_demand

def create_inverse_matrix(technological_matrix:DataFrame): #creation of the inverse matrix of the technological matrix
    identity_matrix = np.eye(78)
    technological_matrix.drop(columns=['id'],axis=1,inplace=True)
    technological_matrix = technological_matrix.astype(np.float64).to_numpy()
    technological_matrix = np.subtract(identity_matrix,technological_matrix)
    inverse_matrix = np.linalg.inv(technological_matrix)
    return inverse_matrix

def used_resources_forecast(used_resources:DataFrame,final_demand:DataFrame,inverse_matrix:ndarray,years:ndarray): #forecasting used resources
    new_used_resources = used_resources[used_resources['year'] == years[-2]]
    final_demand_frame = final_demand[final_demand['year'] == years[-1]]
    c = final_demand_frame['final_demand'].values
    x = np.dot(inverse_matrix,c)
    new_used_resources['all_used_resources'] = x
    new_used_resources['year'] = years[-1]
    used_resources = pd.concat([used_resources,new_used_resources])
    return used_resources

def creating_economic_activity(data:DataFrame,economic_activities:ndarray,economic_activities_name:ndarray): #association of commodity industries into types of economic activity
    years = year(data)
    cols = data.columns
    columns = ['name','economic_activity','value','year']
    economic_activities_frame = pd.DataFrame(columns=columns)
    for i in years:
        k = 0
        for j in economic_activities:
            frame = data[(data['year'] == i) & (data['skp'].str.contains(j))]
            economic_activities_frame.loc[len(economic_activities_frame.index)] = [economic_activities_name[k],j,frame[cols[2]].sum(),i]
            k += 1
    return economic_activities_frame

def gdp_forecast(gdp:DataFrame,e_a_used_resources:DataFrame,e_a_export:DataFrame,e_a_import:DataFrame,economic_activities:ndarray,years:ndarray,economic_activities_name:ndarray): #forecasting GDP using linear regression
    k = 0
    for i in economic_activities:
        x = np.empty(0)
        new_x = np.empty(0)
        y_frame = gdp[gdp['economic_activity'] == i]
        y = y_frame['gdp'].values
        for j in range(years[0],years[-1]):
            frame_1 = e_a_used_resources[(e_a_used_resources['economic_activity'] == i) & (e_a_used_resources['year'] == j)]
            frame_2 = e_a_export[(e_a_export['economic_activity'] == i) & (e_a_export['year'] == j)]
            frame_3 = e_a_import[(e_a_import['economic_activity'] == i) & (e_a_import['year'] == j)]
            x = np.append(x,[frame_1.iloc[0,2],frame_2.iloc[0,2],-1 * frame_3.iloc[0,2]])
        x = np.reshape(x,(years[-1]-years[0],3))
        model = LinearRegression().fit(x,y)
        frame_1 = e_a_used_resources[(e_a_used_resources['economic_activity'] == i) & (e_a_used_resources['year'] == years[-1])]
        frame_2 = e_a_export[(e_a_export['economic_activity'] == i) & (e_a_export['year'] == years[-1])]
        frame_3 = e_a_import[(e_a_import['economic_activity'] == i) & (e_a_import['year'] == years[-1])]
        new_x = np.append(new_x,[frame_1.iloc[0,2],frame_2.iloc[0,2],-1 * frame_3.iloc[0,2]])
        new_x = np.reshape(new_x,(1,3))
        y_pred = model.predict(new_x)
        y_pred = float(y_pred)
        gdp.loc[len(gdp.index)] = [economic_activities_name[k],i,y_pred,years[-1]]
        k += 1
    return gdp

def second_modul_main(first_module_result:DataFrame,user_year:int,skp:list,alpha:float,alpha_exp:float): #we take the result of the work of the first module and the alpha of exports, the result is a forecast of GDP by type of activity
    technological_matrix = db_clint.matrix()
    inverse_matrix = create_inverse_matrix(technological_matrix)
    all_import_export = db_clint.import_export_for_db()
    all_used_resources_final_demand = db_clint.x_and_c_for_db()
    gdp = db_clint.gdp()
    economic_activities = gdp['economic_activity'].unique()
    economic_activities_name = gdp['name'].unique()
    years_imp_exp = all_import_export['year'].unique()
    years_ur_fd = all_used_resources_final_demand['year'].unique()
    years_gdp = gdp['year'].unique()

    used_resources = creating_all_used_resources(all_used_resources_final_demand)
    final_demand = creating_all_final_demand(all_used_resources_final_demand)
    all_imp = creating_all_import(all_import_export)
    all_exp = creating_all_export(all_import_export)

    other_imp = other_import(all_imp,first_module_result,skp,years_imp_exp)
    starting_point = years_imp_exp[-1]
    for i in range(starting_point,user_year):
        years_imp_exp = np.append(years_imp_exp,i+1)
        other_imp = import_forecast(other_imp,years_imp_exp,alpha)
        all_exp = export_forecast(all_exp,years_imp_exp,alpha_exp)
    all_imp = final_import_forecast(other_imp,first_module_result,starting_point,skp)
    all_exp.fillna(0,inplace=True)
    all_imp.fillna(0,inplace=True)

    starting_point_1 = years_ur_fd[-1]
    for i in range(starting_point_1,user_year):
        years_ur_fd = np.append(years_ur_fd, i+1)
        final_demand = final_demand_forecast(final_demand,all_imp,years_ur_fd)
        used_resources = used_resources_forecast(used_resources,final_demand,inverse_matrix,years_ur_fd)

    economic_activity_import = creating_economic_activity(all_imp,economic_activities,economic_activities_name)
    economic_activity_export = creating_economic_activity(all_exp,economic_activities,economic_activities_name)
    economic_activity_used_resources = creating_economic_activity(used_resources,economic_activities,economic_activities_name)
    starting_point_2 = years_gdp[-1]
    for i in range(starting_point_2,user_year):
        years_gdp = np.append(years_gdp,i+1)
        gdp = gdp_forecast(gdp,economic_activity_used_resources,economic_activity_export,economic_activity_import,economic_activities,years_gdp,economic_activities_name)
    return gdp
    
#comment2


if __name__ == '__main__':
    country_id = ['Армения','Беларусь','Казахстан','Кыргызстан','Российская Федерация']
    skp = ['C13','C14','C15','C21','C29','C30']
    duties = [[5,12,25,7,10,15],
    [4,11,24,6,9,14],
    [3,10,23,5,8,13],
    [2,9,22,4,7,12],[1,8,21,3,6,11],[0,7,20,2,5,10],[0,6,19,1,4,9],[0,5,18,0,3,8],[0,4,17,0,2,7],[0,3,16,0,1,6],[0,2,15,0,0,5],
    [0,1,14,0,0,4],[0,0,13,0,0,3],[0,0,12,0,0,2],[0,0,11,0,0,1],[0,0,10,0,0,0]]
    products = ['МЕХ ИСКУССТВЕННЫЙ И ИЗДЕЛИЯ ИЗ НЕГО',
    'ПРЕДМЕТЫ ОДЕЖДЫ И ПРИНАДЛЕЖНОСТИ К ОДЕЖДЕ, ИЗ НАТУРАЛЬНОЙ КОЖИ ИЛИ КОМПОЗИЦИОННОЙ КОЖИ:ПРЕДМЕТЫ ОДЕЖДЫ:ИЗ НАТУРАЛЬНОЙ КОЖИ',
    'ДУБЛ.КОЖА ИЛИ КОЖЕВЕН.КРАСТ ИЗ ШКУР К.Р.С.(ВКЛ. БУЙВОЛ),ЖИВОТ.СЕМ-ВА ЛОШАДИНЫХ,...:ВО ВЛАЖНОМ СОСТ.(ВКЛ.ХРОМИРОВАНН.ПОЛУФАБРИКАТ):НЕШЛИФОВ.ЛИЦЕВЫЕ НЕДВОЕНЫЕ;ЛИЦЕВЫЕ ДВОЕНЫЕ:ИЗ ЦЕЛЫХ ШКУР К.Р.С.(ВКЛ.БУЙВОЛ),ПЛОЩАДЬ ПОВЕРХН.КОТ.< 2,6 М2 (28 КВАДРАТ.ФУТОВ)',
    'КИСЛОТЫ КАРБОНОВЫЕ, СОДЕРЖАЩИЕ ФЕНОЛЬНУЮ ГРУППУ, НО НЕ СОДЕРЖАЩИЕ ДРУГУЮ КИСЛОРОДСОДЕРЖАЩУЮ ФУНКЦИОНАЛЬНУЮ ГРУППУ, ИХ АНГИДРИДЫ, ГАЛОГЕНАНГИДРИДЫ, ПЕРОКСИДЫ, ПЕРОКСИКИСЛОТЫ И ИХ ПРОИЗВОДНЫЕ: САЛИЦИЛОВАЯ КИСЛОТА И ЕЕ СОЛИ',
    'ПРОЧИЕ ИЗДЕЛИЯ ИЗ СВИНЦА:ПРОЧИЕ',
    'ЖЕЛЕЗНОДОРОЖНЫЕ ЛОКОМОТИВЫ, С ПИТАНИЕМ ОТ ВНЕШНЕГО ИСТОЧНИКА ЭЛЕКТРОЭНЕРГИИ, ИЛИ АККУМУЛЯТОРНЫЕ: С ПИТАНИЕМ ОТ ЭЛЕКТРИЧЕСКИХ АККУМУЛЯТОРОВ']
    user_year = 2035
    alpha = 0.05
    alpha_exp = 0.03
    exchange_rate = 11000.0
    res = first_modul_main(country_id,skp,products,duties,user_year,alpha,exchange_rate)
    print(res['imp'])
    # res_2 = second_modul_main(res,user_year,skp,alpha,alpha_exp)
    # print(res_2)
