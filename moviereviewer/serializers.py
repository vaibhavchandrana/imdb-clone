from rest_framework import serializers
from .models import Genre,Movie,SimilarMovie,Cast,Reviews,WatchList

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
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
    movie_id = MovieSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        fields = '__all__'
