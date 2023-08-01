from django.urls import path
from .views import (
    CreateUserView,
    VerifyAPIView,
    GetNewVerification,
    ChangeInformationView,
    ChangeUserPhotoView,
    LogInVeiw,
    LogInRefreshView,
    LogOutView,
    ForgotPasswordView,
    ResetPasswordView
)



urlpatterns = [
    path('login/', LogInVeiw.as_view()),
    path('login/refresh', LogInRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeInformationView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
