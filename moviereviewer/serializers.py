from rest_framework import serializers
from .models import Genre, Movie, SimilarMovie, Cast, Reviews
from django.contrib.auth.models import User
from .models import Watchlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Include any other user fields you want


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewsSerializerGet(serializers.ModelSerializer):
    added_by = UserSerializer()  # Serialize the user details

    class Meta:
        model = Reviews
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class SimilarMovieSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = SimilarMovie
        fields = '__all__'


class WatchlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = '__all__'


class WatchlistSerializerGet(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField()
    movie_details = serializers.SerializerMethodField()
    shared_by_details = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = '__all__'

    def get_owner_details(self, obj):
        owner = obj.owner
        if owner:
            return {
                'id': owner.id,
                'username': owner.username,
                'email': owner.email  # You can include more fields as needed
            }
        return None

    def get_movie_details(self, obj):
        movie = obj.movies
        if movie:
            return {
                'id': movie.id,
                'title': movie.title,
                'rating': movie.vote_average,
                'poster_path': movie.poster_path,
                'release_date': movie.release_date
            }
        return None

    def get_shared_by_details(self, obj):
        shared_by = obj.shared_by
        if shared_by:
            return {
                'id': shared_by.id,
                'username': shared_by.username,
                'email': shared_by.email  # Include more fields as needed
            }
        return None
