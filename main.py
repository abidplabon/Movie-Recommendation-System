import streamlit as stl
import pickle
import pandas as pd
import requests



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c1bf277847a77074dd072d49175feb96&language=en-US'.format(movie_id))
    #convert it to json format
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



#movie recommend function here again
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        #error line or else it will take data index instead of movie index
        movie_id = movies.iloc[i[0]].movie_id
        #getting poster from the TMDB api

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
#convert the pickle get obj into a dataframe
movies      = pd.DataFrame(movies_dict)

stl.title('Movie Recommender System')

selected_movie_name = stl.selectbox(
    '',
    movies['title'].values
)


if stl.button('Recommend'):
    name,poster = recommend(selected_movie_name)
    #for i in recommendations:
    #    stl.write(i)

    col1, col2, col3, col4, col5 = stl.columns(5)

    with col1:
        stl.text(name[0])
        stl.image(poster[0])

    with col2:
        stl.text(name[1])
        stl.image(poster[1])

    with col3:
        stl.text(name[2])
        stl.image(poster[2])

    with col4:
        stl.text(name[3])
        stl.image(poster[3])

    with col5:
        stl.text(name[4])
        stl.image(poster[4])
