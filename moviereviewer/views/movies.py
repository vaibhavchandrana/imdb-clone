
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Genre,Movie,SimilarMovie,Cast,Reviews
# from .serializers import GenreSerializer
# import requests

# class FetchAndStoreGenres(APIView):
#     def get(self, request):
#         url = "https://api.themoviedb.org/3/genre/tv/list?language=en"

#         headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I"
#         }
#         response = requests.get(url,headers=headers)
#         data = response.json()
#         print(data)
#         for genre_data in data['genres']:
#             genre_id = genre_data['id']
#             genre_name = genre_data['name']
#             genre, created = Genre.objects.get_or_create(id=genre_id, name=genre_name)

#         return Response({'message': 'Genres fetched and stored successfully'})



# class FetchAndStoreMovies(APIView):
#     def get(self, request):
#         # Movie.objects.all().delete()
#         for i in range(1, 50):  # Adjust the range as needed
#             url = f"https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={i}"
#             headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I"
#         }
#             response = requests.get(url,headers=headers)
#             data = response.json()
#             print(data)
#             for movie_data in data['results']:  # Assuming 'results' is the key containing movie data
#                 genres_data = movie_data['genre_ids']
#                 genres = []
#                 for genre_id in genres_data:
#                     genre, created = Genre.objects.get_or_create(id=genre_id)
#                     genres.append(genre)

#                 movie = Movie.objects.create(
#                     id=movie_data['id'],
#                     backdrop_path = movie_data.get('backdrop_path', ''),
#                     adult=movie_data['adult'],
#                     original_language=movie_data['original_language'],
#                     original_title=movie_data['original_title'],
#                     overview=movie_data['overview'],
#                     popularity=movie_data['popularity'],
#                     poster_path=movie_data['poster_path'],
#                     release_date=movie_data['release_date'],
#                     title=movie_data['title'],
#                     video=movie_data['video'],
#                     vote_average=movie_data['vote_average'],
#                     vote_count=movie_data['vote_count']
#                 )
#                 movie.genre_ids.set(genres)

#         return Response({'message': 'Movies fetched and stored successfully'})
# def id_exists(movie_id):
#     return Reviews.objects.filter(id=movie_id).exists()
# class FetchAndStoreSimilarMovies(APIView):
#     def get(self, request):
#         SimilarMovie.objects.all().delete()

#         dataM= Movie.objects.all()
#         print(dataM)
#         for i in dataM:  # Adjust the range as needed
#             print(i.id)
#             url = f"https://api.themoviedb.org/3/movie/{i.id}/similar?language=en-US&page=1"
#             headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I"
#         }
#             response = requests.get(url,headers=headers)
#             data = response.json()
#             print(data)
#             for movie_data in data['results'][0:10]: 
#                 if id_exists(movie_data['id'])==False and movie_data.get('poster_path'):
#                     genres_data = movie_data['genre_ids']
#                     genres = []
#                     for genre_id in genres_data:
#                         genre, created = Genre.objects.get_or_create(id=genre_id)
#                         genres.append(genre)
        
#                     movie = SimilarMovie.objects.create(
#                         id=movie_data['id'],
#                         backdrop_path = movie_data.get('backdrop_path', ' '),
#                         adult=movie_data['adult'],
#                         original_language=movie_data['original_language'],
#                         original_title=movie_data['original_title'],
#                         overview=movie_data['overview'],
#                         popularity=movie_data['popularity'],
#                         poster_path=movie_data.get('poster_path'," temp"),
#                         release_date=movie_data['release_date'],
#                         title=movie_data['title'],
#                         video=movie_data['video'],
#                         vote_average=movie_data['vote_average'],
#                         vote_count=movie_data['vote_count'],
#                         similar_to=i.id
#                     )
#                     movie.genre_ids.set(genres)

#         return Response({'message': 'Movies fetched and stored successfully'})
    
# class FetchAndStoreCast(APIView):
#     def get(self, request):
#         Cast.objects.all().delete()

#         dataM= Movie.objects.all()
#         print(dataM)
#         for i in dataM:  # Adjust the range as needed
#             print(i.id)
#             url = f"https://api.themoviedb.org/3/movie/{i.id}/credits?language=en-US"
#             headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I"
#         }
#             response = requests.get(url,headers=headers)
#             data = response.json()
#             print(data)
#             for movie_data in data['cast'][0:10]: 
#                 if id_exists(movie_data['id'])==False :
                    
#                     cast = Cast.objects.create(
#                         id=movie_data['id'],
#                         name=movie_data['name'],
#                         profile_path=movie_data['profile_path'],
#                         character_name=movie_data['character'],
#                         movie_id=i.id,
                        
#                     )

#         return Response({'message': 'Movies fetched and stored successfully'})
    


# class FetchAndStoreReview(APIView):
#     def get(self, request):
#         Cast.objects.all().delete()

#         dataM= Movie.objects.all()
#         print(dataM)
#         for i in dataM:  # Adjust the range as needed
#             print(i.id)
#             url = f"https://api.themoviedb.org/3/movie/{i.id}/reviews?language=en-US&page=1"
#             headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YTJhNmQyZmFiZjNhZTMwNjE0ZTMwZjk4Njk4OTE3YiIsInN1YiI6IjY0ZTBjZjBjYTNiNWU2MDFkODc1NjdlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P21N-Z4urgYNTW3iLBfC9aiOMAEii2aE6AoHibCvC6I"
#         }
#             response = requests.get(url,headers=headers)
#             data = response.json()
#             print(data)
#             for movie_data in data['results'][0:10]:  
#                 cast = Reviews.objects.create(
#                     name=movie_data['author'],
#                     review_data=movie_data['content'],
#                     created_at=movie_data['created_at'],
#                     movie_id=i.id,
                    
#                 )

#         return Response({'message': 'Movies fetched and stored successfully'})

