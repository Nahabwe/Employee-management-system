from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            refresh=RefreshToken.for_user(user)
            return Response({
                'access':str(refresh.access_token),
                'refresh':str(refresh),
                'user':user.username,
                'email':user.email
            },status=status.HTTP_200_OK)
        return Response({'message':'Failed to login'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
     try:
        refresh_token=request.data.get('refresh')
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message':'Successfully logedout'},status=status.HTTP_200_OK)
     except Exception as e:
          return Response({'error':'invalid token'},status=status.HTTP_400_BAD_REQUEST)
      

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    email=request.data.get('email')
    try:
        user=User.objects.get(email=email)
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)
        link=f'http://localhost:8000/auth/password-reset-confirm/{uidb64}/{token}'
        send_mail(
            subject='Password Reset',
           message= f'Click here to reset your password: {link}',
            from_email= settings.EMAIL_HOST_USER,
             recipient_list=[user.email],
             fail_silently=False,
        )
        return Response({'Password reset link sent please check in your email'},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message":"User not found"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request,uidb64,token):
    try:
         uid=urlsafe_base64_decode(uidb64).decode()
         user=User.objects.get(pk=uid)
    except(TypeError,OverflowError,ValueError, User.DoesNotExist):
         user=None

    if user is not None and default_token_generator.check_token(user,token):
        new_password=request.data.get('new_password')
        confirm_password =request.data.get('confirm_password')
        if confirm_password != new_password:
            return Response({'error':'Password does not match'})
        user.set_password(new_password)
        user.save()
        return Response({'message':'Password was reset successfuly'},status=status.HTTP_200_OK)
    return Response({'error':'Invalid token or user'},status=status.HTTP_400_BAD_REQUEST)
    
