from .models import MovieList, Plateform, Reviews
from .serializers import MovieListSerializer, PlateformSerializer
from .serializers import ReviewSerailizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class StreamPlateformListAV(APIView):
    def get(self, request):
        plateform = Plateform.objects.all()  # return query set
        serial = PlateformSerializer(plateform, many=True)
        return Response(serial.data)

    def post(self, request):
        serial = PlateformSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)


class StreamDetailAV(APIView):
    def get(self, request, pk):
        data = Plateform.objects.get(pk=pk)
        serial = PlateformSerializer(data)
        return Response(serial.data)

    def put(self, request, pk):
        one_movie = Plateform.objects.get(pk=pk)
        serial = PlateformSerializer(one_movie, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

    def delete(self, request, pk):
        one_movie = Plateform.objects.get(pk=pk)
        one_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    def get(self, request):
        movies = MovieList.objects.all()  # return query set
        serial = MovieListSerializer(movies, many=True)
        return Response(serial.data)

    def post(self, request):
        serial = MovieListSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)


class WatchDetailAV(APIView):
    def get(self, request, pk):
        data = MovieList.objects.get(pk=pk)
        serial = MovieListSerializer(data)
        return Response(serial.data)

    def put(self, request, pk):
        one_movie = MovieList.objects.get(pk=pk)
        
        serial = MovieListSerializer(one_movie, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors)

    def delete(self, request, pk):
        one_movie = MovieList.objects.get(pk=pk)
        one_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(generics.ListAPIView):
    # queryset=Reviews.objects.all()
    serializer_class = ReviewSerailizer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(movielist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerailizer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerailizer

    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = MovieList.objects.get(pk=pk)
        # code for checking thet user already post any review or not
        user = self.request.user
        review_queryset = Reviews.objects.filter(
            movielist=movie, review_user=user)
        if review_queryset.exists():
            raise ValidationError({"error":"You can not review twice"})
            

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (
                movie.avg_rating+serializer.validated_data['rating'])/2

        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(movielist=movie, review_user=user)
