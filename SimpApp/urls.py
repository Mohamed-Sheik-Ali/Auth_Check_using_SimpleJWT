from django.urls import path
from SimpApp.views import LoginAPIView, PasswordTokenCheckAPIView, RegisterView, SetNewPasswordAPIView, VerifyEmail, RequestPasswordResetEmailAPIView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('request-reset-email/', RequestPasswordResetEmailAPIView.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>',
         PasswordTokenCheckAPIView.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name="password-reset-complete")
]
