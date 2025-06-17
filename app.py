import streamlit as st
import sqlite3
import pandas as pd


def load_data():
    conn = sqlite3.connect("baseball.db")
    
    batting_avg = pd.read_sql_query("SELECT * FROM batting_avg", conn)
    home_runs = pd.read_sql_query("SELECT * FROM home_runs", conn)
    career_strikeouts = pd.read_sql_query("SELECT * FROM career_strikeouts", conn)
    
    conn.close()
    
    return batting_avg, home_runs, career_strikeouts


df_batting, df_home_runs, df_career_strikeouts = load_data()

st.sidebar.header("Filters")

years = sorted(df_batting["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

max_home_runs = int(df_home_runs["Career_Home_Runs"].max())
selected_home_runs = st.sidebar.slider("Minimum Career Home Runs", 0, max_home_runs, 100)

leagues = sorted(df_career_strikeouts["League"].unique())
selected_league = st.sidebar.selectbox("Select League", leagues)

# -------Main dashboard --------
st.title(" ⚾ Baseball Stats Dashboard")

# Batting Average Distribution for Selected Year
st.header(f"Batting Averages in {selected_year}")
df_year = df_batting[df_batting['Year'] == selected_year]
st.bar_chart(df_year.set_index("Name")["Batting_Average"])

# Top Career Home Runs
st.header(f"Players with ≥ {selected_home_runs} Career Home Runs")
df_hr = df_home_runs[df_home_runs['Career_Home_Runs'] >= selected_home_runs]
st.dataframe(df_hr.sort_values("Career_Home_Runs", ascending=False)[["Name", "Career_Home_Runs"]])
st.bar_chart(df_hr.set_index("Name")["Career_Home_Runs"])

# Career Strikeouts by League
st.header(f"Career Strikeouts in {selected_league} League")
df_strikeouts = df_career_strikeouts[df_career_strikeouts['League'] == selected_league]
st.line_chart(df_strikeouts.set_index("Name")["Career_Strikeouts"])

# Combined Stats for a Player
st.header("🔍 Combined Stats for a Player")
player_list = sorted(df_batting["Name"].unique())
selected_player = st.selectbox("Select Player", player_list)
df_combined = (
    df_batting[df_batting["Name"] == selected_player]
    .merge(df_home_runs, on="Name", how="left")
    .merge(df_career_strikeouts, on="Name", how="left")
)
if not df_combined.empty:
    st.write(df_combined.set_index("Name"))
else:
    st.write("No combined stats found for this player.")