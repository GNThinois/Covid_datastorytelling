import pandas as pd

path1 = '../data/owid-covid-data.csv'
path2 = '../data/vaccination-data.csv'
path3 = '../data/WHO-COVID-19-global-data.csv'

def cov_vac_display(name_of_country):
    #On charge les 2 csv
    covid_DF = pd.read_csv(path1)
    vacc_DF = pd.read_csv(path3)
    #Liste des pays présent dans chaque csv
    list_of_country_covid = covid_DF.location.unique()
    list_of_country_vacc = vacc_DF.Country.unique()
    #Liste des pays en communs dans les 2 listes des pays
    country_in_both_df = set(list_of_country_covid) & set(list_of_country_vacc)
    
    #Crée un graphe pour le pays demandé si présent dans la liste commune
    if name_of_country in country_in_both_df :
        country_covid_DF = covid_DF[covid_DF['location'] == name_of_country]
        country_vacc_DF = vacc_DF[vacc_DF['Country'] == name_of_country]
        joined_DF = country_covid_DF.set_index('date').join(country_vacc_DF.set_index('Date_reported'))
        return joined_DF
    else:
        print('Not in df')


def display_vacc_covid_graph(country):
    df = pd.read_csv(path1)
    country_DF = df[df['location'] == country]
    data = pd.DataFrame(country_DF, columns=["date", "new_cases_per_million", "new_vaccinations_smoothed_per_million", "new_deaths"]).fillna(0)
    data.plot(x="date", y=["new_cases_per_million", "new_vaccinations_smoothed_per_million", "new_deaths"],
        kind="line", figsize=(10, 10), title=country)
    print(data)


#x = input('Pays à afficher:')
#x = 'France'
#display_vacc_covid_graph(x)


# data = cov_vac_display('France')
# data = pd.DataFrame(data, columns=["date", "new_cases"]).fillna(0)
# print(data)