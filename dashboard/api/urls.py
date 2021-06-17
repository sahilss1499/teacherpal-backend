from django.urls import path


from .customauth_views import (SignUp, LoginAPIView, SaveFCMToken)
from .batches_views import (BatchCreateListView)


urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('save-fcm-token/', SaveFCMToken.as_view()),

    path('batch', BatchCreateListView.as_view()),

]