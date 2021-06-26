from django.urls import path


from .customauth_views import (SignUp, LoginAPIView, SaveFCMToken, CreateWebPushTokenObject)
from .batches_views import (BatchCreateListView, BatchDetailView, BatchStudentList, 
                            AttendanceRequestView, AttendanceResponseView, AttendanceDetailView, QuizRequestView)


urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', LoginAPIView.as_view()),
    path('save-fcm-token', SaveFCMToken.as_view()),
    path('subscribe', CreateWebPushTokenObject.as_view()),

    path('batch', BatchCreateListView.as_view()),
    path('batch/<int:pk>', BatchDetailView.as_view()),
    path('batch-students/<int:pk>', BatchStudentList.as_view()),
    path('attendance-detail/<int:pk>', AttendanceDetailView.as_view()),

    path('take-attendance', AttendanceRequestView.as_view()),
    path('attendance-response', AttendanceResponseView.as_view()),
    path('take-quiz', QuizRequestView.as_view()),
]