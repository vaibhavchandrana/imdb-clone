from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_app.serializers import RegistrationSerializers
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
# Create your views here.


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RegistrationView(APIView):
    def post(self, request):
        try:
            serializer = RegistrationSerializers(data=request.data)
            data = {}

            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "Registration Successful"
                data['username'] = account.username
                data['email'] = account.email
                token, created = Token.objects.get_or_create(user=account)

                if not created:
                    # Token already exists for this user, return the existing token
                    data['token'] = token.key
                else:
                    data['token'] = token.key

                data['id'] = account.id
                return Response(data, status=status.HTTP_201_CREATED)

            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {'error': str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    try:
        user_id = request.user.id
        return Response({'user_id': user_id}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
