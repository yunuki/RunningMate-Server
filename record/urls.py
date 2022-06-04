from django.urls import path

from record.views import RecordCreateView, RecordDetailView, RecordListView, RecordStatisticsView

urlpatterns = [
    path('', RecordCreateView.as_view()),
    path('/<int:pk>', RecordDetailView.as_view()),
    path('/list', RecordListView.as_view()),
    path('/statistics/<int:account_id>', RecordStatisticsView.as_view())
]