from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .utils import create_jwt, decode_jwt
from django.contrib.auth.hashers import make_password, check_password
import requests # pip install requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from deep_translator import GoogleTranslator # pip install deep-translator


@api_view(['POST'])
def register_user(request):
    data = request.data.copy()
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):
            token = create_jwt(user)
            return Response({'token': token})
        return Response({'error': 'Invalid credentials'}, status=400)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['GET', 'PUT'])
def user_detail(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'error': 'Authorization required'}, status=401)

    token = auth_header.split(" ")[-1]
    payload = decode_jwt(token)
    if not payload:
        return Response({'error': 'Invalid or expired token'}, status=401)

    try:
        user = User.objects.get(user_id=payload['user_id'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def translate_text(request):
    token = request.headers.get('Authorization', '').split()[-1]
    payload = decode_jwt(token)
    if not payload:
        return Response({'error': 'Invalid or expired token'}, status=401)

    source_text = request.data.get('text')
    source_lang = request.data.get('source_lang', 'auto')
    target_lang = request.data.get('target_lang', 'es')

    if not source_text:
        return Response({'error': 'Text is required'}, status=400)

    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(source_text)
        return Response({
            'original': source_text,
            'translated': translated
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)



@api_view(['GET'])
def frontend(request):
    return render(request, 'index.html')