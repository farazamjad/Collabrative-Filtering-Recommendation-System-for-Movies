import pandas as pd
import numpy as np
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ipynb.fs.full.CollaborativeFiltering import movie_recommender_run

#Set page configuration
st.set_page_config(layout = "wide", page_title = "Movie Recommendation App", page_icon = ":Cinema:")

#Write code to call movie_recommender_run and display recommendations
col_names=['user_id','user_name','Movie_ID','rating','timestamp']
movies_df=pd.read_csv('Movie_data.csv',sep=',',names=col_names)
n_users=movies_df.user_name.unique()

st.header("Collabrative filtering recommendation system")

User_name=st.selectbox("Select a user name:", (n_users))

st.write("this user might be interested in the following movies: ")
result=movie_recommender_run(User_name)
st.table(result.Movie_Title)
#Display movie rating charts here
ids= result.Movie_ID
Names=result.Movie_Title
fig = make_subplots(
    rows=5, cols=2,
    subplot_titles=(Names),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}] 
    ])

# x_row and y_col will determine the location of a plot in the plot-grid
x_row=1
y_col=1
for i in range (len(result)):
    temp=(movies_df.loc[movies_df['Movie_ID'] == ids[i]]).groupby('rating').user_id.count().reset_index()
    
    Rating=temp.rating.to_numpy()
    User_ID= temp.user_id.to_numpy()

    x_row= int( i/2 +1)
    y_col= i%2 + 1
    
    fig.add_trace(go.Bar(x=[1,2,3,4,5], y=User_ID), row=x_row, col=y_col)

fig.update_layout(height=900,width=800, showlegend=False, title= "Ratings of Suggested Movies")

st.plotly_chart(fig, use_container_width=True)