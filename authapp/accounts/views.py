import datetime

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import jwt

from .serializers import UserSerializer, EditSerializer
from .models import UserBase


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def dashboard(request):
    return render(request, 'dashboard.html')

#=====================API============================
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    email = request.data['email']
    password = request.data['password']
    user = UserBase.objects.filter(email=email).first()
    if user:
        if user.check_password(password):
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'django-insecure-6imtjep_f57jrz7y4lf7&9qnxv2pzv$1zf7gn--kahoe1dhesa', algorithm='HS256')
            response = Response()
            response.set_cookie(key='token', value=token, httponly=True)
            response.data = {
                'token': token
            }
            return response
        else:
            raise AuthenticationFailed('Invalid email or password')
    else:
        raise AuthenticationFailed('User not found')

@api_view(['GET'])
def dashboard_view(request):
    token = request.COOKIES.get('token')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'django-insecure-6imtjep_f57jrz7y4lf7&9qnxv2pzv$1zf7gn--kahoe1dhesa', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    user = UserBase.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def edit_view(request):
    token = request.COOKIES.get('token')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'django-insecure-6imtjep_f57jrz7y4lf7&9qnxv2pzv$1zf7gn--kahoe1dhesa', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    user = UserBase.objects.filter(id=payload['id']).first()
    serializer = EditSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_view(request):
    token = request.COOKIES.get('token')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'django-insecure-6imtjep_f57jrz7y4lf7&9qnxv2pzv$1zf7gn--kahoe1dhesa', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    user = UserBase.objects.filter(id=payload['id']).first()
    serializer = EditSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout_view(request):
    response = Response()
    response.delete_cookie('token')
    response.data = {
        'message': 'logout success'
    }
    return response