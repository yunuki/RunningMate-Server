from django.urls import path

from account.views import AccountView, AccountListView

urlpatterns = [
    path('<int:pk>', AccountView.as_view()),
    path('list', AccountListView.as_view())
]
