from rest_framework import viewsets, filters,generics,decorators
from rest_framework.views import APIView,status
from .models import Movie,Cast,Genre,Reviews,Cast,WatchList
from .serializers import MovieSerializer,CastSerializer,ReviewsSerializer,GenreSerializer,CastSerializer,WatchlistSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.response import Response
import requests
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [filters.OrderingFilter]  # Enable ordering filter
    ordering_fields = ['vote_average', 'release_date']  # Define fields for sorting

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the sorting field and order from query parameters
        sort_by = request.query_params.get('sort_by', None)
        order = request.query_params.get('order', 'asc')  # Default to ascending order if not specified

        if sort_by:
            if sort_by in self.ordering_fields:
                # Apply sorting based on field and order
                if order == 'desc':
                    sort_by = f'-{sort_by}'  # For descending order
                queryset = queryset.order_by(sort_by)

        # Iterate through queryset and update poster_path
        for movie in queryset:
            movie.poster_path = f"https://image.tmdb.org/t/p/w500/{movie.poster_path}"
            movie.backdrop_path=f"https://image.tmdb.org/t/p/w500/{movie.backdrop_path}"

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MovieSearchView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        print("hello")
        # Get the search query parameter from the request
        query = self.request.query_params.get('query', '')

        # Perform a case-insensitive search for movies with names containing the query
        queryset = Movie.objects.filter(title__icontains=query)
        print(f"Search Query: {query}")
        print(f"Number of Results: {queryset.count()}")

        return queryset


class CastViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer



class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieByGenre(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPageNumberPagination  # Use your custom pagination class

    # Define a custom action to filter movies by selected genres
    @decorators.action(detail=False, methods=['GET'])
    def by_genre(self, request):
        # Get the list of genre IDs from the request query parameters
        genre_ids = request.query_params.getlist('genre_ids')

        # Filter movies by selected genres
        movies = Movie.objects.filter(genre_ids__id__in=genre_ids)

        # Apply pagination
        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serialize the filtered movies and return the response
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class SaveCastData(APIView):
    def get(self, request,movie_id):

        # Define the API URL
        cast_db_data=Cast.objects.filter(movie_id=movie_id)
        if cast_db_data.count()>0:
            serializer = CastSerializer(cast_db_data, many=True)
            return Response(serializer.data) 
        cast_db_ids = set(Cast.objects.filter(movie_id=movie_id).values_list('id', flat=True))
        api_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US'
        
        # Set the authorization header
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I',  # Replace with your API key
            'accept': 'application/json',
        }
        
        # Make the GET request to the API
        response = requests.get(api_url, headers=headers)
        data = response.json()
        print(data)
        # Extract cast data and save it to the Cast model
        cast_data = data.get('cast', [])
        cast_data.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        print(cast_data)

        # Select only the top 10 highest popularity cast members
        cast_data = cast_data[:10]
        cast_objects = []
        for cast_member in cast_data:
            if cast_member['known_for_department']=="Acting" and  cast_member['id'] not in cast_db_ids:
                cast_objects.append({
                    'id': cast_member['id'],
                    'name': cast_member['name'],
                    'character_name': cast_member['character'],
                    'profile_path': f"https://image.tmdb.org/t/p/w500/{cast_member['profile_path']}",
                    'movie_id': movie_id,
                })
        Cast.objects.bulk_create([Cast(**cast) for cast in cast_objects])

        # Serialize and return the saved data
        serializer = CastSerializer(Cast.objects.filter(movie_id=movie_id), many=True)
        return Response(serializer.data)


class ReviewData(APIView):
    def get(self, request,movie_id):

        # Define the API URL
        ReviewData_db_data=Reviews.objects.filter(movie_id=movie_id)
        if ReviewData_db_data.count()>0:
            serializer = ReviewsSerializer(ReviewData_db_data, many=True)
            return Response(serializer.data) 
        cast_db_ids = set(Reviews.objects.filter(movie_id=movie_id).values_list('id', flat=True))
        api_url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1'
        
        # Set the authorization header
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I',  # Replace with your API key
            'accept': 'application/json',
        }
        
        # Make the GET request to the API
        response = requests.get(api_url, headers=headers)
        data = response.json()
        print(data)
        # Extract cast data and save it to the Cast model
        cast_data = data.get('results', [])
       
        print(cast_data)

      
        cast_objects = []
        for review_element in cast_data:
                cast_objects.append({
                    'name':review_element['author'],
                    'review_data':review_element['content'],
                    'created_at':review_element['created_at'],
                    'movie_id': movie_id,
                })
        Reviews.objects.bulk_create([Reviews(**cast) for cast in cast_objects])

        # Serialize and return the saved data
        serializer = ReviewsSerializer(Reviews.objects.filter(movie_id=movie_id), many=True)
        return Response(serializer.data)

class WatchListCreateView(APIView):
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)