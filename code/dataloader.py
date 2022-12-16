import pandas as pd

path1 = '../data/owid-covid-data.csv'
path2 = '../data/vaccination-data.csv'
path3 = '../data/WHO-COVID-19-global-data.csv'

def cov_vac_display(name_of_country):
    covid_DF = pd.read_csv(path1)
    vacc_DF = pd.read_csv(path3)
    list_of_country_covid = covid_DF.location.unique()
    list_of_country_vacc = vacc_DF.Country.unique()
    #print(list_of_country_covid.size)
    #print(list_of_country_vacc.size)
    tmp = set(list_of_country_covid) & set(list_of_country_vacc)
    if 'United states' in tmp :
        print(tmp)

cov_vac_display('aa')