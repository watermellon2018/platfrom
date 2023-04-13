from django.shortcuts import render

# Create your views here.

# myapp/views.py
from django.http import HttpResponse
import json

def hello(request):

    # user = User.objects.create_user(username='admin', password='admin')

    data = {
        'message': 'Привет, Мир!'
    }
    json_data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json; charset=utf-8')



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from health.serializers import UserSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

        return HttpResponse('Ошибка чет хз', status=status.HTTP_400_BAD_REQUEST)


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Создаем токен
            refresh = RefreshToken.for_user(user)

            # Возвращаем токен в ответе
            return Response({
                'status': 'success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        else:
            return Response({'status': 'fail'})


