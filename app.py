import streamlit as st
import pickle
import pandas as pd
import requests
import os


# Function to download the large file dynamically from Google Drive
def download_large_file():
    file_id = "12QsufaBXWapJhKFbA2dmHfdB7zklvXxC"
    output_filename = "similarity.pkl"

    # Only download if the file doesn't exist locally on the server yet
    if not os.path.exists(output_filename):
        with st.spinner("Downloading machine learning model... Please wait..."):
            url = f"https://google.com{file_id}"
            response = requests.get(url, stream=True)
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)


# Run the download function before trying to open the file
download_large_file()


# Your existing pickle opening code stays below here:
# similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c5009cf7a26dfa0a4df31b08344ddec4&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies =[]
    recommended_movies_poster = []
    for i in movies_list:
        movie_id =movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies= pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Select Movie to recommend', movies['title'].values)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
