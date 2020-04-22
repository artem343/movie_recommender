# Movie Recommender

A simple Django app with a movie recommendaion system, based on __cosine similarity__ between users' preferences.

## Try it
1. Go to [movies.artempetrov.work](https://movies.artempetrov.work)
1. Log in or register.
1. Open the "Rate" page and rate some movies.
1. Open the "Recommendations" page and see whether you like your recommendations.

## Run it locally
1. Clone the repository:
    ```
    git clone https://github.com/artem343/movie_recommender.git
    ```
2. Download the MovieLens 100K dataset from https://www.kaggle.com/rajmehra03/movielens100k into `data/*.csv`
3. Run:
    ```
    python manage.py migrate users
    python manage.py migrate
    python manage.py runserver
    ```
