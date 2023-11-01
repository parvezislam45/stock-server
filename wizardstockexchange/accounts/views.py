from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializer import CustomUserSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from tradeApi.models import UserWallet

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Add this line for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            
            try:
                user_wallet = UserWallet.objects.get(user=user)
                print(user_wallet)
            except UserWallet.DoesNotExist:
                # If the user doesn't have a wallet, create one
                user_wallet = UserWallet.objects.create(user=user, balance=0.0)
            
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@method_decorator(csrf_exempt, name='dispatch')
class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({'username': request.user.username, 'email': request.user.email})
    
