import streamlit as st
import pandas as pd
# import dataloader as data

# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# df
# data.cov_vac_display('FRANCE')

lock = [
    {"Lockdown": "Lockdown 1", "Start date": "March 17, 2020", "End date": "May 11, 2020"},
    {"Lockdown": "Lockdown 2", "Start date": "October 30, 2020", "End date": "December 15, 2020"},
    {"Lockdown": "Lockdown 3", "Start date": "April 3, 2021", "End date": "May 2, 2021"}
]

lockdown = pd.DataFrame(lock)
print(lockdown.loc[0]['Start date'])