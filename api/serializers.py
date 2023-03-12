from rest_framework import serializers
from .models import MovieList,Plateform,Reviews
       
class ReviewSerailizer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Reviews
        # fields="__all__"
        exclude=('movielist',)



class MovieListSerializer(serializers.ModelSerializer):
    movieReview=ReviewSerailizer(many=True,read_only=True)
    class Meta:
        model=MovieList
        fields="__all__"
        # fields=['name','desc']
        # exclude=['active']

class PlateformSerializer(serializers.ModelSerializer):
    MovieList=MovieListSerializer(many=True, read_only=True)

    class Meta:
        model=Plateform
        fields="__all__"
    