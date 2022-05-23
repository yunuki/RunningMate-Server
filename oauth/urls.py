from django.urls import path

from oauth.views import AppleOAuthView

urlpatterns = [
    path('apple', AppleOAuthView.as_view()),
]