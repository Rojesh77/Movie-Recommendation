import pytest
from main import app, fetch_poster, get_recommendations, fetch_cast_and_crew, fetch_movie_details

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_fetch_poster():
    movie_id = 19995 
    poster_url = fetch_poster(movie_id)
    assert poster_url.startswith('https://image.tmdb.org/t/p/w500/')

def test_get_recommendations():
    movie_title = 'Avatar' 
    get_recommendations(movie_title)
    recommended_titles, recommended_posters, recommended_ids = get_recommendations(movie_title)
    assert len(recommended_titles) == 8
    assert len(recommended_posters) == 8
    assert len(recommended_ids) == 8

def test_fetch_cast_and_crew():
    movie_id =19995   
    cast_and_crew = fetch_cast_and_crew(movie_id)
    assert 'cast' in cast_and_crew
    assert 'crew' in cast_and_crew

def test_fetch_movie_details():
    movie_id = 19995 
    movie_details = fetch_movie_details(movie_id)
    assert movie_details is not None