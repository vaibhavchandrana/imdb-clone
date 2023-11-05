from .models import Watchlist, Movie
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, filters, generics, decorators
from rest_framework.views import APIView, status
from .models import Movie, Cast, Genre, Reviews, Cast
from .serializers import MovieSerializer, CastSerializer, ReviewsSerializerGet,  ReviewsSerializer, GenreSerializer, CastSerializer, WatchlistSerializerGet
from .pagination import CustomPageNumberPagination
from rest_framework.response import Response
import random
from django.contrib.auth.models import User
from .serializers import WatchlistSerializer
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


def get_random_user():

    return User.objects.order_by('?').first()


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['vote_average', 'release_date']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            sort_by = request.query_params.get('sort_by', None)
            order = request.query_params.get('order', 'asc')

            if sort_by:
                if sort_by in self.ordering_fields:
                    if order == 'desc':
                        sort_by = f'-{sort_by}'
                    queryset = queryset.order_by(sort_by)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieSearchView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        try:
            query = self.request.query_params.get('search', '')
            queryset = Movie.objects.filter(title__icontains=query)
            for movie in queryset:
                movie.poster_path = movie.poster_path
                movie.backdrop_path = movie.backdrop_path
            return queryset
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CastViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None


class MovieByGenre(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPageNumberPagination

    @decorators.action(detail=False, methods=['get'], url_path='by_genre')
    def by_genre(self, request):
        try:
            genre_id = request.query_params.get('genre_id')

            if genre_id is not None:
                try:
                    genre_id = int(genre_id)
                    movies = self.queryset.filter(genre_ids__id=genre_id)
                    if not movies.exists():
                        return Response({"error": "No movies found for the provided genre"}, status=status.HTTP_404_NOT_FOUND)
                except ValueError:
                    raise ValidationError("Genre ID must be a valid integer")
            else:
                movies = self.queryset.none()

            page = self.paginate_queryset(movies)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(movies, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCastByMovie(APIView):

    def get(self, request, movie_id):
        try:
            cast_query = Cast.objects.filter(movie_id=movie_id)

            serializer = CastSerializer(cast_query, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetReviewByMovie(APIView):

    def get(self, request, movie_id):
        try:
            review_query_data = Reviews.objects.filter(movie_id=movie_id)

            serializer = ReviewsSerializerGet(review_query_data, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RandomizeRatings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            reviews = Reviews.objects.all()
            for review in reviews:
                review.rating = random.randint(1, 5)
                review.save()

            serializer = ReviewsSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchlistCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class WatchlistDetailView(generics.ListAPIView):
    serializer_class = WatchlistSerializerGet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Assuming you pass the userId in the URL
        userId = self.kwargs['userId']
        return Watchlist.objects.filter(owner_id=userId)


class WatchlistShareView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        owner_email = request.data.get('owner_email')
        shared_by = request.data.get('shared_by')
        movie_id = request.data.get('movie')

        try:
            owner = User.objects.get(email=owner_email)
            shared_by = User.objects.get(id=shared_by)
            movie = Movie.objects.get(id=movie_id)
            watchlist = Watchlist(
                owner=owner, shared_by=shared_by, movies=movie)
            watchlist.save()

            return Response({"message": "Watchlist created successfully"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WatchlistDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, watchlist_id):
        try:
            watchlist = get_object_or_404(Watchlist, id=watchlist_id)
            watchlist.delete()
            return Response({"message": "Watchlist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
