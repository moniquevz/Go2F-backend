from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from django.contrib.auth.models import User

from base.serializers import UserSerializer, UserSerializerWithToken, ResetPasswordRequestSerializer, SetNewPasswordSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework import status


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes

from django_email_verification import send_email
from ..utils import Util
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data 

    try:
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        user.is_active = False
        send_email(user)
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disableUser(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    message ={'DETAIL: USER DEACTIVATED'}
    try:
        user.is_active = False
        user.save()
        return Response(message)
    except:
        message =  {'detail': 'could not deactivate'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def resetPasswordEmail(request):
    data = request.data
    email = data['email']
    user = User.objects.get(email=email)
    user_data = UserSerializer(user).data
    serializer = ResetPasswordRequestSerializer(data = data)
    serializer.is_valid()
    #print(serializer.data)
    uidb64 = urlsafe_base64_encode(force_bytes(user_data['_id']))
    #print(uidb64)
    
    token = PasswordResetTokenGenerator().make_token(user)


    relative_link = reverse('password-reset-confirm', kwargs={'uidb64' : uidb64, 'token': token})
    absurl ='http://127.0.0.1:8000' + relative_link
    
    email_body = 'Please reset your password \n' +absurl

    data ={'email_body': email_body, 'to_email': email, 'email_subject' : 'Reset password'}

    Util.send_email(data)
   

    return Response({'detail': 'Password reset link sent'})

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request,uidb64,token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            print(request.data)
            user = User.objects.get(id = id)
            check = PasswordResetTokenGenerator().check_token(user,token)
            if not check:
                return Response({'error': 'Link is no longer valid, please try again'}, status =status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token})
            

        except:
            return Response({'error': 'Link is no longer valid, please try again'}, status =status.HTTP_400_BAD_REQUEST)
 



@api_view(['PATCH'])
def SetNewPassword(request):

    serializer = SetNewPasswordSerializer(data= request.data)
    serializer.is_valid()

    return Response({'success': True, 'message': 'Password reset success'}, status = status.HTTP_200_OK)
