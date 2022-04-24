from django.urls import path

from .views      import (
                     SignUpView,
                     LogInView ,
                     # TokenCheckView,
                     FollowRecommendationView
                 )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LogInView.as_view()),
    # path('/tokencheck', TokenCheckView.as_view()),
    path('/follow_recommendation', FollowRecommendationView.as_view())
]