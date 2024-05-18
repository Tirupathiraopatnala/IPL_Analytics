import streamlit as st
import pandas as pd

def playerAnalytics(ipl_data):
    batters = ipl_data['striker'].unique()
    bowlers = ipl_data['bowler'].unique()
    player_df = pd.Series(list(set(batters) | set(bowlers)))

    col1, col2 = st.columns([0.25, 0.75])
    with col1:
        analytics_type = st.selectbox('Select Analytics Type', ['Batting Analytics', 'Bowling Analytics'])
    with col2:
        selected_player = st.selectbox(
            'Search Player',
            player_df,
            index=None,
            placeholder='Type to search for a player',
            help="Type to search for a player"
        )
    col3, col4 = st.columns([0.3, 0.7])

    with col3:
        st.markdown("### Player Image")
        # Add code to display player image here

    with col4:
        st.markdown("### Player Stats")
        st.markdown("Runs:")
        st.markdown("Balls Faced:")
        st.markdown("Average:")
        st.markdown("Strike rate:")
        st.markdown("Highest score:")
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("4's -")
        with col6:
            st.markdown("6's -")

        col7, col8, col9 = st.columns(3)
        with col7:
            if st.button("Runs by Season"):
                pass
        with col8:
            if st.button("Runs by opp-team"):
                pass
        with col9:
            if st.button("Runs by venue"):
                pass
    