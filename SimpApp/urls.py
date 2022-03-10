from django.urls import path
from SimpApp.views import LoginAPIView, RegisterView, VerifyEmail


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]
