import streamlit as st
import pandas as pd
import plotly.express as px

# match_data = pd.read_csv("./data/match_data.csv")
# match_info_data = pd.read_csv("./data/match_info_data.csv")

# ipl_data = pd.merge(match_data, match_info_data, left_on='match_id', right_on='id')

# Define team colors based on the given color codes
team_colors = {
    'Chennai Super Kings': '#fdb913',
    'Mumbai Indians': '#005da0',
    'Royal Challengers Bangalore': '#c8102e',
    'Kolkata Knight Riders': '#3a225d',
    'Punjab Kings': '#DD1F2D',
    'Kings XI Punjab':  '#DD1F2D',
    'Delhi Capitals': '#004c93',
    'Delhi Daredevils': '#004c93',
    'Rajasthan Royals': '#fd2296',
    'Sunrisers Hyderabad': '#f2720f',
    'Deccan Chargers':'#f2720f',
    'Gujarat Titans':'#1B2133',
    'Lucknow Super Giants':'#0057E2',
    "Rising Pune Supergiants": "#004E8F",  
    "Gujarat Lions": "#FF8C00",  
    "Pune Warriors": "#DC143C", 
    "Kochi Tuskers Kerala": "#006400"  
}

# Function to get head-to-head stats between two teams
def get_head_to_head_stats(team1, team2,ipl_data):
    # Filter the data to include only matches between the two teams
    head_to_head_data = ipl_data[(ipl_data["batting_team"] == team1) & (ipl_data["bowling_team"] == team2) |
                                 (ipl_data["batting_team"] == team2) & (ipl_data["bowling_team"] == team1)]

    # Get unique match IDs and calculate overall wins
    unique_matches = head_to_head_data["match_id"].unique()
    team1_wins = len([match_id for match_id in unique_matches if head_to_head_data[head_to_head_data["match_id"] == match_id]["winner"].values[0] == team1])
    team2_wins = len([match_id for match_id in unique_matches if head_to_head_data[head_to_head_data["match_id"] == match_id]["winner"].values[0] == team2])
    total_matches = len(unique_matches)
    team1_win_percentage = (team1_wins / total_matches) * 100 if total_matches > 0 else 0
    team2_win_percentage = (team2_wins / total_matches) * 100 if total_matches > 0 else 0

    # Calculate venue-wise stats
    venue_wins = head_to_head_data.groupby(["venue", "match_id"])["winner"].apply(lambda x: x.values[0]).reset_index()
    venue_stats = venue_wins.groupby("venue")["winner"].value_counts().unstack(fill_value=0)
    venue_stats = venue_stats.rename(columns={team1: f"{team1} Wins", team2: f"{team2} Wins"})

    team1_bowling_data = head_to_head_data[head_to_head_data["bowling_team"] == team1]
    team1_wicket_count = team1_bowling_data["wicket"].count()
    team1_bowling_stats_agg = team1_bowling_data.agg({
         "wides": "sum", "noballs": "sum","byes":"sum","legbyes":"sum","penalty":"sum","extras":"sum"
    })
    team1_bowling_stats = pd.concat([team1_bowling_stats_agg, pd.Series({"wicket": team1_wicket_count})])

    team2_bowling_data = head_to_head_data[head_to_head_data["bowling_team"] == team2]
    team2_wicket_count = team2_bowling_data["wicket"].count()
    team2_bowling_stats_agg = team2_bowling_data.agg({
         "wides": "sum", "noballs": "sum","byes":"sum","legbyes":"sum","penalty":"sum","extras":"sum"
    })
    team2_bowling_stats = pd.concat([team2_bowling_stats_agg, pd.Series({"wicket": team2_wicket_count})])

    # desired_columns = ["wides", "noballs", "byes", "legbyes", "penalty", "wicket"]

    # # Manually reorder the data in team1_bowling_stats and team2_bowling_stats
    # team1_bowling_stats = [team1_bowling_stats[column] for column in desired_columns]
    # team2_bowling_stats= [team2_bowling_stats[column] for column in desired_columns]

    # Calculate top run-scorers and wicket-takers
    top_scorers = head_to_head_data.groupby(["batting_team", "striker"])["runs_off_bat"].sum().reset_index().sort_values(
        ["batting_team", "runs_off_bat"], ascending=[True, False]
    ).groupby("batting_team").head(1)

    top_scorers = top_scorers.rename(columns={"runs_off_bat": "runs"})  
     
    top_wicket_takers = head_to_head_data[~head_to_head_data["wicket"].isna()].groupby(
        ["bowling_team", "bowler"]
    )["wicket"].count().reset_index().sort_values(["bowling_team", "wicket"], ascending=[True, False]).groupby(
        "bowling_team"
    ).head(1)

    # Calculate toss stats
    toss_stats = head_to_head_data[head_to_head_data["toss_winner"].isin([team1, team2])]
    toss_stats = toss_stats.groupby(["toss_winner", "toss_decision"])["match_id"].nunique().reset_index()
    toss_stats = toss_stats.pivot(index="toss_winner", columns="toss_decision", values="match_id")
    toss_stats = toss_stats.rename_axis(index=None, columns=None)

    return (
        team1_wins,
        team2_wins,
        total_matches,
        team1_win_percentage,
        team2_win_percentage,
        venue_stats,
        team1_bowling_stats,
        team2_bowling_stats,
        top_scorers,
        top_wicket_takers,
        toss_stats,
    )

def head_to_head_analysis(ipl_data):
    team1 = st.selectbox("Select Team 1", ipl_data["batting_team"].unique())
    team2 = st.selectbox("Select Team 2", ipl_data["bowling_team"].unique())

    if (team1 and team2) and (team1!=team2):
        (
            team1_wins,
            team2_wins,
            total_matches,
            team1_win_percentage,
            team2_win_percentage,
            venue_stats,
            team1_bowling_stats,
            team2_bowling_stats,
            top_scorers,
            top_wicket_takers,
            toss_stats,
        ) = get_head_to_head_stats(team1, team2,ipl_data)

        st.subheader(f"{team1} vs {team2} total matches: {total_matches}")

        # Display toss stats and overall wins in a 1x2 grid
        col1, col2 = st.columns(2)  # Equal width for both columns
        with col1:
            st.subheader("Toss Stats")
            st.write(toss_stats)
        with col2:
            st.subheader("Win Percentage")
            fig_overall_wins = px.pie(names=[team1, team2], values=[team1_wins, team2_wins], labels=[team1, team2],
                                    height=300,width=300, color_discrete_sequence=[team_colors[team1], team_colors[team2]])
            fig_overall_wins.update_traces(showlegend=True) 
            st.plotly_chart(fig_overall_wins,align='top')  
        # Display venue stats 
        st.subheader("Venue Stats")
        st.write(venue_stats.style.set_table_styles([{'selector': 'table', 'props': [('text-align', 'center')]}]))

        st.markdown("    ")
        # Display bowling stats of both teams in a 1x2 grid with space in between
        col3, col4 = st.columns(2)
        order_to_display = ["wides", "noballs", "byes", "legbyes", "penalty", "wicket"]
        with col3:
            st.subheader(f"{team1} Bowling Stats")
            st.bar_chart(team1_bowling_stats, use_container_width=True,color=team_colors[team1])  # Use container width to reduce height
        with col4:
            st.subheader(f"{team2} Bowling Stats")
            st.bar_chart(team2_bowling_stats, use_container_width=True,color=team_colors[team2])  # Use container width to reduce height

        # Display top run scorers and wicket takers in a 1x2 grid without index column
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("Top Run Scorers")
            st.write(top_scorers.set_index('striker'))  # Hide the index column
        with col6:
            st.subheader("Top Wicket Takers")
            st.write(top_wicket_takers.set_index('bowler'))  # Hide the index column
    else:
        st.error("Team1 and Team2 can not be same, choose a different team!")

