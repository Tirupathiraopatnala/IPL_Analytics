import streamlit as st
import pandas as pd
import plotly.express as px
from headtohead_analytics import head_to_head_analysis
from playeranalytics import playerAnalytics
from about import about

st.set_page_config(page_title="IPL Analytics",
                    page_icon=":cricket_bat_and_ball:")
st.title("IPL Analytics from 2008 to 2023!")

match_data = pd.read_csv("./data/match_data.csv")
match_info_data = pd.read_csv("./data/match_info_data.csv")
ipl_data = pd.merge(match_data, match_info_data, left_on='match_id', right_on='id')
# print(ipl_data.columns)

# player_df.to_csv('./data/playernames.csv')
tab1,tab2 = st.tabs(["Head-to-Head Analysis", "About"])

with tab1:
    head_to_head_analysis(ipl_data)
with tab2:
#     playerAnalytics(ipl_data)
      about()
# with tab3:
#     about()

# horizontal menu
# selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal")

