import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Using columns for each recommended movie pair
    for name1, poster1, name2, poster2 in zip(recommended_movie_names[::2], recommended_movie_posters[::2], recommended_movie_names[1::2] + [''], recommended_movie_posters[1::2] + ['']):
        col1, col2 = st.columns(2)

        with col1:
            if poster1:
                st.markdown(f'<div style="background-color: #cccccc;border:1px solid #ccc; padding:10px; display: flex; flex-direction: column; justfiy-center: center; align-items: center"><img src="{poster1}" width="325">Title<div style="padding: 10px; color: #1d1d1d; font-size: 20px; font-weight: 700"><i>{name1}</i></div></div><br/>', unsafe_allow_html=True)
                

        with col2:
            if poster2:
                st.markdown(f'<div style="background-color: #cccccc;border:1px solid #ccc; padding:10px; display: flex; flex-direction: column; justfiy-center: center; align-items: center"><img src="{poster2}" width="325">Title<div style="padding: 10px; color: #1d1d1d; font-size: 20px; font-weight: 700"><i>{name2}</i></div></div><br/>', unsafe_allow_html=True)
                
