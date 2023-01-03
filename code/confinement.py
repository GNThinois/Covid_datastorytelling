import dataloader as data
import pandas as pd
import streamlit as st
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go



fig = go.Figure()

st.set_page_config(page_title="l'impact de confinement", page_icon=":bar_chart:", layout="wide")
lock = [
    {"Lockdown": "Lockdown 1", "Start date": "March 17, 2020", "End date": "May 11, 2020"},
    {"Lockdown": "Lockdown 2", "Start date": "October 30, 2020", "End date": "December 15, 2020"},
    {"Lockdown": "Lockdown 3", "Start date": "April 3, 2021", "End date": "May 2, 2021"}
]

lockdown = pd.DataFrame(lock)
vacc_DF = pd.read_csv(data.path3,parse_dates=True)

# print(vacc_DF.Country.loc['France'])

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=vacc_DF.Country.unique(),
    default='France',
)
df_selection = vacc_DF.query(
    "Country == @city"
)
# st.table(df_selection)
df = pd.DataFrame(df_selection, columns=["Date_reported", "New_cases"]).fillna(0)
# .reset_index(drop=True)
# st.table(df.head(50))
df['Date_reported'] = pd.to_datetime(df['Date_reported'],format='%d/%m/%Y')
lockdown['Start date'] = pd.to_datetime(lockdown['Start date'])
lockdown['End date'] = pd.to_datetime(lockdown['End date'])

# .dt.strftime('%d/%m/%Y')

# Group the data by month and cumulate the 'New_cases' column       
# df['year'] = df['Date_reported'].dt.year.astype(int)
# df['month'] = df['Date_reported'].dt.month.astype(int)
# left_column, right_column = st.columns(2)
# st.line_chart(df)
print(len(df))
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
st.stop()
# st.table(df['month'])
df_monthly = df.groupby(['month','year'])['New_cases'].sum()
# df_monthly = df_monthly.rename('month','year','cases')

st.table(df_monthly) 
# Convert the Series to a DataFrame
df_monthly = df_monthly.to_frame()
# Set the 'month' column as the index

# df_monthly = df_monthly.set_index('month')
st.line_chart(df_monthly['New_cases'])
df_cumulative = df.groupby(df['Date_reported'].dt.month)['New_cases'].cumsum()

# SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["Date_reported"])
print(df["Date_reported"])
fig_hourly_sales = px.line(
    df_cumulative,
    x=df['Date_reported'].dt.month,
    y=df_cumulative,
    title="<b> lockdown and it's effect on new cases</b>",
    color_discrete_sequence=["#0083B8"] * len(df_cumulative),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),  
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)

st.stop()
print(df_selection)
datas = data.cov_vac_display(df_selection)
df = pd.DataFrame(datas, columns=["date", "new_cases"]).fillna(0)
st.table(df)

