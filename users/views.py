from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.datetime_safe import datetime
from django.core.exceptions import ObjectDoesNotExist

from .models import User, DONE, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE
from .models import User
from shared.utility import check_email_or_phone, send_email

from .serializers import (
    SignUpSerializer,
    ChangeInformation,
    ChangeUserPhotoSerializer,
    LoginSerializer,
    LogInRefreshSerializer,
    LogOutSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)     




# ------------------------
# Create User view
class CreateUserView(CreateAPIView):
     queryset = User.objects.all()
     permission_classes = (permissions.AllowAny,)
     serializer_class = SignUpSerializer
# ------------------------



# ------------------------
# Verify API View
class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = self.request.user             # user ->
        code = self.request.data.get('code') # 4432

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):       # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                "message": "Your verification code is incorrect or out of date"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True
# ------------------------




# ------------------------     
# Get New Verification View 
class GetNewVerification(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number, code)
        else:
            data = {
                "message": "Your email, or phone number is wrong please check."
            }
            raise ValidationError(data)

        return Response(
            {
                "success": True,
                "message": "Your verification code sent again."
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Your code is now working please wait."
            }
            raise ValidationError(data)
# ------------------------




# ------------------------
# change information serail view 
class ChangeInformationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeInformation
    http_method_names = ['patch', 'put']
    
    def get_object(self):
        return self.request.user


    # update
    def update(self, request, *args, **kwargs):
        super(ChangeInformationView, self).update(request, *args, **kwargs)
        
        data = {
            "success": True,
            "message": "User updated successfuly",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=200)
    
    
    # partial update 
    def partial_update(self, request, *args, **kwargs):
        super(ChangeInformationView, self).partial_update(request, *args, **kwargs)
        
        data = {
            "success": True,
            "message": "User updated successfuly",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=200)
# ------------------------




# ------------------------
# change user photo view
class ChangeUserPhotoView(APIView):
    permissions_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({'Your photo successfly changed'}, status=200)
        return Response(
            serializer.errors, status=400
        )
# ------------------------



# ------------------------
# LogInView
class LogInVeiw(TokenObtainPairView):
    serializer_class = LoginSerializer


# ------------------------




# ------------------------
#LogIn Refresh View
class LogInRefreshView(TokenRefreshView):
    serializer_class = LogInRefreshSerializer 

# ------------------------





# ------------------------
#LogOutView
class LogOutView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LogOutSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            data = {
                'success': True,
                'message': 'You are Logged Out'
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)
 
# ------------------------





# ------------------------
# Forgot Password View
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get('email_or_phone')
        user = serializer.validated_data.get('user')
        if check_email_or_phone(email_or_phone) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(email_or_phone, code)
        elif check_email_or_phone(email_or_phone) == 'email':
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone, code)

        return Response(
            {
                "success": True,
                "message": "Your verification code sent",
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
                "user": user.auth_status,
            }, status=200
        )

# ------------------------





# ------------------------
# Reset Password View
class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch', 'put']
    
    def get_object(self):
        return self.request.user
    
    
    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)
        
        try:
            user = User.objects.get(id=response.data.get('id'))
        except ObjectDoesNotExist as e:
            raise NotFound(detail='User not found')
        return Response(
            {
                'seccess': True,
                'message': 'Your Password successfly changed',
                'access': user.token()['access'],
                'refresh_token': user.token()['refresh_token'],
            }
        )

# ------------------------
