# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 00:40:13 2021

@author: Ronald Nyasha Kanyepi
@email : kanyepironald@gmail.com
"""
import os
from datetime import datetime

import dataloader
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from PIL import Image
from requests.exceptions import ConnectionError
import plotly.graph_objects as go
from datetime import date,datetime
import plotly.express as px
import plotly.graph_objects as go



def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'logo.ico'))
    st.set_page_config(page_title='COVID-DASHBOARD', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    st.balloons()
    # I want it to show balloon when it finished loading all the configs


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def list_of_countries():
    df = pd.read_csv("./components/csv/countries.csv")
    return df["Name"].tolist()


def covid_data_menu():
    st.subheader('Covid Data Menu')
    col1, col2, col3 = st.columns([4, 4, 4])
    with col1:
        st.text_input(label="Last Updated", value=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), disabled=True)
    with col2:
        pass
    with col3:
        try:
            url = "https://disease.sh/v3/covid-19/countries"
            response = requests.get(url)
            countries = [i.get("country") for i in response.json()]
            option = st.selectbox('please select country?', (countries), help="Please select country")


        except ConnectionError:
            st.error("There is a connection error we failed to fetch all the countries 😥")
    try:
        response = requests.get("https://disease.sh/v3/covid-19/countries/" + option)
        data = response.json()

        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Country Info")
            country_data = data.pop("countryInfo")
            longitude, latitude = country_data["long"], country_data["lat"]
            country_data.update({"country": data["country"]})
            country_data.pop("lat")
            country_data.pop("long")
            # df = pd.DataFrame.from_dict(country_data, orient="index", dtype=str, columns=['Value'])
            # st.dataframe(df)
            remote_css("")
            st.markdown(f"""
               <table class="table table-borderless">
                    <tr>
                      <td>country</td>
                      <td>{country_data["country"]}</td>
                    </tr>
                     <tr>
                      <td>flag</td>
                      <td><img src="{country_data["flag"]}" style="width:20%;height:40%"></td>
                    </tr>
                    <tr>
                      <td>iso2</td>
                      <td>{country_data["iso2"]}</td>
                    </tr>
                    <tr>
                      <td>iso3</td>
                      <td>{country_data["iso3"]}</td>
                    </tr>
               </table></br>
            """, unsafe_allow_html=True)

            st.write("Covid Statistics")
            data.pop("country")
            data['updated'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            df = pd.DataFrame.from_dict(data, orient="index", dtype=str, columns=['Value'])
            st.write(df)

        with col2:
            st.write("Map")
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=latitude,
                    longitude=longitude,
                    zoom=4.7,
                    pitch=50,
                )
            ))

        st.subheader("Vaccination Data")
        current_date = datetime.today().date()
        first_day_of_month = current_date.replace(day=1)
        number_of_days = (date.today() - first_day_of_month).days

        url = "https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=" + str(number_of_days)
        response = requests.get(url)
        vaccination_data = {}
        for i in response.json():
            if i.get("country") == option:
                vaccination_data = i.get("timeline")

        if len(vaccination_data) != 0:
            vaccination_data = {str(key): str(value) for key, value in vaccination_data.items()}
            st.write(vaccination_data)
            df = pd.DataFrame({'date': vaccination_data.keys(), 'vaccination_value': vaccination_data.values()})
            trace = go.Bar(x=df['date'], y=df['vaccination_value'], showlegend=True)
            layout = go.Layout(title=option)
            data = [trace]
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig)
        else:
            st.write("Vaccination data for %s no available" % option)

        with st.expander('Covid 19 Prevention Tips'):
            st.subheader("Here’s what you can do to protect yourself:")
            st.markdown(f"""<p>At International Medical Corps, we’re always preparing for the unexpected—whether it’s
            an earthquake, a hurricane or an outbreak of infectious disease. As the COVID-19 outbreak grows,
            it’s important to know that there are many actions we can take to protect ourselves, our loved ones and
            our communities.</p>""", unsafe_allow_html=True)

            st.subheader("Here’s what you can do to protect yourself:")
            st.markdown(f""" <ul> <li>Wash your hands frequently with soap and water for at least 20 seconds.</li>
            <li>If soap and water are not available, use an alcohol-based hand sanitizer with at least 60%
            alcohol.</li> <li>Avoid close contact with people who are sick.</li> <li>Especially if you’re in a
            high-risk group, consider limiting your exposure to others, using social distancing—for example,
            avoid large gatherings, crowds of people and frequent trips to the store.</li>
            </li>Visit your state and local public-health websites for additional guidance specific to your area.</li>
             <li>Those at higher risk for serious illness should take additional precautions.</li>
              </ul> """, unsafe_allow_html=True)

            st.markdown(
                f"""</br> Reference for Tips : <a href="https://internationalmedicalcorps.org/emergency-response/covid-19/coronavirus-prevention-tips/">IMC</a>""",
                unsafe_allow_html=True)
        st.text("source : https://disease.sh/v3/covid-19/countries")
    except ConnectionError as e:
        st.error("There is a connection error please retry later 😥")


def vacc_tab():
    st.title("Impact of vaccination on COVD.")
    option = st.selectbox(
    'What country would you like to display ?',
    ("United States", "France", "Brazil", "Japan", "Cameroon", "China"))
    st.plotly_chart(dataloader.display_vacc_covid_graph(option))
    st.text("Even though most country implemented some type of vaccination, the effect seems to vary from one to another.")
    st.text("source : OWID (Our World In Data)")
    st.plotly_chart(dataloader.dvlp_index)

def confine_tab():
    st.title("l'impact de confinement")
    fig = go.Figure()

    lock = [
        {"Lockdown": "Lockdown 1", "Start date": "March 17, 2020", "End date": "May 11, 2020"},
        {"Lockdown": "Lockdown 2", "Start date": "October 30, 2020", "End date": "December 15, 2020"},
        {"Lockdown": "Lockdown 3", "Start date": "April 3, 2021", "End date": "May 2, 2021"}
    ]

    lockdown = pd.DataFrame(lock)
    vacc_DF = pd.read_csv(dataloader.path3,parse_dates=True)

    # print(vacc_DF.Country.loc['France'])

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.selectbox(
        "Select the City:",
        options=vacc_DF.Country.unique(),
        # default='France',
    )
    df_selection = vacc_DF.query(
        "Country == @city"
    )

    #### lockdown and it's effect on new cases #####

    # getting the data frame beased on the country selected
    df = pd.DataFrame(df_selection, columns=["Date_reported", "New_cases"]).fillna(0)


    df['Date_reported'] = pd.to_datetime(df['Date_reported'],format='%d/%m/%Y')
    lockdown['Start date'] = pd.to_datetime(lockdown['Start date'])
    lockdown['End date'] = pd.to_datetime(lockdown['End date'])

    # .dt.strftime('%d/%m/%Y')

    # Group the data by month and cumulate the 'New_cases' column       


    fig=px.line(df.head(700),x='Date_reported',y='New_cases',
            title="<b> lockdown and it's effect on new cases</b>",
            color_discrete_sequence=["#0083B8"] * len(df.head(700)),
        )
    fig.update_xaxes(rangeslider_visible=True)

    fig.add_vrect(
        x0=lockdown.loc[0]['Start date'],x1=lockdown.loc[0]['End date'],
        fillcolor="violet", opacity=0.5,
        layer="below", line_width=0,
        annotation_text="Confinement 1",
    )
    fig.add_vrect(
        x0=lockdown.loc[1]['Start date'],x1=lockdown.loc[1]['End date'],
        fillcolor="violet", opacity=0.5,
        layer="below", line_width=0,
        annotation_text="Confinement 2",
        
    )
    fig.add_vrect(
        x0=lockdown.loc[2]['Start date'],x1=lockdown.loc[2]['End date'],
        fillcolor="violet", opacity=0.5,
        layer="below", line_width=0,
        annotation_text="Confinement 3",
    )
    fig.add_trace(go.Scatter(x=lockdown['Start date'], mode="markers"))
    fig.add_trace(go.Scatter(x=lockdown['End date'], mode="markers"))


    # fig.update_layout(
    #     xaxis=dict(tickmode="linear"),  
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    st.plotly_chart(fig, use_container_width=True)
    


def main():
    config()
    st.sidebar.subheader("COVID-19 DASHBOARD")
    menu = ["COVID-19 DATA","Impact of vaccination", "Effectiveness of confining"]
    choice = st.sidebar.selectbox("", menu)
    if (choice == "COVID-19 DATA") :
        covid_data_menu()
    elif (choice == "Impact of vaccination") :
        vacc_tab() 
    elif (choice == "Effectiveness of confining") :
        confine_tab()


if __name__ == '__main__':
    main()
