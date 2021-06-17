from django.urls import path


from .customauth_views import (SignUp, LoginAPIView)


urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('login/', LoginAPIView.as_view()),
    
]