from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from users.models import Records
from django.contrib.auth.models import User
from users.serializers import RecordSerializer, UserSerializer
from rest_framework.authtoken.models import Token


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def records_list(request):
    if request.method == 'GET':
        user_id = User.objects.get(username=request.user).id
        records = Records.objects.filter(user_id=user_id)
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request_data = request.data
        request_data['user_id'] = User.objects.get(username=request.user).id
        serializer = RecordSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def record_detail(request, pk):
    try:
        record = Records.objects.get(pk=pk)
    except Records.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response(f'token:{token.key}', status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def auth_by_token(request):
    user = Token.objects.get(key=request.data)
    print(user)

@api_view(['POST'])
def auth_by_password(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
    if user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
