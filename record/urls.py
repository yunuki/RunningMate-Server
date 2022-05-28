from django.urls import path

from record.views import RecordCreateView, RecordDetailView, RecordListView

urlpatterns = [
    path('', RecordCreateView.as_view()),
    path('/<int:pk>', RecordDetailView.as_view()),
    path('/list', RecordListView.as_view())
]