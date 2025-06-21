import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

def load_data():
    conn = sqlite3.connect("baseball.db")
    
    batting_avg = pd.read_sql_query("SELECT * FROM batting_avg", conn)
    home_runs = pd.read_sql_query("SELECT * FROM home_runs", conn)
    career_strikeouts = pd.read_sql_query("SELECT * FROM career_strikeouts", conn)
    
    conn.close()
    
    return batting_avg, home_runs, career_strikeouts


df_batting, df_home_runs, df_career_strikeouts = load_data()

st.sidebar.header("Filters")

# Years & Teams for batting‐avg chart
all_years = sorted(df_batting["Year"].unique())
years = st.sidebar.multiselect("Select Year(s)", all_years, default=all_years)
all_teams = sorted(df_batting["Team"].unique())
teams = st.sidebar.multiselect("Select Team(s)", all_teams, default=all_teams)

# Home‐run slider
max_home_runs = int(df_home_runs["Career_Home_Runs"].max())
min_home_runs = st.sidebar.slider("Career Home Runs", 0, max_home_runs, 100)

# League for strikeouts
leagues = sorted(df_career_strikeouts["League"].unique())
league = st.sidebar.selectbox("Select League", leagues)

# -------Main dashboard --------
st.title(" ⚾ Baseball Stats Dashboard")

# Batting Average: line + point chart by Team over Year
st.header("Batting Average Over Time by Team")
df_line = df_batting.query("Year in @years and Team in @teams")
chart = (
    alt.Chart(df_line)
      .mark_line(point=True)
      .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Batting_Average:Q", title="Batting Average"),
        color=alt.Color("Team:N", title="Team"),
        tooltip=["Name", "Team", "Year", "Batting_Average"]
      )
      .properties(width=800, height=400)
)
st.altair_chart(chart, use_container_width=True)


# Top Career Home Runs: bar chart
st.header(f"Players with ≥ {min_home_runs} Career Home Runs")
df_hr = df_home_runs.query("Career_Home_Runs >= @min_home_runs")
bar = (
    alt.Chart(df_hr.sort_values("Career_Home_Runs", ascending=False))
       .mark_bar()
       .encode(
           x=alt.X("Name:N", sort="-y", title="Player"),
           y=alt.Y("Career_Home_Runs:Q", title="Career Home Runs"),
           tooltip=["Name", "Career_Home_Runs"]
       )
       .properties(width=800, height=300)
)
st.altair_chart(bar, use_container_width=True)
st.dataframe(df_hr[["Name","Career_Home_Runs"]].sort_values("Career_Home_Runs", ascending=False),
             use_container_width=True)


# Career Strikeouts by League: area chart
st.header(f"Career Strikeouts in the {league} League")
df_strikeouts = df_career_strikeouts.query("League == @league").sort_values("Career_Strikeouts")
df_strikeouts["Cumulative"] = df_strikeouts["Career_Strikeouts"].cumsum()
area = (
    alt.Chart(df_strikeouts)
      .mark_area(opacity=0.5)
      .encode(
        x=alt.X("Name:N", sort=None, title="Player"),
        y=alt.Y("Cumulative:Q", title="Cumulative Career Strikeouts"),
        tooltip=["Name", "Career_Strikeouts"]
      )
      .properties(width=800, height=300)
)
st.altair_chart(area, use_container_width=True)


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
    st.write(df_combined.set_index("Year")[["Batting_Average", "Career_Home_Runs", "Career_Strikeouts"]])
else:
    st.write("No combined stats found for this player.")