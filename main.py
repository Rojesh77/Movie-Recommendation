from flask import Flask, request, render_template
import requests
import pandas as pd
import pickle

app = Flask(__name__)

movie = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie)

similarity = pickle.load(open('similarity.pkl', 'rb'))



# function to fetch movie poster

def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=d407e9b21a2d3ddb0969dd8f6b89ffc3&language=en-US".format(movie_id)

    data = requests.get(url)

    data = data.json()

    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    return full_path


# Function to fetch movie details from TMDb
def fetch_movie_details(movie_id):
    # TMDb API endpoint for movie details
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d407e9b21a2d3ddb0969dd8f6b89ffc3&language=en-US'
    
    # Make a GET request to TMDb API
    response = requests.get(url)
    
    if response.status_code == 200:
        movie_details = response.json()
        return movie_details
    else:
        return None

# Function to get recommended movies
def get_recommendations(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    movie_titles = []
    movie_posters = []
    movie_ids = []
    movie_release_date = []
    movie_overview = []
    movie_genres = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_ids.append(movie_id)
        movie_titles.append(movies.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))
        movie_details = fetch_movie_details(movie_id)
        
        if movie_details:    
         movie_release_date.append(fetch_movie_details(movie_id).get('release_date'))
         movie_overview.append(fetch_movie_details(movie_id).get('overview'))
         movie_genres.append(',' .join([genre['name'] for genre in fetch_movie_details(movie_id).get('genres', [])]))
        # movie_genres.apppend(fetch_movie_details(movie_id).get('genres'))
        # genres = ', '.join([genre['name'] for genre in movie_details.get('genres', [])])
        else:
            movie_release_date.append(None)
            movie_overview.append(None)
            movie_genres.append(None)
    

    return movie_titles, movie_posters, movie_ids, movie_release_date, movie_genres, movie_overview


@app.route('/index2')
def index2():
     movie_list = movies['title'].tolist()
     return render_template('index2.html',
                            movie_list=movie_list,
                            )
# Recommendation page
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['selected_movie']
    recommended_movie_titles, recommended_movie_posters, recommended_movie_ids, movie_release_date, movie_genres, movie_overview = get_recommendations(movie_title)

    # Fetch popular movies again (can be optimized to avoid duplicate calls)
    url = f'https://api.themoviedb.org/3/movie/popular?api_key=d407e9b21a2d3ddb0969dd8f6b89ffc3&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        popular_movies = data.get('results')
    else:
        popular_movies = []

    return render_template('index2.html',
                       recommended_movie_ids=recommended_movie_ids,
                       movies=popular_movies,
                       recommended_movie_titles=recommended_movie_titles,
                       recommended_movie_posters=recommended_movie_posters,
                       movie_release_date = movie_release_date,
                       movie_genres =movie_genres,
                       movie_overview = movie_overview,
                       movie_list=movies['title'].tolist(),
                       
                       )
# home page
@app.route('/')
def HOME():
    movie_list = movies['title'].tolist()
    return render_template('index1.html', movie_list=movie_list)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():     
    return render_template('services.html')

@app.route('/about')
def about():    
    return render_template('about.html')

# New function to fetch cast and crew with their images
def fetch_cast_and_crew(movie_id):
    api_key = 'd407e9b21a2d3ddb0969dd8f6b89ffc3'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
    response = requests.get(url)
    cast_and_crew = {'cast': [], 'crew': []}

    if response.status_code == 200:
        data = response.json()
        cast = data['cast'][:5]
        crew = data['crew'][:10]
        # crew = data.get('crew', [])

        #many name were coming multiple time so i made a small change to store unique cast and crew
        # Create sets to store unique names for both cast and crew
        unique_cast_names = set()
        unique_crew_names = set()


        # Fetch images for cast
        for actor in cast:
            actor_name = actor.get('name')
            actor_role = actor.get('character')  # Assuming 'character' field contains the role
            actor_profile_path = actor.get('profile_path')
          
            if actor_profile_path and actor_name not in unique_cast_names : 
            # if actor_profile_path and actor_name not in unique_cast_names and actor_rating is not None and actor_rating > 20:
                actor_image_url = f'https://image.tmdb.org/t/p/w500{actor_profile_path}'
                cast_and_crew['cast'].append({'name': actor_name, 'role': actor_role, 'image_url': actor_image_url})
                unique_cast_names.add(actor_name)

        # Fetch images for crew
        for member in crew:
            crew_name = member.get('name')
            crew_role = member.get('job')  # Assuming 'job' field contains the role
            crew_profile_path = member.get('profile_path')

            if crew_profile_path and crew_name not in unique_crew_names:
                crew_image_url = f'https://image.tmdb.org/t/p/w500{crew_profile_path}'
                cast_and_crew['crew'].append({'name': crew_name, 'role': crew_role, 'image_url': crew_image_url})
                unique_crew_names.add(crew_name)

    return cast_and_crew

    

@app.route('/show_movie')
def show_movie(): 
    movie_id = request.args.get('movie_id')

    if movie_id:
        # Fetch movie details from TMDb using movie_id
        movie_details = fetch_movie_details(movie_id)

        if movie_details:
            # Extract necessary details (e.g., poster, overview, release date, genre)
            poster_path = fetch_poster(movie_id)
            title = movie_details.get('title')
            overview = movie_details.get('overview')
            release_date = movie_details.get('release_date')
            genres = ', '.join([genre['name'] for genre in movie_details.get('genres', [])])

            # Fetch cast and crew with their images
            cast_and_crew = fetch_cast_and_crew(movie_id)

            # Render a template to display movie details along with cast and crew
            return render_template('moviedetail.html',
                                   poster_path=poster_path,
                                   title=title,
                                   overview=overview,
                                   release_date=release_date,
                                   genres=genres,
                                   cast=cast_and_crew['cast'],
                                   crew=cast_and_crew['crew'])
        else:
            return 'Movie details not found'
    else:
        return 'Movie ID not provided'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
