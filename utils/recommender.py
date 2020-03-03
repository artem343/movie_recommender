from movie_rec.models import Rating, Movie
from users.models import Profile, User
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:

    def __init__(self, user: User):
        self.user = user

    def __str__(self):
        return f"Recommender for user {self.user.id}"

    def get_preferences_unstacked(self):

        df = pd.DataFrame.from_records(Rating.objects.all().values())

        df_unstacked = df \
            .groupby(['user_id', 'movie_id'])['rating'] \
            .first() \
            .unstack(1) \
            .fillna(0.0)

        return df, df_unstacked

    def get_cosine_similarity_matrix(self, df, df_unstacked):

        cosim_df = pd.DataFrame(
            cosine_similarity(df_unstacked),
            index=df_unstacked.index,
            columns=df_unstacked.index
        )

        return cosim_df

    def get_user_watched_movies(self):

        movie_list = list(Rating.objects.filter(
            user_id=self.user.id).values_list('movie_id', flat=True))

        return movie_list

    def get_recommendations(self, n: int = 5):
        user_watched_movies = self.get_user_watched_movies()
        if not len(user_watched_movies):
            return []
        df, df_unstacked = self.get_preferences_unstacked()

        cosim_df = self.get_cosine_similarity_matrix(df, df_unstacked)

        buddy = cosim_df[self.user.id].sort_values().index[-2]
        buddy_favs = list(
            df_unstacked.iloc[buddy].sort_values(ascending=False).index)
        recommendations = [
            x for x in buddy_favs if x not in user_watched_movies]
        print(f"the buddy is {buddy}")
        return list(Movie.objects.filter(id__in=recommendations[:n]))


if __name__ == "__main__":
    r = Recommender(User.objects.get(id=611))
    recs = r.get_recommendations()
    print(recs)
